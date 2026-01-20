from ninja import NinjaAPI
from ninja.errors import ConfigError

# Basic singleton pattern for the Main API
# This ensures that even if the module is re-imported, we don't crash on double registration
_api = None

def get_api():
    global _api
    if _api is None:
        try:
            _api = NinjaAPI(
                title="Alessandra M. Donadon API", 
                version="1.0.0", 
                urls_namespace='main'
            )
        except ConfigError:
            # If we hit this, it means it's already registered globally by Ninja
            # but we lost our local reference. This shouldn't happen with proper module imports
            # but we catch it just in case.
            pass
    return _api

api = get_api()

# Function to attach routers, ensuring it only happens once per process/reload
def setup_api():
    if api is None:
        return
        
    # Import routers here to avoid circular imports
    from in_brief.api.endpoints import router as in_brief_router
    from apps.intake.api.router import router as intake_router
    from apps.integrations.api.router import router as integrations_router
    from apps.portals.api.router import router as portals_router

    # Ninja handles duplicate router attachment via ConfigError
    try:
        api.add_router("/in-brief", in_brief_router)
        api.add_router("/intake", intake_router)
        api.add_router("/integrations", integrations_router)
        api.add_router("/portals", portals_router)
    except ConfigError:
        pass

# Initialize it
setup_api()
