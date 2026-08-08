---
name: projeto-profissional-template
description: Development & operations workflow for the user's "projeto-professional" template (Node 20 + Express + MongoDB/Mongoose + EJS SSR + JWT). Captures recurring gotchas — require-cache restart, demo-DB reseed, Zod field-strip, i18n literal cause, browser session loss, 3-database (app/test/demo) architecture, AND the demo-seed pitfalls that crash boot (orphan Docker-container server causing E11000 dup-key, escapeAttr-is-not-defined in client JS, Meta.insertMany needing models.Meta), plus the user's delivery workflow (split big features into GitHub issues, commit per feature in their name).
---

# projeto-profissional template

Template base de app web do usuário: autenticação JWT (cookie httpOnly ou Bearer),
papéis `admin`/`user`, registro controlado por admin, quadro Kanban, projetos,
profissionais e painel. Stack: Node 20 + Express, MongoDB/Mongoose, EJS SSR + JS
vanilla (sem build), Zod, Jest + Supertest. Repo em
`/home/pedro/Repositorios/templates/projeto-profissional`, app em `./app`.

## Quando usar
Sempre que mexer nesse repo: adicionar feature de domínio, corrigir bug de UI,
populhar/resear o banco demo, rodar a suíte de testes, ou fazer commit/push.

## Arquitetura (resumo crítico)
- **Três bancos físicos** na mesma instância Mongo, via `connection.useDb`:
  `app_db` (produção), `app_test_db` (teste), `app_demo_db` (demo).
  Models são registrados por connection num registry (`src/models/registry.js`).
- O JWT carrega `mode` no payload; `auth` **rejeita token de modo diferente**
  (token de demo não abre produção).
- Demo é acessível pela landing (`/demo/start` autologa num usuário demo).
- Fluxo obrigatório: **Rota → Controller → Service → Model**. Validação Zod
  obrigatória em toda entrada (middleware `validate(schema)`).

## Armadilhas recorrentes (leia antes de debugar)

### 1. Edições server-side NÃO surtem efeito sem restart (require-cache)
`i18n.js`, `demoService.js`, `taskService.js`, `task.model.js`, controllers,
routes, schemas — todos são cacheados pelo `require`. Se você editar `i18n.js`
e uma key `t('task.x')` ainda aparece **literal** no browser, NÃO é bug do
código: é o servidor rodando com o módulo antigo. **Reinicie o servidor**
(procedimento em `references/server-ops.md`). Esse foi o caso das keys
`task.*`/`board.intro` aparecendo literais.

### 2. Campo novo some silenciosamente na API (Zod strip)
Se você adiciona um campo no model (ex: `horario`, `arquivos`, `comentarios`)
mas NÃO o adiciona ao schema Zod em `src/schemas/demo.schemas.js`, o
`validate()` **stripa** o campo — ele não persiste no PATCH/POST e volta vazio.
Sempre atualize em conjunto: model + service + controller + view/JS + **schema
Zod**. O EJS/JS pode exibir o campo, mas a API o remove.

### 3. Reseed do banco demo
O boot (`src/server.js` → `seedBanco('demo')`) só semeia se o banco estiver
vazio. Para forçar dados novos (ex: contagem massiva), **drope `app_demo_db`**
e reinicie — o boot re-seeda com os números em `server.js` (atualmente
`usuarios:200, projetos:400, itens:300, tarefas:3000, profissionais:120`).
Não tente `POST /api/demo/load?force=true` pelo shell — o `csrfGuard`/auth
dá 401/403 no `node -e` por escaping do body; use o browser (session cookie +
Origin corretos) ou drope o DB.

### 4. Drag-and-drop no Kanban
Cartões renderizados pelo SSR (EJS) NÃO têm `draggable="true"` por padrão — só
os criados via JS. Após `renderizarCards()` sete o atributo em todos:
`document.querySelectorAll('.tcard').forEach(c => c.setAttribute('draggable','true'))`.

### 5. Browser perde a sessão em navegação direta por URL
`browser_navigate` para `http://localhost:4450/demo/board` direto **perde o
cookie** de demo e cai em 401. Navegue primeiro para `/demo/start` (seta o
cookie) e depois **clique nos links internos** da navbar. Use `browser_vision`
para validar design visual antes de commitar mudanças de UI.

### 6. Testes usam mongodb-memory-server
`npm test` (em `app/`) sobe um Mongo em memória. Na PRIMEIRA execução baixa o
binário (~100MB) — precisa de rede; pode demorar. Não é erro. Já há ~78 testes
(task, project, professional, meta, auth, admin, seed, demo, paginas, config).

### 7. Model com campo `required` QUEBRA o seed demo (e o boot)
Se você adiciona um campo obrigatório no model (ex: `responsavelId` em
`Project`, `email` em `Professional` com `match`/`required`), o seed
(`demoService.js`) **precisa definir esse campo em todos os docs**, senão o
`insertMany` lança ValidationError e o **servidor não sobe**. Ao adicionar
`required`/`match` no model, edite também o `demoService.js` (bloco de
`projDocs`/`profDocs`) para passar o campo. Validação extra no schema Zod
(`z.string().email()`, `z.string().regex(/^[a-f\d]{24}$/)`) só roda na API,
não no seed — então o seed pode passar mesmo sem o campo se o model não
exigir; mas se o model exigir, o seed quebra. Regra: **model + schema Zod +
demoService.seed em conjunto**.

