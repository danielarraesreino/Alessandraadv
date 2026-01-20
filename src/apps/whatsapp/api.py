from ninja import NinjaAPI, Schema
from ninja.errors import ConfigError
import logging

logger = logging.getLogger(__name__)

# Basic singleton pattern for the WhatsApp API
_api = None

def get_api():
    global _api
    if _api is None:
        try:
            _api = NinjaAPI(
                title="Legal Intelligence Platform WhatsApp API", 
                version="1.1.0", 
                urls_namespace='whatsapp'
            )
        except ConfigError:
            pass
    return _api

api = get_api()

class IncomingMessage(Schema):
    from_number: str
    message_body: str
