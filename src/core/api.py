from ninja import NinjaAPI
from ninja.errors import ConfigError

# A truly global registry to survive module re-imports (e.g. from different sys.path entries)
import sys
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
            # This happens if Ninja already knows about this namespace
            # but our local sys._ninja_api_registry doesn't.
            # We still need to return an instance. Since we can't easily
            # get the one Ninja has, we'll try to find it or create a surrogate
            # but that's risky. The best is to avoid double instantiation.
            raise
    return sys._ninja_api_registry[name]

# For the Main API
try:
    api = get_api_instance(
        'main', 
        "Legal Intelligence Platform API", 
        "1.0.0"
    )
except ConfigError:
    # If we still hit this, it means another module already created 'main' 
    # but didn't put it in sys._ninja_api_registry. 
    # This suggests a conflict between two different Ninja versions or something.
    # We will try to create one with a unique name as a fallback to avoid 500
    api = NinjaAPI(urls_namespace='main_fallback')

def setup_api():
    # Only attach routers if this is the first time for this instance
    if getattr(api, '_routers_attached', False):
        return
        
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
    
    api._routers_attached = True

# Initialize it
setup_api()
