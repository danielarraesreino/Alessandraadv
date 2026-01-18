from django.apps import AppConfig


class PortalsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.portals"
    verbose_name = "Portal do Cliente"
    
    def ready(self):
        """Import signals when app is ready."""
        import apps.portals.signals
