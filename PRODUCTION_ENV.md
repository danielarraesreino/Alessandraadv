# 🚀 Variáveis de Ambiente para Produção

**IMPORTANTE:** Configure estas variáveis no painel do seu serviço de hosting (Railway/Render/Heroku)

## Django Core

```bash
SECRET_KEY=(h0)=tpct-66i&=ap-5_)yh1+^6)4k4ib@sow7kj9==ab&!%n-
DEBUG=False
ALLOWED_HOSTS=web-production-36079.up.railway.app,*.railway.app
```

## Database

```bash
# Será auto-configurado pelo Railway PostgreSQL
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

## Encryption (CRITICAL! ⚠️)

```bash
# NUNCA MUDE ESSA CHAVE APÓS O PRIMEIRO DEPLOY!
ENCRYPTION_KEY=gLGPfeKUhKGlQ-2cU4BUJTbVeAumAl-HE_bfkdjThN0=
```

## WhatsApp

```bash
WHATSAPP_DECISOR_NUMBER=+5519993257342

# Configure quando tiver credenciais do Twilio:
# TWILIO_ACCOUNT_SID=ACxxxxx
# TWILIO_AUTH_TOKEN=your_token
# TWILIO_WHATSAPP_NUMBER=+14155238886
```

## Email (Gmail SMTP)

```bash
# Configure quando tiver App Password do Gmail:
# EMAIL_HOST_USER=alessandra@alessandradonadon.adv.br
# EMAIL_HOST_PASSWORD=sua-app-password
```

## CSRF Configuration

No arquivo `settings.py`, já está configurado:
```python
CSRF_TRUSTED_ORIGINS = ["https://web-production-36079.up.railway.app", "https://*.railway.app"]
```

---

## 📋 Checklist de Deploy

- [ ] Configurar `SECRET_KEY` no Railway
- [ ] Configurar `ENCRYPTION_KEY` no Railway (NUNCA MUDE!)
- [ ] Configurar `DEBUG=False` no Railway
- [ ] Configurar `ALLOWED_HOSTS` no Railway
- [ ] PostgreSQL será auto-configurado pelo Railway
- [ ] Push para GitHub (deploy automático)
- [ ] Verificar logs de build no Railway
- [ ] Testar: `https://web-production-36079.up.railway.app/health/`
- [ ] Acessar admin: `https://web-production-36079.up.railway.app/admin/`

---

**Status:** Pronto para deploy! 🚀
