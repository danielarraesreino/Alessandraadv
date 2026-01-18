from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from django.views.generic import TemplateView
from in_brief.api.endpoints import router as in_brief_router
from apps.intake.api.router import router as intake_router
from apps.integrations.api.router import router as integrations_router
from apps.portals.api.router import router as portals_router
from apps.whatsapp.api import api as whatsapp_api

# Define Main API
api = NinjaAPI(title="Alessandra Donadon API", version="1.0.0")
api.add_router("/in-brief", in_brief_router)
api.add_router("/intake", intake_router)
api.add_router("/integrations", integrations_router)
api.add_router("/portals", portals_router)

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path("api/", api.urls), # Main API
    path("api/whatsapp/", whatsapp_api.urls), # WhatsApp API Instance
    path("in-brief/", include("in_brief.urls")),
    path("portal-admin/", include("admin_portal.urls")),
]
