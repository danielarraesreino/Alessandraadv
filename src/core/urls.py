from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.templatetags.static import static as static_url

from apps.portals import views as portals_views
from core.api import api
from core import views
from core.views import role_based_redirect


urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.png")),
    path("", views.home, name="home"),
    path("contato/", TemplateView.as_view(template_name="contact.html"), name="contact"),
    path("politica-de-privacidade/", views.privacy_policy, name="privacy_policy"),
    path("health/", views.health_check, name="health_check"),
    path("role-redirect/", role_based_redirect, name="role_redirect"),
    path("admin/", admin.site.urls),
    path("api/", api.urls), # Main API with merged routers (including WhatsApp)
    path("in-brief/", include("in_brief.urls")),
    path("portal-admin/", include("admin_portal.urls")),
    path("portal-admin/observatory/", include("apps.observatory.urls")),
    path("acesso/", portals_views.client_login, name="client_login"),
    path("portal/", include("apps.portals.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('accounts/', include('allauth.urls')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
