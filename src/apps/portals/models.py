"""
Models for Client Portal & Case Journey.

Inspired by Hona system - provides transparency and autonomy for clients.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.legal_cases.models import LegalCase


class CaseTimeline(models.Model):
    """
    Timeline tracking for legal cases.
    
    Provides Kanban-style visualization of case progress.
    """
    STAGES = [
        ('INTAKE', 'Triagem Inicial'),
        ('ANALYSIS', 'Análise Jurídica'),
        ('PETITION', 'Petição Elaborada'),
        ('FILED', 'Protocolo Realizado'),
        ('DISCOVERY', 'Fase Instrutória'),
        ('HEARING', 'Audiência Agendada'),
        ('DECISION', 'Sentença Proferida'),
        ('APPEAL', 'Recurso Interposto'),
        ('CLOSED', 'Caso Encerrado'),
    ]
    
    legal_case = models.OneToOneField(
        LegalCase, 
        on_delete=models.CASCADE,
        related_name='timeline'
    )
    current_stage = models.CharField(
        "Etapa Atual",
        max_length=20, 
        choices=STAGES, 
        default='INTAKE'
    )
    milestones = models.JSONField(
        "Marcos do Processo",
        default=list,
        help_text="Lista de {stage, date, notes, updated_by}"
    )
    last_update = models.DateTimeField("Última Atualização", auto_now=True)
    
    class Meta:
        verbose_name = "Linha do Tempo"
        verbose_name_plural = "Linhas do Tempo"
    
    def __str__(self):
        return f"Timeline: {self.legal_case}"
    
    def progress_percentage(self) -> int:
        """Calculate progress as percentage."""
        try:
            stage_index = [s[0] for s in self.STAGES].index(self.current_stage)
            return int((stage_index / (len(self.STAGES) - 1)) * 100)
        except ValueError:
            return 0
    
    def add_milestone(self, stage: str, notes: str, updated_by: User):
        """Add a new milestone to the timeline."""
        milestone = {
            'stage': stage,
            'date': timezone.now().isoformat(),
            'notes': notes,
            'updated_by': updated_by.get_full_name() or updated_by.username
        }
        self.milestones.append(milestone)
        self.current_stage = stage
        self.save()
    
    def get_completed_stages(self) -> list:
        """Return list of completed stage codes."""
        return [m['stage'] for m in self.milestones]


class CaseDocument(models.Model):
    """
    Documents associated with a legal case.
    
    Supports client uploads and lawyer-provided documents.
    """
    DOCUMENT_TYPES = [
        ('PETITION', 'Petição Inicial'),
        ('EVIDENCE', 'Documento Probatório'),
        ('COURT_ORDER', 'Decisão Judicial'),
        ('CORRESPONDENCE', 'Correspondência'),
        ('CONTRACT', 'Contrato/Acordo'),
        ('OTHER', 'Outro'),
    ]
    
    legal_case = models.ForeignKey(
        LegalCase,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(
        "Tipo de Documento",
        max_length=20,
        choices=DOCUMENT_TYPES
    )
    title = models.CharField("Título", max_length=255)
    description = models.TextField("Descrição", blank=True)
    file = models.FileField(
        "Arquivo",
        upload_to='case_documents/%Y/%m/'
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Enviado por"
    )
    uploaded_at = models.DateTimeField("Data de Upload", auto_now_add=True)
    is_visible_to_client = models.BooleanField(
        "Visível para Cliente",
        default=True,
        help_text="Se desmarcado, apenas advogados podem ver"
    )
    
    class Meta:
        verbose_name = "Documento do Caso"
        verbose_name_plural = "Documentos dos Casos"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_document_type_display()})"


class ClientPortalAccess(models.Model):
    """
    Manages client access to their case portal.
    
    Uses token-based authentication for security.
    """
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='portal_access'
    )
    legal_case = models.ForeignKey(
        LegalCase,
        on_delete=models.CASCADE
    )
    access_token = models.CharField(
        "Token de Acesso",
        max_length=64,
        unique=True,
        help_text="Token único para acesso ao portal"
    )
    is_active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    last_accessed = models.DateTimeField("Último Acesso", null=True, blank=True)
    
    class Meta:
        verbose_name = "Acesso ao Portal"
        verbose_name_plural = "Acessos ao Portal"
        unique_together = ['client', 'legal_case']
    
    def __str__(self):
        return f"Portal Access: {self.client} - {self.legal_case}"
    
    def record_access(self):
        """Record that the client accessed the portal."""
        self.last_accessed = timezone.now()
        self.save(update_fields=['last_accessed'])
