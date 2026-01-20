# 📖 Manual de Uso Total: ERP Jurídico Alessandra Donadon

Este manual foi desenvolvido para guiar você pela interface premium do seu novo sistema jurídico. O sistema foi projetado para ser intuitivo, rápido e focado em resultados.

---

## 1. Dashboard de Inteligência 📊
O Dashboard é o cérebro do seu escritório. Ele resume as métricas financeiras e operacionais mais importantes em tempo real.

![Dashboard Premium](file:///home/dan/Área de Trabalho/alessandra antigravity/assets/manual/dashboard_premium_1768845914198.png)

- **Total em Contingência**: Soma de todos os valores de risco dos casos ativos.
- **Contas a Receber**: Honorários pendentes de recebimento.
- **Gráficos de Funil**: Veja quantos leads estão em cada etapa da jornada.

---

## 2. Gestão de Casos e Leads (Kanban) ⚖️
Utilizamos o sistema Kanban (cartões) para facilitar a visualização do fluxo de trabalho.

### Funil de Leads
![Leads Kanban](file:///home/dan/Área de Trabalho/alessandra antigravity/assets/manual/leads_kanban_premium_1768845970405.png)
- **Score de Captura**: Leads com score > 60 são qualificados para atendimento priorizado.
- **Conversão**: Com um clique, você converte um Lead em um Cliente/Caso real.

### Fluxo de Casos
![Casos Kanban](file:///home/dan/Área de Trabalho/alessandra antigravity/assets/manual/cases_kanban_premium_1768845958613.png)
- Organize seus processos por: `Análise`, `Ativo`, `Suspenso` ou `Arquivado`.
- Clique em qualquer cartão para ver o detalhe completo do caso.

---

## 3. Gestão Financeira 💰
O módulo financeiro é dividido em **Contas a Pagar** e **Contas a Receber**.

![Gestão Financeira](file:///home/dan/Área de Trabalho/alessandra antigravity/assets/manual/finance_premium_1768845928942.png)

- **Ações Rápidas**: Use o botão "Confirmar Recebto" para baixar honorários recebidos.
- **Atrasos**: O sistema destaca automaticamente em vermelho as contas vencidas.

---

## 4. Automação de Documentos 📄
Você pode gerar documentos base (como procurações e contratos) usando seu papel timbrado oficial.

1. Acesse o **Detalhe do Caso**.
2. Clique em **"Gerar Documento Base"**.
3. O sistema lerá o arquivo `TIMBRADO.docx` e preencherá automaticamente os dados do cliente e do processo.

---

## 5. Portal do Cliente: A Experiência Premium 📱
Seu cliente acompanha o processo de forma moderna, via Linha do Tempo.

### Acesso via Token
![Login do Cliente](file:///home/dan/Área de Trabalho/alessandra antigravity/assets/manual/portal_login_experience_1768845946292.png)
- O cliente não precisa de senha. Ele usa um **Token de Acesso** enviado por você.
- **Dica**: Gere o token no painel administrativo em "Acessos ao Portal".

### Linha do Tempo (Timeline)
- Exibe o progresso em linguagem humana ("Análise Jurídica", "Petição Elaborada").
- O cliente visualiza apenas os documentos que você marcar como "Visível para Cliente".

---

## 🔧 Manutenção e Suporte
- **Servidor**: Para ligar o sistema localmente, use `python manage.py runserver`.
- **Arquivos**: O template timbrado está em `./src/core/templates/documents/TIMBRADO.docx`.

---
*Desenvolvido com Antigravity Intelligence.*
