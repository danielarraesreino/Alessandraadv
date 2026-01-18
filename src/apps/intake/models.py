from django.db import models
from django.utils import timezone

class Lead(models.Model):
    CASE_TYPES = [
        ('LIPEDEMA', 'Lipedema/Saúde'),
        ('SUPER', 'Superendividamento'),
        ('CULTURAL', 'Lei Rouanet/Cultural'),
        ('OTHER', 'Outros Assuntos'),
    ]

    full_name = models.CharField("Nome do Lead", max_length=255)
    contact_info = models.CharField("WhatsApp/Email", max_length=255)
    case_type = models.CharField("Tipo de Caso", max_length=20, choices=CASE_TYPES)
    
    # Store triage as JSON for flexibility
    triage_data = models.JSONField(default=dict, blank=True)
    
    score = models.IntegerField(default=0)
    is_qualified = models.BooleanField(default=False)
    
    # [NEW] External system tracking
    external_id = models.CharField(
        "ID Externo (Clio/Jestor)", 
        max_length=255, 
        blank=True, 
        null=True,
        help_text="ID do caso no sistema Legal Ops"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.get_case_type_display()}"

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

class TriageSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    current_step = models.IntegerField(default=1)
    temp_data = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)
