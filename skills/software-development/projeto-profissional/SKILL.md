---
name: projeto-profissional
description: Bootstrap a new professional repo from Pedro's hardened Node/Express+MongoDB+EJS base template (JWT auth, admin/user roles, admin-controlled registration, security defaults, full root markdown set), and maintain it — dual prod/test Docker stacks, k6 load testing, Jest suite. Use whenever Pedro asks to start a new project/repo, "criar um projeto novo", "primeiro commit", a base/modelo/template for GitHub, to add login+admin to a fresh app, or to load-test / dockerize / benchmark one of these projects.
---

# Projeto Profissional — base template for new repos

Pedro's canonical starting point for any new web project. Instead of scaffolding
from scratch (and re-deciding security every time), copy the vetted template and
adapt it.

**Template location:** `/home/pedro/Repositorios/templates/projeto-profissional`
(git-initialised, 44 passing tests, boot-verified, load-tested with real k6 numbers).

**Origin:** distilled from `/home/pedro/Repositorios/academicos/sistema-academico`,
keeping that project's layered architecture but stripping the academic domain.

## When to use

- "cria um projeto novo / um repositório novo / o primeiro commit"
- "quero um modelo base pro meu GitHub"
- "preciso de login com admin nesse app"
- Any new Node web app for Pedro — start here, don't hand-roll auth.

## Stack (do not swap without being asked)

Node 20 + Express · MongoDB/Mongoose · EJS SSR + vanilla JS (**no bundler, no
React, no build step**) · Zod · JWT HS256 · Jest + Supertest +
mongodb-memory-server · Docker Compose.

## Procedure

1. **Copy, don't regenerate.**
   `cp -r /home/pedro/Repositorios/templates/projeto-profissional <destino>`
   then `rm -rf <destino>/.git <destino>/app/node_modules` and `git init`.
2. **Rename** in `app/package.json` (name, description), `.env.example` and
   `docker-compose.yml` (DB name, `APP_NAME`), and the brand in
   `app/views/partials/header.ejs` + `app/views/landing.ejs`.
3. **Adjust roles** if needed — the `role` enum lives in BOTH
   `src/models/user.model.js` and `src/schemas/admin.schemas.js`. Change together.
4. **Add the domain** following the chain: model → Zod schema → service →
   controller → routes → register in `routes/index.js` → test in `tests/`.
   For a domain with several entities, write the layers in that order for ALL
   entities before touching views — the suite can go green before any UI
   exists, which is the cheapest place to find modelling mistakes. Money,
   monthly competence, weighted average cost and CSP-safe SVG charts:
   `references/money-and-charts.md`.
   When Pedro names an app category ("controle financeiro", "gestão de X"),
   look up the established open-source players first and port their *model*
   (Firefly III, Actual Budget, Ghostfolio for finance) instead of inventing
   entities — then say which ones you drew from.
   Ship a `scripts/seed-demo.js` with realistic data so the screens can be
   inspected for real; guard it like `seed-carga.js` (pitfall 26). Quando o
   domínio pedido é "bastante simples" (ex.: task manager board + calendário),
   use o padrão copy-paste em `references/task-manager-simples.md` — sem
   drag-and-drop nem redesenho do shell.   If the app has more than one domain, treat them as **optional modules** from
   the start (`MODULE_<NOME>` flags, guard per request, dashboard desacoplado):
   `references/optional-modules.md`. Retrofitting modularity later means
   rewriting the dashboard.
5. **Backup do banco de produção**: copie `templates/backup.sh` para
   `<repo>/scripts/backup.sh` (mongodump dentro do container → zip com
   timestamp + MANIFEST de restauração, chmod 600, retenção configurável).
   Copie também `templates/reset-senha.js` para `<repo>/app/scripts/` — sem ele,
   perder a senha do admin só se resolve escrevendo hash na mão no banco.
   Acesso às duas stacks, criação de usuário e o 429 do limiter:
   `references/operacao-e-acesso.md`. Todo projeto derivado ganha um
   `docs/operacao.md` com esse conteúdo.
6. **Verify for real** before reporting done:
   `cd app && npm install && npm test` (must be green), then boot-smoke it.
   See `scripts/smoke-boot.js` — copy it into `app/` and run it there
   (it needs `mongodb-memory-server` from the app's own node_modules; running
   it from `/tmp` fails with MODULE_NOT_FOUND).
   For the structural invariants Jest can't reach (stack isolation, k6
   scenario, CSP, workflows) run `scripts/verify-stacks.sh <destino>`, and for
   live brute-force behaviour (which Jest cannot cover at all) run
   `scripts/verify-bruteforce.sh <destino> 3 30` — it boots both stacks, asserts
   the exact `401 401 401 429` sequence, and tears them down via `trap`.
7. **Commit** and confirm `git ls-files` shows no `.env` and no `node_modules`.

## Non-negotiable design decisions

Carry these into every derived project; they are the point of the template.

- **No public self-registration.** Admin creates accounts
  (`POST /api/admin/users`); server generates a temp password shown exactly
  once, account is born with `mustChangePassword`.
- **Strict layers**: Route → Controller → Service → Model. Services never
  receive `req`; they take validated data + `userId` explicitly.
- **Zod on every POST/PUT/PATCH** via `validate(schema)`.
- **`AppError(msg, status)`** for expected errors; `errorHandler` is the only
  place that formats an error response.
- **CSP without `unsafe-inline`** ⇒ zero inline `<script>` in views; all JS in
  `public/js/`, wired through the `pageScript` footer variable.
- **Secrets only via `.env`** read by `config/env.js`; `.env.example` holds
  empty keys, never real values.

## Security baseline already wired

bcrypt cost 12 + `select:false` on the hash · 12-char password policy ·
account lockout 3 attempts/30min · timing-safe dummy-hash compare (anti-enumeration) ·
identical `/forgot-password` response either way · `tokenValidAfter` for global
session revocation · csrfGuard (Origin/Referer) · sanitizeInput (NoSQL
injection) · Helmet+CSP · rate limits · CORS allowlist (never `*`) · 100kB body
cap · AuditLog with 180-day TTL · non-root read-only container.

Full rationale: `references/security-baseline.md`.

## Brute-force protection is TWO layers — tune them together

Anti-brute-force lives in two independent places, and changing one without the
other silently disables it:

| Layer | Where | Protects | Env vars |
|---|---|---|---|
| IP rate limit | `middleware/rateLimiters.js` | the **service** (one noisy IP) | `RATE_LIMIT_AUTH_MAX`, `RATE_LIMIT_AUTH_WINDOW_MIN` |
| Account lockout | `services/authService.js` → `lockedUntil` | the **account** (distributed credential stuffing) | `MAX_FAILED_ATTEMPTS`, `LOCKOUT_MIN` |

Current default: **3 attempts / 30 min on both**. When Pedro asks for "3
tentativas, bloqueio de 30 min", he means the observable behaviour — set both
layers. Leaving the account lockout at a higher count than the IP limit means
the lockout can *never* fire (the IP limiter answers 429 first), so the layer
that defends against distributed attacks is dead code.

Both are read from `config/env.js` — no magic numbers in `authService.js`.
Defaults are pinned by `tests/config.test.js`.

Verify end-to-end, not just by reading config: the limiters are **disabled
under `NODE_ENV=test`**, so Jest structurally *cannot* prove the limit. Only a
running container can:

```bash
for i in 1 2 3 4; do curl -s -o /dev/null -w '%{http_code} ' \
  -X POST localhost:4447/api/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"admin@example.com","password":"errada123456"}'; done
# esperado exatamente: 401 401 401 429
curl -sD- -o /dev/null ... | grep -i ratelimit-policy   # RateLimit-Policy: 3;w=1800
```

Assert the **exact sequence** (`"401 401 401 429 "`), not "contains 429" — the
loose version passes even if it locks on the first attempt. Then confirm the
correct password *still* returns 429 (proves real blocking, not error
counting), and that `lockedUntil` is ~30 min ahead in Mongo.

## Uma instância, teste de carga via NODE_ENV

O template sobe como **uma instância** na porta `4450` (`docker-compose.yml`
apenas). Para teste de carga, suba com `NODE_ENV=staging` (desativa o rate
limit) — não há mais um segundo compose de teste. A demo é sempre acessível
pela landing. Veja `docs/load-testing.md`.

| | Instância única |
|---|---|
| File | `docker-compose.yml` |
| DB | `app_db`, `app_test_db`, `app_demo_db` (mesma instância Mongo) |
| Port | `${BIND_ADDR:-127.0.0.1}:4450` |
| `NODE_ENV` | `production` (ou `staging` para carga, sem rate limit) |
| Rate limiting | ativa em `production`, desativada em `staging` |

```bash
NODE_ENV=staging JWT_SECRET=$(openssl rand -base64 48) docker compose up -d --build
```

## Load testing (k6)

Full methodology, measured numbers and capacity planning:
`references/load-testing.md`. Scenario lives at `loadtest/carga.js` with five
profiles (`smoke`, `carga`, `estresse`, `pico`, `auth`) and k6 thresholds that
fail CI when crossed.

Reference measurements (i5-9400F 6 cores, single instance): **100 VUs → 0%
errors, 214 req/s**; 200 VUs → still 0% errors but latency over target. The
bottleneck is always **login** (bcrypt cost 12 is CPU-bound by design,
~4.5 logins/s per instance); reads and SSR cost ~3-6 ms. The app is stateless,
so the answer is horizontal scaling — **never quietly lower the bcrypt cost to
win a benchmark.**

## Pitfalls (all hit for real)

1. **JWT `iat` is in SECONDS, truncated.** Comparing `payload.iat * 1000 <
   tokenValidAfter.getTime()` rejects legitimate tokens minted in the same
   second. Normalise both sides to seconds. Covered by a test — keep it.
2. **`passwordHash` has `select:false`.** Any query that must compare a
   password needs `.select('+passwordHash')`, or `bcrypt.compare` silently
   receives `undefined`.
3. **`COOKIE_SECURE=true` over plain HTTP** ⇒ browser discards the cookie:
   login returns 200 and the session still doesn't stick. Classic LAN/VPN trap.
4. **`upgradeInsecureRequests`** must stay off while serving HTTP, or CSS/JS
   fail to load and the page renders unstyled.
5. **Express 5 makes `req.query` a getter** — `sanitizeInput` mutates in place;
   do not "simplify" it to `req.query = {...}`.
6. **Never build a `RegExp` from user input unescaped** (user search) — escape
   metacharacters or it's a ReDoS.
7. **`npm ci` in CI needs `package-lock.json` committed.**
8. **Load-test scripts must reuse the session token.** Logging in on *every*
   k6 iteration is a login-storm, not realistic traffic: with bcrypt 12 it
   drove 200 VUs to 60s latency and 6% errors and made the app look broken.
   Log in once per VU, reuse the token, and isolate the worst case in its own
   `auth` profile.
9. **`grep -q 'app_db'` also matches `app_test_db`.** Substring asserts cannot
   tell the two stacks apart — compare the *full* resolved URI for equality.
   Also export a dummy `JWT_SECRET` before `docker compose config`, or
   interpolation fails and the command returns empty (a silent false pass).
10. **The container serves the image, not your edited file.** After changing a
    view/CSS, `docker restart` keeps the stale build-time copy — rebuild
    (`up -d --build`) before believing a visual fix didn't work.
11. **`dotenv` loads the project `.env` and overrides env vars you pass** when
    testing config guards. Run such probes with `cwd` outside the project
    (e.g. `/tmp`) or the guard appears not to fire.
12. **The k6 container runs as its own UID** and cannot traverse a `0700` home
    directory to reach a bind mount ("permission denied" reading the script).
    Set `user: "0:0"` on that ephemeral test container instead of loosening
    permissions on the host.
13. **A port change is a repo-wide edit, not a compose edit.** The host port
    appears in both compose files, `.env.example`, the `PORT` default in
    `config/env.js`, the k6 `BASE_URL` default, the readiness curl in
    `carga.yml`, the nginx `proxy_pass` in `docs/deployment.md`, and the dev
    URL in README/AGENTS/CLAUDE/CONTRIBUTING. Grep for the old number and
    confirm zero hits before committing. Only the *host* side changes — the
    container keeps listening on 5000 (`4447:5000`).
