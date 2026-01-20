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
        print(">>> NINJA API IS NONE, SKIPPING SETUP <<<")
        return
        
    print(">>> STARTING NINJA API ROUTER ATTACHMENT <<<")
    
    # Import and add routers one by one with logging
    try:
        from in_brief.api.endpoints import router as in_brief_router
        api.add_router("/in-brief", in_brief_router)
        print(">>> ATTACHED /in-brief <<<")
    except Exception as e:
        print(f">>> ERROR ATTACHING /in-brief: {e} <<<")

    try:
        from apps.intake.api.router import router as intake_router
        api.add_router("/intake", intake_router)
        print(">>> ATTACHED /intake <<<")
    except Exception as e:
        print(f">>> ERROR ATTACHING /intake: {e} <<<")

    try:
        from apps.integrations.api.router import router as integrations_router
        api.add_router("/integrations", integrations_router)
        print(">>> ATTACHED /integrations <<<")
    except Exception as e:
        print(f">>> ERROR ATTACHING /integrations: {e} <<<")

    try:
        from apps.portals.api.router import router as portals_router
        api.add_router("/portals", portals_router)
        print(">>> ATTACHED /portals <<<")
    except Exception as e:
        print(f">>> ERROR ATTACHING /portals: {e} <<<")

    print(">>> FINISHED NINJA API ROUTER ATTACHMENT <<<")

# Initialize it
setup_api()
