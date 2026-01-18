"""
Django Ninja API endpoints for Legal Ops synchronization.
"""
from ninja import Router
from django.http import HttpResponse
from typing import Optional

from apps.intake.models import Lead
from apps.integrations.base.sync_service import LegalOpsSyncService

router = Router()


@router.post("/sync/lead-to-matter/{lead_id}/")
def sync_lead_to_matter(request, lead_id: int, provider: Optional[str] = None):
    """
    Synchronize a qualified lead to the Legal Ops system.
    
    Args:
        lead_id: ID of the lead to sync
        provider: Optional provider override ('clio', 'jestor')
        
    Returns:
        JSON with sync result
    """
    try:
        lead = Lead.objects.get(id=lead_id)
    except Lead.DoesNotExist:
        return {"error": "Lead not found"}, 404
    
    # Initialize sync service
    sync_service = LegalOpsSyncService(provider_name=provider)
    
    # Perform sync
    result = sync_service.sync_lead_to_matter(lead)
    
    if result.success:
        return {
            "success": True,
            "lead_id": lead_id,
            "external_id": result.external_id,
            "provider": sync_service.provider_name
        }
    else:
        return {
            "success": False,
            "error": result.error_message
        }, 400


@router.get("/sync/health-check/")
def health_check(request, provider: Optional[str] = None):
    """
    Check connection to Legal Ops provider.
    
    Args:
        provider: Optional provider to check ('clio', 'jestor')
        
    Returns:
        JSON with health status
    """
    sync_service = LegalOpsSyncService(provider_name=provider)
    is_healthy = sync_service.health_check()
    
    return {
        "provider": sync_service.provider_name,
        "healthy": is_healthy,
        "status": "connected" if is_healthy else "disconnected"
    }


@router.post("/sync/auto-sync-qualified/")
def auto_sync_qualified_leads(request):
    """
    Automatically sync all qualified leads that haven't been synced yet.
    
    Returns:
        JSON with sync summary
    """
    sync_service = LegalOpsSyncService()
    
    # Find qualified leads without external_id
    unsynced_leads = Lead.objects.filter(
        is_qualified=True,
        external_id__isnull=True
    )
    
    results = {
        "total": unsynced_leads.count(),
        "synced": 0,
        "failed": 0,
        "errors": []
    }
    
    for lead in unsynced_leads:
        result = sync_service.sync_lead_to_matter(lead)
        if result.success:
            results["synced"] += 1
        else:
            results["failed"] += 1
            results["errors"].append({
                "lead_id": lead.id,
                "error": result.error_message
            })
    
    return results
