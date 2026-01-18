# WhatsApp Webhook Integration - Implementation Plan

Automatizar o envio de leads qualificados para o WhatsApp da Dra. Alessandra Donadon.

## Objetivo

Integrar o sistema de triagem com o WhatsApp para que leads com `score > 60` sejam automaticamente notificados ao número **(19) 98801-4465** com um resumo estruturado.

---

## Proposed Changes

### 1. WhatsApp Service Layer

#### [NEW] [`apps/whatsapp/services/notification.py`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/apps/whatsapp/services/notification.py)

**Responsabilidade:** Formatar e enviar mensagens via API do WhatsApp.

```python
class WhatsAppNotificationService:
    def send_lead_notification(self, lead: Lead) -> bool:
        """
        Envia notificação de lead qualificado para o WhatsApp decisor.
        
        Formato da mensagem:
        🎯 NOVO LEAD QUALIFICADO
        
        Nome: {lead.full_name}
        Tipo: {lead.get_case_type_display()}
        Score: {lead.score}/100
        Contato: {lead.contact_info}
        
        Dados da Triagem:
        {formatted_triage_data}
        """
```

**Integrações Possíveis:**
1. **WhatsApp Business API** (oficial, requer aprovação Meta)
2. **Twilio API for WhatsApp** (mais rápido para MVP)
3. **Evolution API** (self-hosted, open-source)

---

### 2. Update Intake Router

#### [MODIFY] [`apps/intake/api/router.py`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/apps/intake/api/router.py#L30-L45)

**Mudança:** Adicionar chamada ao serviço de notificação após salvar o lead.

```python
from apps.whatsapp.services.notification import WhatsAppNotificationService

@router.post("/step-2/")
def intake_step_2(request, session_id: str):
    # ... código existente ...
    
    lead.save()
    
    # [NEW] Enviar notificação se qualificado
    if lead.is_qualified:
        notification_service = WhatsAppNotificationService()
        notification_service.send_lead_notification(lead)
    
    return render(request, 'intake/step_final.html', {'lead': lead})
```

---

### 3. Configuration & Environment

#### [MODIFY] [`settings.py`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/core/settings.py)

**Adicionar:**
```python
# WhatsApp Configuration
WHATSAPP_DECISOR_NUMBER = "+5519988014465"
WHATSAPP_API_URL = os.getenv('WHATSAPP_API_URL')
WHATSAPP_API_TOKEN = os.getenv('WHATSAPP_API_TOKEN')
```

#### [NEW] `.env.example`

```bash
WHATSAPP_API_URL=https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json
WHATSAPP_API_TOKEN=your_twilio_auth_token_here
```

---

### 4. Admin Interface Enhancement

#### [MODIFY] [`apps/intake/admin.py`](file:///home/dan/Área de Trabalho/alessandra antigravity/src/apps/intake/admin.py)

**Adicionar ação customizada:**
```python
@admin.action(description='Reenviar notificação WhatsApp')
def resend_whatsapp_notification(modeladmin, request, queryset):
    service = WhatsAppNotificationService()
    for lead in queryset:
        service.send_lead_notification(lead)
```

---

## Verification Plan

### Automated Tests

```python
# tests/test_whatsapp_notification.py
def test_send_qualified_lead_notification():
    lead = Lead.objects.create(
        full_name="Test Lead",
        case_type="LIPEDEMA",
        score=75,
        is_qualified=True
    )
    
    service = WhatsAppNotificationService()
    result = service.send_lead_notification(lead)
    
    assert result is True
```

### Manual Verification

1. **Teste via Admin:** Criar um lead manualmente com score > 60 e verificar recebimento no WhatsApp
2. **Teste via Bot:** Completar o fluxo de triagem e confirmar notificação automática
3. **Browser Recording:** Capturar o fluxo completo end-to-end

---

## Implementation Options

### Option 1: Twilio (Recomendado para MVP)

**Prós:**
- Setup rápido (< 30 minutos)
- Documentação excelente
- Suporte oficial

**Contras:**
- Custo por mensagem (~$0.005 USD)

### Option 2: Evolution API (Open Source)

**Prós:**
- Gratuito
- Self-hosted
- Controle total

**Contras:**
- Requer servidor próprio
- Manutenção manual

### Option 3: WhatsApp Business API (Produção)

**Prós:**
- Oficial Meta
- Recursos avançados (templates, botões)

**Contras:**
- Processo de aprovação longo
- Complexidade maior

---

## Next Steps

1. ✅ Escolher provedor (Twilio para MVP)
2. [ ] Criar conta e obter credenciais
3. [ ] Implementar `WhatsAppNotificationService`
4. [ ] Atualizar `intake/router.py`
5. [ ] Testar notificação end-to-end
6. [ ] Documentar no walkthrough

---

## Estimated Effort

- **Implementação:** 2-3 horas
- **Testes:** 1 hora
- **Documentação:** 30 minutos

**Total:** ~4 horas para MVP funcional
