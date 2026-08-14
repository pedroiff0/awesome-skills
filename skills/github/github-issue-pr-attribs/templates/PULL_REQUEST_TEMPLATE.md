<!--
Template de PR — padrão financas-app.
Preencha os blocos; o checklist de ATRIBUIÇÕES garante que nada fica pendente.
Code review forte: veja docs/CODE_REVIEW.md (estrutura e rubricas).
-->

## 📌 Resumo

<!-- O quê e por quê. Link da issue: "Fecha #ISSUE" ou "Relaciona #ISSUE". -->

Fecha #

## 🧭 Atribuições (preencher antes de pedir review)

> Repo de dev único: Assignee e Reviewer são `pedroiff0` por padrão (remova se
> for outro contexto). Project/Milestone pré-definidos no template de issue.

- [ ] **Assignee:** @pedroiff0
- [ ] **Reviewer:** @pedroiff0
- [ ] **Labels:** (ex.: `bug`, `modulo:financas`, `frontend`, `testes`)
- [ ] **Project:** Financas App - Roadmap
- [ ] **Milestone:** (ex.: `Backlog`, `v0.4.0`)
- [ ] **Development:** branch `feat/...`/`fix/...` ligada à issue
- [ ] **Relationship:** issue de origem linkada (Fecha/Relaciona)

## 🔍 Self-Review (autocheck antes do review alheio)

- [ ] `npm test` verde (inclui testes novos)
- [ ] `npm run test:e2e` não regrediu (se tocou UI)
- [ ] Schema Zod em toda entrada nova (via `validate(schema)`)
- [ ] `auth` + `requireRole` corretos nas rotas novas
- [ ] `escapeHtml()` em toda saída user-facing; sem `<%- %>` com dado de usuário
- [ ] Sem segredo no código; `.env.example` atualizado se surgiu variável nova
- [ ] Sem log de PII, senha ou token
- [ ] Dinheiro em centavos inteiros (`*Cents`); valor agregado é derivado
- [ ] UI: aprovada por screenshot no :6789 antes do commit (se tocou visual)
- [ ] README/SECURITY/DESIGN.md atualizados se o comportamento mudou

## 🧩 Tipo de mudança

- [ ] 🐞 Bug fix (corrige defeito)
- [ ] 🚀 Feature (nova funcionalidade)
- [ ] 📋 Task / Refactor / Docs / Chore
- [ ] 🔒 Segurança

## 🧪 Como testar

```bash
cd app && npm test
# UI: rode no :6789 e anexe screenshot (mobile 375 + desktop 1920)
```

## 📎 Notas de revisão (para o reviewer)

<!-- Pontos que merecem atenção extra: trade-offs, áreas sensíveis, dúvidas. -->
