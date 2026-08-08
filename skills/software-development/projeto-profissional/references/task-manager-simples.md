# Task manager simples (board + calendário) — padrão copy-paste

Quando o Pedro pede "popule o sistema como um task manager com calendário e view
em board (bastante simples)", entregue EXATAMENTE isto — nada de drag-and-drop,
animação ou redesenho do shell. O produto é o domínio; a landing continua sendo
a profissional (pitfall 72). Padrão validado em `projeto-profissional`.

## Model (`src/models/task.model.js`)
```js
const taskSchema = new mongoose.Schema({
  title:    { type: String, required: true, trim: true },
  description: { type: String, default: '' },
  status:   { type: String, enum: ['todo','doing','done'], default: 'todo' },
  dueDate:  { type: Date, default: null },
  ownerId:  { type: ObjectId, ref: 'User', required: true },
  ownerName:{ type: String, default: '' },
  assigneeId: { type: ObjectId, ref: 'User', default: null },
  assigneeName:{ type: String, default: '' },
}, { timestamps: true });
taskSchema.index({ ownerId: 1, status: 1 });
taskSchema.index({ ownerId: 1, dueDate: 1 });
```
Registre em `models/registry.js` (`Task: conn.model('Task', taskSchema)`) e
exporte no objeto `models`. Sem model global (pitfall 55).

## Schema Zod (`src/schemas/task.schemas.js`)
```js
const taskCreate = z.object({
  title: z.string().min(2).max(140),
  description: z.string().max(2000).optional().default(''),
  status: z.enum(['todo','doing','done']).optional(),
  dueDate: z.coerce.date().nullable().optional(),
  assigneeId: z.string().regex(/^[0-9a-fA-F]{24}$/).nullable().optional(),
});
const taskUpdate = taskCreate.partial();
```

## Service — escopo por usuário (igual a projectService)
- `listar({userId, role, filtro})`: se `role !== 'admin'`, `q.ownerId = userId`.
- `criar(data, userId, userName, models)`: `Task.create({...data, ownerId, ownerName})`; se `assigneeId`, resolve o nome.
- `atualizar`: aplica `title/description/status/dueDate` e `assigneeId` (com nome).
- `obter`/`remover`: busca por id e bloqueia acesso se não for owner (admin vê tudo).

## Rotas (`src/routes/task.routes.js`) — `auth` + `validate`
```
router.use(auth);
router.get('/', listar);            // retorna { tasks: [...] }
router.get('/:id', obter);
router.post('/', validate(taskCreate), criar);
router.patch('/:id', validate(taskUpdate), atualizar);   // move = PATCH {status}
router.delete('/:id', remover);
```
Registre em `routes/index.js`: `router.use('/tasks', require('./task.routes'));`
A API fica em `/api/tasks` (prefixo `/api` do app.js) e as páginas em
`/board` e `/calendario` (pages.routes).

## Páginas (EJS + `public/js/*.js`, CSP proíbe inline)
- `views/board.ejs`: container `<section id="board" data-api-base="<%= apiBase %>">`
  com 3 colunas (`data-status="todo|doing|done"`); formulário de nova tarefa
  (`hidden` até o botão "Nova tarefa"). O JS busca `/api/tasks`, agrupa por
  status e monta cards. Cada card tem botões `←` (volta status) e `→` (avança)
  que dão `PATCH /api/tasks/:id {status}` e `✕` que dá `DELETE`.
- `views/calendario.ejs`: `<section id="calendar" data-api-base="<%= apiBase %>">`
  com `cal-grid` de 7 colunas (Dom..Sáb) + corpo `#cal-body`. O JS calcula o mês
  (primeiro dia → `getDay()` para espaços, `daysInMonth`), e para cada dia põe
  os chips das tasks cujo `dueDate` cai naquele dia. Botões `←`/`→` mudam o mês
  (`view.setMonth(...)`) e re-renderizam.
- Passar `apiBase: '/api/tasks'` (ou `/api/<modo>/tasks`) via `res.render`.

### JS — move/delete sem token
```js
async function api(method, path, body) {
  const opts = { method, credentials: 'same-origin', headers: {} };
  if (body !== undefined) { opts.headers['Content-Type'] = 'application/json'; opts.body = JSON.stringify(body); }
  const res = await fetch(apiBase + path, opts);
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || ('HTTP ' + res.status));
  return data;
}
```
O `csrfGuard` é por Origin/Referer (não token); fetch mesmo-origin passa. Ver
`references/i18n-e-tema.md`.

### CSS (tokens do DESIGN.md, sombra única)
```css
.board { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }
.board-col { background:var(--bg); border:1px solid var(--border); border-radius:var(--radius); padding:.75rem; }
.task-card { background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:.75rem; box-shadow:var(--shadow); }
.cal-grid { display:grid; grid-template-columns:repeat(7,1fr); gap:.4rem; }
.cal-cell { background:var(--surface); border:1px solid var(--border); border-radius:8px; min-height:84px; padding:.35rem; }
.cal-task { font-size:.72rem; padding:.15rem .4rem; border-radius:6px; text-decoration:none; border-left:3px solid var(--primary); }
```
Ponto de quebra único em 860px: `.board { grid-template-columns:1fr; }`.
Sem emoji — usar `✕` (U+2715) ou SVG inline.

## Seed idempotente (`src/seeds/task.seed.js`)
```js
async function seedTasks(models, ownerId, ownerName) {
  const Task = models.Task; const hoje = new Date();
  for (const [title, status, offset] of TITLES) {
    if (await Task.findOne({ title, ownerId })) continue;   // idempotente
    const due = new Date(hoje); due.setDate(due.getDate() + offset);
    await Task.create({ title, status, dueDate: due, ownerId, ownerName });
  }
}
```
No `server.js`, após semear os bancos: ache o dono (`demo1` no demo, `admin` no
teste) e chame `seedTasks`. Produção fica limpa. Não use `deleteMany` (pitfall 26).

## Teste (`tests/task.test.js`)
- Cria → lista → PATCH status → DELETE (204). **Status de validação Zod é 422,
  não 400 (pitfall 33).**
- Escopo: usuário comum só vê as suas; admin vê todas. Reuse `carregarDemo`
  para criar `demo1`/`demo2` e logar (senão o `register` pode falhar no teste).
- `login(email)` helper: `await carregarDemo(...)` + POST `/api/test/auth/login`
  com `AdminComum123!!`.