### 8. Filtros em Kanban massivo (client-side) e comentários editáveis
Padrão validado neste repo para board com milhares de cards:
- **Filtro client-side** sobre os cards já renderizados (sem refetch): cada
  `.tcard` carrega `data-projeto`, `data-profissional`, `data-tags`,
  `data-inicio`, `data-prazo` (YYYY-MM-DD). Um `applyFilters()` esconde cards
  que não batem (`card.style.display='none'`). Contadores de coluna devem
  refletir **só os visíveis** (`querySelectorAll('.tcard:not([style*="display: none"])')`).
  Veja `references/kanban-patterns.md` para o snippet pronto.
- **Comentários editar/remover**: o model `Task.comentarios` é um array sem
  `_id`. Para editar/remover, modifique o array local por **índice estável**
  e faça `PATCH /api/tasks/:id` com o array `comentarios` completo. Para editar
  inline, troque o `<p>` por `<textarea>` + botões Salvar/Cancelar; ao salvar,
  `Object.assign(comentarios[idx], { texto })` e PATCH. Veja
  `references/kanban-patterns.md`.

### 9. CSP proíbe `<script>` inline — nem mesmo `window.__x = ...` no EJS
O CSP deste repo não permite `unsafe-inline`. Não injete dados no EJS via
`<script>window.__usuarios = <%= JSON.stringify(...) %></script>` (a página
não carrega o script). Para passar listas do backend ao JS da página, **popule
no controller/service** (ex: `Project.find().populate('responsavelId','name')`)
e leia do JSON da API no cliente, ou gere `<option>` no EJS (SSR, permitido).
Toda lógica de handler vai em arquivo `.js` servido de `/js/`.

### 10. Servidor zumbi em container Docker causa `E11000 duplicate key` no seed
Se o boot crasha com `MongoBulkWriteError: E11000 duplicate key error ...
collection: app_demo_db.users index: email_1`, NÃO é bug do schema: há um
**node server órfão de sessão anterior ainda vivo** (preso num
`containerd-shim-runc-v2`, i.e. DENTRO de um container Docker) re-seedando/
reinserindo `users` (`demoN@example.com`) no mesmo banco demo. O seed demo NÃO
é idempotente (`insertMany` falha em dup key), então o conflito trava o boot.
Diagnóstico e reset (não tente só `dropDatabase` isolado — o zumbi reinsere):
```bash
pgrep -af 'node src/server.js'          # achar PIDs vivos
ps -o pid,ppid,cmd -p <pid>              # se ppid for containerd-shim-runc-v2, está num container
kill -9 <pid_zumbi>                     # mata só ele
# depois: drop + sobe UM servidor (recipe em references/demo-reset.md)
```
O servidor do projeto-profissional escuta 4450 e usa `MONGO_URI=.../app_db`.
Confirme `curl -s -o /dev/null -w '%{http_code}' http://localhost:4450/` = `000`
antes de subir o seu. Veja `references/demo-reset.md`.

### 11. `escapeAttr` NÃO existe no escopo dos `.js` do cliente
Nos `public/js/*.js` só existe `escapeHtml` (definida no próprio arquivo). Usar
`escapeAttr(...)` lança `ReferenceError: escapeAttr is not defined` e quebra a
tabela/modal. Para atributos, faça `escapeHtml(v).replace(/"/g,'&quot;')` ou só
`escapeHtml`. Nunca invente `escapeAttr`.

### 12. `Meta.insertMany` no seed usa `models.Meta`, não `require('../models/meta.model')`
O `require` do schema retorna o **schema**, não o model — logo `Meta.insertMany
is not a function`. No `demoService.js` use `models.Meta ||
require('mongoose').model('Meta')` (o `models` vem do parâmetro
`carregarDemo({...}, models)`). Mesma regra para qualquer model acessado dentro
do seed: prefira o `models.<Model>` passado.

## Workflow de entrega (commits/features) — pedido do usuário
O usuário quer features grandes **divididas em issues no GitHub e executadas
por partes, commitando etapa a etapa EM SEU NOME** (pedro). Regras:
- Antes de feature grande: `gh issue create --title '...' --body '...'
  --label feature` (uma issue por sub-feature).
- Implemente UMA sub-feature por vez; `git commit` **pequeno e coeso**
  (model+schema+service+view+js+i18n juntos quando couberem na mesma feature),
  mensagem em PT (`feat: ...`). NÃO faça um commit gigante de tudo.
- Commit em nome do usuário (git local já é pedro). Se necessário:
  `git -c user.name=... -c user.email=...`.
- Push por feature: `git push origin <branch>`. Nunca comite `.env`.
- Valide no browser (screenshot) ANTES de commitar mudança de UI.

## Comunicação com o usuário
- Responda em **português**, texto puro de terminal, **sem markdown**.
- Estilo KISS/DRY; prefere layout full-width e verificação visual (screenshot)
  antes de commitar UI. É exigente com design — valide no browser e mostre
  screenshot antes de declarar pronto.

## Ver também
- `references/server-ops.md` — comandos exatos de restart/reseed (PID, docker
  mongo, drop DB, env).
- `references/demo-reset.md` — recipe de reset limpo do `app_demo_db` (mata
  servidor zumbi em container, drop, sobe UM servidor) + gotchas de seed
  (`projIndice`, `Meta.insertMany`, `escapeAttr`).
- `AGENTS.md` / `CLAUDE.md` no repo — regras arquiteturais e checklist de PR.
- `TEMPLATE.md` no repo — o que remover para usar só o núcleo de auth/segurança.
- `docs/deploy.md` — deploy em produção.
