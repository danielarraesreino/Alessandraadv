from ninja import NinjaAPI, Schema
from ninja.errors import ConfigError
import logging
import uuid

logger = logging.getLogger(__name__)

# RANDOMIZED NAMESPACE HOTFIX:
_unique_suffix = uuid.uuid4().hex[:8]

api = NinjaAPI(
    title="Legal Intelligence Platform WhatsApp API", 
    version="3.3.0", 
    urls_namespace=f'whatsapp_{_unique_suffix}'
)

class IncomingMessage(Schema):
    from_number: str
    message_body: str
