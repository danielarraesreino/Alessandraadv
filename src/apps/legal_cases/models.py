from django.db import models
from apps.clients.models import Client
from core.security.fields import EncryptedField

class LegalCase(models.Model):
    """
    Legal Case Management.
    """
    
    AREA_CHOICES = [
        ('CIVIL', 'Direito Cível'),
        ('BUSINESS', 'Direito Empresarial'),
        ('HEALTH', 'Saúde (Lipedema)'),
        ('THIRD_SECTOR', 'Terceiro Setor (Lei Rouanet)'),
        ('OTHER', 'Outros'),
    ]

    STATUS_CHOICES = [
        ('ANALYSIS', 'Em Análise'),
        ('ACTIVE', 'Ativo'),
        ('SUSPENDED', 'Suspenso'),
        ('ARCHIVED', 'Arquivado'),
    ]

    RISK_CHOICES = [
        ('LOW', 'Baixo - Provável Êxito'),
        ('MEDIUM', 'Médio - Possível Êxito'),
        ('HIGH', 'Alto - Remoto Êxito'),
    ]

    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='cases')
    title = models.CharField("Título do Caso", max_length=255)
    area = models.CharField("Área de Atuação", max_length=20, choices=AREA_CHOICES)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='ANALYSIS')
    process_number = models.CharField("Número do Processo", max_length=100, blank=True)
    description = models.TextField("Descrição/Observações", blank=True)
    
    # [NEW] ERP / Risk Provisioning
    risk_level = models.CharField("Nível de Risco (Contingência)", max_length=10, choices=RISK_CHOICES, default='LOW')
    contingency_value = models.DecimalField("Valor da Causa/Contingência", max_digits=12, decimal_places=2, default=0.00)
    
    entry_date = models.DateField("Data de Entrada", auto_now_add=True)
    last_update = models.DateTimeField("Última Atualização", auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.client.full_name}"

    class Meta:
        verbose_name = "Caso Jurídico"
        verbose_name_plural = "Casos Jurídicos"
