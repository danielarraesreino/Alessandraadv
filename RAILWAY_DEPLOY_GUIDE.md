# 🚀 Guia Definitivo de Deploy no Railway - Plataforma Dra. Alessandra Donadon

## 📋 Pré-requisitos

- ✅ Conta no [Railway](https://railway.app)
- ✅ Repositório Git configurado
- ✅ Código atualizado com todas as correções

---

## 🔧 Passo 1: Configurar Variáveis de Ambiente no Railway

Acesse o **Railway Dashboard** → Seu projeto "Alessandraadv" → **Variables**

### Variáveis Obrigatórias

```bash
# Django Core (CRITICAL!)
SECRET_KEY=(h0)=tpct-66i&=ap-5_)yh1+^6)4k4ib@sow7kj9==ab&!%n-
DEBUG=False
ALLOWED_HOSTS=*.railway.app,web-production-36079.up.railway.app

# Encryption (NUNCA MUDE ESSA CHAVE!)
ENCRYPTION_KEY=gLGPfeKUhKGlQ-2cU4BUJTbVeAumAl-HE_bfkdjThN0=

# WhatsApp
WHATSAPP_DECISOR_NUMBER=+5519993257342
```

### Variáveis Automáticas (Railway configura)

- `DATABASE_URL`: Gerado automaticamente pelo PostgreSQL plugin
- `PORT`: Definido automaticamente pelo Railway

---

## 🗄️ Passo 2: Adicionar PostgreSQL Database

1. No Railway Dashboard, clique em **"New"** → **"Database"** → **"PostgreSQL"**
2. O Railway criará automaticamente a variável `DATABASE_URL`
3. Certifique-se de que o serviço da aplicação está **linked** ao banco de dados

---

## 📦 Passo 3: Configurar Build Settings

### No `Procfile` (Automatizado 🚀)

Configuramos o `Procfile` para rodar migrações e popular dados em cada deploy:
```
release: python manage.py migrate --noinput && python manage.py populate_articles
web: cd src && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --timeout 120
```

---

## 🚢 Passo 4: Deploy

1. Faça commit de todas as alterações:
   ```bash
   git add .
   git commit -m "Production ready: fixes and auto-population"
   git push origin main
   ```

2. O Railway detectará o push e fará deploy automático.

---

## ✅ Passo 5: Validação Pós-Deploy

### 1. Testar Endpoint de Saúde
```bash
curl https://web-production-36079.up.railway.app/health/
```
**Resposta esperada:** `{"status": "ok"}`

### 2. Validar "In Brief"
Acesse `https://web-production-36079.up.railway.app/in-brief/`. Os artigos (Lipedema, Lei Rouanet, etc.) devem aparecer automaticamente.

### 3. Validar LGPD
Acesse o rodapé do site e clique em **Política de Privacidade**. Verifique também os **Selos de Segurança**.

---

## 🐛 Troubleshooting

### Erro 500: Internal Server Error
✅ O erro de registro da `NinjaAPI` foi corrigido com o padrão Singleton. Caso ocorra outro erro, verifique os logs no Railway Dashboard.

### Página Vazia no In Brief
✅ Garantimos que o comando `populate_articles` roda no deploy. Caso não apareça nada, tente o comando manual no terminal do Railway:
`python manage.py populate_articles`

---

**Daniel Arraes Reino (Japa)**  
📱 +55 19 99325-7342  
💬 "IA é o motor, você é o piloto!"