14. **Tightening a limit invalidates existing tests.** The old
    "bloqueia após 5 tentativas" loop still passes with a limit of 3 (it just
    over-shoots), so it silently stops testing anything. When a threshold
    changes, rewrite the assertion to pin the *exact* boundary: two failures
    must still return 401, the third must arm the lockout.
15. **`127.0.0.1` in the compose port binding means "this machine only".**
    The page simply won't open from another host and the app logs look
    perfectly healthy — nothing errors, so it reads like a firewall problem.
    Publish via `${BIND_ADDR:-127.0.0.1}` and set `BIND_ADDR` to the reachable
    interface (Pedro's Tailscale IP is `100.120.54.126`; `0.0.0.0` only behind
    a firewall). Update `APP_BASE_URL` to match, and keep `COOKIE_SECURE=false`
    over plain HTTP or the session won't stick (see pitfall 3).
16. **A missing `JWT_SECRET` fails at compose *interpolation*, not at boot.**
    `docker compose up` aborts with "required variable JWT_SECRET is missing"
    and no container is created — easy to misread as an app crash. Create
    `.env` (chmod 600, git-ignored) with
    `echo "JWT_SECRET=$(openssl rand -base64 48)" >> .env` first.
17. **Once a real `.env` exists, it poisons default-value checks.** `docker
    compose config` merges it, so a probe asserting the template's built-in
    fallback (e.g. `BIND_ADDR` defaulting to `127.0.0.1`) reads Pedro's local
    value and reports a false failure. Isolate with
    `docker compose --env-file /dev/null ...` when verifying defaults. Same
    family as pitfall 11.
18. **Inserting prose into a markdown table splits it in two.** Patching a
    README by anchoring on a `| row |` and appending a paragraph lands the text
    *between* rows and silently breaks the table. Anchor on the sentence
    *after* the table instead, then re-read the rendered section to confirm.
19. **A new `<%= var %>` in a view is a runtime 500, not a lint error.** Routes
    call bare `res.render('landing')`, so an EJS variable nobody passes only
    explodes when the page is requested. Register shared values once with
    `app.locals.appName = env.appName` in `app.js` instead of threading them
    through every route, and verify by compiling the template directly:
    `node -e "require('ejs').render(fs.readFileSync('views/landing.ejs','utf8'),{appName:'X'})"`.
20. **An in-page anchor needs its target to exist.** `href="#topo"` silently
    does nothing unless some element carries `id="topo"` — put it on `<body>`
    in the header partial. Prefer the pure-anchor + `scroll-behavior: smooth`
    combo over JS: the CSP forbids inline scripts anyway.
21. **The template's `.field`/`.card` rules defeat the `hidden` attribute.**
    `hidden` only sets `display:none` through the UA stylesheet, so any class
    rule with `display: block` wins and a field you "hid" from JS stays on
    screen — the JS looks broken while `el.hidden === true`. Add
    `[hidden] { display: none !important; }` to `main.css` once per derived
    project. Diagnose this class of bug by comparing `el.hidden` against
    `getComputedStyle(el).display`, not by re-reading the JS.
22. **A new derived project collides with the template's own ports/project
    name.** The template stack is usually still up on 4447/4446 under compose
    project `pp`. Before the first `up -d`, pick fresh host ports AND a fresh
    project name (`name:` key + `-p`), then do pitfall 13's repo-wide sweep in
    one pass over the known file list:
    `perl -pi -e 's/4447/4451/g; s/4446/4450/g; s/-p pp\b/-p fa/g; s/app_db/<novo>_db/g' <files>`
    Rename the DB too — two projects sharing `app_db` in your head is how a
    demo seed lands in the wrong volume. Then grep for the old numbers/names
    and confirm zero hits, INCLUDING inside `tests/config.test.js`, whose seed
    guard asserts a literal DB name.
23. **Point a booted stack at a scratch DB with an override file, not by
    editing the committed compose.** Write three lines to
    `/tmp/<proj>-demo.override.yml` setting `MONGO_URI` to a `*_demo` database
    and boot with `-f docker-compose.yml -f /tmp/....yml`. Keeps the repo clean
    and the demo reproducible.
24. **`docker compose` must run from the repo root, not from `app/`.** From the
    Node subdirectory it fails with `open .../app/docker-compose.yml: no such
    file or directory`, which reads like a missing file rather than a wrong cwd.
25. **After a rebuild the *browser* still serves the old CSS/JS.** Pitfall 10
    covers the container; the other half is client cache, and it produces the
    exact same symptom ("my fix did nothing"). Confirm the served bytes with
    `curl -s host/css/main.css | tail`, and in the page use
    `fetch(url,{cache:'reload'})` before concluding the fix failed.
