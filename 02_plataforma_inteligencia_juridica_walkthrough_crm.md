# Legal CRM & Mission Control Implementation Plan

Transforming the institutional site of Dra. Alessandra Donadon into an elite Legal Ops platform.

## User Review Required

> [!IMPORTANT]
> **Data Privacy (LGPD)**: All PII in the CRM (CPFs, Addresses) will be encrypted using `EncryptedField`.
> **Webhooks**: WhatsApp integration requires a webhook endpoint (Django Ninja) to receive lead data.
> **DDD Architecture**: New modules (`apps.clients`, `apps.intake`) will follow Domain-Driven Design principles.

## Proposed Changes

### 1. Lead Intake & Smart Triagem (HTMX)
#### [MODIFY] [home.html](file:///home/dan/Área de Trabalho/alessandra antigravity/src/core/templates/home.html)
- Replace static contact form with an HTMX-powered step-by-step triage bot.
- Capture specific data for **Lipedema** and **Superendividamento**.

### 2. Back-End CRM & Intelligence
#### [NEW] [apps.intake](file:///home/dan/Área de Trabalho/alessandra antigravity/src/intake)
- `models.py`: Lead scoring and qualification logic.
- `api.py`: Django Ninja router for WhatsApp Resumo (webhook).

#### [NEW] [apps.clients](file:///home/dan/Área de Trabalho/alessandra antigravity/src/clients)
- `models.py`: Encrypted client profiles.
- `case_journey.py`: Domain logic for the case timeline/journey.

### 3. White-Label Client Portal
#### [NEW] [portal/index.html](file:///home/dan/Área de Trabalho/alessandra antigravity/src/core/templates/portal/index.html)
- Dashboard in TailwindCSS (Palette #DFAE9A).
- Interactive "Case Journey" timeline.

### 4. Legal Ops & Financials
#### [NEW] [apps.finance](file:///home/dan/Área de Trabalho/alessandra antigravity/src/finance)
- `billing.py`: Passive activity tracking (inspired by Smokeball).
- `calculators.py`: CPC/CPP Deadline logic.

## Verification Plan

### Automated Tests
- `pytest` for Lead Scoring algorithm.
- Integration tests for `EncryptedField` decryption.

### Manual Verification
- **Browser Recording**: Simulate a full triage flow in the front-end bot.
- **WhatsApp Audit**: Verify webhook delivery to Dra. Alessandra's number.
