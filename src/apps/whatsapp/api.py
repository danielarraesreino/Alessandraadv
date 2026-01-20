from ninja import NinjaAPI, Schema
from ninja.errors import ConfigError
import logging

logger = logging.getLogger(__name__)

_api = None

def get_api():
    global _api
    if _api is None:
        try:
            _api = NinjaAPI(
                title="Legal Intelligence Platform WhatsApp API",
                version="4.0.0",
                urls_namespace='whatsapp'
            )
        except ConfigError:
            _api = NinjaAPI(urls_namespace='whatsapp_alt')
    return _api

api = get_api()

class IncomingMessage(Schema):
    from_number: str
    message_body: str
