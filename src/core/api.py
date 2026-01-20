from ninja import NinjaAPI
from ninja.errors import ConfigError

# Define Main API as a singleton-friendly object
api = NinjaAPI(
    title="Alessandra M. Donadon API", 
    version="1.0.0", 
    urls_namespace='main'
)
print(">>> NINJA API INITIALIZED WITH NAMESPACE: 'main' <<<")

# Function to attach routers, ensuring it only happens once per process/reload
def setup_api():
    # Import routers here to avoid circular imports
    from in_brief.api.endpoints import router as in_brief_router
    from apps.intake.api.router import router as intake_router
    from apps.integrations.api.router import router as integrations_router
    from apps.portals.api.router import router as portals_router

    try:
        api.add_router("/in-brief", in_brief_router)
        api.add_router("/intake", intake_router)
        api.add_router("/integrations", integrations_router)
        api.add_router("/portals", portals_router)
    except ConfigError:
        # Already attached
        pass

# Initialize it
setup_api()
