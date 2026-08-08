# financas-app: one port (4460), demo under /demo, three DBs

Goal: single published port; demo reachable by button on the landing page with
its own database; principal instance (test or prod) chosen via .env.

## docker-compose.yml (project `fa`, so `fa_mongo_data` volume survives)
```yaml
name: fa
services:
  mongo:
    image: mongo:7
    restart: unless-stopped
    volumes: [mongo_data:/data/db]
  mongo-demo:
    image: mongo:7
    restart: unless-stopped
    tmpfs: /data/db
  app:
    build: { context: ., dockerfile: app/Dockerfile }
    depends_on: [mongo]
    environment:
      NODE_ENV: ${NODE_ENV:-development}
      PORT: 5000
      MONGO_URI: ${MONGO_URI:-mongodb://mongo:27017/financas_test_db}
      MONGO_URI_DEMO: mongodb://mongo-demo:27017/financas_demo_db
      DEMO_AUTOLOGIN: "false"
    networks: [interna]
  app-demo:
    build: { context: ., dockerfile: app/Dockerfile }
    depends_on: [mongo-demo]
    environment:
      NODE_ENV: staging
      PORT: 5000
      MONGO_URI: mongodb://mongo-demo:27017/financas_demo_db
      JWT_SECRET: ${JWT_SECRET_DEMO:-...}
      DEMO_AUTOLOGIN: "true"
      RATE_LIMIT_DISABLED: "true"
    networks: [interna]
  nginx:
    image: nginx:1.27-alpine
    depends_on: [app, app-demo]
    ports: ["${BIND_ADDR:-127.0.0.1}:4460:5000"]
    volumes: [./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro]
    networks: [interna]
networks: { interna: { driver: bridge } }
volumes: { mongo_data: }
```
Note: only `nginx` publishes a host port. `app` and `app-demo` are internal.

## nginx/default.conf
```
upstream financas_app { server app:5000; }
upstream financas_demo { server app-demo:5000; }
server {
  listen 5000;
  # Keeps the /demo redirect RELATIVE. Without this nginx rewrites the
  # Location with its own listen port (5000) and the browser hits a dead
  # port outside the host. See SKILL.md "CRITICAL" note.
  absolute_redirect off;
  port_in_redirect off;
  location = /demo { return 302 /demo/app; }
  location /demo/ { proxy_pass http://financas_demo/; }
  location / { proxy_pass http://financas_app; }
}
```

## app/src/app.js — mount demo routes under /demo when DEMO_AUTOLOGIN
```js
if (process.env.DEMO_AUTOLOGIN === 'true' && env.nodeEnv !== 'production') {
  app.use('/demo/api', apiLimiter);
  app.use('/demo/api', csrfGuard);
  app.use('/demo/api', apiRoutes);
  app.use('/demo', pageRoutes);
}
```
Plus: the autologin middleware sets `res.locals.apiPrefix = '/demo'` so the
EJS layout can emit `data-api-prefix="/demo"` (see express-csp-runtime-config
skill — do NOT use an inline script for this).

## Seed the demo (manual; tmpfs resets on restart)
`docker compose -p fa exec app-demo node scripts/seed-demo.js`

## Verify
- `curl -o /dev/null -w '%{http_code}' http://127.0.0.1:4460/`            → 200
- `curl -o /dev/null -w '%{http_code}' http://127.0.0.1:4460/demo/app`    → 200 (autologin)
- `curl -o /dev/null -w '%{http_code}' http://127.0.0.1:4460/demo/admin` → 403
- `curl -o /dev/null -w '%{http_code}' http://127.0.0.1:4460/app`         → 302 (login)
- With autologin cookie: `/demo/api/dashboard` → 200; `/api/dashboard` → 401.

## Demo autologin gotchas (real bugs hit in financas-app)
1. **Frontend helper not defined → "Can't find variable: txt".** If a shared
   DOM helper (`txt`, `sinal`, `formatarMoeda`, `hojeISO`, ...) is used by a
   page's JS but only DEFINED inside another page's IIFE (e.g. `investimentos.js`
   defined `txt`/`sinal` but `dashboard.js` used them 17x with no definition),
   the browser throws at load and the dashboard KPIs never render. Audit with:
   `for f in $(grep -rl "document.addEventListener" --include=*.js .); do
    for h in txt sinal hojeISO formatarMoeda; do u=$(grep -c "$h(" "$f");
    d=$(grep -c "const $h \|function $h\|$h =" "$f");
    [ "$u" -gt 0 ] && [ "$d" -eq 0 ] && echo "$f usa $h mas nao define"; done; done`
   Globals loaded by the layout (financas-lib.js) are fine; IIFE-local ones are not.
2. **Autologin middleware order.** Register `demoAutologin` BEFORE the
   `/demo/api` and `/demo` mounts (so it populates `req.user` and re-emits the
   demo cookie before `auth`/`pageAuth` run), but exclude the root `/` with a
   regex `app.use(/^(?!\/$).*/, demoAutologin)` so the landing stays visible on
   the demo instance. It must be gated by `DEMO_AUTOLOGIN==='true' &&
   nodeEnv!=='production'` so it never exists in prod.
3. **pageAuth must trust an already-populated req.user.** When `demoAutologin`
   set `req.user`, `pageAuth` should short-circuit (`if (req.user) { res.locals.user
   = req.user; return next(); }`) and NOT re-resolve the token — otherwise a
   cookie from the PRINCIPAL instance (same origin 127.0.0.1:4460) is validated
   against the demo DB and rejected with 401 "Token invalido".
*** End Patch