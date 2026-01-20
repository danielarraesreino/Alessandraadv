from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from apps.portals import views as portals_views
from core import views
from core.views import role_based_redirect

# Temporarily disabled all APIs to isolate 500 error
# from core.api import api
# from apps.whatsapp.api import api as whatsapp_api

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("health/", views.health_check, name="health_check"),
    path("role-redirect/", role_based_redirect, name="role_redirect"),
    path("admin/", admin.site.urls),
    # path("api/", api.urls), 
    # path("api/whatsapp/", whatsapp_api.urls), 
    path("in-brief/", include("in_brief.urls")),
    path("portal-admin/", include("admin_portal.urls")),
    path("portal-admin/observatory/", include("apps.observatory.urls")),
    path("acesso/", portals_views.client_login, name="client_login"),
    path("portal/", include("apps.portals.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('accounts/', include('allauth.urls')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
