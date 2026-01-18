# Configuração de Qualidade e Segurança

Este documento descreve as ferramentas e práticas de qualidade implementadas no projeto.

## Ferramentas de Análise Estática

### Bandit (Segurança Python)
```bash
pip install bandit
bandit -r src/ -f json -o bandit-report.json
```

### Pytest (Testes Unitários e Integração)
```bash
pytest src/apps/intake/tests.py -v --cov=apps.intake --cov-report=html
```

## Quality Gates

- ✅ **0 vulnerabilidades** de segurança críticas
- ✅ **80%+ cobertura** de código em novos módulos
- ✅ **Todos os testes** passando antes de commit

## MCP Servers Recomendados

1. **Sentry MCP** - Análise de erros em produção
2. **PostgreSQL MCP** - Administração de banco de dados
3. **SonarQube MCP** - Análise de qualidade de código

## Conformidade LGPD

- ✅ Dados sensíveis criptografados (`EncryptedField`)
- ✅ Logs sem PII (Informações Pessoais Identificáveis)
- ✅ Hashing Argon2 para senhas
