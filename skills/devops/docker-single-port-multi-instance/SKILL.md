---
name: docker-single-port-multi-instance
description: "Consolidate multiple Docker Compose app instances (production / test / demo) behind ONE host port using an nginx reverse proxy that routes by URL path prefix (e.g. /demo). Use when a user wants 'one port, several apps/banks' or a demo reachable simultaneously from the main landing page with its own database."
author: Docker / DevOps Community
---

# One port, many instances: nginx reverse proxy by path prefix

## When this applies
- You have an app that runs as several instances: production, test, and a
  public demo — each with its OWN database.
- The user asks for a single published port (e.g. 4460) where the demo is
  reached by clicking a button on the landing page, and the demo's data lives
  in its own DB, isolated from prod/test.
- Key constraint: the demo must be reachable SIMULTANEOUSLY with the main app.

## Prefer nginx-by-prefix over in-app multi-tenancy
When the ONLY goal is routing separate instances, do NOT refactor the app to
hold two DB connections (e.g. a second mongoose connection) just to serve
/demo/* from the same process. That touches ~30 files (every model + service +
controller) and risks regressing the normal routes. Instead:

- Keep each instance as its own container (own DB, own env).
- Put ONE nginx container on the public port; it routes:
  - `/demo/*`  → `app-demo`  (strip prefix: `proxy_pass http://app-demo:5000/;`)
  - `/` (rest) → `app`        (the principal: test or prod chosen via .env)
- The demo container keeps its existing autologin; the button on the landing
  just points to `/demo/app`.

This delivers "one port, demo with own DB, simultaneous" with near-zero risk
to the main app's logic.

## The non-obvious gotcha: APIs must also be prefixed
If the demo is served under `/demo/*` but its client JS calls `/api/...`
(absolute), the proxy sends those calls to the PRINCIPAL instance, not the
demo → tokens fail (401 "Token invalido"). You must route the demo's APIs to
the demo instance too:

1. Mount the demo's API router under `/demo/api` in the app (only when a
   DEMO_AUTOLOGIN-style flag is set), in addition to the normal `/api`.
2. Make the frontend prefix API calls with `/demo` when running in the demo.
   Inject the prefix WITHOUT an inline script (CSP will block it — see the
   express-csp-runtime-config skill): use `data-api-prefix="/demo"` on `<html>`
   and read it with `getAttribute` inside the shared fetch wrapper.

nginx location block:
```
location = /demo { return 302 /demo/app; }
location /demo/ { proxy_pass http://app-demo:5000/; }
location / { proxy_pass http://app:5000; }
```

## CRITICAL: make the `/demo` redirect relative (absolute_redirect off)
The snippet above is subtly broken in production. When nginx `listen`s on the
INTERNAL port (e.g. 5000, mapped to 4460 on the host) and you `return 302
/demo/app`, nginx builds an ABSOLUTE `Location: http://host:5000/demo/app`
using the listen port — not the port the browser used (4460). The user's
browser is then thrown at a port that does not exist outside the host, and
`/demo` appears dead even though `/demo/app` works directly.

Fix: disable absolute redirects in the `server` block so the `Location`
stays relative (`/demo/app`) and the browser resolves it against the real
port:
```nginx
server {
  listen 5000;
  absolute_redirect off;   # keep Location relative -> /demo/app
  port_in_redirect off;    # belt-and-suspenders, drop the port entirely
  location = /demo { return 302 /demo/app; }
  location /demo/ { proxy_pass http://app-demo:5000/; }
  location / { proxy_pass http://app:5000; }
}
```
Verify with `curl -s -D - -o /dev/null URL/demo | grep -i location` — it must
show `Location: /demo/app` (NO `:5000`), never `http://host:5000/demo/app`.
If you see `:5000`, the config did not take: rebuild the nginx image and
`docker compose up -d --force-recreate nginx` (a plain `up` may not replace it).

## docker-compose shape
- One file, project name preserved (so named volumes survive, e.g. `fa_mongo_data`).
- Services: `app`, `app-demo`, `mongo`, `mongo-demo` (tmpfs for demo), `nginx`.
- Only `nginx` publishes the host port. `app` and `app-demo` have NO host port
  (internal network only).
- Demo DB on tmpfs so it resets on restart; seed manually via
  `docker compose exec app-demo node scripts/seed-demo.js`.

## Pitfall: nginx serves STALE routing after a sibling container rebuild
After you `docker compose build app app-demo` (or `up -d app app-demo`) to push
a code change, the demo can suddenly break even though the app code is correct:
`/demo/veiculos` (and any `/demo/*` page) returns `302 -> /login`, and the demo
API `/demo/api/*` returns `401`. The container `app-demo` is healthy and answers
`200` when hit DIRECTLY on its internal IP:port, but via the published port it
fails. Root cause: **the nginx container never re-read its `default.conf`** — it
kept the in-memory routing from before the rebuild and is sending `/demo/*` to
the PRINCIPAL instance (which has no demo autologin → 302 /login).

Tell-tale sign (this is the key diagnostic): hit `/demo/veiculos` through the
published port, then check BOTH app logs. If **neither** `app` nor `app-demo`
logged the request but nginx returned a 302 with the app's CSP headers, the
request never reached an app — nginx generated the redirect itself from a stale
`location`/`return`. (Add a one-line `console.log('[mw]', req.path)` at the top
of the demo autologin middleware to confirm whether the demo instance even saw
the request; remove it after.)

Fix (cheapest first):
1. `docker compose restart nginx` — forces nginx to re-read `default.conf`.
   Re-test `/demo/veiculos` → should now be `200` and the autologin middleware
   should log `path= / host= <published-host>`.
2. If restart alone doesn't take, rebuild + recreate the image:
   `docker compose build nginx && docker compose up -d --force-recreate nginx`.
Do NOT reach for `docker compose down -v` — that wipes named volumes (e.g.
`fa_mongo_data`); the HANDOFF explicitly forbids it.

Why this happens: `up -d app app-demo` recreates those services but leaves the
long-running `nginx` container untouched, and nginx does not hot-reload its config
on a sibling's restart. A plain `restart` re-reads the (already-correct, baked-into
the-image) conf.

## Verify server-side (don't trust a caching browser)
The inspection browser may keep stale HTML/JS across navigations and report
phantom 401s even after a correct rebuild. Validate at the HTTP layer instead:
1. Capture the autologin Set-Cookie: `CK=$(curl -s -i URL/demo/app | grep -i set-cookie | ...)`.
2. Call the demo API WITH that cookie:
   `curl -o /dev/null -w '%{http_code}' --cookie "$CK" URL/demo/api/dashboard`
   → expect 200. The same cookie against `/api/dashboard` (no prefix) → 401
   (hits principal). That pair proves routing + auth are correct.
3. If a `/demo/*` PAGE returns 302 /login, run the stale-routing diagnostic
   above BEFORE suspecting app code — 9 times out of 10 it's the nginx conf
   not being reloaded.

## Reference
See references/nginx-demo-example.md for a concrete financas-app
docker-compose.yml + nginx/default.conf + app.js mount snippet.
