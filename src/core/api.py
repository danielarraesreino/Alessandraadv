from ninja import NinjaAPI
from ninja.errors import ConfigError

# The key Ninja uses in its internal registry: "{urls_namespace}:{version}"
API_REGISTRY_KEY = "main:1.0.0"

def get_api_instance():
    from ninja.main import api_registry
    
    # Check if already registered to avoid ConfigError on reload
    if API_REGISTRY_KEY in api_registry:
        return api_registry[API_REGISTRY_KEY]
        
    return NinjaAPI(
        title="Alessandra M. Donadon API", 
        version="1.0.0", 
        urls_namespace='main'
    )

api = get_api_instance()

# Function to attach routers, ensuring it only happens once per process/reload
def setup_api():
    # Import routers here to avoid circular imports
    from in_brief.api.endpoints import router as in_brief_router
    from apps.intake.api.router import router as intake_router
    from apps.integrations.api.router import router as integrations_router
    from apps.portals.api.router import router as portals_router

    # Only add routers if they aren't already there (Ninja handles this internally but we wrap it)
    try:
        api.add_router("/in-brief", in_brief_router)
        api.add_router("/intake", intake_router)
        api.add_router("/integrations", integrations_router)
        api.add_router("/portals", portals_router)
    except ConfigError:
        pass

# Initialize it
setup_api()
