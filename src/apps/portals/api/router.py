"""
Django Ninja API for Client Portal.
"""
from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.portals.models import CaseTimeline, CaseDocument, ClientPortalAccess
from apps.legal_cases.models import LegalCase

router = Router()


# Schemas
class MilestoneSchema(Schema):
    stage: str
    date: str
    notes: str
    updated_by: str


class TimelineSchema(Schema):
    case_id: int
    current_stage: str
    progress_percentage: int
    milestones: List[MilestoneSchema]
    last_update: str


class DocumentSchema(Schema):
    id: int
    document_type: str
    title: str
    description: str
    file_url: str
    uploaded_at: str
    uploaded_by: str


# Endpoints
@router.get("/timeline/{access_token}/", response=TimelineSchema)
def get_case_timeline(request, access_token: str):
    """
    Get timeline for a case using client access token.
    
    Args:
        access_token: Unique token for client portal access
        
    Returns:
        Timeline with milestones and progress
    """
    access = get_object_or_404(
        ClientPortalAccess,
        access_token=access_token,
        is_active=True
    )
    access.record_access()
    
    timeline = access.legal_case.timeline
    
    return {
        "case_id": access.legal_case.id,
        "current_stage": timeline.current_stage,
        "progress_percentage": timeline.progress_percentage(),
        "milestones": timeline.milestones,
        "last_update": timeline.last_update.isoformat()
    }


@router.get("/documents/{access_token}/", response=List[DocumentSchema])
def get_case_documents(request, access_token: str):
    """
    Get all documents visible to the client.
    
    Args:
        access_token: Unique token for client portal access
        
    Returns:
        List of documents
    """
    access = get_object_or_404(
        ClientPortalAccess,
        access_token=access_token,
        is_active=True
    )
    
    documents = access.legal_case.documents.filter(
        is_visible_to_client=True
    )
    
    return [
        {
            "id": doc.id,
            "document_type": doc.get_document_type_display(),
            "title": doc.title,
            "description": doc.description,
            "file_url": doc.file.url if doc.file else "",
            "uploaded_at": doc.uploaded_at.isoformat(),
            "uploaded_by": doc.uploaded_by.get_full_name() if doc.uploaded_by else "Sistema"
        }
        for doc in documents
    ]


@router.post("/documents/{access_token}/upload/")
def upload_document(request, access_token: str, file: str, title: str, description: str = ""):
    """
    Allow client to upload a document to their case.
    
    Args:
        access_token: Unique token for client portal access
        file: Uploaded file
        title: Document title
        description: Optional description
        
    Returns:
        Success message with document ID
    """
    access = get_object_or_404(
        ClientPortalAccess,
        access_token=access_token,
        is_active=True
    )
    
    document = CaseDocument.objects.create(
        legal_case=access.legal_case,
        document_type='EVIDENCE',
        title=title,
        description=description,
        file=file,
        uploaded_by=None,  # Client upload
        is_visible_to_client=True
    )
    
    return {
        "success": True,
        "document_id": document.id,
        "message": "Documento enviado com sucesso"
    }


@router.get("/validate-token/{access_token}/")
def validate_access_token(request, access_token: str):
    """
    Validate if an access token is valid and active.
    
    Args:
        access_token: Token to validate
        
    Returns:
        Validation status and client info
    """
    try:
        access = ClientPortalAccess.objects.get(
            access_token=access_token,
            is_active=True
        )
        
        return {
            "valid": True,
            "client_name": access.client.full_name,
            "case_number": access.legal_case.case_number if hasattr(access.legal_case, 'case_number') else "N/A"
        }
    except ClientPortalAccess.DoesNotExist:
        return {
            "valid": False,
            "error": "Token inválido ou expirado"
        }, 401
