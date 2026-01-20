from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from ninja.errors import ConfigError
from django.views.generic import TemplateView

from apps.portals import views as portals_views

from core.api import api


from core import views
from core.views import role_based_redirect
from apps.whatsapp.api import api as whatsapp_api

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("health/", views.health_check, name="health_check"),
    path("db-health/", views.db_health_check, name="db_health_check"),
    path("role-redirect/", role_based_redirect, name="role_redirect"),
    path("admin/", admin.site.urls),
    path("api/", api.urls), # Main API
    path("api/whatsapp/", whatsapp_api.urls), # WhatsApp API Instance
    path("in-brief/", include("in_brief.urls")),
    path("portal-admin/", include("admin_portal.urls")),
    path("portal-admin/observatory/", include("apps.observatory.urls")),
    path("acesso/", include([
        path("", portals_views.client_login, name="client_login"),
    ])),
    path("portal/", include("apps.portals.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('accounts/', include('allauth.urls')), # [NEW] Allauth URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
