# Phase 4: Production Hardening & Strategic Intelligence

**Implementation Plan**  
**Priority:** CRITICAL - Aesthetic Refinement + Legal Intelligence  
**Estimated Effort:** 3-4 days

---

## 🎯 Objective

Elevate the platform from "functional" to "Class A" by addressing aesthetic gaps and implementing predictive legal intelligence that generic AIs typically neglect.

---

## 🚨 Critical Gaps Identified

### 1. Aesthetic Deficiencies (URGENT)

> [!CAUTION]
> **Current Issues:**
> - Emojis in WhatsApp notifications (🔥, 👤, 📱) - unprofessional for legal context
> - Generic clip-art icons in "Áreas de Atuação"
> - Rigid containers breaking fluid layout philosophy
> - Inconsistent typography (missing Playfair Display in key areas)

**Impact:** Undermines the 25-year authority of Dra. Alessandra

### 2. Intelligence Deficiencies

> [!WARNING]
> **Missing Features:**
> - No ClaimScore™ refinement (basic scoring only)
> - No tribunal monitoring integration
> - No predictive risk analysis
> - Power BI dashboard not implemented

---

## Proposed Changes

### Part 1: Aesthetic Refinement (Priority 1)

#### 1.1 Typography Enforcement

**[MODIFY]** [`theme.css`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/core/static/css/theme.css)

**Changes:**
- Force Playfair Display on ALL headings
- Remove any fallback to system fonts in hero section
- Increase letter-spacing for authority projection

```css
/* Elite Typography Enforcement */
h1, h2, h3, .hero-title, .section-title {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700;
    letter-spacing: -0.03em; /* Tighter for sophistication */
}

.hero-quote {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1.5rem;
    color: var(--color-gray-dark);
}
```

#### 1.2 SVG Icon System

**[NEW]** `src/core/static/icons/`

Create minimalist SVG icons for practice areas:
- `health-law.svg` (Lipedema)
- `consumer-law.svg` (Superendividamento)
- `cultural-law.svg` (Lei Rouanet)
- `general-practice.svg`

**Design Spec:**
- Stroke width: 2px
- Color: `#1A1A1A` (solid black)
- Size: 64x64px
- Style: Line art, no fills

**[MODIFY]** [`home.html`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/core/templates/home.html)

Replace emoji/clip-art with SVG:
```html
<div class="practice-area-icon">
    <svg class="icon-svg">
        <use href="{% static 'icons/health-law.svg' %}#icon"></use>
    </svg>
</div>
```

#### 1.3 100% Fluid Layout Audit

**[MODIFY]** [`theme.css`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/core/static/css/theme.css)

Remove ALL rigid containers:
```css
/* REMOVE */
.container {
    max-width: 1200px; /* ❌ Rigid */
}

/* REPLACE WITH */
.section-fluid {
    width: 100%;
    padding: 0 clamp(2rem, 5vw, 8rem); /* Responsive padding */
    background: var(--color-creme);
}
```

#### 1.4 WhatsApp Message Professionalization

**[MODIFY]** [`apps/whatsapp/services/notification.py`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/apps/whatsapp/services/notification.py)

Remove emojis, use formal language:
```python
def _format_lead_message(self, lead) -> str:
    priority = "ALTA PRIORIDADE" if lead.is_qualified else "Padrão"
    
    message = f"""
*NOVO LEAD - {lead.get_case_type_display().upper()}*
Prioridade: {priority}

Nome: {lead.full_name}
Contato: {lead.contact_info}
Score de Qualificação: {lead.score}/100

Dados da Triagem:
"""
    # ... rest of message
```

---

### Part 2: Case Journey Portal (Priority 2)

#### 2.1 Portal Architecture

**[NEW]** `apps/portals/`

```
apps/portals/
├── models.py           # CaseTimeline, Milestone
├── views.py            # Client-facing views
├── api/
│   └── router.py       # Django Ninja endpoints
└── templates/
    ├── portal_login.html
    ├── case_timeline.html
    └── document_upload.html
```

#### 2.2 Timeline Model

**[NEW]** [`apps/portals/models.py`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/apps/portals/models.py)

