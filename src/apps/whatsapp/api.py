from ninja import NinjaAPI, Schema
from ninja.errors import ConfigError
import logging
import sys

logger = logging.getLogger(__name__)

# DEFENSIIVA ABSOLUTA: Usar sys como âncora global para evitar dupla instanciação
if not hasattr(sys, '_ninja_whatsapp_api'):
    print(">>> INSTANTIATING WHATSAPP NINJA API (FIRST TIME) <<<")
    try:
        sys._ninja_whatsapp_api = NinjaAPI(
            title="Legal Intelligence Platform WhatsApp API", 
            version="3.2.0", 
            urls_namespace='whatsapp_final'
        )
    except ConfigError:
        print(">>> CONFIG ERROR DURING WHATSAPP INSTANTIATION <<<")
        sys._ninja_whatsapp_api = NinjaAPI(urls_namespace='whatsapp_emergency')
else:
    print(">>> REUSING EXISTING WHATSAPP NINJA API <<<")

api = sys._ninja_whatsapp_api

class IncomingMessage(Schema):
    from_number: str
    message_body: str
