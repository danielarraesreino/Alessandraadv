from django.db import models
from apps.clients.models import Client
from core.security.fields import EncryptedField

class LegalCase(models.Model):
    """
    Legal Case Management.
    """
    
    STATUS_CHOICES = [
        ('ANALYSIS', 'Em Análise'),
        ('ACTIVE', 'Ativo'),
        ('SUSPENDED', 'Suspenso'),
        ('ARCHIVED', 'Arquivado'),
    ]
    
    AREA_CHOICES = [
        ('CIVIL', 'Cível'),
        ('BUSINESS', 'Empresarial'),
        ('HEALTH', 'Saúde (Lipedema)'),
        ('THIRD_SECTOR', 'Terceiro Setor (Lei Rouanet)'),
        ('OTHER', 'Outros'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cases')
    title = models.CharField("Título da Causa", max_length=255)
    
    # Sensitive Data
    process_number = EncryptedField("Número do Processo", max_length=255, blank=True, null=True)
    
    area = models.CharField("Área de Atuação", max_length=20, choices=AREA_CHOICES, default='CIVIL')
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='ANALYSIS')
    
    description = models.TextField("Descrição/Anotações", blank=True)
    
    entry_date = models.DateField("Data de Entrada", auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.process_number or 'N/A'} - {self.title}"

    class Meta:
        verbose_name = "Caso Jurídico"
        verbose_name_plural = "Casos Jurídicos"
