# Phase 4 Final - BI, ClaimScore™ & Quality Gates

**Strategic Value:** R$70k+ Legal Intelligence Platform  
**Completion:** 90% → 100%

---

## 1. Power BI Dashboard Integration

### Objective
Transform raw legal data into strategic KPIs for Dra. Alessandra's decision-making.

### Architecture

```mermaid
graph LR
    A[Django Models] -->|Export Service| B[Power BI REST API]
    B --> C[Power BI Datasets]
    C --> D[Dashboard Visuals]
    D --> E[KPIs]
    
    style C fill:#2196F3
    style E fill:#4CAF50
```

### Implementation

#### Analytics Export Service

**File:** `apps/analytics/export.py`

```python
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from apps.intake.models import Lead
from apps.legal_cases.models import LegalCase
from apps.portals.models import CaseTimeline


class PowerBIExporter:
    """Export legal data to Power BI for strategic analytics."""
    
    def __init__(self):
        self.api_url = getattr(settings, 'POWERBI_API_URL', None)
        self.access_token = getattr(settings, 'POWERBI_ACCESS_TOKEN', None)
    
    def export_leads_funnel(self):
        """
        Export lead conversion funnel data.
        
        KPI: Taxa de Conversão (Leads → Casos)
        """
        last_30_days = timezone.now() - timedelta(days=30)
        leads = Lead.objects.filter(created_at__gte=last_30_days)
        
        dataset = {
            "rows": [
                {
                    "Date": lead.created_at.date().isoformat(),
                    "CaseType": lead.get_case_type_display(),
                    "Score": lead.score,
                    "Qualified": lead.is_qualified,
                    "Synced": bool(lead.external_id),
                    "Source": "Website"
                }
                for lead in leads
            ]
        }
        
        return self._push_dataset("LeadsFunnel", dataset)
    
    def export_case_metrics(self):
        """
        Export case operational metrics.
        
        KPIs: Lead-time médio, Taxa de Êxito
        """
        cases = LegalCase.objects.select_related('timeline').all()
        
        dataset = {
            "rows": [
                {
                    "CaseID": case.id,
                    "CaseType": case.case_type,
                    "CurrentStage": case.timeline.current_stage if hasattr(case, 'timeline') else 'INTAKE',
                    "ProgressPct": case.timeline.progress_percentage() if hasattr(case, 'timeline') else 0,
                    "DaysOpen": (timezone.now() - case.created_at).days,
                    "EstimatedValue": 0  # Placeholder for financial data
                }
                for case in cases
            ]
        }
        
        return self._push_dataset("CaseMetrics", dataset)
    
    def export_risk_analysis(self):
        """
        Export risk projection data.
        
        KPI: Risco Financeiro Projetado
        """
        # Placeholder for risk analysis logic
        # In production, integrate with legal precedent database
        pass
    
    def _push_dataset(self, dataset_name: str, data: dict) -> bool:
        """Push data to Power BI REST API."""
        if not self.api_url or not self.access_token:
            print(f"[Power BI] Mock export to {dataset_name}: {len(data['rows'])} rows")
            return True
        
        try:
            response = requests.post(
                f"{self.api_url}/datasets/{dataset_name}/rows",
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                },
                json=data,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"[Power BI Error] {e}")
            return False
```

### Power BI Measures (DAX)

```dax
// Taxa de Conversão
ConversionRate = 
DIVIDE(
    COUNTROWS(FILTER(LeadsFunnel, LeadsFunnel[Qualified] = TRUE)),
    COUNTROWS(LeadsFunnel),
    0
)

// Lead-time Médio
AvgLeadTime = 
AVERAGE(CaseMetrics[DaysOpen])

// Taxa de Êxito (casos fechados com sucesso)
SuccessRate = 
DIVIDE(
    COUNTROWS(FILTER(CaseMetrics, CaseMetrics[CurrentStage] = "CLOSED" && CaseMetrics[Outcome] = "SUCCESS")),
    COUNTROWS(FILTER(CaseMetrics, CaseMetrics[CurrentStage] = "CLOSED")),
    0
)

// Receita Projetada
ProjectedRevenue = 
SUMX(
    FILTER(CaseMetrics, CaseMetrics[CurrentStage] <> "CLOSED"),
    CaseMetrics[EstimatedValue]
)
```

### Django Management Command

```python
# apps/analytics/management/commands/export_to_powerbi.py
from django.core.management.base import BaseCommand
from apps.analytics.export import PowerBIExporter

class Command(BaseCommand):
    help = 'Export data to Power BI'
    
    def handle(self, *args, **options):
        exporter = PowerBIExporter()
        
        self.stdout.write('Exporting leads funnel...')
        exporter.export_leads_funnel()
        
        self.stdout.write('Exporting case metrics...')
        exporter.export_case_metrics()
        
        self.stdout.write(self.style.SUCCESS('Export complete!'))
```

**Cron Job (Production):**
```bash
# Run every 6 hours
0 */6 * * * cd /path/to/project && ./.venv/bin/python manage.py export_to_powerbi
```

---

## 2. ClaimScore™ Algorithm Refinement

### Current vs Enhanced

**Current (Basic):**
```python
score = 50
if "urgente" in str(data).lower(): score += 30
if "sim" in str(data).lower(): score += 20
```

**Enhanced (Predictive):**