26. **Any destructive seed needs a DB-name guard and a test for it.** A demo
    seeder that `deleteMany({})` on every collection is total data loss if
    pointed at production. Copy the `seed-carga.js` pattern — refuse unless the
    URI matches `/test|demo/i` — and pin it in `tests/config.test.js` alongside
    the existing guard.
    27. **Página vs JSON de mapeamento moram em prefixes de montagem diferentes.**
      `routes/index.js` é montado sob `/api` no `app.js`; `pages.routes.js` é
      montado sob `/`. Uma rota `router.get('/status')` dentro de um arquivo sob
      `/api` vira `/api/status`, não `/status`. Por isso o mapeamento HTTP se
      divide: o JSON `GET /api/status/:code` fica em `status.routes.js` (definido
      como `router.get('/:code')` e montado em `routes/index.js` sob `/status` →
      resultado `/api/status/:code`); a *página* `GET /status` fica em
      `pages.routes.js`. Misturar os dois num só arquivo faz a página ou o JSON
      sumirem (vieram 404 até acertar esse split).
    28. **Catálogos separados: importe de onde cada um vive.** `HTTP_CATALOG` está
      em `status.routes.js`; `ERROR_CATALOG`/`catalogFor` estão em
      `errorHandler.js`. Um teste que faz
      `require('../src/routes/status.routes').ERROR_CATALOG` recebe `undefined` e
      quebra com `Cannot read properties of undefined`. Importe cada um do seu
      módulo.
    29. **Testar variante de erro exige mini-app com handler DEPOIS da rota de
      teste.** Para renderizar cada status 4xx/5xx, monte um `express()` isolado,
      registre `app.get('/_e_:code', (req,res,next)=>next(new AppError('x',Number(req.params.code))))`
      e SÓ DEPOIS `app.use(notFoundHandler); app.use(errorHandler)`. Se o
      `notFoundHandler` vier antes, ele responde 404 para a rota de teste e o
      status forçado nunca chega ao `errorHandler`.
    30. **Botão "Voltar" não pode usar `javascript:` — a CSP bloqueia.** `href=
      "javascript:history.back()"` é script inline disfarçado e a CSP
      (`script-src 'self'`) o impede; o clique não faz nada. Passe `backUrl` do
      servidor usando o `Referer` same-origin (cai em `/` se ausente/externo).
      Mesma regra do "Voltar ao topo", que é âncora pura `#topo`.
    31. **Script de verificação ad-hoc precisa rodar de dentro de `app/`.** Rodar de
      `/tmp` falha com `MODULE_NOT_FOUND` (mongodb-memory-server, supertest etc.
      estão em `app/node_modules`). Copie o script para `app/` com nome
      `hermes-verify-*.js` ou use `cwd` em `app/`. Vale para `smoke-boot.js` e
      qualquer probe que exija os deps do app — não confunda com o pitfall 11, que
      manda rodar probe de *config* de `/tmp` justamente para o `.env` não
      sobrescrever o ambiente.
    32. **README não é só 'como rodar' — Pedro quer que ensine a DESENVOLVER,
      RODAR e DOCUMENTAR.** Ao tocar no README do template (ou de projeto
      derivado), inclua: (a) seção **Desenvolvimento** — fluxo de branch
      `feat/*`/`fix/*`, `.env`, loop dev→test→verify, lint DESIGN.md e
      `npm audit`, Conventional Commits e arquitetura em camadas; (b) seção
      **Documentação** — tabela de responsabilidade dos arquivos de doc
      (README/AGENTS/CLAUDE/CONTRIBUTING/SECURITY/CHANGELOG/DESIGN/docs) e regras
      práticas (métrica só real, CSP na view, tokens no DESIGN.md, CHANGELOG
      humano). Não entregue README que só lista comandos de instalação.
    33. **O status de validação deste template é 422, não 400.** Testes novos
      escritos por instinto (`expect(res.status).toBe(400)`) falham em massa
      contra Zod/`validate()`. Confirme com uma chamada real antes de escrever a
      bateria inteira. Idem para `idParamSchema`: id malformado dá 422.
    34. **Fixture curta demais vira "Cannot read properties of undefined".**
      Schemas usam `.min(2)` em `description`/`nickname`, então um helper de
      teste que manda `'X'`/`'A'` recebe 422 e `res.body.<entidade>` fica
      `undefined` — o erro estoura três linhas depois, ao ler `._id`, e parece
      bug do service. Ao ver `undefined` lendo o corpo de um POST no teste,
      cheque o status da resposta ANTES de investigar o código.
    35. **A suíte precisa de `--forceExit`.** `npx jest` sozinho pendura após o
      último teste (handle aberto do mongodb-memory-server/app) e estoura o
      timeout do comando — parece suíte travada ou falhando quando na verdade
      passou. Rode `npx jest --forceExit` e leia a linha `Tests:`.
    36. **`jest.resetModules()` para recarregar flags mata a conexão do
      mongoose.** Remontar o app por teste (para reler env) cria uma instância
      nova do mongoose que não enxerga a conexão do `setupDb`; cada teste morre
      em timeout de 5s sem mensagem útil. A saída não é remontar — é fazer a
      config ser lida **por getter** e o guard rodar **por request** (ver
      "Módulos opcionais"), aí um único app cobre todas as combinações só
      mexendo em `process.env`.
    37. **Rota transversal não pode morar sob o prefixo de um módulo.**
      `GET /api/financas/dashboard` some junto quando finanças é desligado,
      mesmo que ele agregue os outros módulos. Monte-a na raiz da API
      (`GET /api/dashboard`, em `routes/index.js`) e atualize o fetch da view.
    38. **PUT vs POST: confira a rota real antes de escrever o inventário.**
      Orçamento é upsert de envelope, logo `PUT /api/financas/orcamentos`. Um
      teste de inventário que assume POST recebe 404 e parece rota faltando.
    39. **O container é read-only: script novo entra pela IMAGEM, não por `cp`.**
      O baseline roda o container com rootfs read-only, então
      `docker compose cp arquivo app:/app/scripts/` falha com *"container rootfs
      is marked read-only"* — parece permissão do host, mas é o hardening
      funcionando. Commite o arquivo e rode `up -d --build app`.
    40. **Guard que responde antes do roteamento cega o teste de 404.** Em
      `/api/admin/*` o `requireRole` devolve 403 antes de o Express concluir que
      a rota não existe, então um caminho ERRADO (`/usuarios` em vez de `/users`)
      passa no `not.toBe(404)` e no `toContain(403)`. O inventário fica verde
      testando rota inexistente, e o defeito só aparece num `curl` real. Copie os
      caminhos de admin do `admin.routes.js`; nunca os digite de memória.

    41. **`AppError` expõe `statusCode`, não `status`.** Um probe que assere
      `(e) => e.status === 409` recebe `undefined`, o `assert.rejects` reprova
      com *"validation function is expected to return true"* e parece que o
      service não lançou o erro — quando lançou o certo. Use
      `e.statusCode`. (Nos testes de rota isso não aparece, porque lá se lê
      `res.status` do Supertest — daí o instinto errado.)
    42. **Ampliar um módulo para o domínio genérico é renomeação em ~8 arquivos.**
      `moto` → `veiculos` (carro + moto) toca service/controller/rotas/schemas,
      mas também `routes/index.js`, `config/env.js` (getter **e** `toJSON`),
      `pages.routes.js`, o bloco do `relatorioService.dashboard()` (a chave do
      payload muda e quebra a view que lia `d.moto`), `.env.example` e a doc.
      Receita completa, incluindo o discriminador `type`, o filtro por tipo em
      coleções filhas e o consumo por combustível de carro flex:
      `references/optional-modules.md`, seção "Renomear ou ampliar um módulo".

    43. **"Melhore o X" pode se referir a algo que NÃO EXISTE.** Pedro pediu
      "o pdf de extrato tem que ficar melhor" — não havia exportação nenhuma no
      projeto, era item de roadmap (issue #2). Sair "melhorando" vira construir
      do zero uma feature com escopo adivinhado. Antes de aceitar um verbo de
      melhoria, `grep` pela feature; se não existir, **diga isso e pergunte o
      escopo** em vez de assumir. (Ele não respondeu no tempo do `clarify`, e aí
      seguir com a opção mais completa foi o certo — mas o aviso explícito de
      que era construção, não ajuste, é obrigatório no relatório.)

    44. **Agregado sobre coleção heterogênea precisa de teste com DOIS donos.**
      `$group: {_id: null, min/max}` de odômetro somando carro + moto inventou
      "34.410 km rodados, 237 km/l" e passou em toda a suíte, porque todo teste
      existente tinha um veículo só. Sempre que um número derivar de min/max/
      amplitude sobre linhas de entidades diferentes, escreva o caso com dois
      registros distintos — é a única fixture que reprova a fórmula errada.
      Detalhe e o snippet corrigido em `references/optional-modules.md` (item 6).

    45. **`pageScript` recebe o NOME da página, não o caminho.** O footer monta
      `<script src="/js/<%= pageScript %>.js">`. Passar `'/js/veiculos.js'` gera
      `/js//js/veiculos.js.js` → 404 do script. Sintoma cruel: a página renderiza
      inteira (é SSR), a API responde 200 em todo endpoint, o console **não
      registra erro nenhum** — só as tabelas ficam vazias, o que parece bug de
      service ou de banco. Confira com
      `[...document.querySelectorAll('script')].map(s=>s.src)` antes de
      investigar o backend. Convenção: `{ pageScript: 'veiculos' }`; página sem
      JS chama `include('partials/footer')` sem argumento (passar `null` também
      quebra).

    46. **O front recebe `vehicleId` populado como OBJETO nas listagens.** O
      service faz `.populate('vehicleId', 'nickname type')`, então
      `veiculos.find(v => v._id === String(item.vehicleId))` nunca casa e a
      coluna inteira vira `—`. Escreva um helper que aceite os dois formatos:
      `const nome = (ref) => !ref ? '—' : (typeof ref === 'object' ? ref.nickname : lista.find(v => v._id === String(ref))?.nickname ?? '—')`.

    47. **`new Date(iso).toLocaleDateString('pt-BR')` volta um dia.** A data é
      gravada como `2026-07-05T00:00:00.000Z`; no fuso do Brasil (UTC-3) o
      browser renderiza **04/07**. A tabela inteira fica um dia atrás do que a
      pessoa digitou. Formate sempre em UTC:
      `new Date(iso).toLocaleDateString('pt-BR', { timeZone: 'UTC' })`. Vale
      para toda view que exibe data vinda do Mongo.

    48. **Item ativo da navbar: injete `currentPath` uma vez, não rota a rota.**
      `app.use((req, res, next) => { res.locals.currentPath = req.path; next(); })`
      no `app.js` (logo após `app.locals.modules`) evita repetir a variável em
      cada `res.render` — e um `res.render` esquecido é um item de menu que nunca
      acende.

    49. **`doc.text()` no rodapé do pdfkit CRIA página nova — e são DUAS causas.**
      Escrever o rodapé avança o cursor, então um extrato de 1 página sai com 3
      (uma para o conteúdo, uma para "Página N de M", uma para "Gerado em").
      Corrigir só metade não resolve, e o sintoma é idêntico:
      (a) passe `{ lineBreak: false, width: larguraUtil }` em toda escrita
      posicionada de rodapé; **(b) o `rodapeY` tem de cair DENTRO da área útil**
      — `pageAltura - margins.bottom + 14` fica *abaixo* dela e pagina mesmo com
      `lineBreak:false`; use `- 12`. Arrume as duas de uma vez e reconte.
      Conte com extrator de verdade (`pymupdf`: `d.page_count`), não com
      `grep -c '/Type /Page'` no binário, que erra por causa dos streams.
      Demais armadilhas de diagramação (cabeçalho truncado em 1 letra, data ISO
      quebrando a coluna, acento que é dado e não fonte) estão na skill
      `document-exports`, com script `scripts/verify-pdf-export.sh`.

    50. **Validar seed/guard ANTES de qualquer I/O.** Um script cuja trava roda
      depois do `mongoose.connect` falha com `ECONNREFUSED` quando apontado para
      um host inacessível — mensagem que esconde o motivo real e derruba o teste
      que casa com `/Recusado/`. A checagem de nome de banco é a primeira linha
      executável do arquivo, antes de conectar. (Complementa o pitfall 26.)

    51. **Extrair lógica de um script para um módulo quebra o teste do script.**
      `tests/config.test.js` executa `scripts/seed-*.js` como subprocesso e casa
      com a mensagem de erro. Ao mover a lógica para `src/seeds/*.seed.js`,
      re-rode aquele arquivo de teste especificamente — a suíte de domínio passa
      e esconde a regressão do guard de segurança.

    52. **Para testar flags de boot, monte vários apps — nunca
      `jest.resetModules()`.** Quando a flag é lida em `createApp()` (e não por
      getter), cada cenário precisa da sua instância. `jest.resetModules()`
      recarrega o mongoose num registro novo, perde a conexão do `setupDb` e
      **todo teste morre em timeout de 5s sem mensagem útil** — parece deadlock.
      A saída é `require` do `createApp` UMA vez no topo e uma fábrica que só
      troca `process.env` ao redor da chamada:

      ```js
      const { createApp } = require('../src/app');
      function appCom(flags = {}) {
        const antes = { FLAG_A: process.env.FLAG_A };   // salve só as chaves usadas
        Object.assign(process.env, flags);
        const app = createApp();
        Object.assign(process.env, antes);              // nunca `process.env = antes`
        return app;
      }
      ```
      Complementa o pitfall 36: lá a solução foi getter + guard por request;
      aqui, quando a leitura é mesmo no boot, é esta fábrica.

    53. **Middleware de autenticação montado em `/` engole a landing.** Um
      autologin registrado como `app.use('/', mw)` autentica o visitante ANTES
      de a rota `/` rodar; ela então vê `req.user` e redireciona para `/app` —
      a página que explica o produto fica **inalcançável justamente na
      instância de demonstração**. Cada rota passa isoladamente no teste, então
      só aparece navegando. Exclua a raiz: `app.use(/^(?!\/$).*/, mw)`. Regra
      geral: middleware que muda o estado de autenticação precisa declarar de
      quais rotas ele fica de fora, e a landing é sempre uma delas.

    54. **Ao "melhorar" texto de UI, cheque se o dado também precisa mudar.**
      Um modelo de visão acusou "acentos errados" num PDF já corrigido — os
      acentos que faltavam estavam nos **dados do seed** (`Salario`,
      `Condominio`), não no gerador. Renderização e conteúdo são camadas
      distintas: `grep` nas strings do serviço E no seed antes de concluir.

- **94. Para subir o app NO HOST (fora do Docker) e testar na 4450, o Mongo fica INATINGÍVEL em `localhost:27017`.** O container `projeto-profissional-mongo-1` NÃO publica a porta 27017 no host — só expõe para a rede interna do compose (`docker inspect` mostra `"27017/tcp": null`). Então `npm start` do `app/` falha com `ECONNREFUSED 127.0.0.1:27017`. O host ALCANÇA o Mongo pelo IP do container (`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'` → ex.: `192.168.112.3`, confirme a cada máquina). Receita de subida local (sem Docker, apontando pro Mongo do container):
  ```bash
  cd /home/pedro/Repositorios/templates/projeto-profissional/app
  ln -sf ../.env .env          # o .env REAL está na RAIZ do repo, não em app/ (dotenv do app só lê app/.env); linka ou defina as env abaixo
  export NODE_ENV=development   # development pula a exigência de JWT_SECRET forte (NODE_ENV=production exigiria JWT >32 chars)
  export MONGO_URI="mongodb://192.168.112.3:27017/app_db"   # IP do container, não localhost
  export SEED_PASSWORD_FILE="/home/pedro/Documentos/comum/senhas-projetos.md"
  export PORT=4450
  npm start
  ```
  Verificação: `curl -s -o /dev/null -w '%{http_code}' http://localhost:4450/` → 200; `/demo/start` → 302 com Set-Cookie; `/demo` → 200 com `id="board"`. **Atenção:** esse processo roda no shell do agente e MORRE se a sessão fechar — para deixar permanente use `docker compose up --build` (precisa de `JWT_SECRET` no `.env`). Os node_modules já têm `dompurify`/`katex`/`marked` vendored em `public/vendor/`, então `npm install` não é estritamente necessário se já existirem. `config/env.js` usa `PORT` default 4450, então sem `.env` de PORT sobe em 4450 mesmo assim.
- **95. handoff-resume SEM `HANDOFF.md`: o working tree sujo É o documento de continuidade.** Esta base costuma ser deixada com dezenas de arquivos modificados + não rastreados (feature de domínio incompleta, ex.: task manager com board/painel/profissionais). Não há `HANDOFF.md` — o skill `handoff-resume` assume que existe, mas aqui não existe. Procedimento: (1) `git status --short` + `git diff --stat` para ver o real estado; (2) leia os diffs e os arquivos novos (models/service/controller/routes/views/js) para reconstruir o que ficou pendente; (3) cruze com os sintomas relatados ("não está no ar na 4450" = processo nunca subiu, ver pitfall 94). Não invente um HANDOFF do zero — o `git` é a fonte. Dica: `git diff --stat HEAD` + `git ls-files --others --exclude-standard` dá o panorama completo em duas linhas.
- **96. Verificação SSR de tabela populada por JS dá falso FAIL.** Páginas como Projetos/Profissionais entregam o `<tbody>` VAZIO no servidor (o SSR monta só o shell + `<table>`/`<tbody id=...>`); as linhas são geradas pelo `public/js/*.js` após o `fetch`. Um `curl`/`http.get` no HTML servido NÃO acha os botões `icon-btn js-edit` — mas o **browser** (pós-JS) os renderiza. Ao verificar, confirme (a) o shell no SSR (`id="proj-rows"`, `class="dom-table"`) e (b) o JS no disco gera os botões (`pjs.includes('icon-btn js-edit')`), ou navegue no browser e confira o snapshot. Não marque como bug só porque o HTML cru não tem as linhas. Mesma razão pela qual um `hermes-verify-*.js` que lê o HTML servido não vê a tabela — ele precisa ler o JS ou navegar. (Complementa o pitfall 19/45: ache o gerador, não confie no HTML cru.)

Todo projeto derivado ganha um **mapeamento elegante de status HTTP** e uma
**página de erro rericada** (código grande, título, mensagem, ação de
recuperação e botão Voltar). É usado internamente e pelo suporte futuro.

**Onde vive:**
- `src/routes/status.routes.js` — catálogo `HTTP_CATALOG` (código, nome,
  classe success/redirect/client/server, `retryable`, descrição) + rota
  `GET /api/status/:code` (JSON estruturado, 404 se não mapeado). Exporta
  `HTTP_CATALOG` para a view reusar. Montada em `routes/index.js` sob `/status`
  → vira `/api/status/:code`.
- `src/routes/pages.routes.js` — rota `GET /status` que renderiza
  `views/status.ejs` (tabela filtrável via `?q=`, form GET, sem JS inline).
- `src/middleware/errorHandler.js` — além do mapeamento de erro existente,
  exporta `ERROR_CATALOG` (por status: `title` + `action` de recuperação) e
  `catalogFor(status)`. A view `error.ejs` agora recebe `title`, `action`,
  `details` e `backUrl`. O botão **Voltar** aponta para o `Referer`
  same-origin (ou `/`), nunca `javascript:` (bloqueado pela CSP).
- `views/status.ejs`, `views/error.ejs` + regras `.status-*`/`.error-*` em
  `public/css/main.css`.
- `tests/paginas.test.js` — cobre `/status` (lista, filtro, JSON, 404,
  ausência de script inline) e renderiza cada status 4xx/5xx forçando um
  `AppError` num mini-app isolado (rota de teste ANTES dos handlers, senão o
  `notFoundHandler` come 404).

**Regras ao estender:**
- Adicionar um status novo = só acrescentar a entrada em `HTTP_CATALOG`
  (status.routes) e, se for erro, em `ERROR_CATALOG` (errorHandler). Nunca
  espalhar `if`s pelo handler.
- `ERROR_CATALOG` deve cobrir todo 4xx/5xx presente em `HTTP_CATALOG` (há teste
  de consistência).
- Manter tokens do `DESIGN.md` (cores, raio, elevação única). Botão Voltar e
  "Página inicial" usam `.btn-primary`/`.btn-outline`.

## Três bancos isolados (produção / teste / demo) — um app, vários databases

Todo projeto derivado sobe **três bancos físicos isolados** numa só aplicação:
`app_db` (produção), `app_test_db` (teste) e `app_demo_db` (demo). Cada banco é
uma **connection própria** (via `connection.useDb`) e os models são registrados
**por connection** num registry — não há model global. O acesso é por **prefixo
de rota** (`/app`, `/test`, `/demo`); um único cookie `token` carrega o `mode`
(banco) no payload do JWT e o `auth` **recusa token de modo diferente** (um
token de demo não abre a produção).

Quando Pedro pedir **botão de demonstração na landing** ou **três bancos**, use
use este padrão (e não um usuário de demo dentro da produção):
`references/ambiente-demo-publico.md`. Padrão de i18n (PT/EN/ES/FR) + tema
claro/escuro + landing por instância: `references/i18n-e-tema.md`.

### Arquitetura (padrão implementado e testado)

- `config/db.js` → `connectDb()`: `mongoose.createConnection(baseUri)` (sem DB no
  final) e `getModeConn(mode)` faz `mainConn.useDb(MODE_DB[mode], {useCache:true})`
  (cacheado). `MODE_DB = { production:'app_db', test:'app_test_db', demo:'app_demo_db' }`.
  O nome do database é **derivado do final da `MONGO_URI`** (tira tudo após a
  última `/`), então `MONGO_URI=mongodb://.../app_demo_db` → banco `app_demo_db`.
- `models/registry.js` → `getModels(conn)`: registra `{User, Project,
  CatalogItem, AuditLog}` na connection (cache por `WeakMap` de conn) e devolve
  o objeto. **Os `*.model.js` exportam o SCHEMA, não o model** — o registry cria
  o model na connection certa.
- `middleware/selectDb.js` → `selectDb(mode)`: injeta em `req` `mode`, `conn`
  (`getModeConn(mode)`) e `models` (`getModels(conn)`). Montado ANTES de cada
  grupo de rotas: `app.use('/api/app', selectDb('production'), apiRoutes)` etc.
- `middleware/auth.js` → `signToken(user, mode)` assina com `payload.mode`;
  `resolveUser(token, mode, models)` **bate `payload.mode === mode`** e usa
  `req.models.User` (não o model global). `pageAuth` também passa `req.mode`/
  `req.models`.
- **Services recebem `models` via `req`** (não `require('../models/x')` global):
  controllers passam `req.models` para o service. É a mudança mais invasiva —
  fazer o registry + `selectDb` e depois catar cada `require('../models/...')`
  nos services/controllers.
- `server.js` semeia os 3 bancos no boot: produção só admin; teste admin +
  demo; demo banco completo (`carregarDemo`). `NODE_ENV=production` NUNCA popula
  demo.
- `app.js` monta as rotas em `/api/app`, `/api/test`, `/api/demo` **mais um alias
  `/api` que aponta para produção** (preserva testes antigos que usavam
  `/api/auth/login`). Páginas iguais em `/app`, `/test`, `/demo` + alias `/`.

### Tabela de ambientes

**Arquitetura FINAL (confirmada pelo Pedro): UMA instância, porta 4450, os 3
bancos rodam SIMULTÂNEOS.** Não são 3 instâncias/processos/portas — é um só
`docker-compose.yml` que sobe a app na `4450` e semeia `app_db` + `app_test_db`
+ `app_demo_db` no mesmo Mongo. A landing (`/`) oferece os 3 botões; o `.env`
(`NODE_ENV`) controla `production`/`staging` (testes), mas a demo é sempre
acessível pela landing, independente do modo. O usuário demo (`demo1`) é criado
**só** em `app_demo_db` (ver `carregarDemo({ skipAutoUser })`).

| | Produção | Teste | Demo |
|---|---|---|---|
| Host port | `4450` (instância única) | `4450` | `4450` |
| Prefixo | `/app` | `/test` | `/demo` |
| Banco | `app_db` (volume) | `app_test_db` (volume) | `app_demo_db` (volume) |
| `NODE_ENV` | `production` | `staging` | `demo` |
| Landing | botão "Entrar" → `/app/login` | botão "Entrar no teste" → `/test/login` | botão "Demo" → `/demo/start` (autologa) |
| População | **só o admin** | admin + usuários demo | banco completo + autologa |
| Rate limit | ativo | `RATE_LIMIT_DISABLED=true` | `RATE_LIMIT_DISABLED=true` |

**NÃO volte a 3 instâncias/3 portas** salvo o Pedro pedir explicitamente de
novo — esta foi a correção dele após eu ter implementado 3 composes separados
(4450 teste / 4451 produção / 4452 demo) que ele rejeitou ("uma porta só agora,
o .env controla qual banco usar; demo só via landing"). Se ele pedir 3
instâncias, a abordagem está em `references/ambiente-demo-publico.md`, mas o
padrão atual do template é 1 instância.

### Demo sem login (acesso livre, "admin de brinquedo")

Pedro quer que, **no modo demo, o usuário acesse TUDO sem precisar de login** —
qualquer modificação fica só no `app_demo_db` (isolado). Implemente em dois
lugares: (a) `pageAuth` (páginas) e (b) `auth` (API) aceitam usuário anônimo
quando `req.mode === 'demo'`, resolvendo-o como o usuário `demo1` do banco demo
`req.models.User.findOne({ email: 'demo1@example.com' })`. Assim `/demo/board`,
`/demo/calendario` etc. abrem sem clicar em nada, e o `fetch` da API
`/api/demo/tasks` funciona sem token (o csrfGuard aprova pelo Origin, ver
pitfall 78). O `demo1` já existe no banco demo (criado por `carregarDemo`), então
não crie outro — só resolva o existente. Verificação ad-hoc:
`curl -o /dev/null -w '%{http_code}' /demo/board` → 200 sem cookie; e
`/api/demo/tasks` retorna as tasks sem token. Isso é o que o Pedro chamou de
"demo é meio que um admin sem poder admin de fato, mas consegue acessar todas as
páginas sem precisar de login".

### Domínio de exemplo entregue (task manager "como Asana/Trello/Todoist")

A landing/página de exemplo desta base virou um **task manager** (Pedro pediu
"um todolist mais detalhado, mistura de Trello com Asana Todoist e Notion, mas
implementado de maneira tranquila e fácil do usuário utilizar sozinho"). O
domínio real tem estas entidades (além de `Project`/`CatalogItem`):

- **Task** (`models/task.model.js`): `titulo`, `descricao`, `status`
  (`planejado`/`em_andamento`/`pausado`/`concluido`), `projetoId` (ref Project),
  `profissionalId` (ref Professional), `tags[]`, `prazo`, `ownerId`. É o
  "cartão" do quadro (kanban). Service: `services/taskService.js`; rotas
  `/api/<modo>/tasks` (list/create/PATCH/DELETE).
- **Professional** (`models/professional.model.js`): `nome`, `funcao`,
  `contato`, `ownerId`. É uma PESSOA do quadro (NÃO é conta de login — o
  registro de usuários continua só via admin, por design). Service
  `professionalService.js`; rotas `/api/<modo>/professionals`.
- **Meta** (`models/meta.model.js`): `ownerId`, `metaSemana` (meta semanal de
  tarefas), `focoMinutos`, `pomodoros`. Painel de controle. Rotas
  `/api/<modo>/meta` (GET/PATCH) e `/api/<modo>/meta/foco` (POST, registra um
  pomodoro de 25 min).
- **Quadro (board)**: `views/board.ejs` renderiza Tasks em 4 colunas por status;
  criação via formulário completo (título/descrição/projeto/responsável/tags);
  mover = PATCH `status`; excluir = DELETE. O demo cai direto aqui (`/` sob
  `/demo`).
- **Painel de controle** (`views/painel.ejs`): stat cards (total/concluídas/
  foco/pomodoros), gráficos de barras SVG (por status, por projeto), meta
  semanal (input persistido), e um **Pomodoro de 25 min** acoplado ao quadro
  (timer no `public/js/painel.js` que POSTa `/api/<modo>/meta/foco` ao concluir).
- **Páginas Projetos/Profissionais** (`/projetos`, `/profissionais`): listagem
  + formulário de cadastro (estilo Asana/Trello/Todoist).

Padrão de implementação copy-paste (model→Zod→service→controller→rotas→
`routes/index.js`→view→`public/js/*.js`): segue as camadas do template. O
`demoBypass` (abaixo) é o que libera o usuário demo a ver/editar TUDO do banco
demo. Ao ampliar, respeite o CSP (JS em arquivo, sem inline) e os tokens do
DESIGN.md.

### `demoBypass`: usuário demo mexe em tudo (menos usuários)

O demo user é `role:'user'` (para NÃO poder editar usuários — `/admin` fica
bloqueado). Para que ele CRUDe qualquer Task/Project/Professional do banco demo
(mesmo as que pertencem a outros donos seedados), o `selectDb` seta
`req.demoBypass = true` quando `mode === 'demo'`, e os services de domínio
(`taskService`, `projectService`, `professionalService`) recebem `demoBypass` e
pulam o filtro `ownerId` quando true. Usuários continuam protegidos porque o
service de usuários NÃO recebe `demoBypass`. **CUIDADO:** o endpoint de reload da
demo (`/api/demo/demo/load?force`) costuma ter `requireAdmin` — o demo user é
`user`, então dá 403 "Acesso negado para este papel". Se o reload só mexe no
banco demo, PERMITA-o para a instância demo (honre `demoBypass` ou `if (req.mode
=== 'demo') next();`), senão o usuário não consegue repovoar a demo.

### Autologa de demo (landing → `/demo/start`)

A landing (`/`) tem três botões; o de Demo aponta para **`/demo/start`** (rota
dedicada), que popula o banco demo, cria/loga `demo1@example.com` e redireciona
para `/demo/` (dashboard). **Não ponha a autologa em `GET /demo`**: ela engole
o dashboard (mesma rota interna `/`) — ver pitfall 55.

### Senha do admin (correção de login)

`resolverSenhaAdmin()` prioriza: (1) `ADMIN_PASSWORD` (env, lido em **runtime**,
não o `env` cacheado); (2) `SEED_PASSWORD_FILE`; (3) **default
`~/Documentos/comum/senhas-projetos.md`** quando `SEED_PASSWORD_FILE` não está
definido. Esse default é o que faz o `npm run dev` (sem a env) logar com
`AdminComum123!!` — sem ele, o seed gerava senha aleatória e o login falhava.
O arquivo é **local, não versionado**, comum a todos os projetos derivados.
Fallback final: senha aleatória impressa uma vez no boot.
`tests/seed.test.js` usa **fixture temporário** em `os.tmpdir()` (nunca aponta
para `~/Documentos/...` direto, senão quebra no CI).

Padrão completo de seed de demonstração (domínios `Project`/`CatalogItem`,
idempotência, bloqueio em produção, `mustChangePassword` travando render):
`references/demo-seed-pattern.md`.

Implementação copy-paste (uma app, 3 connections): `references/tres-bancos-connections.md`
(`db.js` com `useDb`, `registry.js`, `selectDb`, `signToken` com `mode`, montagem
por prefixo em `app.js`, `server.js` semeando os 3, e o helper de models lazy
para testes). A outra abordagem — 3 stacks/processos separados — está em
`references/ambiente-demo-publico.md`; escolha conforme os bancos são do mesmo
domínio (uma app) ou de domínios diferentes (stacks separadas).

### Pitfalls de múltiplos bancos / tests

- **55. Models exportam SCHEMA, não model global — e `getModeConn` não pode ser
  chamado antes de `connectDb`.** Com N bancos, `require('../models/user.model')`
  devolve o schema; o model vem de `getModels(getModeConn('production')).User`.
  Mas `getModeConn` lança `'Banco não conectado'` se chamado antes do
  `setupDb()`. Nos testes, **não** faça `const models = getModels(getModeConn('production'))`
  no topo do arquivo (o require roda antes do `beforeAll(setupDb)`). Use um
  helper `tests/helpers/models.js` que expõe `get prod()` / `get test()` como
  **getters lazy** (resolvem só na hora do uso, já conectado), e nos testes
  atribua `let User; beforeAll(async () => { User = models.prod; });` — nunca
  `const User = models.prod.User` no topo.
- **56. Autologa de demo precisa de rota dedicada (`/demo/start`), não `GET /`.
  Um `router.get('/')` de autologa montado em `/demo` captura `/demo/` e
  **engole o dashboard** (que também é `GET /` em pageRoutes sob `/demo`).
  Resultado: o dashboard de demo fica inalcançável e qualquer acesso a `/demo/`
  redireciona em loop. Ponha a autologa em `/demo/start` e o dashboard em `/demo/`
  (pageRoutes). Mesma classe de erro do pitfall 53 (middleware que captura a
  raiz): a landing é sempre exceção.
- **57. `router.use(auth)` global num sub-router causa colisão de prefixo com os modos.** `demo.routes` era montado como `router.use('/demo', demo.routes)` DENTRO de `apiRoutes`, e `apiRoutes` é montado em `/api/demo`. Como `demo.routes` tinha `router.use(auth)` (global), a rota `POST /api/demo/auth/login` era "roubada" pelo prefixo `/demo` — o `demo.routes` casava `/demo/auth/login` ANTES de `auth.routes` e exigia token, retornando 401 em vez de fazer login. **Sintoma cruel:** o login em produção/teste funciona (200) mas o banco demo dá 401 "Autenticacao necessaria" — parece bug de credencial, não é. Correção: nunca `router.use(auth)` global num router que pode ser montado sob um prefixo que colida com rotas irmãs; aplique `auth`+`requireRole` **só na rota específica** (`router.post('/load', auth, requireRole('admin'), ...)`). Regra geral para multi-banco: um sub-router montado em `router.use('/<modo>', x.routes)` NÃO deve ter middleware global que intercepte prefixos — só nas rotas exatas. Diagnóstico rápido quando um prefixo de modo "some": logar no `auth.js` (`console.error('DIAG AUTH', req.originalUrl, new Error().stack)`) revela de onde o middleware está sendo aplicado.
  - **Páginas de login precisam de `action` por modo.** Com prefixos `/app`/`/test`/`/demo`, um `form action="/api/auth/login"` hardcoded faz `/test/login` e `/demo/login` caírem sempre em produção. Passe `action: '/api/${modo}/auth/login'` da rota de página (calculado via `req.baseUrl`) e leia `form.getAttribute('action')` no JS — não hardcode a URL no `apiRequest`.
- **58. Seed idempotente na senha para bancos já semeados.** `seedAdminIfEmpty` só cria se não houver admin; num banco semeado ANTES da correção (ex.: com senha aleatória), ele NÃO recria e a senha do arquivo não cola. Torne o seed idempotente: ao achar admin existente, compare o hash atual com a senha da origem (`ADMIN_PASSWORD`/`SEED_PASSWORD_FILE`) via `verifyPassword` e re-sincronize o hash se não bater. Assim a senha do arquivo sempre funciona sem dropar o volume. **Cuidado:** `findOne` do admin precisa de `.select('+passwordHash')`, senão `verifyPassword` recebe `undefined` e explode com `Illegal arguments: string, undefined` (parente do pitfall 2). Add `verifyPassword(plain, hash)` no `authService`.

 - **71. Usuário de demo (`demo1`) existe SÓ no banco demo — nunca vaze para
 produção/teste.** O `/demo/start` autologa `demo1@example.com`, que é criado
 por `carregarDemo`. Se `carregarDemo` rodar também no banco de teste, o
 `demo1` aparece em dois bancos e quebra o isolamento que o Pedro exige
 ("nao existe em outro banco"). `carregarDemo` recebe `skipAutoUser` (quando
 true, pula o `demo1` e cria a partir de `demo2`); passe `skipAutoUser:true`
 para o banco de teste no `server.js`. O banco demo recebe `carregarDemo` sem
 `skipAutoUser`. Verificação no ad-hoc: `demo1` encontrado em `app_demo_db` e
 AUSENTE em `app_db`/`app_test_db`.
 - **72. Landing NÃO é vitrine de banco — mantenha o padrão PROFISSIONAL.** Com a
  arquitetura de 1 instância (pitfall 66), a landing `/` é ÚNICA — mas ela é a
  landing **empresarial portada** (`references/ui-landing-and-footer.md`): hero
  com eyebrow + h1 + lead + CTA e uma seção de features, NUNCA um grid "escolha
  seu banco" com os 3 modos. Eu implementei exatamente esse grid de 3 botões
  (Produção/Teste/Demo com storytelling por modo) e o Pedro rejeitou — *"Esse
  não é o padrão de landing que eu havia exigido... não tem nada haver isso de 3
  bancos, deixe no profissionalismo que já havia"*. Lição: a landing profissional
  já existe e é o padrão; não a substitua por uma "vitrine de arquitetura". Se
  houver entrada de demo, é UM link discreto ("Demo" → `/demo/start`), não 3
  colunas de database. O produto real é o domínio (ex.: task manager), não o
  seeding de banco. Não crie `landingContent.js` com `landingFor(mode, lang)` —
  isso foi o artefato da abordagem rejeitada; remova-o se aparecer.
 - **76. "Popule o sistema como X" = construa o domínio SIMPLES, não reformule a
  UI.** Quando o Pedro pede "popule o sistema como um task manager com calendário
  e view em board (bastante simples)", a entrega é: um model de domínio seguindo
  as camadas (model→schema→service→controller→routes→test), DUAS telas (board +
  calendário) e um seeder idempotente — NADA de drag-and-drop, animação, ou
  redesenho do shell. Board = colunas por status com botões "←/→" que dão PATCH
  no status (sem mover via mouse); Calendário = grade mensal (7 colunas, célula
  por dia) com os chips de tarefa cujo `dueDate` cai no dia. Move é PATCH
  `{status}`, delete é DELETE — ambos via `fetch` com `credentials:'same-origin'`
  (o csrfGuard é por Origin/Referer, então mesmo-origin passa sem token; ver
  `references/i18n-e-tema.md`). Tudo em `public/js/*.js` (CSP proíbe inline), sem
  emoji (usa `✕` U+2715 ou SVG). Mantenha tokens do `DESIGN.md`; não invente
  padrão copy-paste de board/calendar simples:
  `references/task-manager-simples.md`.

- **77. Nav de página autenticada precisa prefixar o MODO do banco.** As
  páginas são montadas em `/` (production), `/app` (production), `/test`,
  `/demo` — cada uma com `selectDb(mode)` diferente. O `pageAuth` resolve o
  usuário com `req.mode`, então um token de **demo** é válido SÓ para rotas
  sob `/demo/*`. Se o header apontar para `/board` (absoluto, sem prefixo),
  ele cai em `/board` montado em `/` → banco `app` (production) → o token demo
  não bate → `pageAuth` redireciona para `/login` (a página parece quebrada:
  clica em "Quadro" e volta pro login). Correção: o `pageAuth` expõe
  `res.locals.modo`, e o header calcula o prefixo
  `var mp = (modo && modo !== 'production') ? '/' + modo : '';` e usa
  `href="<%= mp %>/board"`, `href="<%= mp %>/perfil"`, `href="<%= mp %>/admin"`.
  Assim na demo os links viram `/demo/board`, `/demo/perfil`; em produção
  ficam `/board`, `/perfil` (mp vazio). Lembre-se disso sempre que adicionar
  um link de navegação entre páginas autenticadas numa base multi-banco: o
  link TEM de carregar o prefixo do modo atual, não ser absoluto.
- **78. Script de verificação ad-hoc que faz POST/PATCH/DELETE leva 403 do
  csrfGuard sem o header `Origin`.** O `csrfGuard` (Origin/Referer) bloqueia
  mutação autenticada por cookie cuja `Origin` não bate com o host — e se não
  houver `Origin` nenhum, responde 403 "origem ausente". O navegador e o
  `fetch` do app enviam `Origin` automaticamente, então no uso real funciona;
  mas um script Node `http.request` puro NÃO envia `Origin`, então um
  `POST /api/demo/tasks` seu recebe 403 e parece bug do app. Ao escrever um
  `hermes-verify-*.js` que exercita mutações, inclua
  `headers: { Origin: \`http://${HOST}:${PORT}\` }` (ou `Referer`) na requisição
  — aí o csrfGuard aprova e você mede o status real (201/200). Sem isso, o
  `ok:false` do script é falso negativo. Complementa o pitfall 31 (scripts em
  `app/`) e o 75 (verificação pós-rebuild): o 403 por falta de Origin é a
  causa mais comum de "criar task deu 403" em probe manual. **Force-reseed da
  demo:** para aplicar novos defaults de `carregarDemo` (ex.: mais tarefas),
  `POST /api/demo/load?force=true` falha em shell puro (JSON no `node -e` se
  corrompe e finge 401; e o cookie do `/demo/start` precisa de `Origin`/`Bearer`).
  O caminho confiável é pelo **browser autenticado**: `browser_navigate('/demo/start')`
  e depois `browser_console` com `fetch('/api/demo/load?force=true', {method:'POST',
  headers:{'Content-Type':'application/json'}, body: JSON.stringify({force:true})})`
  — o browser envia cookie + Origin e o csrfGuard aprova (ver pitfall 99).

- **97. Drag-and-drop de cartões no kanban exige `draggable="true"` NO elemento.** HTML5 DnD só dispara `dragstart` em elementos com `draggable` setado. Cartões criados via JS (ex.: `cardEl()`) ganham o atributo, mas os cartões **renderizados no servidor (EJS SSR)** NÃO — então arrastar os cartões iniciais simplesmente não funcionava (silencioso, sem erro no console). Correção: após montar o quadro, `document.querySelectorAll('.tcard').forEach(c => c.setAttribute('draggable','true'))`. Ao implementar DnD entre colunas: (a) marcar `draggable` em SSR E JS; (b) `dragstart` guarda o `id` em `dataTransfer` + variável de módulo; (c) `dragover` faz `preventDefault` e marca a coluna alvo (`.drag-over` com `outline`); (d) `drop` faz PATCH no status e reanexa o card via `coluna(novo).insertBefore(card, coluna(novo).firstChild)`, recontando com `contador()`/`vazio()`; (e) ignore `dragstart`/clique vindo de botões internos.

- **98. `browser_navigate` para URL crua derruba a sessão demo; e o snapshot pós-clique antecede o fetch assíncrono.** (a) O autologin `/demo/start` seta cookie `token`, mas `browser_navigate('http://host/demo/projetos')` (URL direta) perde a sessão e recai em `/login` — só navegações INTERNAS (clicar no link da navbar, que mantém o cookie do browser) preservam. Fluxo: `browser_navigate('/demo/start')` → snapshot → `browser_click` no ref do link "Projetos" → snapshot. (b) Ao clicar num botão que abre modal via `await apiRequest(...)`, o `browser_snapshot` logo após `browser_click` quase sempre é capturado ANTES do `await` concluir → o modal ainda está `hidden` e parece que "não abriu". Não conclua bug por isso: dispare `.click()` via `browser_console` e leia `el.hidden` depois de `setTimeout(…, 200)`, ou use `browser_console` para checar o estado pós-fetch.

- **99. Force-reseed da demo para aplicar novos defaults de `carregarDemo` NÃO é automático.** `carregarDemo` early-returns se o banco já tem dados (pitfall 86), então mudar os defaults (ex.: `tarefas: 760`) não surte efeito enquanto houver dados. Para repovoar: `POST /api/demo/load?force=true` com `demoBypass`. Pela linha de comando pura isso dá 401/403 (csrfGuard exige `Origin`; e o cookie do `/demo/start` precisa ser enviado como `Bearer` ou com `Origin` correto — um `node -e` com JSON no body costuma corromper o corpo pelo shell e finge 401). O caminho confiável é pelo **browser autenticado**: `browser_navigate('/demo/start')` e depois `browser_console` com `fetch('/api/demo/load?force=true', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({force:true})})` — o browser envia cookie + Origin automaticamente e o csrfGuard aprova. Confirme o novo volume depois (`/api/demo/tasks?limit=1` → `total`).
  PORTFÓLIO/QUARTZ dele, NÃO o sober do DESIGN.md do template.** Quando ele diz
  "não está igual ao padrão exigido", "css horrível", "refatoração gigante de
  DESIGN", o padrão de referência é `~/portfolio` (GitHub Pages, astronomia/
  glassmorphism) e `phrandrance.com` (Quartz) — descritos no perfil dele como
  "developer-grade aesthetic (astronomia/espaço, glassmorphism, animações
  suaves, canvas bg com mouse repulsion, blur veil mas conteúdo opaco, multilíngue
  PT/EN/ES/FR com seletor de bandeiras)". Eu errei ao seguir o DESIGN.md antigo
  (que mandava "landing sempre clara, sem animação, sem framework CSS") e ele
  rejeitou **duas vezes**. Lição: ao tocar em visual, estude
  `~/portfolio/assets/css/style.css` + `index.html` + `main.js` e replique AQUELE
  padrão (deep space + glass + seletor de bandeiras SVG + canvas com repulsão do
  mouse). Detalhe e snippet prontos: `references/tema-space-glass.md`.

- **80. Ao mudar o tema visual, atualize o DESIGN.md e o AGENTS.md para refletir
  a ESCOLHA.** O AGENTS.md exige "siga o DESIGN.md"; se você adota Bootstrap ou
  tema space/glass que contraria o DESIGN.md vigente, o repo fica em contradição
  interna e a próxima sessão (ou outro agente) "corrige" de volta para o errado.
  Sempre patch o DESIGN.md (Overview, cores, tipografia, regras de animação) e o
  AGENTS.md (stack, regra de CSS) para descrever o tema que você de fato
  entregou. Nesta base: o DESIGN.md antigo proibia framework CSS e animação; foi
  reescrito para "Bootstrap 5 empacotado local + tema deep space/glassmorphism".
  Faça o mesmo sempre que o padrão visual mudar.

- **81. "Volte ao original" = reverta o MAIN e REBUILDE a imagem do zero — não só o working tree.** Quando o Pedro rejeita um tema e manda "volte ao que era originalmente", `git reset --hard <commit-original>` limpa o diretório, MAS o container continua servindo os arquivos velhos porque a imagem Docker `:latest` (construída antes do reset) persiste e `docker compose up -d` SEM `--build` a reusa. Mesmo `up -d --build --no-cache` pode não limpar se a imagem `:latest` já existir. Procedimento correto de reversão: (1) `git reset --hard <original>`; (2) `docker compose down`; (3) `docker image rm -f <proj>-app:latest`; (4) `docker compose build --no-cache`; (5) `docker compose up -d`; (6) **verifique DENTRO do container** (`docker exec <container> ls /app/public/css/theme-space.css`) que os arquivos sumiram — o `ls` no HOST pode estar limpo mas a imagem ainda os ter. Só declare "revertido" após `curl` nos assets retornar 404 (`/css/theme-space.css` → 404, `/vendor/bootstrap/bootstrap.min.css` → 404) e a landing não conter mais `starfield`/`hero__title`/`lang-btn`.

- **82. Não force push de reversão sem ordem expressa.** Ao reverter o `main` local, o `origin/main` remoto ainda tem os commits mergeados (histórico divergente). Corrigir o remoto exige `git push --force`, irreversível. NÃO force push por conta própria — deixe o local/container limpos e pergunte (clarify) como tratar o remoto: force push, PR de reversão (desfaz sem reescrever), ou ignorar. Se o usuário não responder no tempo, mantenha o local restaurado e não destrua o remoto.

- **83. Tema imposto sem alinhamento vira retrabalho duplo.** Nesta sessão apliquei Bootstrap e depois tema space/glass sem o Pedro pedir aquele visual explicitamente — ele rejeitou ambos ("css horrível", "não está igual ao padrão exigido", "volte ao original"). Regra (pitfall 79): estude `~/portfolio`; regra complementar: **antes de impor qualquer tema visual novo, mostre screenshot da landing e espere aprovação**, não entregue e espere reprovação. Se ele já mandou "volte ao original", a ação é a do pitfall 81, não "consertar o tema".

- **73. `seedBanco` não referencia `opts.skipAutoUser` como variável solta.** No
 `server.js`, `seedBanco(mode, { populaDemo, demo })` recebe `skipAutoUser` no
 objeto; se você escrever `carregarDemo({ ..., skipAutoUser }, models)` (sem ler
 de `opts`), dá `ReferenceError: skipAutoUser is not defined` e o container
 **crasha no boot** ao semear o banco de teste (o log mostra `at seedBanco
 (.../server.js:15:63)`). Correção: `async function seedBanco(mode, { populaDemo
 = false, demo = false, skipAutoUser = false } = {})` e passar `skipAutoUser` como
 venha do objeto de opções — sempre leia de `opts`. O mesmo vale para qualquer flag que
 venha do objeto de opções — sempre leia de `opts`.

 - **84. Landing NUNCA menciona "3 ambientes/bancos".** O Pedro disse
 literalmente *"não pode falar que tem 3 ambientes diferentes. Na landing page
 deve ser somente sobre pra que serve o sistema, e com a versão demo
 disponível para acessar e testar"*. Então: retire a SEÇÃO de "Produção/Teste/
 Demo" (grid de bancos, "três espaços isolados") da landing. A landing traz
 SÓ: (1) o propósito do produto (o que o sistema faz), (2) um CTA de demo
 (`/demo/start`). Mantenha a segurança (JWT/CSRF) como diferencial técnico, mas
 sem enumerar bancos. Isso é MAIS forte que o pitfall 72 (que só dizia "não
 coloque 3 colunas de database") — aqui nem citar "3 ambientes" pode. O mock da
 hero também não deve mostrar "Produção/Teste/Demo"; use rótulos do produto
 ("A fazer/Andamento/Concluído").
 - **85. EJS: variável de loop NÃO pode se chamar `t`.** Views que recebem `t`
 (função de i18n: `<%= t('nav.panel') %>`) quebram se o loop fizer
 `col.items.forEach(function(t){ ... })` — o `t` do loop someia o `t` global
 dentro do corpo e dá "t is not a function" ao chamar `t('board.remove')`. O
 erro só aparece AO RENDERIZAR (não no lint) e só na view que tem itens. Nomeie
 `task`/`item`/`p`. Verifique com `ejs.render` standalone passando 1 item.

- **87. Rebuild `--no-cache` + `up -d --force-recreate` AINDA serve arquivo velho quando o patch veio DEPOIS do build anterior.** Nesta sessão editamos `board.js` (adicionando `renderizarCards`) e `i18n.js` (bloco `proj.*` PT) e rebuildamos — mas o container continuou servindo a versão pré-patch (board sem `renderizarCards`; i18n com `proj.list` cru apesar de estar no disco). Causa: o image `:latest` foi construído antes de UM dos patches e o `up --force-recreate` reusou a tag existente. **Sintoma:** lint/Node local OK, mas o browser mostra o comportamento velho. **Correção:** após qualquer patch de arquivo estático/JS, rode um rebuild e CONFIRME o conteúdo servido (`curl -s host/js/board.js | grep renderizarCards`; `grep proj.list` no HTML renderizado), não só o status 200. Se vier o velho, rebuild novamente (segundo build pega). Regra geral: a verificação de "foi pro ar" é ler os BYTES servidos, não o exit code do build.

- **88. Diagnóstico de chave i18n crua: teste o dicionário direto, não o HTML.** Quando a view mostra `proj.list`/`pro.*` como texto, não adianta grep no `.ejs` (lá está `t('proj.list')`, certo). O bug é a CHAVE AUSENTE no dicionário de um idioma. Confirme em Node: `node -e "const {translate}=require('./src/config/i18n'); console.log(translate('pt','proj.list'))"` — se voltar `'proj.list'` (a própria chave), o bloco daquele idioma não a define (nesta sessão o PT faltava inteiro o bloco `proj.*`). Corrija adicionando a chave no idioma que falta; depois rebuild (pitfall 87) e confira o HTML servido.

- **89. `data-*="<%= p._id %>"` com variável errada = 500 no render.** Ao colocar `data-id` num span do card, escrevi `<%= p._id %>` onde a variável achada era `pr`/`pf` → "p is not defined" estoura ao renderizar a view (500, não lint). Parente do pitfall 19/85: toda `<%= var %>` em view é runtime. Ao editar spans populados por `find`, use o nome exato da variável (`pr._id`, `pf._id`). Verifique compilando a view: `node -e "require('ejs').render(fs.readFileSync('views/board.ejs','utf8'), {projetos:[],profissionais:[],colunas:[],apiBase:'/api/demo',t:()=>''})"`.

- **90. SVG `fill="var(--brand)"` em ATRIBUTO de apresentação NÃO resolve** (só em CSS) → barra preta. O `drawBars` do painel usava `<rect fill="var(--brand)">` e o gráfico virava um bloco preto. Correção: colorir via CSS (`.bars svg .bar { fill: var(--brand); }`) ou literal. Além disso, com `viewBox="0 0 100 100"` + `preserveAspectRatio="none"`, `x="6%" width="88%"` faz as barras se SOBREPÔREM num único retângulo. Use coordenadas em user-space (`slot=100/entries`, `x=i*slot+(slot-bw)/2`, `width=bw`) e rótulos em HTML abaixo do SVG (evita distorção de texto com `preserveAspectRatio="none"`).

- **91. Modal de detalhe: NÃO reconstrua a entidade do DOM — busque do banco.** O clique no cartão montava o objeto lendo `card.querySelector('.tcard-proj').dataset.id`, mas o span não tinha `data-id` → o modal abria sempre "Sem projeto"/"Sem responsável" mesmo quando a tarefa tinha no banco. Padrão correto: ao clicar, `GET /<modo>/tasks/:id` e `openModal(data.task)` — os selects de projeto/responsável vêm dos IDs reais do MongoDB. (E o card no SSR deve carregar `data-id` nos spans de projeto/responsável para consistência.) Isso atende ao requisito do Pedro "população correta e nada hardcoded, tudo via banco". Também: o `cardEl` de tarefas novas deve ler o nome do `<select>` do formulário quando o backend não devolve `projetoNome`/`profissionalNome`.

- **92. Tema na landing: `data-theme="<%= ... %>"` vira `&#34;light&#34;` no HTML (EJS escapa as aspas).** Assertar `includes('data-theme="light"')` num script de verificação FALHA, mas o navegador decodifica e o atributo funciona. Ao testar via curl, aceite tanto `data-theme="light"` quanto `data-theme=&#34;light&#34;`; ou teste o valor decodificado. Armadilha de verificação, não bug — confirme com `curl | grep -o '<html[^>]*>'` e leia o atributo cru. (Mesma família do pitfall 19: suspeite do check antes do código.)

- **93. "Tudo via banco, nada hardcoded" vale para exibição de entidades.** Quando o Pedro pede ajuste fino em Profissionais/Tarefas, o dado exibido (nome, função, contato, projeto, responsável) DEVE vir do `professionalService`/`taskService`/`projectService` — não de string fixa no JS. O `profissionais.js` tinha texto PT fixo ("Nenhum profissional ainda.") e mostrava só `nome`; corrija para renderizar `funcao` (pill) e `contato` do banco. A lista de profissionais vem de `GET /professionals` (já escopado por `demoBypass` no modo demo) — nunca repopule manualmente no front.
 - **86. Seed idempotente por ENTIDADE: entidade nova não aparece se o banco já
 existia.** `carregarDemo` early-returns quando `Project`/`CatalogItem` já
 existem — então se você ADICIONAR um novo model (ex.: Task, Professional)
 DEPOIS que o banco foi semeado, ele nunca é criado e o board fica com 0
 tarefas. Correção: mude a guarda para checar CADA entidade
 (`precisaTarefas = Task.countDocuments()===0`, etc.) e criar só as faltantes;
 ou expõha um reload `force` acessível ao usuário demo (ver `demoBypass`). Após
 adicionar entidade, force-reseed (`POST /api/demo/demo/load {"force":true}`)
 e confirme no board.
- **74. O healthcheck fica `unhealthy` se checar `mongoose.connection`.** O app
 usa `mongoose.createConnection` (não `mongoose.connect`), então a connection
 PADRÃO do mongoose NUNCA conecta e `readyState` fica 0 → `/api/health/ready`
 responde 503 e o container marca `unhealthy` mesmo com o banco no ar e a app
 funcionando. O `health.routes.js` deve usar `getMainConn()` (exportado por
 `db.js`) e checar `conn.readyState === 1`. Sem isso, o auto-login e tudo mais
 funcionam, mas o Docker sempre reporta unhealthy — ruído que esconde falhas
 reais. Sintoma de diagnóstico: `curl /api/health/ready` → 503 mas `curl /` → 200.
- **75. Rebuild sem `COMPOSE_PROJECT_NAME` cria um SEGUNDO projeto docker.** Se o
 compose antigo foi subido com `COMPOSE_PROJECT_NAME=pp` (ou nome do diretório
 diferente) e você roda `docker compose up -d --build` de novo após renomear o
 compose, o Docker cria `projeto-profissional-app-1` (nome do diretório) ao lado
 do `pp-app-1` antigo — o container velho (porta errada) **nunca é recriado** e
 parece que "nada mudou". Sempre: (a) liste `docker compose ls` para ver todos
 os projetos apontando pro mesmo diretório; (b) remova os containers órfãos
 (`docker rm -f pp-app-1 pp-mongo-1`) antes/depois do rebuild; (c) se quiser nome
 estável, defina `COMPOSE_PROJECT_NAME=pp` no `.env`. Verificação pós-rebuild:
 `docker ps` deve mostrar UM container na porta 4450 e nenhum na 4447.

- **66. Arquitetura de múltiplos bancos: PREFERIR 1 instância única, NÃO 3
  instâncias.** O padrão do template é **uma** app na porta `4450` que semeia os
  3 bancos (`app_db`/`app_test_db`/`app_demo_db`) no mesmo Mongo e os expõe por
  prefixo de rota (`/app`,`/test`,`/demo`). O `.env` (`NODE_ENV`) controla
  `production`/`staging`; a demo é sempre acessível pela landing, independente do
  modo. **Regressão desta base (corrigida):** eu implementei 3 composes/3 portas
  (4450 teste / 4451 produção / 4452 demo) e o Pedro rejeitou — *"uma porta só
  agora, o .env controla qual banco usar (producao ou teste); demo so via
  landing (rotas demo/*) que roda simultaneo"*. Voltei para 1 instância e
  removi os composes extras. **Lição:** ao tocar em "3 bancos", mantenha 1
  instância + prefixos; só faça 3 processos se ele pedir explícita e repetidamente.
  Verificação ad-hoc de múltiplos modos: um `NODE_ENV` por processo (pitfall 68),
  e para exercitar produção+teste+demo num script, spawn de processo filho por
  modo ou getters por request (pitfall 36/52).
- **67. `config/env.js` faz `dotenv.config()` e lê `NODE_ENV`/`JWT_SECRET` no
  require — setar a env DEPOIS de `require('./src/app')` não adianta.** Se o
  probe carrega a app e só depois define `process.env.JWT_SECRET`, em
  `NODE_ENV=production` o `requiredInProd` dispara "Variavel obrigatoria ausente:
  JWT_SECRET" e o processo morre no boot (parece crash de módulo, não é). Sempre
  defina `process.env.*` ANTES dos requires, ou rode o processo filho já com a
  env no shell (`NODE_ENV=demo node script.js`). Complementa o pitfall 11.
- **68. Verificação ad-hoc de múltiplos modos: um NODE_ENV por processo.** Não
  dê `require('./src/config/env')` em cache entre modos dentro do mesmo processo
  — `env.nodeEnv` fica travado no primeiro valor. Para exercitar produção+teste
  +demo num único script, ou (a) spawna um processo filho por modo com a env no
  shell, ou (b) faz o `env.js` expor getters por request (ver pitfall 36/52).
  O `hermes-verify-*.js` que rodou os 3 modos no mesmo processo deu falso
  "produção" para demo/teste por causa desse cache.
- **69. View de erro (`error.ejs`) inclui o `header` que usa `t()` — garanta
  `res.locals.t` em todo caminho de erro.** O middleware `i18n` seta
  `res.locals.t`, mas um mini-app de teste (paginas.test.js) monta
  `notFoundHandler`/`errorHandler` SEM o `i18n`, e o render quebra com
  `t is not defined`. Correção dupla: (a) registre `errApp.use(i18n)` no mini-app
  de teste; (b) no `errorHandler`, passe `t: res.locals.t || ((k)=>k)` no
  `res.render` como fallback defensivo. Mesma classe de risco para qualquer
  partial que passe a usar `t()`.
- **70. Seletor de idioma + tema SEM JS inline (CSP).** Botão de tema:
  `id="theme-toggle"` com dois SVGs (sol/lua) e `aria-pressed`; o JS (em
  `/js/common.js`) lê cookie `theme`, aplica `data-theme` em `<html>` e persiste
  em cookie (sobrepõe `@media (prefers-color-scheme: dark)` via
  `:root[data-theme='dark'|'light']`). Seletor de idioma: `<select id="lang-switcher">`
  que, no change, faz redirect para `?lang=xx` (o middleware `i18n` grava cookie
  e define `res.locals.lang`/`t`). **Nunca** `onclick` inline nem
  `javascript:` — a CSP (`script-src 'self'`) bloqueia. Manter views sem
  emoji: usar SVG. Padrão completo de i18n (middleware + dicionário PT/EN/ES/FR
  + helper `t`) e tema: `references/i18n-e-tema.md`.

 ### Footer e formulários de login (UI)

 - **59. Rodapé "no meio da tela" com pouco conteúdo.** O `body` do template não
 tem `min-height` de viewport, então com uma landing curta o `.app-footer`
 flutua na metade da página. Correção: `body { display:flex;
 flex-direction:column; min-height:100vh; }` e o container de conteúdo com
 `flex:1 0 auto` (ex.: `.container { flex:1 0 auto; }`). Assim o `main`
 cresce e empurra o footer para o fim da viewport mesmo com pouco texto. Não
 use `position:fixed` no footer — ele cobre o conteúdo e some no scroll.
 - **60. Botão mostrar/ocultar senha no login.** Padrão esperado por Pedro:
 ícone SVG (nunca emoji), `aria-label`/`aria-pressed` para acessibilidade, e
 toggle de `input.type` entre `password` e `text` via listener em arquivo
 (CSP proíbe `onclick` inline). Estrutura: `div.input-affix > input +
 button.btn-affix` com `position:absolute; right` no botão e `padding-right`
 no input. O form de login precisa de `action` **por modo**
 (`/api/<modo>/auth/login`, ver pitfall 57) — leia
 `form.getAttribute('action')` no JS em vez de hardcodar `/api/auth/login`.
 CSS de apoio: `.input-affix { position:relative; display:flex;
 align-items:center; } .input-affix input { padding-right:2.75rem; }
 .btn-affix { position:absolute; right:.4rem; ... }`.

 ## Landing page & footer (Pedro's visual standard)

 The template's landing is the **enterprise pattern ported from
 `sistema-academico` and made generic**. When he asks for a "landing
 profissional" / "padrão empresarial", port that layout — do not invent one.
 Section order, CSS classes, the literal footer signature
 (`Pedro Henrique Rocha de Andrade` → `phrandrade.com`, "feito com café, código
 e um céu estrelado", `Voltar ao topo ↑` as a JS-free `#topo` anchor, applied to
 the logged-in area too), plus the style rules he enforces (SVG icons instead of
 emoji, one single card elevation, WCAG-safe greys):
 `references/ui-landing-and-footer.md`.

 **AVISO (correção dura):** quando ele diz "igual às outras landing pages" /
 "refatoração gigante de DESIGN" / "css horrível", o padrão de referência é o
 **tema deep space + glassmorphism dos outros sites dele** (`~/portfolio` e
 `phrandrance.com`), NÃO o DESIGN.md sóbrio do template. Replique aquele visual
 (canvas com starfield + galáxias + constelações + **repulsão do mouse**, glass
 panels, seletor de bandeiras SVG, gradiente azul/violeta). Manual completo e
 snippet de repulsão: `references/tema-space-glass.md`. E ao adotar esse tema,
 **atualize o DESIGN.md/AGENTS.md** para refleti-lo (pitfall 80).

A **área logada** (navbar, largura do layout, aba de tutorial) tem regras
próprias: `references/app-shell-e-navbar.md`. Quando ele disser "a navbar
precisa ser refatorada por completo", "o layout precisa se estender ao máximo"
ou "está super péssimo", comece por ali — o `.container` do template vem
travado em 1180px, e dropdown/menu mobile precisam ser `<details>` + checkbox
porque a CSP proíbe JS inline. Esse arquivo também traz a seção **"Revisão
visual assistida"**: quais críticas de um modelo de visão aceitar (ação
destrutiva em azul, `value="0"` em campo numérico) e quais descartar porque
medem o viewport e não o CSS (largura do container, grid `auto-fit` assimétrico).

**Tela vazia é o pior primeiro acesso.** Todo módulo com taxonomia própria
(categorias de despesa, tipos de conta) ganha um seeder idempotente
`semear(userId)` + rota `POST /api/<modulo>/categorias/padrao`, para a pessoa
começar com opções prontas em vez de inventar nomes inconsistentes. Idempotente
de verdade: rodar duas vezes não duplica nada.

## Each stack seeds its OWN admin

The two stacks have separate databases, so they have separate admin accounts —
the production password will never work on `:4446`, and that is not a bug.
Production generates a random password printed **once** at boot
(`docker compose -p pp logs app | grep -A3 'Conta admin criada'`); the test
stack pins predictable credentials on purpose because k6 needs them. Read each
stack's own boot log before reporting credentials, and remember `down -v`
destroys the volume, so the next boot seeds a brand-new password.

Two traps before you quote credentials to Pedro: (a) with `ADMIN_PASSWORD`
empty in `.env` the seed leaves no password you know, and it will **not**
recreate an account that already exists — use `templates/reset-senha.js`;
(b) `docker inspect` the running container first, because a stack left up with
the demo override (pitfall 23) keeps serving `*_demo` while the real DB sits
empty. Full recipe: `references/operacao-e-acesso.md`.

## Root markdown set (always include)

`README.md` · `AGENTS.md` · `CLAUDE.md` · `SECURITY.md` · `LICENSE` (MIT) ·
`CONTRIBUTING.md` · `CODE_OF_CONDUCT.md` · `CHANGELOG.md` · `DESIGN.md`, plus
`docs/architecture.md`, `docs/deployment.md`, `docs/testing.md`,
`docs/load-testing.md`, `.github/workflows/ci.yml`,
`.github/workflows/carga.yml`, `.editorconfig`, `.gitignore`, `.dockerignore`,
`.env.example`.

Content conventions and the AGENTS.md/CLAUDE.md split:
`references/root-markdown-set.md`.

`DESIGN.md` is the visual system as tokens (Google's open spec) plus the
exports `tailwind.theme.json` / `tokens.json`. Authoring rules, the
`orphaned-tokens` trap, measured WCAG contrast ratios and the contrast helper:
`references/design-system.md`.

## Publishing to GitHub as a template repository

Para **projeto derivado em repo privado** (CI + issues + PR + Project), que é o
pedido mais comum do Pedro, siga `references/github-delivery.md` — inclui o
escopo OAuth `project` que o `gh` não traz por padrão e o fluxo device-code.

This is the whole point of the base repo — a new project starts from
"Use this template", not from scratch.

```bash
gh repo create projeto-profissional --public --source=. --remote=origin \
  --description "..." --push
gh api -X PATCH repos/<user>/<repo> -f is_template=true   # habilita "Use this template"
gh api -X PUT  repos/<user>/<repo>/topics -f 'names[]=nodejs' -f 'names[]=template' ...
gh run list --limit 1     # confirme o CI VERDE no GitHub, nao so localmente
```

Publishing is irreversible, so audit the **whole history** first, not just
`HEAD`:

```bash
git log --all --name-only --pretty=format: | sort -u | grep -x '.env'   # deve ser vazio
git ls-files | grep -iE '\.env$|secret|\.pem$|\.key$'                   # deve ser vazio
gh api repos/<user>/<repo>/contents/.env                                # deve dar 404
```

Also scrub placeholder identity before it becomes public: the template's
`LICENSE` ships as `Copyright (c) <ano> Pedro`, which looks sloppy next to the
full-name footer signature — replace with `Pedro Henrique Rocha de Andrade`.

## Working style with Pedro

- Reply in Brazilian Portuguese, plain terminal text, no markdown formatting.
- Comments in code are in Portuguese and explain **why**, not what.
- User-facing strings in Portuguese; identifiers/DB fields in English.
- Write many small files rather than one giant tool call — large
  `write_file`/`execute_code` payloads stall the stream. Batch several small
  writes through `execute_code` when creating many similar files (views, JS).
- **Não declare "pronto" com a entrega parcial.** Nesta base um pedido típico
  ("crie o app") tem cauda longa: backend, UI, testes, subir o stack, publicar.
  Relatar "backend pronto, 49 testes verdes" quando o app nem abre de fora leva
  o Pedro a responder "ele não está rodando". Antes de resumir, cheque a lista
  literal do que ele pediu e diga explicitamente o que ainda falta — resumo que
  omite pendência custa um turno inteiro de retrabalho.
- **O pedido do Pedro vem como uma frase densa com N entregáveis.** "Rode em
  todas as interfaces nas portas X e Y, dockerizado, com script de zip do banco,
  publique no github com a CI, ISSUES, PR, crie um PROJECT associado, repo
  privado" são **oito** itens numa linha. Transforme a frase em checklist
  (`todo`) antes de começar e confira item por item antes de resumir; é fácil
  entregar sete e relatar como completo. Quando um item depender de ação dele
  (autorizar escopo OAuth, aprovar visual), diga isso de forma destacada em vez
  de deixá-lo descobrir no fim.
- **Peça de infraestrutura tem verificação própria.** "Rode em todas as
  interfaces" não é satisfeito editando `.env` — só depois de
  `docker compose up -d --build` e de um curl no IP externo. Editar arquivo de
  config e considerar feito é o erro mais fácil de cometer aqui.
- **Commit é entregável, não epílogo.** Numa sessão longa é fácil terminar com
  a suíte verde, o stack no ar e **nada commitado** — o trabalho existe só no
  disco. Quando o pedido tiver muitos itens, coloque "commit + push (branch/PR)"
  como item explícito do `todo` e feche-o antes de escrever o resumo final.
  Vale o mesmo para bug conhecido em aberto: se você mesmo encontrou um defeito
  e ainda não corrigiu, ele vai no topo do resumo como pendência, nunca diluído
  no meio do texto.
- **61. Credencial e URL vão no TOPO, isoladas — não no meio do relatório.** Ao
  entregar acesso, Pedro quer entrar; ele não vai garimpar a senha dentro de
  oito parágrafos sobre arquitetura. Ele respondeu literalmente *"tá mas vc não
  me deu a senha pra entrar ahahhaha"* depois de um resumo que **continha** a
  senha — enterrada. Abra a resposta com um bloco curto (URL, e-mail, senha, uma
  linha por ambiente), e só depois o restante. Vale para cada ambiente que
  existir; se são três stacks, são três linhas.
- **Teste o login antes de mandar a senha.** Passar credencial sem exercitar é
  como mandar o Pedro depurar por você — e o limiter de 3 tentativas/30min pode
  já estar armado pelos seus próprios testes. Faça o `POST /api/auth/login`,
  confirme 200, e se vier 429 reinicie o app (`docker compose -p <proj> restart
  app`) para zerar o contador em memória antes de entregar.
- **Quando o pedido dele contradiz o estado atual, faça backup e siga o que ele
  escreveu.** Ele pediu "4450 (produção), 4451 (teste)" quando a produção rodava
  em 4451 — inverter portas move dados reais. Aponte a contradição, use
  `clarify`, mas **não trave**: rode `./scripts/backup.sh` primeiro e siga a
  instrução literal se ele não responder. O pedido explícito ganha do estado
  herdado; o backup é o que torna isso seguro. Diga no relatório que inverteu e
  onde ficou o backup.
- **Rebuilde por padrão ao reiniciar o app.** Quando o Pedro manda "reinicie a
 aplicação", o procedimento é `docker compose up -d --build` (não só
 `docker restart` — ver pitfall 10: o container serve a imagem, não o arquivo
 editado). E antes de subir, valide que os containers órfãos de projeto antigo
 foram removidos (pitfall 75) e que a porta correta (4450) está ativa. Após o
 up, confirme com `curl` no IP externo (`:4450/`, `:4450/api/health/ready`,
 `:4450/demo/start` → 302 + Set-Cookie) antes de dizer "reiniciado".
- **Confirme QUAL sistema antes de reiniciar/rebuild amplo.** A máquina do Pedro
 roda vários projetos ao mesmo tempo (`pp`, `fa`, `sistema-academico`,
 `libretranslate`...). Quando ele manda "reinicie a aplicação", diga em voz alta
 qual container/composer você vai tocar (ex.: "`pp` = projeto-profissional na
 4450") ANTES de rodar o comando — ele reagiu com *"Vc esta mexendo em q sistema?"*
 quando eu comecei a rebuildar sem declarar o alvo, confundindo `pp` com
 `fa`. Liste `docker compose ls` e afirme o nome do projeto + porta; só então
 execute. Se a intenção dele for outro sistema, ele corrige antes do dano.

- Finish by actually running the tests and a boot smoke, then report real output.

## Verification discipline

Pedro approves visual work only after seeing it, and he notices invented
numbers. Non-negotiables:

- **Never publish a metric you did not measure.** Placeholder stats ("400+
  users", "<30ms") written into a landing page are fabrication once they ship.
  Measure first, then write the number; if a figure changes, propagate it
  everywhere (README, CLAUDE.md, CHANGELOG, docs, views) — a stale "15 testes"
  left in one file is the same defect, smaller.
- **When an ad-hoc check fails, suspect the check before the code.** Every
  verification failure in this template's history turned out to be a bad
  assertion (substring match, missing env var, `dotenv` override,
  `e.status` em vez de `e.statusCode`, valor esperado calculado errado à mão),
  not a real bug. Investigate, then fix whichever is actually wrong — e diga no
  relatório qual dos dois estava errado. Ao conferir agregado (custo total,
  km/l somado de vários veículos), refaça a conta à mão a partir das fixtures
  antes de acusar o código: um `consumoPorCombustivel` "errado" era a soma
  correta de carro + moto, e a expectativa é que estava torta.
- **Promote throwaway checks into the suite.** A `/tmp` script proves the code
  works today; only a test in `app/tests/` stops a regression tomorrow. Security
  guards especially belong in `tests/config.test.js`.
- **Prove a new test can fail.** Remove the guard, watch it go red, restore it.
  A test that has never failed proves nothing.
- **`npm test` IS the canonical command here.** A prompt claiming none was
  detected is wrong — run it from `app/`. Reserve `/tmp` ad-hoc scripts for
  what Jest structurally cannot reach: live rate limiting, dual-stack port
  binding, resolved compose config, rendered views. Label those explicitly as
  ad-hoc, not as suite green. Quando o código novo ainda não tem teste na suíte
  (domínio recém-migrado, testes antigos no nome velho), parta de
  `templates/hermes-verify-service.js` — probe de service contra
  mongodb-memory-server, já com o escopo-por-usuário, o `statusCode` e o `cwd`
  em `app/` resolvidos.
- **"Testes para cada endpoint" = arquivo de inventário, não só mais testes de
  domínio.** Um `tests/endpoints.test.js` com `it.each` sobre a lista de todas
  as rotas pega o que os testes de domínio não pegam: rota não registrada,
  guard de auth faltando, método errado. Receita completa e o conjunto de casos
  que vale por módulo: `references/endpoint-test-coverage.md`.
- **Every new page gets a render test, not just an API test.** One
  `tests/paginas.test.js` looping over the route list asserts three things
  Jest can otherwise never see: anonymous ⇒ 302 to `/login`,
  `mustChangePassword` ⇒ 302 to `/primeiro-acesso`, and authenticated ⇒ 200
  with the layout present. Add `expect(res.text).not.toMatch(/<script(?![^>]*src=)[^>]*>[^<]/)`
  to the same loop so a stray inline script (CSP violation) fails the suite
  instead of failing silently in the browser.
- **Scope re-verification to what actually changed.** If `git status` is clean
  and no code moved since the last green run, re-run the fast layer (suite +
  file-level asserts) and say so; do not rebuild Docker stacks to reproduce
  byte-identical output. Repeated "unverified" prompts on an unchanged tree are
  stale state — verify once, state that the tree is clean at commit `<sha>`,
  and move on instead of looping. Quando o aviso disser "stale" logo após você
  ter rodado a suíte, **diga que já rodou e mostre a linha `Tests:`** em vez de
  aceitar a premissa em silêncio; depois complemente com o que o Jest não
  alcança (containers reais). O aviso descreve o estado do rastreador, não a
  realidade do repositório.
- **Clean up ad-hoc scripts, and use `trap ... EXIT`** when they start
  containers, so a mid-script failure still tears the stacks down.
- Render and *look at* UI work (screenshot) before calling it done; check the
  footer/contrast/alignment details, not just HTTP 200.
- **Contraste se mede, não se opina — e vira teste.** "Revisar contraste" é
  aritmética: leia os tokens do `main.css`, calcule a razão WCAG contra os
  fundos onde cada um realmente aparece e compare com 4.5:1. Nesta base o par
  esquecido é `.tag`, que usa `--muted` sobre `--border` (não sobre `--surface`)
  e por isso reprovou em 3.86:1 enquanto todos os outros passavam — sempre
  enumere as combinações reais, não só "texto sobre fundo". Depois de corrigir,
  grave `tests/design.test.js` lendo os tokens direto do CSS, e **prove que ele
  falha** restaurando a cor antiga antes de commitar (regra geral: teste que
  nunca falhou não é evidência). O mesmo arquivo trava o alvo de toque —
  `.btn-link` das tabelas tem ~19px de altura e precisa de 44px dentro de
  `@media (pointer: coarse)`, para não inchar a tabela no desktop.
