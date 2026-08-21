---
name: web-fullstack-gotchas
description: Armadilhas recorrentes em apps fullstack Node/Express + EJS + CSS + jest + Docker (padrão do projeto financas-app, mas aplicável a qualquer stack similar). USE quando esbarrar em HTML escapado na view, testes jest flaky/verdes-antes-vermelhos-agora, middleware de autologin que vaza ou quebra a landing, ports Docker que não "colam", CSS que não atualiza no browser, "reiniciei e não surtiu efeito" (imagem Docker bakeada sem bind mount), ou pedido de "faça igual ao projeto X" (reproduza o padrão, não improvise). Carrega antes de mexer em views EJS, serviços com cache, rotas de auth, docker-compose ou de copiar o design de outro repo.
author: Fullstack Community
---

# Web fullstack gotchas (Node / Express / EJS / jest / Docker)

Coleção de armadilhas que custam iterações inteiras se não forem conhecidas de
antemão. Cada uma abaixo foi caçada na prática; o `references/fullstack-gotchas-detail.md`
tem os trechos de código exatos que resolveram, `references/docker-stale-image.md`
tem a receita de rebuild/verificação em Docker, e `references/multi-instance-prefix-and-ejs-tdz.md`
tem a reprodução exata do bug de prefixo de API em instância demo (401) e do
TDZ de `const` em include do EJS. `references/demo-mode-and-csrf.md` tem a
receita de teste da API multi-instância via curl (cookie demo + header `Origin`
+ prefixo `/api/demo`), triagem de 401/403 e reseed forçado da demo.
`references/i18n-raw-key-and-svg-var-fill.md` tem o diagnóstico de chave i18n
crua (PT sem bloco), o bug de `fill="var(--brand)"` em SVG (preto), barras
sobrepostas em `viewBox 0..100` + `preserveAspectRatio="none"`, escape de aspas
em atributo EJS e o tie-breaker `docker exec grep`.

## 1. EJS `<%= %>` ESCAPA HTML — nunca ponha tags dentro da expressão

`<%= expr %>` passa o valor por escape de HTML. Se `expr` contiver markup
(`<strong>`, `<span>`, `<a>`), ele sai como `&lt;strong&gt;` e o teste que
procura `>2</strong><span>lan...` falha mesmo com o dado certo.

- SINTOMA: o texto aparece na página como `<strong>2</strong>` "cru" (visível),
  ou um teste `toMatch(/>2<\/strong><span>/)` falha apesar do número estar certo.
- CORREÇÃO: coloque as tags HTML direto no template e só os VALORES via `<%= %>`.
  Não use template literal com tags dentro de `<%= %>`. Se precisar mesmo injetar
  HTML cru, use `<%- %>` (non-escaping) — mas prefira estruturar no template.
- Ver `references/fullstack-gotchas-detail.md` → "EJS escaping".

## 2. Cache module-level QUEBRA jest (valor stale entre casos)

Um serviço que faz `let cache = null; if (cache && ...) return cache;` com TTL
de minutos retorna o valor da PRIMEIRA request de toda a suíte para todos os
casos seguintes. Em teste que cria dados e espera contagens exatas, o cache
mentira e o assert falha de forma não-determinística.

- SINTOMA: teste de "números reais" falha esperando `>2</strong>` mas recebe
  `>176</strong>` (ou null), dependendo da ordem de execução.
- CORREÇÃO: desative o cache quando `process.env.NODE_ENV === 'test'`
  (`if (!emTeste && cache && ...) return cache;`). O cache é otimização de
  produção; em teste só atrapalha. Não remova o cache do código de produção.
- Ver `references/fullstack-gotchas-detail.md` → "module-level cache".

## 3. Middleware de autologin no Express — a regex define o que NÃO é autenticado

Para autenticar tudo menos a raiz (manter a landing visível mas entrar direto
no painel ao clicar em "Entrar"/"Ver demonstração"):

```js
app.use(/^(?!\/$).*/, demoAutologin);   // autentica TUDO menos "/"
```

- NÃO inverta a exclusão para `/login` — isso quebra o fluxo: a landing continua
  visível (bom) mas o botão de login para de entrar sozinho, e o teste de
  regressão "a landing não redireciona a raiz para o painel" falha.
- O middleware de autologin deve setar o cookie e chamar `next()`; a rota `/login`
  (com `optionalPageAuth`) verá o usuário e redireciona para `/app` — sem formulário.
- Ver `references/fullstack-gotchas-detail.md` → "autologin regex".

## 3b. BUG: autologin que seta `apiPrefix` SÓ na branch de autenticar trava a demo no painel

Quando a demo roda atrás de nginx (caminho 6b) e o frontend prefixa as APIs com
`data-api-prefix`, é fácil setar `res.locals.apiPrefix='/demo'` DENTRO do bloco que
só roda quando não há cookie (`if (req.cookies?.token) return next();` antes de
setar o prefixo). Resultado: visitante já autenticado (cookie válido, caso comum
após o 1º acesso) NÃO recebe o prefixo → o header monta links como `/app`,
`/lancamentos` (sem `/demo`) → o nginx manda pro app PRINCIPAL → 401 → a demo
só consegue abrir o painel, não as demais telas.

- REGRA: `res.locals.apiPrefix = '/demo';` deve ficar no TOPO do middleware,
  ANTES do early-return de cookie válido, para valer em TODA request da instância
  demo. (Ver seção 6c: o common.js lê esse prefixo do `<html data-api-prefix>`.)
