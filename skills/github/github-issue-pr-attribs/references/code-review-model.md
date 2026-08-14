# Code Review — Padrão do Repositório

Este documento define **como conduzir e registrar** o code review no
financas-app. O objetivo é coerência: toda revisão segue a mesma estrutura,
usa a mesma tabela de severidade e termina com uma decisão explícita.

> Aplicável a PRs de feature, fix e refactor. Para mudanças de UI, exigir
> screenshot no `:6789` (mobile 375 + desktop 1920) antes de aprovar.

---

## 1. Princípios

1. **Revisamos código, não pessoas.** Comentário aponta o patch, não o autor.
2. **Camadas são sagradas.** Rota→Controller→Service→Model (ver `AGENTS.md`).
   Lógica de negócio fora do service é motivo de revisão.
3. **Segurança primeiro.** Vazamento de `passwordHash`/token, `unsafe-inline`
   na CSP, entrada crua em HTML → **Blocker** imediato.
4. **Dinheiro é centavo inteiro.** Float em valor monetário é bug.
5. **Teste é parte do PR.** Rota nova sem teste em `app/tests/` não está pronta.
6. **Comentário tem dono e prazo.** Cada item aberto vira ação ou é descartado
   com justificativa.

---

## 2. Estrutura do comentário de Review (modelo .md)

Copie este bloco para o comentário de revisão do PR. Substitua os colcherios.

```markdown
## Code Review — PR #<N>

**Revisor:** @<login>  ·  **Data:** YYYY-MM-DD  ·  **Decisão:** ✅ Aprovado / 🔁 Mudanças solicitadas / ⛔ Bloqueado

### Resumo
<1–3 linhas: o que o PR faz e se atinge o objetivo da issue #<N>.>

### Verificação automática
| Check | Status |
|---|---|
| `npm test` | ✅ verde / ❌ falhou |
| `npm run test:e2e` (se UI) | ⬜ n/a / ✅ / ❌ |
| Lint / `design.md lint` (se UI) | ✅ / ❌ |
| Screenshot :6789 (mobile+desktop) | ✅ anexo / ⬜ n/a |

### Achados por severidade
| # | Severidade | Arquivo:linha | Categoria | Comentário / Sugestão |
|---|---|---|---|---|
| 1 | 🔴 Blocker | `routes/x.js:42` | Segurança | <...> |
| 2 | 🟠 Maior | `services/x.js:18` | Arquitetura | <...> |
| 3 | 🟡 Menor | `views/x.ejs:7` | Estilo | <...> |
| 4 | 🔵 Nit | `x.js:3` | Convenção | <...> |

### Itens obrigatórios conferidos
- [ ] Zod em toda entrada (`validate(schema)`)
- [ ] `auth` + `requireRole` corretos
- [ ] `escapeHtml()` / sem `<%- %>` com dado de usuário
- [ ] Sem segredo no código; `.env.example` atualizado
- [ ] Sem log de PII/senha/token
- [ ] Valor monetário em `*Cents`; agregado é derivado
- [ ] Teste novo + registro em `endpoints.test.js`

### Decisão e próximos passos
<Se 🔁/⛔: liste o que o autor deve ajustar antes do re-review.>
```

---

## 3. Tabela de severidade

| Ícone | Severidade | Significado | Ação |
|---|---|---|---|
| 🔴 | **Blocker** | Quebra segurança, perda de dado, regra de negócio errada ou teste verde mascarando falha. | PR **não** pode mergear. Corrigir antes. |
| 🟠 | **Maior** | Viola arquitetura de camadas, ausência de teste obrigatório, bug em caminho não-feliz. | Deve ser resolvido neste PR ou issue follow-up vinculada. |
| 🟡 | **Menor** | Inconsistência de estilo, nome ruim, comentário que explica o quê em vez do porquê. | Resolver se rápido; senão issue follow-up. |
| 🔵 | **Nit** | Preferência pessoal, formatação cosmética. | Opcional; não bloqueia. |

**Regra de decisão**
- Qualquer 🔴 → **⛔ Bloqueado**.
- Apenas 🟠/🟡/🔵 → **🔁 Mudanças solicitadas** (ou aprovado se autorais).
- Só nits aprovados e itens obrigatórios ok → **✅ Aprovado**.

---

## 4. Rubricas por categoria

### 4.1 Segurança (prioridade máxima)
- Nenhum `passwordHash`/token/reset em resposta (`toPublicUser()`).
- Sem token por query string.
- `escapeHtml()` em toda saída; `RegExp` de entrada com metacaracteres escapados.
- CSP mantida: script em arquivo, nunca `unsafe-inline`.
- Sem segredo hardcoded; fonte única `app/.env`.

### 4.2 Arquitetura
- Regra de negócio no **service**; controller traduz HTTP; model descreve dado.
- Módulo novo = flag `config/env.js` + `seModulo()` + guard de página + bloco de
  dashboard + caso em `tests/modulos.test.js`.
- Papel novo = enum em `user.model.js` **e** `admin.schemas.js` juntos.

### 4.3 Dados e regras de domínio
- Dinheiro em centavos inteiros (`*Cents`); nunca float.
- Valor agregado é **derivado**, nunca congelado em campo.
- Queries escopadas por `userId` explicitamente.

### 4.4 Testes
- Rota nova: feliz + 422 (inválido) + 401 (sem auth) + 403 (sem permissão).
- Registro em `tests/endpoints.test.js`.
- UI nova: spec em `app/cypress/e2e/*.cy.js` (não Playwright novo).

### 4.5 Interface / UX
- Segue `DESIGN.md` (tokens de cor/tipografia/elevação); sem valor improvisado.
- Sem scroll horizontal: layout nunca excede o viewport (cuidado com
  `width:100%` + `margin-left` da sidebar).
- Sem emoji na interface; use SVG inline.
- Aprovada por screenshot no `:6789` antes do commit.

---

## 5. Self-Review (autor antes de pedir review)

O autor preenche o checklist em `.github/PULL_REQUEST_TEMPLATE.md` (seção
**Self-Review**). O reviewer confere e marca o que faltar no seu comentário.

---

## 6. Fluxo

1. PR aberto a partir de `main` (`feat/...`, `fix/...`, `docs/...`, `chore/...`).
2. Autor preenche atribuições + self-review no template.
3. Reviewer posta comentário no modelo da seção 2.
4. Decisão: ✅ → merge `--rebase` no `main`; 🔁/⛔ → ajustes e re-review.
5. Após merge: branch remota e local deletadas.
