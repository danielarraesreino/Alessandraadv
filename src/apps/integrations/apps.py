from django.apps import AppConfig

class IntegrationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.integrations'

    def ready(self):
        from .base.providers import ProviderFactory
        from .providers.native import NativeProvider
        
        # Register Native Provider
        ProviderFactory.register_provider('native', NativeProvider)
