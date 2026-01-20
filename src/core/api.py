from ninja import NinjaAPI
from ninja.errors import ConfigError

_api = None

def get_api():
    global _api
    if _api is None:
        try:
            _api = NinjaAPI(
                title="Legal Intelligence Platform API",
                version="4.0.0",
                urls_namespace='main'
            )
            
            # Attach routers
            try:
                from in_brief.api.endpoints import router as in_brief_router
                _api.add_router("/in-brief", in_brief_router)
            except Exception:
                pass

            try:
                from apps.intake.api.router import router as intake_router
                _api.add_router("/intake", intake_router)
            except Exception:
                pass

            try:
                from apps.integrations.api.router import router as integrations_router
                _api.add_router("/integrations", integrations_router)
            except Exception:
                pass

            try:
                from apps.portals.api.router import router as portals_router
                _api.add_router("/portals", portals_router)
            except Exception:
                pass
                
        except ConfigError:
            # If already registered, return a surrogate or handle gracefully
            # On Railway, this shouldn't happen anymore with correct dependencies
            _api = NinjaAPI(urls_namespace='main_alt')
            
    return _api

api = get_api()
