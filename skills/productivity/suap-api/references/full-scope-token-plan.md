# Full-scope token plan — reaching SUAP histórico via API

Goal: pull the academic transcript (and other full-scope data) through the
**API only** (no scraping), because the consumer is an app that syncs data
automatically for the user.

## Why the simple token fails
- `POST {base}/api/v2/autenticacao/token/` with matrícula+senha yields a JWT
  with only basic-read scope.
- With it: `meus-periodos-letivos/` OK, `aluno-matriculado/` OK, but
  `meu-boletim/{ano}/{periodo}` returns `count:0` for every period, and every
  historico/componentes-cursados candidate 404s.

## Step 1 — obtain a full-scope token via Swagger UI
1. Open `{base}/api/docs/` in a browser.
2. Click "Django login" -> authenticate with matrícula + senha (normal web
   login, not the token endpoint).
3. Click "Authorize" -> copy the Bearer token shown.
4. Export it: `export SUAP_FULL_TOKEN="<token>"`

## Step 2 — retest with the full-scope token
Probe each with `Authorization: Bearer $SUAP_FULL_TOKEN` and
`User-Agent: Mozilla/5.0`:
- `GET /api/ensino/meu-boletim/{ano}/{periodo}/` for the periods from
  `meus-periodos-letivos/` — does it now return the transcript rows?
- `GET /api/ensino/meu-historico/`
- `GET /api/ensino/historico/`
- `GET /api/ensino/aluno/{mat}/historico/`
- `GET /api/ensino/meus-componentes/`
- `GET /api/ensino/componentes-cursados/`
- `GET /api/ensino/meu-calendario-academico/{ano}/{periodo}/`

Some of these 404 ONLY because the simple token hides them; the full-scope
token may reveal them. Record which actually return data.

## Step 3 — if the API still has no historico
Open a ticket with the institute SUAP team (IFF) / upstream (IFRN) requesting
the `historico` (or `componentes-cursados`) v2 endpoint, or scope grant for
your app client. There is currently NO documented public historico endpoint.

## Note on the scraper
`references/scrape-historico.py` works for a manual one-off human pull (it
logs in via `/accounts/login/` and parses the `?tab=historico` table). It is a
STOPGAP ONLY — do not use it as the app integration.
