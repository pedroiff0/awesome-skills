---
name: suap-api
description: Consume the SUAP (Sistema Unificado de Administração Pública) REST API v2 used by Brazilian federal institutes (IFRN, IFF, IFS, etc.) — obtain a JWT via /api/v2/autenticacao/token/, discover real endpoints via /api/openapi.json, and pull student data (boletim, períodos letivos, dados do aluno). Covers the WAF User-Agent gotcha, the username/password JSON body format (NOT Basic Auth), the /api/ensino/ path layout, and the scope limits of the simple token. Use whenever a user wants to script/automate access to SUAP academic data with matrícula + senha, or debug a 403/422/400 from the SUAP token endpoint.
---

# SUAP API (v2) access

SUAP is the unified admin system used by many Brazilian federal institutes. IFRN developed it; other institutes (IFF, IFS, ...) run their own instances, each with its own base URL (e.g. `https://suap.iff.edu.br`, `https://suap.ifrn.edu.br`). The API is django-ninja (Swagger UI at `/api/docs/`). The API surface and auth behaviour differ slightly per instance — always verify against that instance's live `/api/openapi.json`.

## Auth flow (the critical part)
Token endpoint: `POST {base}/api/v2/autenticacao/token/`.

**Gotcha 1 — WAF blocks a missing User-Agent.** Without a `User-Agent` header the nginx/WAF returns `403 Forbidden` immediately (looks like a hard block, but it's just the UA). Always send `User-Agent: Mozilla/5.0`.

**Gotcha 2 — body is username/password, NOT Basic Auth.** The IFRN `suapi` example and some docs suggest Basic Auth, but the IFF instance returns `422` ("missing user_token") for Basic Auth and `400` ("username is required", "password is required") when those keys are absent. Working request:
```
curl -s -X POST "{base}/api/v2/autenticacao/token/" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Content-Type: application/json" \
  -d '{"username": "<matricula>", "password": "<senha>"}'
```
Response (HTTP 200): `{"username": "...", "refresh": "<JWT>", "access": "<JWT>"}`. Use the **`access`** JWT as the Bearer token: `Authorization: Bearer <access>`.

## Discovering the real endpoints
Old docs/examples use paths like `/api/v2/edu/alunos/{mat}/` — these return `404` on the IFF instance. The actual student endpoints live under `/api/ensino/...`. To get the authoritative, current path list for an instance, fetch its OpenAPI spec (the spec URL hides inside the `/api/docs/` HTML as `/api/openapi.json`):
```
curl -s "{base}/api/openapi.json" -o openapi.json
```
Then inspect `paths` for keywords (boletim, periodo, aluno, historico, nota, disciplina) and read `components.securitySchemes` (it's `JWTAuth`/bearer). Loop over each candidate path with the Bearer token to see what actually returns data.

## Verified student endpoints (IFF instance)
- `GET /api/ensino/meus-periodos-letivos/` → `[{ano_letivo, periodo_letivo}, ...]` (paged `results`). ✅ real data.
- `GET /api/ensino/aluno-matriculado/?matricula=<mat>` → nome, curso, campus, periodo_atual, nascimento, cpf, foto_base64. ✅ real data.
- `GET /api/ensino/meu-boletim/{ano_letivo}/{periodo_letivo}/` → paged `{results:[], count, next, previous}`. Returns `200` but `count:0` when no grades are posted (this matches an empty SUAP UI — not an error).
- `GET /api/ensino/meu-calendario-academico/{ano}/{periodo_letivo}/` → `404` for every period with the simple JWT (scope-limited, see below).
- `GET /api/ensino/meus-dados-aluno/` → `500` (server bug on IFF, not an auth problem).

## Scope limits of the simple token
The JWT from `/autenticacao/token/` grants only basic read. Endpoints needing broader scope return `401`/`404`:
- `meu-calendario-academico` → 404 on all periods (no scope for this token).
- `meus-diarios-ead` → 401.
- There is **no `historico` (academic transcript) endpoint** in the IFF v2 API at all. Probed candidates `/api/ensino/meu-historico/`, `/api/ensino/historico/`, `/api/ensino/aluno/{mat}/historico/`, `/api/ensino/meus-componentes/`, `/api/ensino/componentes-cursados/` → all 404.
- `meu-boletim/{ano}/{periodo}` returns HTTP 200 but `count:0` for every period with the simple token — it only exposes POSTED grades, not the full transcript. So the v2 API CANNOT reconstruct the history with this token.

## USER INTENT — API-ONLY, no scraping for app sync
When the goal is to import SUAP data into an application and SYNC it automatically for the user, **scraping is NOT an acceptable solution** — it breaks on any layout change, has no stable contract, and cannot be relied on for a sync job. The only sanctioned path for an app is the **API with a full-scope token**. Do NOT fall back to scraping as "the answer" just because it happens to work in a one-off shell session. If the API cannot deliver the data with the available token, say so plainly and pivot to obtaining broader scope (below) — do not hand over a scraper as the deliverable.
> A working scraper (references/scrape-historico.py) exists and is fine for a **manual one-off human pull**, but treat it as a stopgap, never as the integration.

## Path forward: getting histórico (and other full-scope data) via API
The simple matrícula+senha token is insufficient. To reach historico/calendario/diarios via API you need a token with broader scope:
1. **Generate a full-scope token at the Swagger UI**: open `{base}/api/docs/`, click "Django login" (authenticate with matrícula+senha), then "Authorize". The resulting Bearer token carries the scopes the simple JWT lacks. Retest `meu-boletim/{ano}/{periodo}` (may now return the transcript) and re-probe the historico/componentes-cursados candidates — some endpoints 404 only because the simple token hides them, not because they don't exist. See `references/full-scope-token-plan.md` for the exact retest checklist.
2. **Request scope from support**: open a ticket with the institute's SUAP team (IFF) or the upstream maintainer (IFRN) asking them to expose `historico` (or `componentes-cursados`) in the v2 API, or to grant your app client the needed scope. There is currently no documented public historico endpoint, so this may be the only durable route.

## (Manual stopgap only) Recovering the transcript via web scraping
The full history IS available at the authenticated web page `/edu/aluno/{matricula}/?tab=historico`. The login web page has a reCAPTCHA, BUT a plain `POST /accounts/login/` with `csrfmiddlewaretoken` + `username` + `password` + `next` passes straight through (no captcha token needed) — the reCAPTCHA is a front-end gate only. After login, the session cookie lets you GET the history page; the table is server-rendered in the `data-tab="historico"` pane (no AJAX needed for the HTML).

Parsing the history table (verified on IFF, 39 rows):
- The pane contains one `<table>`; relevant `<tr>` rows have 9 `<td>`:
  `[Ano Letivo, Período do Curso, '-', Código, Componente+Prof, C.H., Nota/Conceito, % Freq., Situação]`.
- Filter rows where `td[0]` matches `^\d{4}/\d$` (skips header/separator rows).
- The Componente cell is `"NOME DA DISCIPLINA Nome do Professor ( Titulacao )"` — collapse whitespace first (the `( Titulacao )` sits after a `\n`), then strip the trailing `( Titulacao )` and split the disciplina (ALL-CAPS) from the professor (Title-Case) at the case transition.
- Requires `beautifulsoup4` + `lxml`. See `references/scrape-historico.py` for a working script. **Manual use only — not for app sync.**

## See also
- `references/full-scope-token-plan.md` — the API-only path to histórico: get a full-scope token from Swagger UI and the exact retest checklist. Use this for app-sync work.
- `references/scrape-historico.py` — working web scraper (manual one-off pull only, NOT for app integration).
- `references/auth-and-endpoints.md` — a copy-paste Python probe that logs in, prints períodos letivos, pulls aluno-matriculado, and probes boletim for the first periods.
