from ninja import NinjaAPI
from ninja.errors import ConfigError
import sys

# DEFENSIIVA ABSOLUTA: Usar sys como âncora global para evitar dupla instanciação
# mesmo que o módulo seja re-importado por caminhos diferentes (ex: src.core.api vs core.api)
if not hasattr(sys, '_ninja_main_api'):
    print(">>> INSTANTIATING MAIN NINJA API (FIRST TIME) <<<")
    try:
        sys._ninja_main_api = NinjaAPI(
            title="Legal Intelligence Platform API", 
            version="3.2.0", 
            urls_namespace='main_final' 
        )
        # Mark that we need to setup routers
        sys._ninja_main_api._needs_setup = True
    except ConfigError:
        print(">>> CONFIG ERROR DURING INSTANTIATION - THIS SHOULD NOT HAPPEN WITH UNIQUE NAMES <<<")
        # Fallback de emergência (não vai ter os routers, mas não quebra o boot)
        sys._ninja_main_api = NinjaAPI(urls_namespace='main_emergency')
else:
    print(">>> REUSING EXISTING MAIN NINJA API <<<")

api = sys._ninja_main_api

def setup_api():
    if not getattr(api, '_needs_setup', False):
        return
        
    print(">>> ATTACHING ROUTERS TO MAIN API <<<")
    try:
        from in_brief.api.endpoints import router as in_brief_router
        api.add_router("/in-brief", in_brief_router)
    except Exception as e:
        print(f">>> ERROR ATTACHING IN-BRIEF: {e} <<<")

    try:
        from apps.intake.api.router import router as intake_router
        api.add_router("/intake", intake_router)
    except Exception as e:
        print(f">>> ERROR ATTACHING INTAKE: {e} <<<")

    try:
        from apps.integrations.api.router import router as integrations_router
        api.add_router("/integrations", integrations_router)
    except Exception as e:
        print(f">>> ERROR ATTACHING INTEGRATIONS: {e} <<<")

    try:
        from apps.portals.api.router import router as portals_router
        api.add_router("/portals", portals_router)
    except Exception as e:
        print(f">>> ERROR ATTACHING PORTALS: {e} <<<")
    
    api._needs_setup = False

# Initialize it
setup_api()