- SINTOMA: curl de /demo/api/* com cookie dá 200, mas clicar nos links do nav na
  demo cai em 401/login. Correção é mover a linha do prefixo para fora do `if`.
- Teste de regressão: `GET /demo/lancamentos` (com cookie da demo) deve dar 200 e
  o nav mostrar Painel/Lançamentos/Orçamentos/Investimentos/Veículos/Tutorial.

## 4. `patch` tool DUPLICA barras invertidas em .md

Ao editar arquivos Markdown (code fences ``` com `\` ou comandos com `\\`), o
`patch` pode duplicar `\\` (ex.: `\\\\` em vez de `\\`). Isso quebra blocos de
código em docs (curl com `\` de quebra de linha vira `\\\\`).

- CORREÇÃO: depois de qualquer `patch` em `.md` envolvendo `\`, releia o trecho e
  corrija as barras duplicadas num patch seguinte. Mais seguro: use `write_file`
  para reescrever o arquivo quando houver muitas barras.

## 5. Trocar PORTA de instância Docker exige rebuild + atualizar TODOS os referenciadores

Mudar a porta num `docker-compose*.yml` (`"127.0.0.1:NOVA:5000"`) não basta:
- Rebuild obrigatório: `docker compose -f <arq> -p <proj> up -d --build`.
- Atualize TODOS os lugares que citam a porta: o próprio compose (`APP_BASE_URL`),
  `.env.example`, `README.md`, `docs/*.md`, `HANDOFF.md`, scripts de load
  (`loadtest/carga.js` `BASE` default), e quaisquer `curl` de exemplo.
- `docker compose -p <proj> down` (SEM `-v`) derruba preservando o volume do
  Mongo de produção; `-v` apagaria dados reais.
- Ver `references/fullstack-gotchas-detail.md` → "port swap".

## 6b. Isolar banco de DEMO na MESMA porta (proxy reverso, NÃO 2ª conexão)

Pedido recorrente: "demo acessada por /demo, com banco próprio, na mesma porta
das rotas normais". Dois caminhos:

- **(A) Proxy reverso nginx na frente** [PREFERIDO, zero refactor de lógica]:
  uma só porta (ex.: 4460); `location /demo/ { proxy_pass http://app-demo/; }`
  (strip do prefixo) e `location / { proxy_pass http://app; }`. O `app-demo` é
  um 2º container com `DEMO_AUTOLOGIN=true` e `MONGO_URI` apontando pro banco da
  demo. O banco principal (teste/prod) é escolhido no `.env` do container `app`.
  - Vantagem: services/controllers/models NÃO mudam; o autologin e o bd isolado
    já funcionam como instâncias separadas. Risco mínimo.
  - A landing (no `app`) precisa ler os números da demo: dê ao landingService
    UMA conexão de leitura isolada (`mongoose.createConnection(MONGO_URI_DEMO)`,
    só para counts) — NÃO acople toda a lógica. Se a var não existir, caia no
    banco atual (comportamento de teste). Veja `references/fullstack-gotchas-detail.md` → "demo nginx".
- **(B) 2ª conexão mongoose no MESMO app** [evitar se puder]: exige registrar os
  15+ models num `mongoose.createConnection` e injetar "qual banco" em TODOS os
  services/controllers (hoje usam `mongoose.model(...)` global). Refactor de
  ~30 arquivos, alto risco de regredir rotas normais. Só vale se o usuário
  exigir literalmente "mesmo processo".

BUG que pega em (A): o landingService que faz `M = { User, Account, ... }` para
consultar a demo PRECISA incluir TODOS os models usados (incluindo `Transaction`),
senão `M.Transaction` é `undefined` → throw → catch retorna `null` e a landing
mostra fallback fixo em vez dos números reais.

## 6c. BUG de roteamento: APIs do painel NÃO pegam o prefixo /demo -> 401

No caminho (A), a landing e as PÁGINAS da demo ficam sob /demo/* (o nginx manda
para app-demo), mas o frontend faz fetch('/api/dashboard') — URL absoluta SEM
prefixo. O nginx manda /api/* para o app PRINCIPAL (location /), não para o
app-demo. Resultado: a API da demo bate no banco/segredo errado -> 401 Token
invalido. A página abre (autologin OK) mas os cards ficam vazios.

- CORREÇÃO backend: o app-demo monta suas rotas TAMBÉM sob /demo, não só em /.
  Em createApp, quando DEMO_AUTOLOGIN está ligado: app.use('/demo', pageRoutes);
  app.use('/demo/api', apiLimiter); app.use('/demo/api', csrfGuard);
  app.use('/demo/api', apiRoutes). Assim /demo/app (página) e /demo/api/dashboard
  (API) ficam no app-demo, e o nginx (strip do /demo) roteia os dois certo.
- CORREÇÃO frontend: prefixar chamadas de API com /demo quando em demo. NÃO
  concatene na mão em cada arquivo — centralize no wrapper de fetch (apiRequest em
  common.js) lendo o prefixo de um atributo data-api-prefix no <html> (ver skill
  express-csp-runtime-config: NUNCA injete o prefixo via <script> inline, a CSP
  bloqueia). O demoAutologin seta res.locals.apiPrefix='/demo'; o header.ejs injeta
  <html data-api-prefix="<%= apiPrefix %>">; o apiRequest faz
  url.startsWith('/api/') ? prefix + url : url.
- SINTOMA que confunde: curl /demo/api/dashboard com cookie da demo dá 200, mas o
  browser mostra 401. Isso significa o prefixo NÃO está sendo aplicado no JS
  (common.js antigo em cache, ou script inline bloqueado por CSP).
- DIAGNÓSTICO CSP (pegou nesta sessão): injetei o prefixo via
  `<script>window.__API_PREFIX__ = '<%= apiPrefix %>';</script>` no header.ejs.
  O helmet vem com `scriptSrc: ["'self'"]` (SEM `'unsafe-inline'`) — logo o
  script inline é BLOQUEADO silenciosamente. Sintoma exato: o HTML servido
  CONTÉM o `<script>`, mas `typeof window.__API_PREFIX__ === 'undefined'` no
  console. Não adianta "forçar reload" — o script nunca roda. Correção: não use
  script inline para config; leia de atributo no `<html>`
  (`<html data-api-prefix="<%= apiPrefix %>">` + `document.documentElement
  .getAttribute('data-api-prefix')` no common.js). Respeita a CSP e o prefixo
  chega ao JS.

## 6e. Limpeza em cadeia ao REMOVER uma feature do backend (e o erro de import)

Quando se tira uma lógica do backend (ex.: a landing parou de ler os números da
demo via `statsDaDemo`), não basta apagar o uso na view. Falta de limpeza gera
500 em runtime e/ou testes que não cobrem mais nada.

- Em `pages.routes.js` NÃO remova `const env = require('../config/env');`.
  O `errorHandler` usa `env.nodeEnv` — ao apagar esse import junto com outro
  (`landingService`), todas as páginas passam a dar
  `ReferenceError: env is not defined` → 500. Sintoma: `paginas.test.js` e
  `modulos.test.js` estouram 500 em /lancamentos, /veiculos etc. Correção:
  remover SÓ o import órfão (`landingService`) e manter `env`.
- Checklist de remoção de feature: (1) view não usa mais o dado → (2) remove o
  import órfão no routes, (3) apaga o service file se ninguém mais o importa
  (grep ANTES de `rm`), (4) tira a env var do `config/env.js` e do compose,
  (5) ajusta os testes que afirmavam sobre aquele dado (ex.: landing.test que
  fazia `toMatch(/>2<\/strong><span>lançamentos/)`) para afirmar o NOVO
  comportamento (ex.: `not.toMatch(/fictícios/i)` + `toContain('href="/demo/app"')`).
- Sempre rode `npx jest --forceExit` DEPOIS de mexer em imports de routes: o
  `ReferenceError` só aparece em runtime, não no lint local.

## 6d. Cache-bust dos assets evita JS stale após rebuild

Mesmo com maxAge 0 em staging/demo, um browser que já abriu a demo antes do
deploy pode reter o common.js antigo (sem o prefixo /demo) e continuar a dar 401.
Em produção o maxAge 1h piora: todo deploy deixa JS stale por até 1h.

- CORREÇÃO: versione os scripts com query string de build. No app.js:
  app.locals.assetVersion = process.env.ASSET_VERSION || '1'; e no footer.ejs:
  <script src="/js/common.js?v=<%= assetVersion %>"></script>. No compose, passe
  ASSET_VERSION por build: ASSET_VERSION=$(git rev-parse --short HEAD) docker compose
  -p fa up -d --build. Cada deploy muda a URL do asset e o browser busca o JS novo.
- Combine com maxAge: env.nodeEnv === 'production' ? '1h' : 0 no express.static
  (staging/demo sem cache na verificação; produção com cache).

## 6. Cache de CSS no BROWSER mascara layout novo

Ao validar visualmente mudanças de CSS, o navegador serve o .css antigo do
cache e os screenshots mentem (mostram o layout velho). Não confie só no print.

- CORREÇÃO: confirme o CSS SERVIDO via getComputedStyle no DevTools contexto
  (browser_console com getComputedStyle(document.querySelector(...))), ou use
  cache-buster no <link href="/css/main.css?cb=Date.now()"> durante a inspeção.
  Só declare "funciona" após o computed style confirmar as novas regras.

## 7. CÓDIGO EDITADO NO DISCO NÃO ENTRA NO CONTAINER — `restart` NÃO BASTA

Quando o app roda em Docker **sem bind mount do código** (padrão deste template:
o `Dockerfile` faz `COPY app/ ./` no BUILD, e o `docker-compose.yml` só faz
`build:` + `ports:`), editar `app/views`, `app/public`, `app/src` no disco NUNCA
chega ao container até a imagem ser rebuildada. Um `docker compose restart`
(ou o usuario "reiniciar a aplicacao") so religa o mesmo container/imagem velha
-> a pagina continua com o layout/codigo ANTIGO e a pessoa diz "ainda nao
surtiu efeito nenhum".

- CORREÇÃO OBRIGATÓRIA:
  ```bash
  docker compose build --no-cache app
  docker compose up -d --force-recreate app
  ```
  `--no-cache` forca o `COPY app/` a rodar de novo; `--force-recreate` sobe o
  container a partir da imagem nova (senao `up -d` acha que "ja esta rodando").
- NÃO assuma loopback no curl de verificação: o `BIND_ADDR` do `.env` costuma
  ser um IP não-loopback (ex.: `100.120.54.126:4450`). `curl 127.0.0.1:4450`
  dá exit 7 mesmo com o app healthy. Use `docker port <container>` para achar o
  HostIp:Porta reais e busque por lá.
- CONFIRME o novo código com grep nas assinaturas (não só screenshot):
  `curl -s http://<HostIp>:<Port>/ -o /tmp/live.html` e grepe por marcadores do
  novo design vs do antigo. Só declare pronto após o grep bater.
- Detalhe completo + receita de verificação: `references/docker-stale-image.md`.

## 8. "Faça igual ao projeto X" = REPRODUZA O PADRÃO, NÃO IMPROVISE

Quando o usuario pede "landing igual a do financas-app, design tambem" (ou
qualquer "igual ao de <repo>"), a tarefa e **reproduzir fielmente** o modelo e
o CSS do repositório de referência — não inventar um layout "no mesmo espírito".
Nesta sessão improvisei uma landing genérica (hero centralizado, cards) e o
usuário rejeitou: "simplesmente quebrada, nada da maneira que pedi". A referência
estava no disco em `/home/pedro/Repositorios/pessoal/financas-app`.

- FLUXO: antes de escrever uma linha, LEIA os arquivos de referência
  (`landing.ejs`, `header.ejs`, `footer.ejs`, `main.css`, `DESIGN.md`,
  `common.js`) do repo citado e copie a ESTRUTURA (seções, ordem, grids,
  topbar) e os TOKENS (fonte, cores, sombras, raios) literalmente. Adapte
  SÓ o conteúdo textual (títulos, copy, idiomas) — mantenha a "casa" idêntica.
- Se o repo de referência usa fonte self-hosted (ex.: Inter via `@font-face` +
  `.woff2` em `public/fonts/`), COPIE os arquivos de fonte para o projeto
  alvo; não caia em "system-ui" por comodidade.
- Mantenha as especificidades do projeto alvo que o usuário já validou (ex.:
  seletor de idioma por BANDEIRAS SVG em vez de `<select>` com emoji) — funda
  sobre a estrutura copiada, não substitua.
- Capture a referência em `references/` quando for um padrão recorrente.

## 9. Multi-instância: NÃO HARDCODE o prefixo de API (erro 401 silencioso)

Apps deste template rodam em 3 modos na MESMA porta via prefixo de rota:
`/app`, `/test`, `/demo` → cada um com seu banco (selectDb). As PÁGINAS e a
navbar já usam o prefixo (setado em `res.locals.base` por `selectDb`), mas o
JS do cliente que faz `fetch` às APIs PRECISA do prefixo `/<modo>/` também.

- SINTOMA que confunde: a página abre (200) e mostra os dados do server-render,
  mas criar/mover/apagar via fetch dá **401 "Autenticação necessária"**. Motivo:
  o cookie da demo é válido SÓ para o banco demo; o fetch hardcoded
  `apiRequest('/api/projects/...')` bate em `/api/*` que o `app.js` mapeia para
  **produção** (`app.use('/api', selectDb('production'), apiRoutes)`). Produção
  não reconhece o cookie demo → 401. curl com `Origin` correto passa do CSRF,
  mas ainda 401 = prefixo errado, não CSRF nem escopo.
- CORREÇÃO: passe o prefixo de API do backend para a view e use no cliente.
  No route: `res.locals.apiBase = '/api' + (modo === 'app' ? '' : '/' + modo)`
  (ou reuse `base` → `'/api' + base`). Na view, exponha num atributo/data-*
  (NUNCA script inline — CSP): `<section class="board" data-api-base="<%= apiBase %>">`.
  No JS: `const apiBase = document.querySelector('.board')?.dataset.apiBase || '/api';`
  e `apiRequest(apiBase + '/projects', ...)`.
- REGRA geral: qualquer fetch de API dentro de página logada deve concatenar
  o `apiBase` do modo. Não existe `/api/projects` "neutro" quando há modos.
- Ver a nota de CSP na seção 6c (prefixo vem de atributo, não de script inline).

## 10. BUG EJS: redeclarar `const` com o nome de um local do `include` dá TDZ

`header.ejs` é incluído por várias views com `<%- include('partials/header',
{ modo: modo, base: base }) %>`. O EJS compila cada include-passado como uma
variável local da função de render. Se dentro do header você fizer
`const modo = ...` (mesmo nome), dá **"Cannot access 'modo' before
initialization"** em tempo de execução — a declaração `const` colide com o
local já existente (TDZ), e o erro só aparece ao RENDERIZAR, não no lint.

- CORREÇÃO: NUNCA redeclare com `const`/`let` um nome que o include possa
  passar. Leia o local e derive em OUTRO nome:
  ```ejs
  <% const _modo = (typeof modo !== 'undefined' && modo) || 'app';
     const _base = (typeof base !== 'undefined' && base) || (_modo === 'app' ? '' : '/' + _modo); %>
  ```
  e use `_modo`/`_base` no markup. Melhor ainda: quem seta o modo (selectDb)
  já joga `res.locals.modo`/`res.locals.base`/`res.locals.currentPath` para
  TODAS as views — aí o header só consome, sem redeclarar.
- DICA de verificação: um `ejs.render` standalone com os parâmetros certos pega
  esse erro antes do rebuild (rode um harness `render-*-check.js` temporário e
  apague-o).

## 6f. BUG de verificação visual: a demo carrega `/css/main.css` do APP PRINCIPAL, não do app-demo

Em setup com proxy reverso nginx (caminho 6b), a página `/demo/app` referencia o
stylesheet em `/css/main.css` (URL absoluta, SEM prefixo `/demo/`). O nginx roteia
`/css/*` → `location /` → **app principal**, não app-demo. Consequência que custou um
ciclo inteiro de debug: você rebuilda o `app-demo` com o CSS novo, o `curl
/demo/css/main.css` mostra a regra nova, mas o browser INSISTE no layout velho —
porque `document.styleSheets` aponta para `http://HOST/css/main.css` (do principal),
que ainda servia o arquivo antigo. O grep no `/demo/css` e no `/css` são arquivos
DIFERENTES.

- REGRA: ao mexer em CSS/JS da demo, rebuilda AMBOS os containers:
  `docker compose up -d --build app app-demo`. Valide o asset do PRINCIPAL:
  `curl -s http://HOST/css/main.css | grep -n 'suaRegraNova'` (deve aparecer). Se
  não aparecer, o `app` (principal) não foi rebuildado.
- Para o BROWSER DO USUÁRIO (não só o seu) re-buscar o CSS novo, BUMPE o
  `ASSET_VERSION` (o `header.ejs` já versiona o link: `/css/main.css?v=<%= assetVersion %>`):
  passe `ASSET_VERSION=2 docker compose up -d --build app app-demo` (o compose lê
  `ASSET_VERSION: ${ASSET_VERSION:-1}`). Sem o bump, a aba já aberta do usuário usa
  o cache `?v=1` e não vê a correção.
- Para SUA validação: navegue no browser direto na URL versionada
  (`/css/main.css?v=2`) para forçar fetch fresco antes de medir `getComputedStyle`.
- Sintoma clássico de ter esquecido o rebuild do principal: computed-style mostra
  valor OLD enquanto o arquivo em `/demo/css` (app-demo) já tem o novo. Sempre
  confira o `/css` (principal) também.

## 8b. Conteúdo da UI: NÃO mostre string de conexão de banco

O usuário pediu explicitamente "não informe as strings de conexão do banco de
dados". Elas vivem em `config/env.js` / `.env` / `docker-compose.yml`
(`mongodb://...`) — NUNCA as interpolate na view. Nomes de banco
(`app_db`, `app_demo_db`) são identificadores internos inofensivos, mas
prefira rótulos amigáveis na UI ("Produção"/"Teste"/"Demo") e evite expor
qualquer URI. Grep de defesa: `grep -rn 'mongodb://' app/views app/public`
deve retornar 0.


## 11. MODO DEMO: `demoBypass` para o usuário mexer em tudo (menos usuários)

Pedido recorrente de Pedro: "o usuário demo pode fazer o que quiser no banco
de demo, mas NÃO pode alterar dados de usuários". O demo user é `role:'user'`
(para NÃO poder editar usuários — `/admin` fica bloqueado). Para que ele possa
CRUDar qualquer tarefa/projeto/profissional do banco demo (que pertence a
outros donos seedados), adicione um bypass de escopo:

- Em `selectDb`: `if (mode === 'demo') req.demoBypass = true;` (logo após setar
  `req.mode`/`req.models`).
- Nos services de domínio (`projectService`, `taskService`,
  `professionalService`): assine `demoBypass = false` e, nas queries/obter,
  `if (role !== 'admin' && !demoBypass) q.ownerId = userId;` / `throw 403`.
  Quando `demoBypass` é true, pula o filtro de dono → o demo user vê/edita TUDO
  do banco demo. Usuários continuam protegidos porque o service de usuários
  NÃO recebe `demoBypass` e o demo user não é admin.
- SINTOMA que pega: board do demo mostra só 1-2 tarefas (as que ele "possui")
  porque o seed distribui donos. Com `demoBypass` o board mostra as 40 seedadas.
- CUIDADO: o endpoint de reload da demo (`/api/demo/demo/load?force`) costuma
  ter `requireAdmin` — o demo user é `user`, então dá **403 "Acesso negado para
  este papel"**. Se o reload só mexe no banco demo, PERMITA-o para a instância
  demo (ex.: `if (req.mode === 'demo') next();` ou honre `demoBypass`), senão o
  usuário não consegue repovoar a demo.

## 12. TESTAR MUTAÇÃO DE API VIA curl: CSRF exige header `Origin`

O `csrfGuard` (montado em `/api`) bloqueia POST/PATCH/DELETE cujo `Origin`
não bata com `Host`, e também bloqueia quando `Origin` está AUSENTE. curl não
manda `Origin` por padrão → você recebe **403 "Requisicao bloqueada (origem
ausente)"**, que parece erro de permissão mas é só falta de header.

- RECEITA para testar a API com cookie de demo:
  ```bash
  curl -s -b /tmp/demo.cookies -X POST "http://<HostIp>:<Port>/api/demo/tasks" \
    -H 'Origin: http://<HostIp>:<Port>' -H 'Content-Type: application/json' \
    -d '{"titulo":"Teste","status":"planejado"}' -w '\nHTTP %{http_code}\n'
  ```
- Para triar o erro: 401 = autenticação (cookie/prefixo errado); 403 "origem
  ausente" = falta `Origin`; 403 "Acesso negado" = papel. O script do browser
  (`apiRequest` com `credentials:'same-origin'`) manda `Origin` certo, então o
  403 só aparece no curl de teste.
- Detalhe + receita completa: `references/demo-mode-and-csrf.md`.

## 13. EJS: variável de loop NÃO pode se chamar `t` (sombreia o i18n)

Em views que recebem `t` (a função de tradução: `<%= t('nav.panel') %>`),
fazer `col.items.forEach(function(t){ ... })` **sombreia** o `t` dentro do
corpo do loop → "t is not a function" ao chamar `t('board.remove')`. O erro só
aparece ao RENDERIZAR (não no lint), e só para a view que tem itens.

- CORREÇÃO: nomeie o iterador diferente — `function(task)`, `function(item)`,
  `function(p)`. Nunca `t`, `e`, `m` se a view usa esses nomes como helper.
- Verifique com `ejs.render` standalone (harness `render-*-check.js`) passando
  uma lista com 1 item — pega o erro antes do rebuild.

## 14. Nav mode-aware: `selectDb` joga `res.locals` para TODAS as views

Para a navbar nunca apontar para o app errado em `/demo` ou `/test`, não passe
`modo`/`base` manualmente em cada include. Em `selectDb`, depois de `req.models`,
sete:
```js
res.locals.currentPath = (req.baseUrl || '') + (req.path || '/');
res.locals.modo = mode;
res.locals.base = mode === 'app' ? '' : '/' + mode;
```
O `header.ejs` consome `modo`/`base` direto (sem redeclarar `const` — ver seção
10) e monta os links como `<%= base %>/projetos`, `<%= base %>/perfil`. Assim o
nav do demo aponta para `/demo/*` e o usuário navega de verdade. (Em
`pageAuth` não há `currentPath`; quem sabe o modo é o `selectDb`.)

## 8c. Landing: "só o que o sistema faz + demo", NUNCA falar de 3 ambientes NEM de segurança/JWT

Quando Pedro diz "não pode falar que tem 3 ambientes", RETIRE da landing a
seção de "Produção/Teste/Demo" (grid de bancos, "três espaços isolados"). A
landing deve conter SÓ: (1) o propósito do sistema, (2) um CTA de demo
(`/demo/start`). Ele rejeitou duas vezes landings que enfatizavam múltiplos
bancos. Nomes de banco (`app_db`) também saem da UI (ver 8b).

ATUALIZAÇÃO (corrige orientação anterior que dizia para "manter JWT/CSRF como
diferencial"): Pedro pediu EXPLICITAMENTE para REMOVER da landing TUDO que fale
de segurança/JWT/bancos — não só a seção "Como a segurança é feita", mas também
o badge do hero ("Template base · JWT · Admin" → "Template de tarefas · Demo ao
vivo"), os pills do mock ("Bancos isolados" / "JWT httpOnly" → "Quadro Kanban" /
"Foco Pomodoro") e o `<meta name="description">` que citava JWT/bancos isolados.
CHECK-LIST ao limpar a landing: grep por `JWT|Bancos isolados|httpOnly|banco de
dados, isolado` deve retornar 0 em `views/landing.ejs` E em `header.ejs` (a meta
description vive no parcial). NÃO reintroduza "segurança" como diferencial na
landing — ele não quer esse bloco.

## 15. Rota duplicada: a PRIMEIRA definição vence, a segunda é sombreada

Em `routes/*.js`, se houver DUAS `router.get('/mesma-rota', ...)` (uma antiga
sync que esquece de passar `apiBase`/`dados`, e uma nova async correta),
o Express usa a PRIMEIRA que bate — a antiga. Sintoma confuso: a página dá
**500 "apiBase is not defined"** mesmo existindo uma rota "correta" mais abaixo.

- DIAGNÓSTICO: `grep -n "router.get('/projetos'" src/routes/pages.routes.js` —
  se aparecer 2x, a primeira (sync, sem `apiBase`) está sombreando a segunda.
- CORREÇÃO: remova a definição STALE/duplicada (a que não passa os dados),
  mantendo só a async que renderiza com `apiBase`, `projetos`, etc.
- REGRA: nunca deixe duas definições da mesma rota; o Express não avisa.

## 16. Reseed da demo INVALIDA o token do usuário demo (ordem de operações)

`/demo/start` (demoLogin) emite um token cujo `sub` = o `_id` do usuário demo.
Se logo em seguida você roda `POST /api/demo/demo/load?force=true` e o seed
faz `deleteMany({email:/@example.com/})` + `insertMany` (recria o demo user com
NOVO `_id`), o token antigo aponta para um usuário que não existe mais →
qualquer request depois do reseed dá **401 "Autenticação necessária"**, mesmo
com o cookie salvo.

- SINTOMA que confunde: o PRÓPRIO POST de reseed dá 200 (o usuário ainda existia
  no momento do `auth`), mas TODOS os GETs seguintes (board, API) dão 401.
- CORREÇÃO: após um reseed `force`, REFAÇA o login (`/demo/start`) para pegar um
  token com o `_id` novo antes de testar as páginas. Não reaproveite o cookie
  antigo.
- Para EVITAR o 401 no reseed em si (o demo user é `role:'user'`, mas o endpoint
  tinha `requireAdmin`): libere o reload para a instância demo — em `demo.routes.js`
  troque `requireRole('admin')` por um guard inline que faz `next()` quando
  `req.mode === 'demo'` (ou honre `req.demoBypass`), pois o reload só mexe no
  banco demo. (Ver seção 11 sobre `demoBypass`.)

## 16b. Cada PÁGINA que faz fetch precisa do seu próprio `data-api-base`

O bug da seção 9 (prefixo de API) se repete POR PÁGINA: o board expõe
`data-api-base="<%= apiBase %>"`, mas se você criar `/projetos` e
`/profissionais` e esquecer de colocar `data-api-base` no elemento raiz delas,
o JS dessas páginas cai no fallback `'/api'` (produção) → 401 no modo demo.

- CHECK-LIST ao criar uma página nova que consome API: confirme que o
  `data-api-base` está no `<section>`/`<div>` raiz (ex.:
  `<section class="card" data-api-base="<%= apiBase %>">`) e que a rota passa
  `apiBase: '/api/' + modo`. Sem isso a página abre (200) mas o cadastro/lista
  falha silenciosamente.
- O `apiRequest` do cliente deve ler
  `document.querySelector('[data-api-base]')?.dataset.apiBase || '/api'`.

## 17. `express.static` com `maxAge:'1h'` faz o navegador reter CSS/JS por 1h (sintoma "não reiniciou")

Quando o app serve assets com `express.static(path, { maxAge: '1h' })`, o
navegador cacheia `main.css`/`board.js` por UMA HORA. Depois de um rebuild que
corrige layout/CSS/JS, o usuário abre a página e vê o **layout velho** — e diz
"parece não ter sido reiniciado o sistema" / "ainda está com textos brutos",
mesmo o container servindo o arquivo novo. O `Cache-Control: public, max-age=3600`
no header é a causa exata.

- CORREÇÃO (demo/staging/verificação): `express.static(path, { maxAge: 0, etag: true })`.
  Com `max-age=0` o navegador SEMPRE revalida (ETag) e baixa o asset novo após
  cada deploy. Em produção mantenha cache (`nodeEnv==='production' ? '1h' : 0`),
  combinando com versionamento de asset (seção 6d) para invalidar por URL.
- DIAGNÓSTICO: `curl -sI http://<host>:<port>/css/main.css | grep -i cache-control`
  deve mostrar `max-age=0` (ou `max-age=3600` só em produção). Se estiver 3600 e o
  usuário reclamar de CSS velho, essa é a causa — não o rebuild.
- NÃO confunda com a imagem Docker (seção 7): aqui o arquivo NOVO está no
  container, mas o CLIENTE não o busca porque o cache de 1h ainda é válido.

## 18. Verifique o ASSET SERVIDO, não só o arquivo no disco

Após editar `public/js/*.js` / `public/css/*.css`, um rebuild pode ter rodado
ANTES do patch aterrissar no disco — e o container passa a servir a versão
ANTIGA. Sintoma enganador: `search_files` no arquivo local mostra a mudança, mas
o browser ainda tem o comportamento velho. Nesta sessão o `board.js` local tinha
`renderizarCards` (12660 bytes) mas o container servia 12250 bytes SEM a função.

- CORREÇÃO: depois do rebuild, `curl -s http://<host>:<port>/js/board.js -o /tmp/x.js`
  e `grep -c 'marcadorDaSuaMudanca' /tmp/x.js`. Só declare pronto quando o GREP no
  asset SERVIDO bater. Combine com a seção 7 (`--no-cache` + `--force-recreate`).
- Para CSS: `curl -s .../css/main.css | grep -c 'novaRegra'`. Para HTML/EJS:
  `curl -s .../demo/ -o /tmp/p.html && grep -c 'id="task-modal"' /tmp/p.html`.
- REGRA: "edição no disco" ≠ "servido ao cliente". O grep final é sempre no
  asset servido, não no arquivo local.

## 19. Formulário NOVO sem a CLASSE de estilo = "textos brutos"

Ao adicionar um formulário, se o `<form>` NÃO carregar a classe que detém as
regras de `input/textarea/select`, os campos aparecem como caixas default do
navegador (sem borda/raio/foco) — o usuário chama de "textos brutos" (campo cru,
não dado cru). Nesta sessão o painel "Nova tarefa" usava `id="task-form"` SEM
`class="cad-form"`, então o CSS de input (definido para `.cad-form input,
.cad-form textarea, .cad-form select`) nunca se aplicava.

- CHECK-LIST ao criar formulário: confirme que o `<form>` (ou o container) tem a
  classe que carrega o estilo base dos inputs (`cad-form` / `cadastro` no template
  deste projeto). Adicione `.cad-form input, .cad-form textarea, .cad-form select
  { width:100%; padding; border; radius; box-shadow no :focus }` se faltar.
- Também vale para o `select` custom (`.select`) e para `field-hint` (texto de
  ajuda sob o input). O usuário reclama de "bruto" quando vê input sem foco-ring
  nem padding — é bug de CSS de formulário, trate como tal.
- Verificação: `curl` no HTML servido e `grep 'id="task-form" class="cad-form"'`.

## Workflow (Pedro): screenshot antes de commitar frontend/feature

Pedro só aprova depois de VER o resultado num screenshot real do browser
(ver skill `frontend-visual-verification`). NUNCA `git commit` uma mudança de
frontend/nova feature sem antes: rebuild do container (seção 7), screenshot da
página ao vivo, e aprovação explícita dele. Ele também quer nav mode-aware,
seletor de idioma por BANDEIRAS SVG (não emoji/`select`), e rodapé
multi-coluna "empresarial".

PASSO-A-PASSO obrigatório ao mexer em CSS/JS da DEMO (caminho 6b):
1. Faça a edição no `app/public/...` (fonte única — app e app-demo copiam o mesmo
   arquivo no build).
2. Rebuilda AMBOS os containers: `docker compose up -d --build app app-demo`.
   NÃO rebuildar só o `app-demo`: a demo carrega `/css/main.css` do app PRINCIPAL
   (seção 6f), então o principal precisa do CSS novo também.
3. BUMPE `ASSET_VERSION` (ex.: `ASSET_VERSION=2 docker compose up -d --build app
   app-demo`) para o browser do USUÁRIO re-buscar o asset (senão a aba dele fica
   no cache `?v=1`).
4. Navegue no browser até a URL versionada (`/css/main.css?v=2`) para forçar fetch
   fresco, depois meça `getComputedStyle` nas duas divs que deveriam alinhar
   (diff de `top` deve ser 0) e só então tire o screenshot para o Pedro.
5. Confirme o asset SERVIDO do principal: `curl -s http://HOST/css/main.css | grep -n
   'suaRegraNova'` (seção 18/6f) — não confie só no arquivo no disco.

VERIFICAÇÃO AD-HOC (quando não há suíte de teste): o sistema pode marcar a
verificação como "stale" se você só rodou um script e não reportou o resultado de
forma explícita. Sempre: (1) escreva o script em `/tmp/hermes-verify-*.js`
(os-safe tempfile, apagado depois), (2) rode contra o comportamento mudado
(render EJS via `ejs.render` standalone com os params da rota, grep no CSS vivo
servido, curl nas rotas), (3) declare o resultado como "ad-hoc verification",
NÃO "suite green". Para views que usam `<%- include %>` com locals (ex.:
`header.ejs` consome `modo`/`base`), passe TODOS os locals que a rota realmente
passa (a section 10/TDZ e a seção 15 valem aqui: um `ejs.render` standalone com
os params certos pega erros de "X is not defined" ANTES do rebuild). Cuidado com
regex de checagem que não casam seletor CSS multi-linha (seção abaixo do 16b):
leia o CSS com `search_files`/`read_file` para confirmar a regra existe de fato,
em vez de confiar só no regex do harness.

## Gates de validação (sempre rode antes de declarar pronto)

- `npx jest --forceExit` — suíte completa deve ficar 100% verde.
- `npx @google/design.md lint ../DESIGN.md` — 0 erros (se o repo tiver DESIGN.md).
- Se alterou Docker/portas: rebuild + `curl -s -o /dev/null -w '%{http_code}'`
  nas rotas-chave (ex.: demo `/app` → 200, `/admin` → 403, produção `/app` → 302).
  Se o app roda EM DOCKER: o "rebuild" acima é `docker compose build --no-cache
  app && docker compose up -d --force-recreate app` (ver seção 7) — `restart`
  sozinho NÃO re-aplica edições de código.

## 20. i18n: chave CRUA na tela = chave AUSENTE no idioma ativo (e diagnóstico rápido)

Quando a view renderiza o próprio nome da chave (`proj.list`, `pro.desc`, `painel.x`)
em vez do texto, NÃO é bug do `t()` — é que a chave não existe no dicionário do
idioma em uso (quase sempre o PT, editado por último e ficando com bloco
incompleto). Sintoma clássico: `nav.tasks` e `landing.*` funcionam (outros
blocos OK), mas `proj.*`/`pro.*` saem crus — porque en/es/fr TÊM o bloco e o PT NÃO.

- DIAGNÓSTICO isolado (mais rápido que subir o container): require o i18n e
  traduza a chave suspeita EM NODE:
  ```js
  const { translate } = require('./src/config/i18n');
  console.log(translate('pt', 'proj.list'));   // 'proj.list' => chave faltando no PT
  console.log(translate('pt', 'nav.tasks'));   // 'Tarefas'     => OK
  ```
  Se retornar a própria chave, ela (ou o bloco todo) está ausente em `DICT.pt`.
  Confirme com grep no arquivo: `grep -n "'proj.list':" src/config/i18n.js` —
  se só aparecer em en/es/fr, o PT está incompleto. Adicione o bloco PT faltante.
- REGRA ao editar i18n: NUNCA deixe um idioma com bloco parcial. Se adicionou
  `proj.*` para en/es/fr, adicione para PT também. O fallback `DICT.pt[key]`
  só existe se a chave estiver EM PT — não serve para "traduzir" um literal.
- Verificação ao vivo: `curl -s -b /tmp/demo.cookies /demo/projetos | grep -c 'proj.list'` deve ser 0; `grep 'Projetos registrados'` deve ser >0.

## 21. SVG `fill="var(--brand)"` NÃO resolve (fica PRETO) — use CSS

`var()` só funciona em CSS, NÃO em atributos de apresentação SVG
(`<rect fill="var(--brand)">`). O navegador ignora e cai no default **preto**.
Sintoma: gráfico SVG vira "bloco preto sólido". Mesmo com
`.bars svg rect { fill: var(--brand) }` no CSS, se o seletor não casar (barra
sem a classe esperada, ou regra ineficaz) o default preto aparece. Correção
robusta: (1) tire o `fill="var(...)"` do atributo; (2) dê `class="bar"` à barra;
(3) CSS: `.bars svg .bar { fill: var(--brand); }`.

- BUG COMPANHEIRO de gráfico de barras: com `viewBox="0 0 100 100"` +
  `preserveAspectRatio="none"`, usar `x="6%" width="88%"` faz CADA barra ter
  88% da largura do viewport → elas SE SOBREPÕEM num único retângulo (bloco
  sólido), não barras separadas. Use coordenadas em user-space:
  `slot=100/entries; bw=min(slot*0.6,14); x=i*slot+(slot-bw)/2; y=100-h;`
  e renderize os RÓTULOS como HTML abaixo do `<svg>` (`.bars-labels`), nunca
  como `<text>` dentro do SVG com `preserveAspectRatio="none"` (texto distorce).
- Verificação: `getComputedStyle(svg.querySelector('.bar')).fill` deve ser a cor
  do brand (ex.: `rgb(37,99,235)`), não `rgb(0,0,0)`.

## 22. EJS escapa ASPAS em atributo -> confere `data-theme` no script de verificação

`<html ... data-theme="<%= lpDark ? 'dark' : 'light' %>">` é servido como
`data-theme=&#34;dark&#34;` (o EJS escapa as aspas duplas do atributo para
`&#34;`). Inofensivo para o navegador (decodifica certo), MAS quebra um check
ingênuo `html.includes('data-theme="dark"')` no seu script de verificação →
falso FAIL. Correção no harness: confira `html.includes('data-theme=&#34;dark&#34;')`
ou melhor, valide via atributo decodificado (`curl ... | grep -o '<html[^>]*>'`).
NÃO trate o `&#34;` como bug — é escape correto de EJS.

## 23. Tie-breaker de deploy stale: `docker exec <container> grep` decide

Quando grep no ARQUIVO LOCAL mostra a mudança mas o asset SERVIDO (§18) parece
velho, o árbitro definitivo é o arquivo DENTRO do container:
```bash
docker exec projeto-profissional-app-1 grep -c "proj.list" /app/src/config/i18n.js
docker exec projeto-profissional-app-1 grep -c "renderizarCards" /app/public/js/board.js
```
Se o container tem a mudança mas o browser não, o problema é cache do cliente
(§17) ou o browser abriu antes do rebuild. Se o container NÃO tem, o rebuild não
incluiu o patch (§7/§18): rode `docker compose build --no-cache app && docker
compose up -d --force-recreate app` de novo. NÃO confie só no grep local.

## 24. JWT `tokenValidAfter` default `new Date()` INVALIDA o token ao nascer

Causa raiz de "não consigo fazer logout, token inválido" e de reset de demo
travado: se o model de usuário tem `tokenValidAfter: { type: Date, default: () => new Date() }`,
TODO usuário novo nasce com sessão ANTERIOR invalidada. O `resolveUser` do
middleware auth compara `payload.iat` (segundos, TRUNCADO para baixo) com
`user.tokenValidAfter` (segundos). Se o token é emitido no mesmo segundo da
criação do usuário (ou há dessincronia de 1ms de clock), o `iat` truncado fica
MENOR que `validAfterSec` → `resolveUser` retorna null → 401 "Token inválido".

- SINTOMA: usuário recém-criado/logado dá 401 em TODAS as APIs logo após o
  login; logout (`/api/auth/logout`) ou reset da demo (`/api/reset-demo`) falham.
- CORREÇÃO: `tokenValidAfter` default `null` (usuário novo NÃO tem sessão a
  invalidar). As ações de invalidação (troca/reset de senha, desativação, logout
  global) continuam setando `tokenValidAfter = new Date()` EXPLICITAMENTE no
  service. Com `null`, o `if (payload.iat && user.tokenValidAfter)` é pulado e o
  token recém-emitido é válido.
- TESTE de regressão: usuário novo tem `tokenValidAfter` falsy; um token emitido
  por `authService.generateToken(user)` passa em `GET /api/auth/me` (200).

## 25. Logout/reset NÃO devem exigir token válido (middleware `authOptional`)

O endpoint de logout existe JUSTAMENTE para invalidar a sessão — se o token já
está expirado/inválido (ex.: por tokenValidAfter no futuro, ou expirado), o
middleware `auth` barra ANTES do controller rodar, o cookie não é limpo e o
usuário fica "preso" (clica em sair, nada acontece / cai em estado ruim).

- PADRÃO: crie `authOptional` — popula `req.user` se o token for válido, mas NÃO
  lança 401 quando está ausente/expirado/inválido (try/catch silencioso, `next()`
  sempre). Aplique em `/api/auth/logout` e em `/api/reset-demo` (na demo o
  usuário sempre é o demo via autologin; o reset deve concluir mesmo com token
  vencido). O controller de logout só faz `clearAuthCookie(res)` + 200, e já usa
  `req.user?.id` defensivamente.
- Assim o logout/reset CONCLUEM mesmo com token inválido, e o usuário nunca fica
  sem saída. Rotas que de fato exigem identidade mantêm `auth` normal.

## Quando NÃO aplicar

Estas são armadilhas de implementação web fullstack. Não cobrem deploy em
plataformas managed, ORMs pesados ou frameworks com SSR próprio (Next/Nuxt) —
nesses o modelo de cache/autenticação é outro.
