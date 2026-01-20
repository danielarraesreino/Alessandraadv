from ninja import NinjaAPI, Schema
import logging

logger = logging.getLogger(__name__)

_api = None

def get_api():
    """
    Singleton for the WhatsApp API instance.
    Uses a unique namespace and version to avoid conflicts with the main API.
    """
    global _api
    if _api is not None:
        return _api
        
    for existing_api in NinjaAPI._registry:
        if getattr(existing_api, "urls_namespace", None) == 'whatsapp':
            _api = existing_api
            return _api

    _api = NinjaAPI(
        title="Legal Intelligence Platform WhatsApp API",
        version="2.1.0", # Distinct version from core
        urls_namespace='whatsapp'
    )
    return _api

api = get_api()

class IncomingMessage(Schema):
    from_number: str
    message_body: str
