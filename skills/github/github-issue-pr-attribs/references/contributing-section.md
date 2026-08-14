# CONTRIBUTING.md — "Atribuições padronizadas" section

Drop this section into a repo's `CONTRIBUTING.md` (between "Fluxo" and "Padrões de código"). Adjust the owner/login and project title.

```markdown
## Atribuições padronizadas (ISSUE e PR)

Toda issue e todo PR devem preencher os sete campos abaixo. Os templates em
`.github/` já pré-preenchem o que a API permite (labels, assignee, project,
milestone); o resto é marcado no checklist do PR. Modelo de review forte em
[`docs/CODE_REVIEW.md`](docs/CODE_REVIEW.md).

### ISSUE

| Campo | Padrão |
|---|---|
| **Assignee** | `pedroiff0` (dev único) |
| **Labels** | Pelo menos uma categoria: `bug` / `enhancement` / `documentation` / `testes` / `ux` / `seguranca` / `infra` / `backlog`; + módulo (`modulo:financas` / `modulo:`...) se aplicável |
| **Project** | *Financas App - Roadmap* (Projects V2) |
| **Milestone** | `Backlog` por padrão; mover para milestone semver (`v0.x.y`) quando ganhar release alvo |
| **Relationship** | Vincular issue pai/filha ou PR de origem quando houver dependência |

> Reviewer não existe em issue — define-se no PR de entrega.

### PR

| Campo | Padrão |
|---|---|
| **Assignee** | `pedroiff0` |
| **Reviewer** | `pedroiff0` (self-review seguindo `docs/CODE_REVIEW.md`) |
| **Labels** | Herdar as da issue + tipo (`frontend`/`backend`/`dashboard`/`seguranca`/`testes`) |
| **Project** | *Financas App - Roadmap* |
| **Milestone** | O mesmo da issue de origem |
| **Development** | Branch `feat/...`/`fix/...` ligada à issue |
| **Relationship** | `Fecha #<issue>` na descrição (ou `Relaciona #<issue>`) |

### Convenção de Milestone / Release

- Releases são **tags semver** (`vMAJOR.MINOR.PATCH`); milestone = a tag alvo.
- `Backlog` é o catch-all para demandas ainda sem release definido.
- Não abra milestone por issue pontual; agrupe por release planejada.

## Code Review

Siga [`docs/CODE_REVIEW.md`](docs/CODE_REVIEW.md): estrutura fixa de comentário,
tabela de severidade (🔴 Blocker / 🟠 Maior / 🟡 Menor / 🔵 Nit) e rubricas por
categoria (segurança, arquitetura, dados, testes, UX). Decisão explícita no fim
(✅ / 🔁 / ⛔).
```
