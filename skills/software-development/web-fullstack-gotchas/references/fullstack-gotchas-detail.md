# Detalhes concretos — web-fullstack-gotchas

Trechos reais extraídos da sessão no projeto financas-app (Express + EJS +
CSS + jest + Docker). Serviram para fechar cada armadilha do SKILL.md.

## EJS escaping

FRAGMENTADO (quebrava o teste `toMatch(/>2<\/strong><span>lan.amentos/)`):

```ejs
<p>
  A demonstração já vem com<%= stats ? ` <strong>${stats.lancamentos.toLocaleString('pt-BR')}</strong><span>lançamentos na demonstração</span> e <strong>${stats.meses}</strong><span>meses de histórico</span>` : ' <strong>12</strong><span>meses de histórico</span>' %>
  de histórico: ...
</p>
```

Resultado no HTML: `&lt;strong&gt;2&lt;/strong&gt;&lt;span&gt;lançamentos...`
— o `<%= %>` escapou todo o markup. O `stats` estava CERTO (2, 3); só o HTML sumiu.

CORRETO (tags no template, valores via `<%= %>`):

```ejs
<p>
  A demonstração já vem com
  <% if (stats) { %>
    <strong><%= stats.lancamentos.toLocaleString('pt-BR') %></strong><span>lançamentos na demonstração</span>
    e <strong><%= stats.meses %></strong><span>meses de histórico</span>
  <% } else { %>
    <strong>12</strong><span>meses de histórico</span>
  <% } %>
  de histórico: ...
</p>
```

## module-level cache

Serviço `landingService.statsDaDemo()` tinha:

```js
let cache = null;
let cacheEm = 0;
const TTL_MS = 5 * 60 * 1000;
async function statsDaDemo() {
  const agora = Date.now();
  if (cache && agora - cacheEm < TTL_MS) return cache;   // <- em teste, stale!
  ...
}
```

Correção (desativa em teste, mantém em produção):

```js
async function statsDaDemo() {
  const agora = Date.now();
  const emTeste = process.env.NODE_ENV === 'test';
  if (!emTeste && cache && agora - cacheEm < TTL_MS) return cache;
  ...
}
```

Diagnóstico que confirmou: `console.error('[DIAG] demo null')` NÃO apareceu → o
`demo` era achado; o problema era o cache retornando valor de um seed anterior.
Sempre que um teste espera contagem exata de um serviço com cache, suspeite do
cache module-level.

## autologin regex

App.js, registrado ANTES de `app.use('/', pageRoutes)`:

```js
if (process.env.DEMO_AUTOLOGIN === 'true' && env.nodeEnv !== 'production') {
  const { demoAutologin } = require('./middleware/demoAutologin');
  // autentica TUDO menos a raiz: landing visível, mas /login e /app entram direto
  app.use(/^(?!\/$).*/, demoAutologin);
}
```

Regex confirmada no node: `/app => true`, `/login => true`, `/ => false`,
`/forgot-password => true`. Inverter para excluir `/login` quebrava o teste
"a landing não redireciona a raiz para o painel" (que exige `/` → 200) e o
fluxo "clicar em login entra direto".

## port swap (Docker)

Produção 4450→4461, Teste 4451→4460, Demo 4452→4462. Em cada compose:

```yaml
ports:
  - "${BIND_ADDR:-127.0.0.1}:4461:5000"   # produção
environment:
  APP_BASE_URL: ${APP_BASE_URL:-http://localhost:4461}
```

Mais: `.env.example` (`APP_BASE_URL_DEMO=...:4462`), `README.md` (tabela de
portas + curl), `docs/operacao.md`, `docs/deployment.md` (proxy_pass),
`docs/load-testing.md` (tabela), `HANDOFF.md` (credenciais + curl), e
`loadtest/carga.js` (`const BASE = __ENV.BASE_URL || 'http://localhost:4460';`).
Rebuild: `docker compose -f docker-compose.demo.yml -p fa-demo up -d --build`.
Derrubar antigas: `docker compose -p fa down` (sem `-v` preserva volume Mongo).

## patch backslash artifact

Em `.env.example` e `docs/operacao.md`, patch com `\\` em code fence duplicou para
`\\\\`. Sempre rever barras após patch em `.md`.

## verificação visual (CSS cache)

`browser_console('getComputedStyle(document.querySelector(".tut-layout"))')`
confirmou `display: grid` e colunas reais — enquanto o screenshot (cache de CSS)
mostrava layout antigo. Use computed style, não só print.

## demo nginx (seção 6b do SKILL.md)

Pedido: "demo acessada por /demo, com banco próprio, na MESMA porta das rotas
normais". Caminho PREFERIDO = proxy reverso nginx (zero refactor de lógica),
NÃO 2ª conexão mongoose no mesmo app (refactor de ~30 arquivos, alto risco).

Compose único: `app` (banco principal via .env MONGO_URI, default teste),
`app-demo` (MONGO_URI demo + DEMO_AUTOLOGIN=true), `nginx` expondo a porta única.

`nginx/default.conf`:

```nginx
upstream financas_app    { server app:5000; }
upstream financas_demo   { server app-demo:5000; }
server {
  listen 5000;
  location = /demo        { return 302 /demo/app; }
  location /demo/         { proxy_pass http://financas_demo/; }
  location /              { proxy_pass http://financas_app; }
}
```

landingService — conexão de leitura isolada SÓ para os números da landing
(evita acoplar toda a lógica à 2ª conexão):

```js
async function obterDemoModels() {
  if (demoModels) return demoModels;
  if (!env.mongoUriDemo) return null;   // em teste, cai no banco atual
  demoConn = mongoose.createConnection(env.mongoUriDemo);
  await new Promise((res, rej) => { demoConn.once('connected', res); demoConn.once('error', rej); });
  demoModels = {
    User:        demoConn.model('User', User.schema),
    Transaction: demoConn.model('Transaction', Transaction.schema),
    Account:     demoConn.model('Account', Account.schema),
  };
  return demoModels;
}
```

PEGADILHA REAL (custou 1 teste vermelho): o objeto de models da demo PRECISA
conter Transaction (e todo model consultado). Faltando um, M.Transaction é
undefined → throw → catch retorna null → a landing mostra fallback fixo
("12 meses") em vez dos números reais do banco da demo.
