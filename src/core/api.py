from ninja import NinjaAPI

_api = None

def get_api():
    """
    Singleton for the main API instance. 
    Ensures unique namespace and version to avoid conflicts.
    """
    global _api
    if _api is not None:
        return _api
        
    for existing_api in NinjaAPI._registry:
        if getattr(existing_api, "urls_namespace", None) == 'main':
            _api = existing_api
            return _api

    _api = NinjaAPI(
        title="Legal Intelligence Platform API",
        version="1.1.0",
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
                
    return _api

api = get_api()
