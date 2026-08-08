# Arquitetura da demo (porta única 4460)

## Roteamento (nginx → compose)
- `nginx/default.conf`: `/demo/*` → `app-demo`; `/*` → `app`. `absolute_redirect off`
  (senão o Location vem com `:5000` interno e o browser cai em porta inexistente).
- `app-demo` registra rotas em `/` E em `/demo` (páginas `/demo/*`, APIs `/demo/api/*`).
  O `demoAutologin` popula `res.locals.apiPrefix='/demo'` para o header injetar
  `data-api-prefix` no `<html>`.

## Autologin (app-demo)
- `src/middleware/demoAutologin.js`: a cada request gera JWT fresco (iat=now) para o
  usuário demo (role `user`, sem acesso a /admin). Ignora cookie de outra origem (mesma
  origem 127.0.0.1:4460) e repõe `req.cookies.token` para o pageAuth confiar.
- Só existe com `DEMO_AUTOLOGIN=true` e `NODE_ENV !== 'production'`.

## Reset da demo
- `POST /demo/api/reset-demo` (controller `resetDemo`): drop de coleções + `semearDemo()`.
  Usa `authOptional` (conclui mesmo com token inválido).
- No frontend (`common.js`): "sair" na demo chama `/api/reset-demo` (prefixado p/ `/demo/api/...`)
  e redireciona para `/demo/app`. Não vai para /login.
- `mongo-demo` usa VOLUME (persiste entre reinícios; seed roda no boot se `SEED_DEMO=true`
  ou via `docker compose exec app-demo node scripts/seed-demo.js`). HANDOFF antigo dizia
  tmpfs — isso está DESATUALIZADO (issue #20).

## Como subir / validar
```bash
cd /home/pedro/Repositorios/pessoal/financas-app
ASSET_VERSION=$(git rev-parse --short HEAD) docker compose -p fa up -d --build
# seed manual da demo:
docker compose -p fa exec app-demo node scripts/seed-demo.js
```
- Containers: `fa-app-1`, `fa-app-demo-1`, `fa-mongo-1`, `fa-mongo-demo-1`, `fa-nginx-1`.
- Verificação server-side: `/` → 200; `/demo` → 302 → `/demo/app`; `/demo/app` → 200;
  `/demo/admin` → 403; `/app` → 302 (login). Com cookie demo: `/demo/api/dashboard` → 200.
