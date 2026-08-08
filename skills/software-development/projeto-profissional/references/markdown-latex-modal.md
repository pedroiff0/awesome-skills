# Markdown + LaTeX em descrições de tarefa (modal de detalhe)

Padrão CSP-safe para renderizar Markdown e fórmulas LaTeX no domínio de tarefas
deste template, sem CDN e sem script inline.

## Quando usar

O usuário pediu: "clicar na tarefa abre o cartão para colocar a descrição, com
suporte a markdown e latex mínimo (fórmula)". Então o board ganha:
- clique no cartão → modal `#task-modal` com título editável, status/projeto/
  responsável, e a descrição em Markdown+LaTeX (visualização + edição).
- a pré-visualização do cartão no quadro também renderiza Markdown+LaTeX
  (passada `renderizarCards()` no load do `board.js`).

## Bibliotecas (self-hosted, NUNCA CDN — a CSP é `script-src 'self'`)

`npm install marked@^12 katex@^0.16 dompurify@^3` e copie para `public/vendor`:

- `public/vendor/marked.umd.js`
- `public/vendor/purify.min.js`
- `public/vendor/katex/katex.min.js`
- `public/vendor/katex/katex.min.css`
- `public/vendor/katex/auto-render.min.js`
- `public/vendor/katex/fonts/*` (copiado de `node_modules/katex/dist/fonts`)

Inclua no final do `board.ejs` (ANTES do `footer.ejs`, que carrega o `board.js`):

```html
<link rel="stylesheet" href="/vendor/katex/katex.min.css" />
<script src="/vendor/marked.umd.js"></script>
<script src="/vendor/purify.min.js"></script>
<script src="/vendor/katex/katex.min.js"></script>
<script src="/vendor/katex/auto-render.min.js"></script>
<%- include('partials/footer') %>
```

## Render no cliente (`public/js/board.js`)

```js
function renderMarkdown(src) {
  if (!src) return '';
  const raw = window.marked
    ? window.marked.parse(src, { breaks: true, gfm: true })
    : escapeHtml(src);
  return window.DOMPurify
    ? window.DOMPurify.sanitize(raw, {
        ADD_TAGS: ['math','semantics','annotation','mrow','mi','mo','mn','msup','span'],
        ADD_ATTR: ['aria-hidden','encoding','xmlns'],
      })
    : raw;
}
function typeset(el) {
  if (window.renderMathInElement) {
    try {
      window.renderMathInElement(el, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false },
          { left: '\\(', right: '\\)', display: false },
          { left: '\\[', right: '\\]', display: true },
        ],
        throwOnError: false,
      });
    } catch (_) {}
  }
}
```

- Abra o modal com `renderMarkdown(task.descricao)` + `typeset(view)`.
- Edição: textarea `#tm-edit` (raw markdown) → salvar via `PATCH /api/<modo>/tasks/:id`
  com `{ descricao }`; o controller `task.controller.atualizar` já devolve `{ task }`.
- `renderizarCards()`: ao carregar, percorre `.tcard-desc` e re-renderiza se o texto
  contiver `*`, `$`, `#` ou `` ` `` (evita reprocessar descrições já HTML).

## Gotchas deste padrão

- **`DOMPurify` come o KaTeX** se você não liberar as tags MathML no
  `ADD_TAGS`/`ADD_ATTR`. Sem isso a fórmula some após o sanitize.
- **CSRF em `PATCH`**: o `apiRequest` do `common.js` manda `Origin` certo, então
  passa; mas um `hermes-verify-*.js` que faz PATCH precisa do header `Origin` ou
  leva 403 "origem ausente" (ver `web-fullstack-gotchas` §12/§78).
- **Asset cache**: marcado `.vendor/*` herda o `maxAge` do `express.static`. Com
  `maxAge:0` (ver `web-fullstack-gotchas` §17) o browser sempre revalida o
  `marked/katex` novo.
- **Campo de descrição**: `maxlength` do textarea em 4000; use `escapeHtml` (ou
  `marked`) — nunca interpole `descricao` crua na view (`<%- %>` com conteúdo de
  usuário é vetor XSS; o sanitize do marked+DOMPurify cobre, mas a view
  server-render deve usar `<%= %>` mesmo assim).
- **Escape de barra invertida no shell de teste**: ao enviar LaTeX por `curl -d`,
  dobre as barras (`\\int`, `\\tfrac`) — o shell consome uma camada.
