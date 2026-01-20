from ninja import NinjaAPI
from ninja.errors import ConfigError
import sys
import uuid

# RANDOMIZED NAMESPACE HOTFIX: 
# Isso garante que mesmo se o módulo for importado múltiplas vezes e a Ninja 
# tentar validar o registro repetidamente, nunca haverá colisão de namespace.
_unique_suffix = uuid.uuid4().hex[:8]

api = NinjaAPI(
    title="Legal Intelligence Platform API", 
    version="3.3.0", 
    urls_namespace=f'main_{_unique_suffix}' 
)

def setup_api():
    try:
        from in_brief.api.endpoints import router as in_brief_router
        api.add_router("/in-brief", in_brief_router)
    except Exception:
        pass

    try:
        from apps.intake.api.router import router as intake_router
        api.add_router("/intake", intake_router)
    except Exception:
        pass

    try:
        from apps.integrations.api.router import router as integrations_router
        api.add_router("/integrations", integrations_router)
    except Exception:
        pass

    try:
        from apps.portals.api.router import router as portals_router
        api.add_router("/portals", portals_router)
    except Exception:
        pass

# Initialize it
setup_api()
