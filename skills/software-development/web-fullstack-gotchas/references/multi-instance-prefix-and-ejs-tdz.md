# Multi-instância: prefixo de API + TDZ do EJS (detalhe de sessão)

Reprodução e correção exatos dos dois bugs caçados em sessão no projeto
`projeto-profissional` (template Express/EJS com modos /app, /test, /demo).

## A) Prefixo de API em instância demo → 401 silencioso

**Sintoma:** a página `/demo/` renderiza (200) com os dados do server-render,
mas quick-add / mover / apagar via `board.js` dá `401 "Autenticação
necessária"`. O cookie da demo é válido; o problema é o DESTINO do fetch.

**Causa:** o `app.js` monta:
```js
app.use('/api',            selectDb('production'), apiRoutes);
app.use('/api/app',        selectDb('production'), apiRoutes);
app.use('/api/test',       selectDb('test'),       apiRoutes);
app.use('/api/demo',       selectDb('demo'),       apiRoutes);
```
O `board.js` chamava `apiRequest('/api/projects/...')` (sem prefixo). Em
`/demo`, `/api/*` cai no primeiro `app.use('/api', selectDb('production'), ...)`
→ banco de PRODUÇÃO. O cookie demo não é aceito lá → 401.

**Diagnóstico via curl (sem enganar com Origin):**
```bash
# pega cookie de autologin da demo
curl -s -c /tmp/d.cookies -o /dev/null 'http://<HostIp>:<Port>/demo/start'
# erro: prefixo errado -> 401
curl -s -b /tmp/d.cookies -X PATCH "http://<HostIp>:<Port>/api/projects/$ID" \
  -H 'Content-Type: application/json' -H "Origin: http://<HostIp>:<Port>" \
  -d '{"status":"concluido"}'
# certo: prefixo /demo -> 200
curl -s -b /tmp/d.cookies -X PATCH "http://<HostIp>:<Port>/api/demo/projects/$ID" \
  -H 'Content-Type: application/json' -H "Origin: http://<HostIp>:<Port>" \
  -d '{"status":"concluido"}'
```
(CSRF só bloqueia sem `Origin`/Referer; com Origin == Host passa. Se mesmo
com Origin der 401, o bug é o prefixo, não CSRF.)

**Correção (server → view → client):**
1. `pages.routes.js` (rota `/`): após `selectDb` já ter setado `res.locals.base`
   (`''` para app, `/demo` para demo), calcule:
   ```js
   const apiBase = '/api' + (res.locals.base || '');
   ```
   e passe `apiBase` ao `res.render('board', { ..., apiBase })`.
2. `board.ejs`: expõe sem script inline:
   ```ejs
   <section class="board" data-api-base="<%= apiBase %>">
   ```
3. `board.js`: leia do atributo e concatene:
   ```js
   const apiBase = document.querySelector('.board')?.dataset.apiBase || '/api';
   apiRequest(apiBase + '/projects', { method:'POST', body:... });
   apiRequest(apiBase + '/projects/' + id, { method:'PATCH', body:... });
   apiRequest(apiBase + '/projects/' + id, { method:'DELETE' });
   ```
**Princípio:** never existe `/api/projects` neutro quando há modos; todo fetch
de página logada leva o `apiBase` do modo.

## B) TDZ do EJS: `const modo` colide com local do include

**Sintoma:** ao renderizar `board.ejs` (que faz
`<%- include('partials/header', { modo: modo, base: base }) %>`) o EJS estoura
`Cannot access 'modo' before initialization` na LINHA do `const modo = ...` do
header. Não aparece no lint, só no render.

**Causa:** EJS transforma cada include-passado (`modo`, `base`) em variável
local da função de render do header. Redeclarar `const modo` dentro do mesmo
escopo entra em Temporal Dead Zone → erro em runtime.

**Correção:** não redeclare o nome; derive em outro:
```ejs
<%
  const _modo = (typeof modo !== 'undefined' && modo) ? modo
            : (rota.startsWith('/demo') ? 'demo' : rota.startsWith('/test') ? 'test' : 'app');
  const _base = (typeof base !== 'undefined' && base) ? base
            : (_modo === 'app' ? '' : '/' + _modo);
%>
```
Melhor ainda (padrão adotado): `selectDb` já joga `res.locals.currentPath`,
`res.locals.modo`, `res.locals.base` para TODAS as views → o header só consome
`modo`/`base` (locais) e usa direto, sem `const`.

**Verificação barata antes do rebuild:** harness temporário
`render-board-check.js`:
```js
const ejs=require('ejs'),fs=require('fs'),path=require('path');
const DICT=require('./src/config/i18n').DICT;
const t=l=>(k)=>(DICT[l][k]??DICT.pt[k]??k);
const vd=path.join(__dirname,'views');
const colunas=['planejado','em_andamento','pausado','concluido']
  .map(k=>({key:k,label:k,items:[{_id:'a1',name:'x',status:k}]}));
const h=ejs.render(fs.readFileSync(path.join(vd,'board.ejs'),'utf8'),
  {user:{name:'D',role:'user'},modo:'demo',base:'/demo',colunas,isDemo:true,
   mostraDemo:true,demoApi:'/api/demo/demo/load',t:t('pt'),currentPath:'/demo'},
  {views:[vd],filename:path.join(vd,'board.ejs')});
if(!h.includes('board-cards')) throw new Error('fail');
console.log('ok');
```
Rode `node render-board-check.js && rm render-board-check.js`. Pega o TDZ
antes de rebuildar o container.

## C) Rebuild obrigatório (recapitula seção 7 do SKILL.md)

Este template NÃO usa bind mount: o `Dockerfile` faz `COPY app/ ./` no build.
Editar `app/*` no disco não entra no container até:
```bash
docker compose build --no-cache app
docker compose up -d --force-recreate app
```
`docker compose restart` sozinho NÃO reaplica edições. Confirme com grep nas
rotas servidas (`curl -s http://<HostIp>:<Port>/ | grep '<marcador>'`), não só
screenshot. HostIp vem de `docker port <container>` (BIND_ADDR costuma ser
IP não-loopback; `curl 127.0.0.1:4450` dá exit 7 mesmo healthy).
