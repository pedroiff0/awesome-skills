# Security baseline — rationale

Why each control exists in the template. Keep these when deriving a project;
removing one should be a conscious, documented decision.

## Passwords

- **bcrypt cost 12.** No SHA/MD5. Never store or log plaintext.
- **`passwordHash` uses `select: false`** so no accidental query leaks it.
  Requires `.select('+passwordHash')` wherever a compare happens.
- **Policy: min 12 chars with lower + upper + digit**, and the new password
  must differ from the current one.
- **Temporary passwords** (account creation, admin reset): 18 random bytes
  (~144 bits) base64url, returned exactly once in the HTTP response. Never
  persisted in plaintext, never logged.

## Sessions

- JWT HS256, 2h default. Cookie `httpOnly` + `SameSite=Lax` for browsers,
  `Authorization: Bearer` for API clients.
- **Token in query string is rejected by design** — it leaks into proxy logs
  and the `Referer` header.
- `JWT_SECRET` required in production (min 32 chars); boot fails rather than
  falling back to an insecure default.
- **`tokenValidAfter`** on the user document is the revocation mechanism for
  otherwise-stateless JWTs. Bumped on password change, reset, and deactivation.
  Compare in SECONDS against `iat` (see pitfall 1 in SKILL.md).

## Anti-enumeration

- Login always answers `Credenciais invalidas` (401) — nonexistent email,
  wrong password and inactive account are indistinguishable.
- When the user doesn't exist, still run `bcrypt.compare` against a module-level
  dummy hash so response time matches.
- `/forgot-password` returns the same message whether or not the account exists.

## Brute force

- Per-account lockout: 5 failures → 15 min (429).
- Per-IP rate limits: 10 req/15min on login+reset, 300 req/5min on the API.
- Limiters and `csrfGuard` self-disable under `NODE_ENV=test` — Supertest is
  not a browser and the suite would rate-limit itself.
- Not a substitute for WAF/CDN against distributed attacks.

## Injection

- **NoSQL**: `sanitizeInput` strips keys starting with `$` or containing `.`
  from body/query/params recursively, with a depth cap. Second layer: Zod
  forces types. Without it, `{"email": {"$gt": ""}}` becomes a query operator.
- **ReDoS**: escape regex metacharacters before building a `RegExp` from
  user-supplied search text.
- **XSS**: CSP with no `unsafe-inline`; EJS `<%= %>` (escaped) everywhere;
  front-end escapes any DB value with `escapeHtml()` before `innerHTML`.
  Never `<%- %>` with user content.
- **CSRF**: `SameSite=Lax` + `csrfGuard` checking Origin/Referer on
  cookie-authenticated mutations. Bearer requests carry no cookie and are
  excluded — they aren't a classic CSRF target.

## Authorization invariants

- `auth` (API, 401 JSON) and `pageAuth` (pages, redirect to /login).
- `requireRole('admin')` always AFTER `auth`.
- `requirePasswordChanged` gates navigation until a provisioned account sets
  its own password.
- **At least one active admin must always exist.** An admin cannot demote or
  deactivate their own account, nor the last active admin. Enforced in
  `userService.atualizarUsuario`, covered by test.

## Transport / headers

Helmet: CSP, `frame-ancestors 'none'`, `object-src 'none'`,
`referrer-policy: same-origin`, `x-powered-by` off. `trust proxy` set to 1 hop
— increase it if there are more proxy layers, otherwise rate limiting sees only
the proxy IP.

## Auditing

`AuditLog` records login success/failure, logout, password change/reset and
admin account operations: actor, target, IP, user-agent. Never password, token
or hash. 180-day TTL index. Writes are best-effort — an audit failure must
never break the main request.

## Incident response

Rotating `JWT_SECRET` invalidates every session at once. That's the correct
response to suspected leakage; warn users they'll need to log in again.
