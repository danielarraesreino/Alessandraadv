from django.db import models
from django.utils import timezone
from core.security.fields import EncryptedField

class Lead(models.Model):
    CASE_TYPES = [
        ('LIPEDEMA', 'Lipedema/Saúde'),
        ('SUPER', 'Superendividamento'),
        ('CULTURAL', 'Lei Rouanet/Cultural'),
        ('OTHER', 'Outros Assuntos'),
    ]

    full_name = models.CharField("Nome do Lead", max_length=255)
    contact_info = EncryptedField("WhatsApp/Email", max_length=255, help_text="Dados sensíveis criptografados")
    case_type = models.CharField("Tipo de Caso", max_length=20, choices=CASE_TYPES)
    
    # Store triage as JSON for flexibility
    triage_data = models.JSONField(default=dict, blank=True)
    
    score = models.IntegerField("ClaimScore", default=0, help_text="Pontuação de viabilidade (0-100)")
    
    VIABILITY_CHOICES = [
        ('PENDING', 'Em Análise'),
        ('HIGH', 'Alta Probabilidade'),
        ('MEDIUM', 'Média Probabilidade'),
        ('LOW', 'Baixa Probabilidade'),
        ('REJECTED', 'Inviável'),
    ]
    viability_status = models.CharField("Viabilidade", max_length=20, choices=VIABILITY_CHOICES, default='PENDING')
    is_qualified = models.BooleanField("Qualificado?", default=False)

    # [NEW] Tracking distribution
    source = models.CharField("Fonte do Lead", max_length=100, default="Orgânico", blank=True)
    location = models.CharField("Localização (Cidade/Estado)", max_length=100, blank=True)
    
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
        return f"{self.full_name} - {self.get_case_type_display()} ({self.score})"

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

class LeadAnalysis(models.Model):
    """
    Detailed AI analysis of a lead's viability.
    Stores the reasoning behind the ClaimScore.
    """
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, related_name='analysis')
    summary = models.TextField("Resumo Executivo")
    positive_points = models.JSONField("Pontos Fortes", default=list)
    negative_points = models.JSONField("Pontos de Atenção", default=list)
    recommended_action = models.CharField("Ação Recomendada", max_length=255)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Análise: {self.lead.full_name}"

class TriageSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    current_step = models.IntegerField(default=1)
    temp_data = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)
