"""
Error Handler Service

Centralized error capture and notification system for production monitoring.
Sends alerts to developer and Dra. Alessandra via WhatsApp and Email.

Mission 1: Error Modal & Proactive Notification System
"""
import logging
import traceback
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from apps.whatsapp.services.notification import WhatsAppNotificationService

logger = logging.getLogger(__name__)


class ErrorHandler:
    """
    Handles error capture, metadata extraction, and multi-channel notifications.
    """
    
    def __init__(self):
        self.whatsapp_service = WhatsAppNotificationService(
            provider=getattr(settings, 'WHATSAPP_PROVIDER', 'mock')
        )
    
    def capture_error(
        self, 
        exception: Exception, 
        request: Any = None,
        extra_context: Optional[Dict] = None
    ) -> str:
        """
        Capture error with full context and send notifications.
        
        Args:
            exception: The raised exception
            request: Django request object (optional)
            extra_context: Additional context dictionary (optional)
        
        Returns:
            str: Unique error ID for tracking
        """
        # Generate unique error ID
        error_id = str(uuid.uuid4())[:8].upper()
        
        # Extract metadata
        metadata = self._extract_metadata(exception, request, extra_context)
        metadata['error_id'] = error_id
        
        # Log error
        logger.error(
            f"SYSTEM_ERROR [{error_id}]: {metadata['error_type']} | "
            f"Path: {metadata['path']} | User: {metadata['user']}"
        )
        
        # Send notifications (only if enabled)
        if getattr(settings, 'ERROR_NOTIFICATIONS_ENABLED', True):
            self._send_notifications(metadata)
        
        return error_id
    
    def _extract_metadata(
        self, 
        exception: Exception, 
        request: Any,
        extra_context: Optional[Dict]
    ) -> Dict[str, Any]:
        """Extract comprehensive error metadata."""
        metadata = {
            'error_type': exception.__class__.__name__,
            'error_message': str(exception),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'path': 'N/A',
            'method': 'N/A',
            'user': 'Anonymous',
            'user_agent': 'N/A',
            'ip_address': 'N/A',
        }
        
        # Extract request data if available
        if request:
            metadata.update({
                'path': request.path,
                'method': request.method,
                'user': (
                    request.user.username 
                    if hasattr(request, 'user') and request.user.is_authenticated 
                    else 'Anonymous'
                ),
                'user_agent': request.META.get('HTTP_USER_AGENT', 'N/A'),
                'ip_address': self._get_client_ip(request),
            })
        
        # Add extra context if provided
        if extra_context:
            metadata['extra_context'] = extra_context
        
        return metadata
    
    def _get_client_ip(self, request: Any) -> str:
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', 'N/A')
    
    def _send_notifications(self, metadata: Dict[str, Any]) -> None:
        """Send WhatsApp and Email notifications."""
        try:
            # 1. WhatsApp Notification
            self.whatsapp_service.send_error_notification(
                error_id=metadata['error_id'],
                error_type=metadata['error_type'],
                path=metadata['path'],
                user=metadata['user']
            )
            logger.info(f"WhatsApp notification sent for error {metadata['error_id']}")
        except Exception as e:
            logger.error(f"Failed to send WhatsApp notification: {e}")
        
        try:
            # 2. Email Notification
            self._send_email_notification(metadata)
            logger.info(f"Email notification sent for error {metadata['error_id']}")
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
    
    def _send_email_notification(self, metadata: Dict[str, Any]) -> None:
        """Send detailed email notification to developer."""
        # Render HTML email template
        html_content = render_to_string(
            'emails/error_notification_email.html',
            {'metadata': metadata}
        )
        
        # Plain text fallback
        text_content = f"""
ALERTA DE SISTEMA: ERRO CRÍTICO

ID do Erro: {metadata['error_id']}
Tipo: {metadata['error_type']}
Mensagem: {metadata['error_message']}
Timestamp: {metadata['timestamp']}

Contexto da Requisição:
- Path: {metadata['path']}
- Method: {metadata['method']}
- Usuário: {metadata['user']}
- IP: {metadata['ip_address']}
- User Agent: {metadata['user_agent']}

Traceback:
{metadata['traceback']}

---
Este alerta foi gerado automaticamente pelo Portal Dra. Alessandra.
        """.strip()
        
        # Determine recipients
        recipients = []
        developer_email = getattr(settings, 'DEVELOPER_EMAIL', None)
        if developer_email:
            recipients.append(developer_email)
        else:
            # Fallback to DEFAULT_FROM_EMAIL if DEVELOPER_EMAIL not set
            recipients.append(settings.DEFAULT_FROM_EMAIL)
        
        # Send email
        email = EmailMultiAlternatives(
            subject=f"[ALERTA] Erro de Sistema - {metadata['error_id']}",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
