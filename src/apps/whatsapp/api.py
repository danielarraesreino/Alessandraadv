from ninja import NinjaAPI, Schema
from django.http import HttpRequest
import logging
from apps.clients.models import Client

logger = logging.getLogger(__name__)

api = NinjaAPI(
    title="Alessandra M. Donadon WhatsApp API", 
    version="1.1.0", 
    urls_namespace='whatsapp'
)

class IncomingMessage(Schema):
    from_number: str
    message_body: str
    timestamp: str

@api.post("/webhook")
def whatsapp_webhook(request: HttpRequest, payload: IncomingMessage):
    """
    Receives messages from WhatsApp (simulated webhook).
    1. Check if client exists by phone (encrypted search might be slow, so we do exact match logic or hash).
    2. Log interaction.
    3. Return Triage menu.
    """
    # Simple logic for MVP 8h deadline
    # Note: EncryptedField doesn't support direct filtering easily without deterministic encryption.
    # For now, we will just create/log.
    
    logger.info(f"Received message from {payload.from_number}: {payload.message_body}")
    
    # Mock Response Logic
    response_text = (
        "Olá! Sou a assistente virtual da Alessandra M. Donadon Advocacia.\n"
        "Para agilizar seu atendimento, selecione uma área:\n\n"
        "1. Cível & Família\n"
        "2. Empresarial & Terceiro Setor\n"
        "3. Saúde (Lipedema/Negativas)\n"
        "4. Financeiro/Outros"
    )
    
    return {
        "reply_to": payload.from_number,
        "text": response_text,
        "status": "TRIAGE_INITIATED"
    }
