from ninja import Router, Schema
from django.shortcuts import render
from django.http import HttpResponse
from django_htmx.http import trigger_client_event
from ..models import Lead, TriageSession
import uuid

router = Router()

# Schemas for request validation
class Step1Schema(Schema):
    name: str
    case_type: str

class Step2Schema(Schema):
    session_id: str
    urgencia: str = None
    contact: str = None

@router.post("/step-1/")
def intake_step_1(request, data: Step1Schema):
    """Step 1: Capture name and case type, create triage session."""
    session_id = str(uuid.uuid4())
    TriageSession.objects.create(
        session_id=session_id,
        temp_data={'name': data.name, 'case_type': data.case_type}
    )
    
    # Conditional response based on case type
    if data.case_type == 'LIPEDEMA':
        template = 'intake/step_lipedema.html'
    elif data.case_type == 'SUPER':
        template = 'intake/step_super.html'
    else:
        template = 'intake/step_generic.html'
        
    response = render(request, template, {'name': data.name, 'session_id': session_id})
    return response

@router.post("/step-2/")
def intake_step_2(request, data: Step2Schema):
    """Step 2: Process detailed case info and create lead."""
    session = TriageSession.objects.get(session_id=data.session_id)
    
    # Update session data
    session.temp_data.update({
        'urgencia': data.urgencia,
        'contact': data.contact
    })
    session.save()
    
    # Create Lead
    lead = Lead.objects.create(
        full_name=session.temp_data['name'],
        case_type=session.temp_data['case_type'],
        contact_info=data.contact or 'Não informado',
        triage_data=session.temp_data
    )
    
    # [ENHANCED] ClaimScore™ Algorithm
    from apps.intake.scoring import calculate_claim_score
    lead.score = calculate_claim_score(lead, session.temp_data)
    lead.is_qualified = lead.score > 60
    lead.save()
    
    # [NEW] Enviar notificação WhatsApp se qualificado
    if lead.is_qualified:
        try:
            from apps.whatsapp.services.notification import WhatsAppNotificationService
            notification_service = WhatsAppNotificationService(provider='mock')
            notification_service.send_lead_notification(lead)
        except Exception as e:
            # Log error but don't break the user flow
            print(f"Erro ao enviar notificação WhatsApp: {e}")
    
    return render(request, 'intake/step_final.html', {'lead': lead})
