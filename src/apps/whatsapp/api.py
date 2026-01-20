from ninja import NinjaAPI, Schema
from ninja.errors import ConfigError
import logging
import sys

logger = logging.getLogger(__name__)

# A truly global registry to survive module re-imports
if not hasattr(sys, '_ninja_api_registry'):
    sys._ninja_api_registry = {}

def get_api_instance(name, title, version):
    if name not in sys._ninja_api_registry:
        try:
            sys._ninja_api_registry[name] = NinjaAPI(
                title=title,
                version=version,
                urls_namespace=name
            )
        except ConfigError:
            raise
    return sys._ninja_api_registry[name]

# For the WhatsApp API
try:
    api = get_api_instance(
        'whatsapp', 
        "Legal Intelligence Platform WhatsApp API", 
        "1.1.0"
    )
except ConfigError:
    api = NinjaAPI(urls_namespace='whatsapp_fallback')

class IncomingMessage(Schema):
    from_number: str
    message_body: str