```python
class CaseTimeline(models.Model):
    STAGES = [
        ('INTAKE', 'Triagem Inicial'),
        ('PETITION', 'Petição Elaborada'),
        ('FILED', 'Protocolo Realizado'),
        ('HEARING', 'Audiência Agendada'),
        ('DECISION', 'Sentença Proferida'),
        ('CLOSED', 'Caso Encerrado'),
    ]
    
    legal_case = models.ForeignKey('legal_cases.LegalCase', on_delete=models.CASCADE)
    current_stage = models.CharField(max_length=20, choices=STAGES, default='INTAKE')
    milestones = models.JSONField(default=list)  # [{stage, date, notes}]
    
    def progress_percentage(self):
        stage_index = [s[0] for s in self.STAGES].index(self.current_stage)
        return int((stage_index / (len(self.STAGES) - 1)) * 100)
```

#### 2.3 Kanban UI Component

**[NEW]** [`apps/portals/templates/case_timeline.html`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/apps/portals/templates/case_timeline.html)

```html
<div class="timeline-kanban">
    {% for stage, label in timeline.STAGES %}
    <div class="timeline-stage {% if stage == timeline.current_stage %}active{% endif %}">
        <div class="stage-indicator"></div>
        <h4>{{ label }}</h4>
        {% if stage in completed_stages %}
        <span class="stage-date">{{ stage.completion_date }}</span>
        {% endif %}
    </div>
    {% endfor %}
</div>

<style>
.timeline-kanban {
    display: flex;
    justify-content: space-between;
    padding: 3rem 0;
}

.timeline-stage {
    flex: 1;
    text-align: center;
    position: relative;
}

.timeline-stage.active .stage-indicator {
    background: var(--color-salmon);
    box-shadow: 0 0 0 4px var(--color-salmon-light);
}

.stage-indicator {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--color-gray-light);
    margin: 0 auto 1rem;
    transition: all 0.3s ease;
}
</style>
```

---

### Part 3: Power BI Dashboard Integration (Priority 3)

#### 3.1 Analytics Export Service

**[NEW]** [`apps/analytics/export.py`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/apps/analytics/export.py)

```python
import requests
from django.conf import settings
from apps.intake.models import Lead
from apps.legal_cases.models import LegalCase

class PowerBIExporter:
    """Export data to Power BI datasets."""
    
    def __init__(self):
        self.api_url = settings.POWERBI_API_URL
        self.access_token = settings.POWERBI_ACCESS_TOKEN
    
    def export_leads_dataset(self):
        """Export leads for conversion funnel analysis."""
        leads = Lead.objects.all().values(
            'case_type',
            'score',
            'is_qualified',
            'created_at',
            'external_id'
        )
        
        dataset = {
            "rows": [
                {
                    "CaseType": lead['case_type'],
                    "Score": lead['score'],
                    "Qualified": lead['is_qualified'],
                    "CreatedDate": lead['created_at'].isoformat(),
                    "Synced": bool(lead['external_id'])
                }
                for lead in leads
            ]
        }
        
        return self._push_dataset("LeadsFunnel", dataset)
    
    def export_case_metrics(self):
        """Export case metrics for operational BI."""
        cases = LegalCase.objects.select_related('timeline').all()
        
        dataset = {
            "rows": [
                {
                    "CaseID": case.id,
                    "CaseType": case.case_type,
                    "CurrentStage": case.timeline.current_stage,
                    "ProgressPct": case.timeline.progress_percentage(),
                    "DaysOpen": (timezone.now() - case.created_at).days
                }
                for case in cases
            ]
        }
        
        return self._push_dataset("CaseMetrics", dataset)
    
    def _push_dataset(self, dataset_name, data):
        """Push data to Power BI REST API."""
        response = requests.post(
            f"{self.api_url}/datasets/{dataset_name}/rows",
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            },
            json=data
        )
        return response.status_code == 200
```

#### 3.2 KPIs Configuration

**Power BI Measures (DAX):**

