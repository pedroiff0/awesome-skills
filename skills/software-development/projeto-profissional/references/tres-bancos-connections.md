# Três bancos numa só app (connections via useDb)

Alternativa ao padrão de 3 stacks separadas (`ambiente-demo-publico.md`): uma
única aplicação Express servindo 3 databases Mongo isolados, acessados por
prefixo de rota. Usado em `projeto-profissional` quando Pedro pediu "1 projeto,
1 landing, 3 bancos".

## Quando preferir este padrão

- Quer um único processo/deploy e uma única landing que escolhe o ambiente.
- Os 3 bancos são da MESMA aplicação (mesmo domínio, mesmo código).
- Não quer manter 3 `docker-compose` + 3 `NODE_ENV` com código duplicado.

Se os bancos forem de domínios diferentes (ex.: finanças vs acadêmico), o
padrão de 3 stacks separadas é melhor — cada uma com seu repo/deploy.

## Peças (copy-paste)

### `config/db.js`
```js
const mongoose = require('mongoose');
const env = require('./env');
const MODE_DB = { production: 'app_db', test: 'app_test_db', demo: 'app_demo_db' };
let mainConn = null;
const modeConns = {};
function baseUri() {
  const u = env.mongoUri.replace(/\/[^/?]*(\?.*)?$/, '/'); // tira o db do final
  return u.endsWith('/') ? u : u + '/';
}
async function connectDb() {
  mainConn = mongoose.createConnection(baseUri(), { ... });
  await mainConn.asPromise();
  return mainConn;
}
function getModeConn(mode) {
  if (!mainConn) throw new Error('Banco não conectado');
  if (!MODE_DB[mode]) throw new Error(`Modo inválido: ${mode}`);
  if (!modeConns[mode]) modeConns[mode] = mainConn.useDb(MODE_DB[mode], { useCache: true });
  return modeConns[mode];
}
module.exports = { connectDb, disconnectDb, getModeConn, MODE_DB };
```

### `models/registry.js`
```js
const userSchema = require('./user.model');
const auditLogSchema = require('./auditLog.model');
const projectSchema = require('./project.model');
const catalogItemSchema = require('./catalogItem.model');
const cache = new WeakMap();
function getModels(conn) {
  if (cache.has(conn)) return cache.get(conn);
  const models = {
    User: conn.model('User', userSchema),
    AuditLog: conn.model('AuditLog', auditLogSchema),
    Project: conn.model('Project', projectSchema),
    CatalogItem: conn.model('CatalogItem', catalogItemSchema),
  };
  cache.set(conn, models);
  return models;
}
module.exports = { getModels };
```
**Os `*.model.js` exportam o SCHEMA, não o model.** Quem cria o model é o
registry, na connection certa. Isso é o que quebra a compilação se você
`require('../models/user.model')` esperando o model.

### `middleware/selectDb.js`
```js
const { getModeConn } = require('../config/db');
const { getModels } = require('../models/registry');
function selectDb(mode) {
  return (req, res, next) => {
    req.mode = mode;
    req.conn = getModeConn(mode);
    req.models = getModels(req.conn);
    next();
  };
}
module.exports = { selectDb };
```

### `middleware/auth.js` (isolamento por banco)
```js
function signToken(user, mode = 'production') {
  return jwt.sign({ id: user._id, role: user.role, mode }, env.jwtSecret, { algorithm: 'HS256', expiresIn: env.jwtExpiresIn });
}
async function resolveUser(token, mode, models) {
  const payload = jwt.verify(token, env.jwtSecret, { algorithms: ['HS256'] });
  if (payload.mode && payload.mode !== mode) throw new AppError('Token de ambiente inválido', 401);
  const user = await (models || require('../models/registry').getModels(require('../config/db').getModeConn('production'))).User.findById(payload.id);
  if (!user || !user.isActive) return null;
  return user;
}
```

### `app.js` — montar por prefixo
```js
const pageRoutes = require('./routes/pages.routes');
const apiRoutes = require('./routes');
app.use('/', landingRoutes);                                  // landing pública
app.use('/api', selectDb('production'), apiRoutes);           // alias p/ testes antigos
app.use('/api/app', selectDb('production'), apiRoutes);
app.use('/api/test', selectDb('test'), apiRoutes);
app.use('/api/demo', selectDb('demo'), apiRoutes);
app.use('/', selectDb('production'), pageRoutes);             // alias
app.use('/app', selectDb('production'), pageRoutes);
app.use('/test', selectDb('test'), require('./routes'));     // se precisar de páginas de teste
app.use('/demo', selectDb('demo'), demoLoginRoutes);         // /demo/start (autologa)
app.use('/demo', selectDb('demo'), pageRoutes);              // /demo/ (dashboard)
```

### `server.js` — semear os 3 no boot
```js
for (const mode of ['production','test','demo']) {
  const models = getModels(getModeConn(mode));
  await seedAdminIfEmpty({ populaDemo: mode !== 'production' }, models);
  if (mode !== 'production' && process.env.POPULA_DEMO !== 'false') {
    await carregarDemo({ usuarios: 30, projetos: 40, itens: 120 }, models);
  }
}
```

## Services recebem `models` via `req`

Cada service que tocava banco passa a receber `models` (de `req.models`) em vez
de `require('../models/x')`. Controllers fazem `service.x(req.models, ...)`. É a
parte mais trabalhosa — faça o registry + `selectDb` primeiro, depois grep por
`require('../models/` e ajuste um a um.

## Testes: helper de models lazy

`tests/helpers/models.js` (NÃO chame `getModeConn` no topo do teste — ele lança
antes de `setupDb`):
```js
const { getModeConn } = require('../../src/config/db');
const { getModels } = require('../../src/models/registry');
module.exports = {
  get prod() { return getModels(getModeConn('production')); },
  get test() { return getModels(getModeConn('test')); },
};
```
E nos testes: `let User; beforeAll(async () => { User = models.prod; });` —
jamais `const User = models.prod.User` no topo.

## Verificação mínima de runtime
- Landing `/` lista os 3 botões (`/app/login`, `/test/login`, `/demo/start`).
- `GET /demo/start` → 302 para `/demo/`, seta cookie, redireciona ao dashboard.
- `GET /app` com o cookie de demo → 302 para `/login` (isolamento: token de
  demo não abre produção).
- `npm test` verde.
