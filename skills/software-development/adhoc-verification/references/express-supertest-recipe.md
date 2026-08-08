# Express + supertest ad-hoc harness recipe (from financas-app session)

Context: an Express app (`createApp()`) gated by `process.env.DEMO_AUTOLOGIN`
and JWT secrets. We needed to prove (a) the demo autologin enters `/app`
without a password, (b) the demo landing `/` stays visible (does NOT redirect
to /app), and (c) a second instance (main, no autologin) rejects a cookie
minted by the demo instance.

## Key facts about THIS app (yours may differ — read first)
- `createApp()` reads `DEMO_AUTOLOGIN` + `NODE_ENV` at build time; middleware is
  only registered when `DEMO_AUTOLOGIN==='true' && NODE_ENV!=='production'`.
- One instance with autologin on applies `demoAutologin` to ALL paths except
  `/` (regex `^(?!\/$).*`). So a single instance will ALSO authenticate
  `/api/*` — that's why a single-instance "isolation" check is a false pass.
- Two real instances share the same origin (nginx :4460) in production; the bug
  class is "cookie from instance A leaks to instance B". Reproduce with two
  `createApp()` instances + a foreign-signed JWT.

## Gotchas that bit us (and are general)
1. Script in /tmp => `MODULE_NOT_FOUND` for supertest. Put it in `app/`.
2. Used `beforeAll`/`afterAll` from Jest => `ReferenceError` under bare `node`.
   Replaced with explicit `async` IIFE + `setupDb()`/`teardownDb()` from
   `tests/helpers/db`.
3. First assertion was wrong: "GET /api/dashboard with demo cookie => 401" is
   FALSE in a single demo instance (it re-authenticates). The real isolation
   check needs a second, non-autologin instance. Rewrote to two instances.

## Verification matrix that PASSED (3/3)
- DEMO + foreign cookie on `/demo/api/dashboard` => 200 (autologin overwrites,
  no 401).
- DEMO + GET `/` => 200 and landing text visible (no redirect to /app).
- MAIN (autologin off) + demo cookie on `/app` => not 200 (redirect to login).

Also ran canonical `npx jest --forceExit` => 227 passed, and `design.md lint`
=> 0 errors, to back the harness up.
