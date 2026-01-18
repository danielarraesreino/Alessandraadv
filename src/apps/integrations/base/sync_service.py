"""
Sync service for Legal Ops integrations.

Orchestrates synchronization between Django models and external Legal Ops systems.
"""
import logging
from typing import Optional
from django.conf import settings

from apps.intake.models import Lead
from apps.integrations.base.providers import (
    ProviderFactory, 
    MatterData, 
    SyncResult
)

logger = logging.getLogger(__name__)


class LegalOpsSyncService:
    """
    Service for synchronizing leads with Legal Ops platforms.
    """
    
    def __init__(self, provider_name: str = None):
        """
        Initialize sync service.
        
        Args:
            provider_name: 'clio', 'jestor', or 'custom'
                          Defaults to LEGAL_OPS_PROVIDER setting
        """
        self.provider_name = provider_name or getattr(
            settings, 
            'LEGAL_OPS_PROVIDER', 
            'clio'
        )
        self.provider = ProviderFactory.get_provider(self.provider_name)
    
    def sync_lead_to_matter(self, lead: Lead) -> SyncResult:
        """
        Sync a qualified lead to the Legal Ops system.
        
        Args:
            lead: Lead instance to sync
            
        Returns:
            SyncResult with external_id if successful
        """
        if not lead.is_qualified:
            logger.warning(f"Lead {lead.id} is not qualified, skipping sync")
            return SyncResult(
                success=False,
                error_message="Lead not qualified"
            )
        
        # Check if already synced
        if lead.external_id:
            logger.info(f"Lead {lead.id} already synced to {lead.external_id}")
            return SyncResult(
                success=True,
                external_id=lead.external_id
            )
        
        # Prepare matter data
        matter_data = MatterData(
            client_name=lead.full_name,
            case_type=lead.case_type,
            description=f"Lead from website - {lead.get_case_type_display()}",
            contact_info=lead.contact_info,
            score=lead.score,
            triage_data=lead.triage_data
        )
        
        # Create matter in external system
        result = self.provider.create_matter(matter_data)
        
        if result.success:
            # Save external ID to lead
            lead.external_id = result.external_id
            lead.save(update_fields=['external_id'])
            
            logger.info(
                f"Lead {lead.id} synced to {self.provider_name}: {result.external_id}"
            )
        else:
            logger.error(
                f"Failed to sync lead {lead.id}: {result.error_message}"
            )
        
        return result
    
    def update_matter_from_lead(self, lead: Lead, updates: dict) -> SyncResult:
        """
        Update an existing matter with new data.
        
        Args:
            lead: Lead instance
            updates: Fields to update
            
        Returns:
            SyncResult indicating success/failure
        """
        if not lead.external_id:
            return SyncResult(
                success=False,
                error_message="Lead not synced yet"
            )
        
        return self.provider.update_matter(lead.external_id, updates)
    
    def health_check(self) -> bool:
        """
        Check if the Legal Ops provider is accessible.
        
        Returns:
            True if provider is healthy
        """
        return self.provider.health_check()
