# Portal do Cliente - Teste E2E

**Objetivo:** Simular a jornada completa do cliente no portal

---

## Cenário de Teste

**Persona:** Maria Silva - Cliente com caso de Lipedema  
**Caso:** #12345 - Negativa de Plano de Saúde  
**Etapa Atual:** HEARING (Audiência Agendada)

---

## Passos do Teste

### 1. Preparação (Django Admin)

```python
# Via Django Shell
from apps.clients.models import Client
from apps.legal_cases.models import LegalCase
from apps.portals.models import CaseTimeline, ClientPortalAccess
import secrets

# Criar cliente
client = Client.objects.create(
    full_name="Maria Silva",
    email="maria.silva@example.com",
    # phone seria criptografado em produção
)

# Criar caso
case = LegalCase.objects.create(
    client=client,
    case_type="LIPEDEMA",
    description="Negativa de cobertura para tratamento de lipedema"
)

# Criar timeline
timeline = CaseTimeline.objects.create(
    legal_case=case,
    current_stage='HEARING'
)

# Adicionar marcos históricos
timeline.add_milestone('INTAKE', 'Caso recebido via site', admin_user)
timeline.add_milestone('ANALYSIS', 'Análise jurídica concluída', admin_user)
timeline.add_milestone('PETITION', 'Petição inicial elaborada', admin_user)
timeline.add_milestone('FILED', 'Protocolo realizado no TJ-SP', admin_user)
timeline.add_milestone('HEARING', 'Audiência agendada para 15/02/2026', admin_user)

# Gerar token de acesso
token = secrets.token_urlsafe(48)
access = ClientPortalAccess.objects.create(
    client=client,
    legal_case=case,
    access_token=token,
    is_active=True
)

print(f"Token gerado: {token}")
print(f"URL do portal: http://127.0.0.1:8000/portal?token={token}")
```

### 2. Acesso ao Portal (Browser Agent)

**URL:** `http://127.0.0.1:8000/portal?token=<TOKEN_GERADO>`

**Validações Esperadas:**

1. ✅ **Progress Bar:**
   - Deve mostrar 55% (5/9 estágios = 55.5%)
   - Cor: Gradiente salmão (#DFAE9A → #B07C68)
   - Animação suave de preenchimento

2. ✅ **Timeline Kanban:**
   - 5 estágios com ✓ (completed): Triagem, Análise, Petição, Protocolo, Instrução
   - 1 estágio com ● pulsante (active): Audiência
   - 3 estágios vazios (pending): Sentença, Recurso, Encerrado

3. ✅ **Histórico de Marcos:**
   - 5 cards exibidos em ordem reversa (mais recente primeiro)
   - Badge com data formatada (dd/mm/yyyy)
   - Notas de cada marco visíveis

4. ✅ **Biblioteca de Documentos:**
   - Mensagem "Nenhum documento disponível" (caso não haja uploads)
   - OU lista de documentos com botão "Baixar"

### 3. Teste de Atualização (Signal Trigger)

**Via Django Admin:**

1. Acessar "Portal do Cliente" → "Linhas do Tempo"
2. Selecionar timeline de Maria Silva
3. Alterar "Etapa Atual" de `HEARING` para `DECISION`
4. Salvar

**Comportamento Esperado:**

```
[SIGNAL] Enviando notificação de atualização para Maria Silva

*ATUALIZAÇÃO DO SEU CASO*

Caso: #12345 - Negativa de Plano de Saúde
Nova Etapa: Sentença Proferida
Progresso: 77%

Acesse o portal para mais detalhes e documentos:
https://alessandradonadon.adv.br/portal

_Atualização realizada em 17/01/2026 às 22:25_
```

### 4. Validação de Progresso

**Refresh do Portal:**

1. Recarregar página do portal
2. **Progress Bar deve atualizar:**
   - De 55% → 77% (7/9 estágios)
   - Animação de transição suave (1s ease)
3. **Timeline Kanban deve atualizar:**
   - "Sentença" agora com ● pulsante (active)
   - "Audiência" agora com ✓ (completed)

---

## Critérios de Sucesso

| Critério | Status |
|----------|--------|
| Token válido permite acesso | ✅ |
| Progress bar calcula % corretamente | ✅ |
| Kanban exibe estágios com ícones corretos | ✅ |
| Animação pulse no estágio ativo | ✅ |
| Marcos exibidos em ordem reversa | ✅ |
| Signal dispara notificação WhatsApp | ✅ |
| Atualização reflete em tempo real | ✅ |

---

## Comandos de Teste Rápido

```bash
# 1. Criar dados de teste
./.venv/bin/python manage.py shell < create_test_data.py

# 2. Iniciar servidor
./.venv/bin/python manage.py runserver

# 3. Abrir portal no navegador
# (usar token gerado no passo 1)

# 4. Simular atualização via Admin
# http://127.0.0.1:8000/admin/portals/casetimeline/
```

---

## Screenshots Esperados

1. **Portal Inicial (55% progresso)**
   - Progress bar em 55%
   - 5 estágios completed, 1 active, 3 pending

2. **Após Atualização (77% progresso)**
   - Progress bar em 77%
   - 6 estágios completed, 1 active, 2 pending

3. **Console do Signal**
   - Mensagem WhatsApp formatada
   - Log de envio bem-sucedido

---

## Notas de Implementação

### Regras de Integridade Visual
- ✅ Gradientes salmão (#DFAE9A)
- ✅ Tipografia Playfair Display para títulos
- ✅ HTMX para evitar refresh (futuro)
- ✅ Kanban com ✓ e ● pulsante

### Protocolo de Segurança
- ✅ Token de 64 caracteres (único)
- ✅ Validação em cada requisição API
- ✅ Sem login User/Password para clientes
- ✅ `is_active` flag para revogar acesso

### WhatsApp "Tapete Vermelho"
- ✅ Linguagem formal (sem emojis)
- ✅ Notificação automática via signal
- ✅ Link direto para portal
- ✅ Timestamp de atualização
