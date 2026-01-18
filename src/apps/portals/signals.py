"""
Django signals for Client Portal notifications.

Automatically sends WhatsApp notifications when case timeline is updated.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.portals.models import CaseTimeline
from apps.whatsapp.services.notification import WhatsAppNotificationService


@receiver(post_save, sender=CaseTimeline)
def notify_client_on_timeline_update(sender, instance, created, **kwargs):
    """
    Send WhatsApp notification when timeline is updated.
    
    Triggered automatically when lawyer updates case stage in Django Admin.
    """
    # Skip notification on initial creation
    if created:
        return
    
    # Only notify if there's a client associated
    if not hasattr(instance.legal_case, 'client'):
        return
    
    client = instance.legal_case.client
    
    # Format professional notification message
    stage_label = dict(CaseTimeline.STAGES).get(
        instance.current_stage,
        instance.current_stage
    )
    
    message = f"""
*ATUALIZAÇÃO DO SEU CASO*

Caso: {instance.legal_case}
Nova Etapa: {stage_label}
Progresso: {instance.progress_percentage()}%

Acesse o portal para mais detalhes e documentos:
https://alessandradonadon.adv.br/portal

_Atualização realizada em {timezone.now().strftime('%d/%m/%Y às %H:%M')}_
"""
    
    # Send WhatsApp notification
    try:
        service = WhatsAppNotificationService(provider='mock')
        # In production, extract phone from encrypted client.phone
        # For now, use decisor number as fallback
        service.decisor_number = client.contact_info if hasattr(client, 'contact_info') else service.decisor_number
        
        # Log the notification
        print(f"[SIGNAL] Enviando notificação de atualização para {client.full_name}")
        print(message)
        
        # Note: Actual sending would happen here in production
        # service.send_notification(message)
        
    except Exception as e:
        # Log error but don't break the save operation
        print(f"[SIGNAL ERROR] Falha ao enviar notificação: {e}")