```dax
// Taxa de Conversão
ConversionRate = 
DIVIDE(
    COUNTROWS(FILTER(LeadsFunnel, LeadsFunnel[Qualified] = TRUE)),
    COUNTROWS(LeadsFunnel)
)

// Lead-time Médio
AvgLeadTime = 
AVERAGE(CaseMetrics[DaysOpen])

// Receita Projetada
ProjectedRevenue = 
SUMX(
    FILTER(CaseMetrics, CaseMetrics[CurrentStage] <> "CLOSED"),
    CaseMetrics[EstimatedValue]
)
```

---

### Part 4: ClaimScore™ Refinement (Priority 4)

#### 4.1 Advanced Scoring Algorithm

**[MODIFY]** [`apps/intake/api/router.py`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/apps/intake/api/router.py)

```python
def calculate_claim_score(lead: Lead, triage_data: dict) -> int:
    """
    ClaimScore™ Algorithm - Predictive lead qualification.
    
    Factors:
    - Urgency indicators (30 points)
    - Documentation readiness (20 points)
    - Case complexity (20 points)
    - Financial viability (15 points)
    - Geographic proximity (15 points)
    """
    score = 50  # Base score
    
    # Urgency Analysis
    urgency_keywords = ['urgente', 'imediato', 'prazo', 'vencendo']
    if any(kw in str(triage_data).lower() for kw in urgency_keywords):
        score += 30
    
    # Documentation Readiness
    if triage_data.get('has_denial_letter') == 'sim':
        score += 20
    elif triage_data.get('has_medical_report') == 'sim':
        score += 15
    
    # Case Complexity (inverse scoring - simpler = higher)
    if lead.case_type == 'LIPEDEMA':
        score += 10  # Well-defined legal precedent
    elif lead.case_type == 'SUPER':
        score += 5   # More complex, case-by-case
    
    # Financial Viability
    if triage_data.get('employment_status') == 'employed':
        score += 15
    
    # Geographic Proximity (Campinas region)
    if '19' in lead.contact_info:  # DDD 19 = Campinas
        score += 15
    
    return min(score, 100)  # Cap at 100
```

---

## Verification Plan

### Automated Tests

**[NEW]** `apps/portals/tests.py`
```python
def test_timeline_progress_calculation():
    timeline = CaseTimeline.objects.create(current_stage='HEARING')
    assert timeline.progress_percentage() == 60  # 3/5 stages
```

**[NEW]** `apps/analytics/tests.py`
```python
def test_powerbi_export():
    exporter = PowerBIExporter()
    result = exporter.export_leads_dataset()
    assert result is True
```

### Manual Verification

1. **Aesthetic Audit:**
   - [ ] No emojis in WhatsApp messages
   - [ ] All icons are SVG (no clip-art)
   - [ ] Playfair Display on all headings
   - [ ] Zero rigid containers

2. **Portal Testing:**
   - [ ] Timeline renders correctly
   - [ ] Progress bar updates
   - [ ] Client can upload documents

3. **BI Dashboard:**
   - [ ] Data exports to Power BI
   - [ ] KPIs calculate correctly
   - [ ] Real-time updates work

---

## User Review Required

> [!IMPORTANT]
> **Design Decisions:**
> 1. **SVG Icons:** Should we commission custom icons or use open-source (Heroicons)?
> 2. **Portal Access:** OAuth2 via Clio or custom Django authentication?
> 3. **Power BI:** Use embedded reports or standalone dashboard?

---

## Estimated Timeline

| Task | Effort | Priority |
|------|--------|----------|
| Aesthetic Refinement | 4-6 hours | P0 (CRITICAL) |
| SVG Icon System | 2-3 hours | P0 |
| WhatsApp Message Fix | 30 min | P0 |
| Case Journey Portal | 1-2 days | P1 |
| Power BI Integration | 1 day | P2 |
| ClaimScore™ Refinement | 3-4 hours | P2 |

**Total:** 3-4 days for complete Phase 4

---

## Next Steps

1. ✅ Get approval on this plan
2. Execute P0 tasks (aesthetic fixes)
3. Implement Case Journey portal
4. Configure Power BI connection
5. Deploy to staging for UAT
