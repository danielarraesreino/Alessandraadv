from django.db import models
from django.utils import timezone

class HumanRightsCase(models.Model):
    PERIOD_CHOICES = [
        ('SEC_20', 'Século XX (1901-2000)'),
        ('SEC_21', 'Século XXI (2001-Presente)'),
    ]

    VIOLATION_CHOICES = [
        ('CENSURA', 'Censura e Liberdade de Expressão'),
        ('TORTURA', 'Tortura e Tratamento Desumano'),
        ('TRABALHO_ESCRAVO', 'Trabalho Análogo à Escravidão'),
        ('VIOLENCIA_POLICIAL', 'Violência Policial / Letalidade'),
        ('PERSEGUICAO_POLITICA', 'Perseguição Política'),
        ('NEGLIGENCIA_ESTATAL', 'Negligência Estatal / Saúde / Educação'),
        ('DIREITOS_INDIGENAS', 'Violação de Direitos Indígenas/Ambientais'),
        ('DISCRIMINACAO', 'Discriminação (Raca, Gênero, Orientação)'),
        ('MASSACRE', 'Massacres e Chacinas'),
    ]

    STATUS_CHOICES = [
        ('RECONHECIDO', 'Reconhecido pelo Estado (Anistia/Indenização)'),
        ('EM_ANALISE', 'Em Análise / Judicializado'),
        ('IMPUNE', 'Impune / Arquivado'),
        ('MEMORIA', 'Memória/Legado (Sem resolução judicial)'),
    ]

    name = models.CharField("Nome da Vítima/Caso", max_length=255)
    period = models.CharField("Período Histórico", max_length=20, choices=PERIOD_CHOICES)
    violation_type = models.CharField("Tipo de Violação", max_length=50, choices=VIOLATION_CHOICES)
    description = models.TextField("Descrição do Caso")
    date_event = models.DateField("Data do Evento (Aprox)", default=timezone.now)
    location = models.CharField("Localização (Estado/Cidade)", max_length=100)
    impact_level = models.IntegerField("Nível de Impacto Histórico (1-10)", default=5)
    status = models.CharField("Status Jurídico/Histórico", max_length=50, choices=STATUS_CHOICES, default='MEMORIA')
    
    # Metadata
    source_link = models.URLField("Fonte/Referência", blank=True, null=True)
    image_url = models.URLField("Imagem (URL)", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Caso de Direitos Humanos"
        verbose_name_plural = "Observatório - Casos"
        ordering = ['-date_event']

    def __str__(self):
        return f"{self.name} ({self.get_period_display()})"
