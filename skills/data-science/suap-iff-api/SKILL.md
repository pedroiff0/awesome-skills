---
name: suap-iff-api
description: Authenticate to and consume the SUAP IFF (Instituto Federal Fluminense) API v2 from the CLI — obtain the JWT access/refresh token via matricula+senha, then fetch student data (periodos letivos, dados do aluno, boletim). Use when the user has a suap.iff.edu.br matricula+senha and wants to extract academic data, integrate with the SUAP IFF API, or reference suap.iff.edu.br/api endpoints.
author: IFF Community
---

# SUAP IFF API (v2 / django-ninja)

## When to use
- User has a SUAP IFF matricula + senha and wants data programmatically (boletim, períodos, dados do aluno, calendário).
- User references `suap.iff.edu.br/api/...`.

## Key facts / pitfalls (learned the hard way)
- The SUAP instance is `https://suap.iff.edu.br` — NOT `suap.ifrn.edu.br`. They are different instances with different data. The IFRN docs/swagger describe the SAME django-ninja API shape, but the user's data lives on the IFF instance.
- Real API v2 endpoints are under `/api/ensino/...` (django-ninja), NOT `/api/v2/edu/...`. The `/api/v2/...` edu paths mostly 404.
- The WAF blocks requests with no `User-Agent` → returns **403 Forbidden** (nginx). ALWAYS send `-H "User-Agent: Mozilla/5.0"`.
- The auth endpoint does NOT use Basic Auth. Send `username` + `password` in the JSON body. (Sending Basic Auth or a `user_token` body first yields 422 "Field required".)

## Step 1 — Get the token
```bash
curl -s -X POST "https://suap.iff.edu.br/api/v2/autenticacao/token/" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Content-Type: application/json" \
  -d '{"username": "<MATRICULA>", "password": "<SENHA>"}'
```
Returns **HTTP 200** with:
```json
{"username": "<MAT>", "refresh": "<JWT>", "access": "<JWT>"}
```
Save it (e.g. `/tmp/suap_token.json`). The `access` JWT is what you send as Bearer.

## Step 2 — Use the token
```
Authorization: Bearer <access>
```

## Endpoints that WORK for a regular student profile (tested, real data)
| Method | Path | Result |
|---|---|---|
| GET | `/api/ensino/meus-periodos-letivos/` | 200, `{"results":[{"ano_letivo":2026,"periodo_letivo":1}, ...], "count":N}` |
| GET | `/api/ensino/aluno-matriculado/?matricula=<MAT>` | 200, `nome, matricula, curso, campus, periodo_atual, nascimento, cpf, foto_base64` |
| GET | `/api/ensino/meu-boletim/{ano_letivo}/{periodo_letivo}/` | 200 but `count:0` when no grades are posted (matches the empty UI) |

## Endpoints that do NOT return data for a regular student (tested)
| Path | Result | Note |
|---|---|---|
| `/api/ensino/meu-calendario-academico/{ano}/{periodo}/` | **404** on EVERY period | Not exposed for this profile — NOT a param error (schema wants integer ano + integer periodo_letivo) |
| `/api/ensino/meus-diarios/{ano}/{periodo}/` | **404** | Not exposed |
| `/api/ensino/meus-diarios-ead/` | **401** Unauthorized | Needs a different scope (OAuth2TokenAuth/TrustedAppAuth) |
| `/api/ensino/meus-dados-aluno/` | **500** | Server bug on the IFF instance (not auth) |
| `/api/ensino/meu-boletim/...` | 200 `count:0` | Empty when UI is empty (confirmed by user) |

The 404 on calendário across ALL 7 valid periods (with valid Bearer OR valid sessionid) means the IFF instance simply does not expose that endpoint for this profile. It is a server-side per-profile limitation, not a token/param mistake.

## Alternative auth: SessionAuth (web sessionid cookie)
If Bearer isn't enough, get a `sessionid` cookie by logging into the web login page and reuse it as `Cookie: sessionid=...`. Same endpoint limitations apply (calendário/diarios still 404/401) — the limit is server-side, not auth-method dependent.

```python
import urllib.request, urllib.parse, http.cookiejar, re
MAT, PW = "<MATRICULA>", "<SENHA>"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
html = op.open(urllib.request.Request('https://suap.iff.edu.br/accounts/login/',
           headers={'User-Agent':'Mozilla/5.0'})).read().decode('utf-8','ignore')
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html).group(1)
data = urllib.parse.urlencode({'csrfmiddlewaretoken':csrf,'username':MAT,
           'password':PW,'next':'/'}).encode()
op.open(urllib.request.Request('https://suap.iff.edu.br/accounts/login/', data=data,
      headers={'User-Agent':'Mozilla/5.0','Referer':'https://suap.iff.edu.br/accounts/login/',
               'Content-Type':'application/x-www-form-urlencoded'}))
sid = next(c.value for c in cj if c.name=='sessionid')
```

## Extracting boletim/calendário when the API is empty
The API returns empty/404 for boletim grades and calendário for this profile. That data DOES exist in the web UI (`/edu/...` area). Use authenticated scraping with the `sessionid` cookie (build the opener above, then GET the calendar/boletim page and parse the HTML). There is **NO `historico` endpoint** in the IFF API v2.

## Discovering exact paths/params
The IFRN instance serves its OpenAPI schema at `/api/openapi.json` (django-ninja). The IFF instance blocks it (403), but the API shape is identical. Download it from IFRN to learn exact paths/schemas, then filter paths containing: `boletim, periodo, aluno, histor, nota, disciplina, calendario, diario, ensino`.

## Minimal Python helper (token + periods + aluno)
```python
import json, urllib.request, urllib.error
BASE="https://suap.iff.edu.br"
def auth(mat,pw):
    req=urllib.request.Request(BASE+"/api/v2/autenticacao/token/",
        data=json.dumps({"username":mat,"password":pw}).encode(),
        headers={"User-Agent":"Mozilla/5.0","Content-Type":"application/json"})
    return json.loads(urllib.request.urlopen(req).read())
def get(path, token):
    H={"User-Agent":"Mozilla/5.0","Accept":"application/json",
       "Authorization":f"Bearer {token['access']}"}
    return json.loads(urllib.request.urlopen(
        urllib.request.Request(BASE+path, headers=H)).read())
# t=auth("<MAT>","<PW>")
# print(get("/api/ensino/meus-periodos-letivos/", t))
# print(get(f"/api/ensino/aluno-matriculado/?matricula=<MAT>", t))
```
