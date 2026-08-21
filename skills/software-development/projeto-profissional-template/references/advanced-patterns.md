# Advanced patterns — projeto-professional template

Receitas condensadas para as features adicionadas em sessões recentes. O SKILL.md
carrega o resumo; aqui estão os detalhes copiáveis.

## 1. Demo seed: acoplamento model -> seed
Ao adicionar campo obrigatório no model, o `demoService.carregarDemo` DEVE definir
esse campo nos docs, senão o boot crasha em `insertMany`.

- `Project.responsavelId` obrigatório -> em `demoService.js` adicione `responsavelId: dono._id`
  no `projDocs` (o dono e um `owners[i]`).
- `Professional.email` obrigatorio (Zod `.email()`) -> adicione `email: \`pro${i+1}@exemplo.com\``
  no `profDocs` e expanda a lista de `nomes` (estava em 24, subiu para 60).
- `Meta` (foco semanal): popule `focoPorDia`/`pomodorosPorDia` (array de 7) e `metaSemana`
  realista (ex: `250 + k%5*50`) para nao ficar menor que as concluidas (incoerencia "226/25").

### Erro `Meta.insertMany is not a function`
`require('../models/meta.model')` retorna o **schema**, nao o model compilado.
Use o model que vem como 2o arg:
```js
const Meta = models.Meta || require('mongoose').model('Meta');
await Meta.insertMany(metas);
```

## 2. Comentarios editar/remover (PATCH do array inteiro)
Backend: `PATCH /api/:modo/tasks/:id` aceita `{ comentarios: [...] }`. O schema
`comentarioSchema` deve ter `autor` **opcional** (o seed pode ter `autor: null`):
```js
const comentarioSchema = z.object({
  autor: z.string().max(120).optional(),
  autorId: z.string().regex(/^[a-f\d]{24}$/).optional(),
  texto: z.string().min(1).max(2000),
  criadoEm: z.string().datetime({ offset: true }).optional(),
});
```
No client (`board.js`), ao salvar, normalize ANTES do fetch (evita "Expected string, received null"):
```js
const limpos = (comentarios || []).map((c) => ({
  autor: String(c.autor || c.autorId || '—'),
  autorId: c.autorId || undefined,
  texto: String(c.texto || ''),
  criadoEm: c.criadoEm || undefined,
})).filter((c) => c.texto.trim().length > 0);
await apiRequest(apiBase + '/tasks/' + modalTask._id, { method: 'PATCH', body: JSON.stringify({ comentarios: limpos }) });
```
Botoes com icone SVG (lapis/lixeira) + `.comment-actions .comment-del:hover { background:#ef4444 }`.
Edicao inline: troca o `<p>` por `<textarea class="comment-edit-area">` + Salvar/Cancelar.

## 3. Filtros do quadro kanban (client-side, 3000+ cards)
No `.ejs` (render SSR) e no `cardEl` (JS) adicione `data-*`:
```html
<article class="tcard" data-id="<%= task._id %>" data-status="<%= task.status %>"
  data-projeto="<%= task.projetoId || '' %>" data-profissional="<%= task.profissionalId || '' %>"
  data-tags="<%= (task.tags||[]).join(',') %>" data-inicio="<%= ymd(task.dataInicio) %>" data-prazo="<%= ymd(task.prazo) %>">
```
`cardEl` JS: `el.dataset.projeto = t.projetoId||''` etc (use `toDateInput(t.dataInicio)` p/ datas).
Filtro: ler selects/inputs, esconder cards com `display:none`, recompor contadores por coluna
(`.board-col[data-status] .board-count`). Tags: todas as tags informadas devem estar em `data-tags`.
Datas: comparar strings `YYYY-MM-DD` (lexico = cronologico).

### Drag-and-drop nativo
Cards do SSR NAO sao `draggable` (o atributo nao vem do server). Apos `renderizarCards()`,
faça `document.querySelectorAll('.tcard').forEach(c => c.setAttribute('draggable','true'))`.
Handlers: `dragstart` (seta `dataTransfer.setData('text/plain', id)`), `dragover` (preventDefault +
classe), `drop` (PATCH status, re-insere o card na coluna alvo).

## 4. Responsavel digitavel + selecionavel
Em `projetos.ejs` (cadastro e modal) use input + select:
```html
<span>Responsavel</span>
<input type="text" id="resp-search" placeholder="Digite para filtrar…" autocomplete="off" />
<select name="responsavelId" id="resp-select" required>
  <option value="">Selecione…</option>
  <% usuarios.forEach(u => <option value="<%= u._id %>"><%= u.name %></option>) %>
</select>
```
JS (`projetos.js`): `setupRespFilter('resp-search','resp-select')` — no `input`, esconde options
nao correspondentes e auto-seleciona se sobrar uma. A rota `/projetos` (pages.routes.js) precisa
passar `usuarios: await req.models.User.find({isActive:true}).select('_id name email').lean()`.

## 5. Painel rize.io (barras + donut + linha de foco + pomodoro)
- Stat cards: total, concluidas, focoMinutos, pomodoros, % conclusao (reativos ao filtro de chip).
- Barras (`drawBars`): `viewBox="0 0 100 102"`, `<rect class="bar st-<status>">` com cores via
  CSS `.bars svg .bar.st-planejado { fill: var(--st-planejado) }` (NAO use `style="fill:var()"` inline
  no SVG — nao resolve conforme tema).
- Donut: `<circle r=42 ... stroke-dasharray="len rest" stroke-dashoffset>` com `transform="rotate(-90 50 50)"`.
- Linha de foco semanal: `apiRequest(apiBase+'/meta')` -> `meta.focoPorDia` (array 7); desenhe
  polyline + polygon (area) + dots + labels dos dias.
- Pomodoro integrado: ao fim do timer, `POST /meta/foco {minutos:25}`; entao re-leia `/meta` e
  atualize os cards de foco + redesenhe a linha.
- Carregue dados via API no client (NAO injete JSON inline por causa do CSP).

## 6. Projetos: Markdown/LaTeX na tabela
`projetos.js` renderiza a descricao com `marked`+`DOMPurify`+`katex` (vendor em `/public/vendor/`).
A pagina `projetos.ejs` inclui `<script src="/vendor/marked.umd.js">` etc. Apos inserir o HTML:
```js
if (window.renderMathInElement) rows.querySelectorAll('.md-block').forEach(el =>
  renderMathInElement(el, { delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}] }));
```

## 7. Profissionais: email obrigatorio
Model: `email: { type:String, required:true, match:[/^\S+@\S+\.\S+$/,'E-mail invalido'] }`.
Schema: `email: z.string().email('E-mail invalido').max(160)`. Tabela: coluna E-mail com
`<a href="mailto:...">`. Cuidado: use `escapeHtml(p.email)`, NAO `escapeAttr` (nao existe no escopo
do arquivo — causou `escapeAttr is not defined` na tabela).
