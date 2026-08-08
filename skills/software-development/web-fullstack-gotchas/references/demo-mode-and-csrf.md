# Demo mode + CSRF: testing the multi-instance API with curl

This template runs `app`/`test`/`demo` on ONE port via route prefix (`/api`,
`/api/test`, `/api/demo`), each with its own DB selected by `selectDb`. The
demo user auto-logs in via `/demo/start` and should be able to CRUD the whole
demo DB (but not users).

## 1. Get a demo cookie (auto-login redirect)

```bash
curl -s -c /tmp/demo.cookies -o /dev/null -w '%{http_code} -> %{redirect_url}\n' \
  'http://<HostIp>:<Port>/demo/start'
# 302 -> http://<HostIp>:<Port>/demo/
```
The jar now has the httpOnly JWT cookie scoped to the demo instance.

## 2. Read the board (server-rendered)

```bash
curl -s -b /tmp/demo.cookies -o /tmp/board.html -w '%{http_code}\n' 'http://<HostIp>:<Port>/demo/'
grep -c 'tcard' /tmp/board.html      # cards rendered?
grep -o '/demo/painel' /tmp/board.html   # nav mode-aware?
```

## 3. CREATE via the API (the curl/CSRF trap)

A bare curl POST hits **403 "Requisicao bloqueada (origem ausente)"** because
`csrfGuard` (mounted on `/api`) requires an `Origin` header matching `Host`.
curl never sends `Origin`. The browser's `apiRequest` (with
`credentials:'same-origin'`) does send it, so this 403 is a TEST artifact only.

```bash
H=http://<HostIp>:<Port>
# CREATE a task (note the /api/demo prefix — NOT /api)
curl -s -b /tmp/demo.cookies -X POST "$H/api/demo/tasks" \
  -H "Origin: $H" -H 'Content-Type: application/json' \
  -d '{"titulo":"Tarefa de teste","status":"planejado","projetoId":null,"profissionalId":null,"tags":["teste"]}' \
  -w '\nHTTP %{http_code}\n'

# CREATE a project
curl -s -b /tmp/demo.cookies -X POST "$H/api/demo/projects" \
  -H "Origin: $H" -H 'Content-Type: application/json' \
  -d '{"name":"Projeto teste","description":"x","tags":[]}' -w '\nHTTP %{http_code}\n'

# CREATE a professional
curl -s -b /tmp/demo.cookies -X POST "$H/api/demo/professionals" \
  -H "Origin: $H" -H 'Content-Type: application/json' \
  -d '{"nome":"Ana Teste","funcao":"Dev","contato":"a@x.com"}' -w '\nHTTP %{http_code}\n'

# MOVE a task (PATCH status)
curl -s -b /tmp/demo.cookies -X PATCH "$H/api/demo/tasks/<ID>" \
  -H "Origin: $H" -H 'Content-Type: application/json' \
  -d '{"status":"concluido"}' -w '\nHTTP %{http_code}\n'

# Set weekly goal (meta) + log a Pomodoro focus session
curl -s -b /tmp/demo.cookies -X PATCH "$H/api/demo/meta" \
  -H "Origin: $H" -H 'Content-Type: application/json' -d '{"metaSemana":7}'
curl -s -b /tmp/demo.cookies -X POST "$H/api/demo/meta/foco" \
  -H "Origin: $H" -H 'Content-Type: application/json' -d '{"minutos":25}'
```

## 4. Triaging errors

| HTTP | Meaning | Fix |
|------|---------|-----|
| 401 "Autenticação necessária" | cookie missing/prefix wrong | use `/api/demo/*` (not `/api/*`) with the demo jar |
| 403 "origem ausente" | no `Origin` header | add `-H "Origin: $H"` |
| 403 "Acesso negado para este papel" | demo user is `user` hitting an admin-only route (e.g. demo reload) | allow the demo instance to call it (see section 11) |
| 422 | Zod reject | fix the JSON body (ids must be 24-hex; `tags` array) |

## 5. Reseed the demo (force)

The demo DB may have been seeded by an OLD run before a new entity existed
(e.g. Tasks/Professionals added later). `carregarDemo` early-returns when
projects already exist, so new entities never get created → board shows 0
tasks. Force it:

```bash
curl -s -b /tmp/demo.cookies -X POST "$H/api/demo/demo/load" \
  -H "Origin: $H" -H 'Content-Type: application/json' -d '{"force":true}'
```
If this returns 403 "Acesso negado", the reload route is `requireAdmin` while
the demo user is `user` — relax it for the demo instance (section 11 of the
SKILL). After force-reseed, reload `/demo/` and the board should show the
seeded tasks.
