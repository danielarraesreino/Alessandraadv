from ninja import NinjaAPI
from ninja.errors import ConfigError

# Basic singleton pattern for the Main API
_api = None

def get_api():
    global _api
    if _api is None:
        try:
            _api = NinjaAPI(
                title="Legal Intelligence Platform API", 
                version="1.0.0", 
                urls_namespace='main'
            )
        except ConfigError:
            pass
    return _api

api = get_api()

def setup_api():
    if api is None:
        return
        
    # Import and add routers one by one with logging
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