```python
def calculate_claim_score(lead: Lead, triage_data: dict) -> int:
    """
    ClaimScore™ - Predictive lead qualification algorithm.
    
    Factors (weighted):
    - Urgency indicators (30 points)
    - Documentation readiness (20 points)
    - Case complexity (20 points)
    - Financial viability (15 points)
    - Geographic proximity (15 points)
    
    Returns:
        Score 0-100 (>60 = qualified)
    """
    score = 50  # Base score
    
    # 1. Urgency Analysis (30 points)
    urgency_keywords = ['urgente', 'imediato', 'prazo', 'vencendo', 'emergência']
    urgency_count = sum(1 for kw in urgency_keywords if kw in str(triage_data).lower())
    score += min(urgency_count * 10, 30)
    
    # 2. Documentation Readiness (20 points)
    if triage_data.get('has_denial_letter') == 'sim':
        score += 20
    elif triage_data.get('has_medical_report') == 'sim':
        score += 15
    elif triage_data.get('has_evidence') == 'sim':
        score += 10
    
    # 3. Case Complexity (inverse scoring - simpler = higher)
    complexity_map = {
        'LIPEDEMA': 15,  # Well-defined legal precedent
        'SUPER': 10,     # More complex, case-by-case
        'CULTURAL': 12,  # Moderate complexity
        'OTHER': 5       # Unknown complexity
    }
    score += complexity_map.get(lead.case_type, 5)
    
    # 4. Financial Viability (15 points)
    employment_status = triage_data.get('employment_status', '').lower()
    if 'empregado' in employment_status or 'clt' in employment_status:
        score += 15
    elif 'autonomo' in employment_status or 'mei' in employment_status:
        score += 10
    elif 'desempregado' in employment_status:
        score += 5  # Still viable with contingency fee
    
    # 5. Geographic Proximity (15 points)
    # DDD 19 = Campinas region (easier logistics)
    contact = lead.contact_info
    if '19' in contact or '(19)' in contact:
        score += 15
    elif any(ddd in contact for ddd in ['11', '13', '15']):  # SP state
        score += 10
    else:
        score += 5  # Remote but still viable
    
    # 6. Bonus: Referral or returning client
    if triage_data.get('referral_source') == 'client':
        score += 10  # Bonus for referrals
    
    return min(score, 100)  # Cap at 100
```

### A/B Testing Framework

```python
# apps/intake/scoring.py
from enum import Enum

class ScoringAlgorithm(Enum):
    BASIC = "basic"
    CLAIMSCORE = "claimscore"

def score_lead(lead: Lead, algorithm: ScoringAlgorithm = ScoringAlgorithm.CLAIMSCORE):
    """Route to appropriate scoring algorithm."""
    if algorithm == ScoringAlgorithm.BASIC:
        return _basic_score(lead)
    else:
        return calculate_claim_score(lead, lead.triage_data)
```

---

## 3. Quality Gates (SonarQube + Sentry MCP)

### SonarQube Configuration

**File:** `sonar-project.properties`

```properties
sonar.projectKey=alessandra-legal-ops
sonar.projectName=Alessandra Donadon - Legal Intelligence Platform
sonar.projectVersion=4.0.0

# Source directories
sonar.sources=src/apps,src/core,src/in_brief
sonar.exclusions=**/migrations/**,**/tests.py,**/__pycache__/**

# Python specific
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml

# Quality Gates
sonar.qualitygate.wait=true
sonar.qualitygate.timeout=300

# Thresholds
sonar.coverage.exclusions=**/tests/**,**/migrations/**
```

**Quality Gate Rules:**
- ✅ 0 vulnerabilities (blocker)
- ✅ 0 bugs (critical)
- ✅ 80%+ coverage on new code
- ✅ Duplicação < 3%
- ✅ Complexidade ciclomática < 15

### Sentry Integration

**File:** `core/settings.py`

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=False,  # LGPD compliance
        before_send=redact_pii,  # Custom PII redaction
    )

def redact_pii(event, hint):
    """Redact PII from Sentry events."""
    # Remove sensitive data from exception context
    if 'request' in event:
        event['request'].pop('cookies', None)
        event['request'].pop('headers', None)
    return event
```

### Bandit Security Scan

```bash
# Install
pip install bandit

# Run scan
bandit -r src/ -f json -o bandit-report.json

# Critical checks
bandit -r src/ -ll  # Only high severity
```

### Pre-commit Hooks

**File:** `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: ['-ll', '-i']  # High severity only
  
  - repo: local
    hooks:
      - id: django-check
        name: Django Check
        entry: python manage.py check
        language: system
        pass_filenames: false
```

---

## Implementation Timeline

| Component | Effort | Priority |
|-----------|--------|----------|
| Power BI Export Service | 2-3 hours | P2 |
| ClaimScore™ Refinement | 1-2 hours | P1 |
| SonarQube Setup | 1 hour | P2 |
| Sentry Integration | 30 min | P1 |
| Pre-commit Hooks | 30 min | P2 |

**Total:** 5-7 hours (~1 day)

---

## Success Metrics

### Power BI
- ✅ Dashboards atualizam a cada 6 horas
- ✅ Taxa de conversão visível
- ✅ Lead-time médio calculado

### ClaimScore™
- ✅ Precisão > 85% (qualified leads convert)
- ✅ Redução de 30% em leads não qualificados

### Quality Gates
- ✅ 0 vulnerabilidades críticas
- ✅ 80%+ cobertura de testes
- ✅ Sentry captura 100% dos erros em produção

---

## Next Steps

1. Implement ClaimScore™ (highest ROI)
2. Setup Sentry for production monitoring
3. Create Power BI export service
4. Configure SonarQube quality gates
5. Deploy to staging for validation
