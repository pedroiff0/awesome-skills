# Load testing the template (k6, dockerized)

Everything here was measured, not estimated. Reproduce before quoting.

## Layout

```
loadtest/carga.js          k6 scenario (5 profiles, thresholds)
loadtest/resultados/       artifacts (gitignored)
app/scripts/seed-carga.js  synthetic users, test-DB-only guard
docker-compose.test.yml    isolated stack + k6 service (profile "carga")
.github/workflows/carga.yml  manual / weekly, uploads summary
docs/load-testing.md       the user-facing writeup
```

## Run it

```bash
docker compose -f docker-compose.test.yml -p pp-test up -d --build
docker compose -f docker-compose.test.yml -p pp-test \
  exec -T app-test node scripts/seed-carga.js 50
docker compose -f docker-compose.test.yml -p pp-test --profile carga \
  run --rm -e PERFIL=carga -e CARGA_VUS=100 -e DURACAO=1m k6 run /scripts/carga.js
docker compose -f docker-compose.test.yml -p pp-test down -v
```

`k6` sits behind a Compose `profiles: ["carga"]` so a plain `up` doesn't start
it. Seeding hashes the password **once** and reuses it across all users —
bcrypt 12 × 50 users would otherwise take ~15s.

## Profiles

| Profile | Purpose | Shape |
|---|---|---|
| `smoke` | scenario sanity | 1 VU, 20s |
| `carga` | steady-state capacity | ramp → plateau → down |
| `estresse` | find saturation | 100 → 300 → 600 → 1000 |
| `pico` | elasticity | 10 → N in 5s |
| `auth` | worst case, login every iteration | CPU-bound by design |

Thresholds (crossing one exits non-zero, failing CI):

```
http_req_failed                    < 1%
http_req_duration{tipo:leitura}    p95 < 300ms
http_req_duration{tipo:pagina}     p95 < 500ms
http_req_duration{tipo:login}      p95 < 2000ms
login_sucesso                      > 99%
```

## Measured results

Intel i5-9400F (6 cores), 15 GiB, single app instance, Mongo 7 on tmpfs, k6 on
the same host (so these are a conservative floor).

| Load | Errors | Throughput | read p95 | Verdict |
|---|---|---|---|---|
| 1 VU (smoke) | 0% | — | 5 ms | pass |
| **100 VUs** | **0.00%** | **214 req/s** | 287 ms | **all thresholds pass** |
| 200 VUs | 0.00% | 262 req/s | 989 ms | no errors, latency over target |

Auth-only profile: 10 VUs → 2.5 logins/s, p95 2.71s · 50 VUs → 3.6 logins/s,
p95 28s. Classic CPU saturation: more concurrency only grows the queue.
Sustainable ≈ **4.5 logins/s per instance**.

Idle resources: app 50 MiB RAM / 0.13% CPU; mongo 439 MiB / 42.9% CPU.

Under overload the platform **queues and serves** rather than dropping
requests — 0% errors even at 200 VUs. Only latency degrades.

## Interpreting VUs

A k6 VU pauses 1s between iterations; a human pauses tens of seconds. Using a
conservative 1 VU ≈ 10 real active users:

| Setup | VUs | Real users (est.) |
|---|---|---|
| 1 instance (measured) | 100 | ~1,000 |
| 1 instance (no-error ceiling) | 200 | ~2,000 |
| 4 instances behind LB | ~400 | ~4,000 |

## How to raise capacity

1. **Scale horizontally** — stateless JWT, no in-memory session. Best ratio.
2. Longer token TTL → fewer logins/day (weigh against exposure window).
3. bcrypt 12 → 11 halves login cost. **Security trade-off, decide explicitly.**
   12 stays the default.
4. Serve static assets via CDN/nginx.
5. Check Mongo query plans when adding domain collections.

## Traps that cost time here

- **Login every iteration = login-storm.** First version did this: 200 VUs hit
  60s latency and 6% errors. Fixed by reusing the token per VU; the worst case
  now lives in the `auth` profile. This flipped the result from "broken" to
  "0% errors".
- **k6 container UID can't cross a `0700` home** to read the bind mount →
  "permission denied". Fix with `user: "0:0"` on the throwaway container.
- **Rate limiter would dominate the numbers** (300 req/5min). Disable via env
  *in staging only*; `env.js` throws if that flag appears under production.
- **`docker compose config` needs `JWT_SECRET` exported**, otherwise it fails
  quietly and greps against empty output pass by accident.
- **`grep 'app_db'` matches `app_test_db`** — assert on the full URI.
- **Auth thresholds follow the auth config.** The `login` p95 threshold and the
  `TOTAL_USUARIOS`/seed count assume the login path is reachable. After
  tightening the IP rate limit (now 3/30min by default) the load stack still
  works only because it runs with `RATE_LIMIT_DISABLED=true` under `staging`.
  If a future run suddenly reports a wall of 429s, check that flag first — the
  scenario is measuring the limiter, not the app.

## Host ports (current)

Production `127.0.0.1:4447`, test/load `127.0.0.1:4446`; containers still
listen on 5000 internally. `loadtest/carga.js` defaults `BASE_URL` to
`localhost:4446` for host-side runs, but inside Compose it targets
`http://app-test:5000` over the Docker network.
