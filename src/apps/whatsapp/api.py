from ninja import NinjaAPI, Schema
from ninja.errors import ConfigError
import logging

logger = logging.getLogger(__name__)

# WhatsApp API Instance
# Using a unique namespace suffix to avoid any persistent registration conflicts on Railway
api = NinjaAPI(
    title="Legal Intelligence Platform WhatsApp API", 
    version="3.1.0", 
    urls_namespace='whatsapp_v3'
)

class IncomingMessage(Schema):
    from_number: str
    message_body: str
