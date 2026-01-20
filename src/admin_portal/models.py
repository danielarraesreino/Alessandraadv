from django.db import models

class SystemSettings(models.Model):
    whatsapp_enabled = models.BooleanField(default=True)
    clio_integration_active = models.BooleanField(default=False)
    jestor_integration_active = models.BooleanField(default=False)
    client_notification_auto = models.BooleanField(default=True)
    token_validity_days = models.IntegerField(default=30)
    office_name = models.CharField(max_length=200, default="Alessandra M. Donadon")
    
    class Meta:
        verbose_name = "Configurações do Sistema"
        verbose_name_plural = "Configurações do Sistema"

    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(id=1)
        return settings

    def __str__(self):
        return f"Configurações - {self.office_name}"
