from django.db import models
from core.security.fields import EncryptedField

class Client(models.Model):
    """
    Client Identity Management.
    Sensitive data (CPF, Phone) is encrypted at rest.
    """
    
    TYPE_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]
    
    full_name = models.CharField("Nome Completo", max_length=255)
    client_type = models.CharField("Tipo", max_length=2, choices=TYPE_CHOICES, default='PF')
    
    # PII - Personally Identifiable Information (Encrypted)
    cpf_cnpj = EncryptedField("CPF/CNPJ", max_length=255, unique=True, help_text="Stored encrypted")
    phone = EncryptedField("Telefone/WhatsApp", max_length=255, help_text="Stored encrypted")
    email = models.EmailField("E-mail", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.get_client_type_display()})"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-created_at']
