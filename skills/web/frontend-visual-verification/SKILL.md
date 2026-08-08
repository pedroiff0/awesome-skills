---
name: frontend-visual-verification
description: "Confirm a CSS/HTML/template change actually rendered in a running browser — without being fooled by stale browser cache. Use whenever you edited frontend code (CSS, EJS/HTML, components) and must verify the visual result, especially when a vision screenshot seems to contradict the DOM or the served asset."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [frontend, css, verification, browser, qa, visual]
    related_skills: [dogfood]
---

# Frontend Visual Verification (beating stale browser cache)

## Overview

You changed a stylesheet/template and want to *see* it worked. The trap: a
`browser_vision` screenshot can show the **old** layout even though the server
is already serving your new code. The browser cache (notably for `/css/*.css`
and other static assets) survives a container rebuild and a re-`navigate` to the
same URL — the HTML re-renders but the stale stylesheet is reused. The vision
model then confidently describes the OLD layout as if it were real.

**Never trust a single screenshot when it contradicts the DOM or the served
asset.** Cross-check with the triple below.

## The triple-check (do this before declaring "it didn't work")

1. **DOM** — `browser_snapshot()`. The *markup* reflects the HTML you served.
   If your new wrapper/selector is present, the HTML is new.
2. **Computed style** — run in `browser_console`, read the returned dict:
   ```js
   (() => {
     const el = document.querySelector('.your-new-selector');
     if (!el) return 'SELECTOR NOT IN DOM';
     const cs = getComputedStyle(el);
     return { display: cs.display, position: cs.position,
              grid: cs.gridTemplateColumns, borderRight: cs.borderRightWidth };
   })()
   ```
   If this shows OLD values while the DOM shows the new structure, it's cache.
3. **Served asset** — from the terminal:
   `curl -s http://HOST/css/main.css | grep -c 'your-new-token'`
   Server new + browser computed-style old ⇒ 100% cache, not your code.

## Force a fresh stylesheet (no hard-reload in the toolset)

Bust the cache by rewriting the `<link>` href to a unique query string, wait
~600ms, then re-screenshot:
```js
(() => {
  const l = document.querySelector('link[rel="stylesheet"]');
  l.href = l.href.split('?')[0] + '?cb=' + Date.now();
  return 'busted: ' + l.href;
})()
```
Now `browser_vision` reflects the new CSS.

## Container / static-asset gotchas

- **Docker with read-only filesystem**: local file edits do NOT reach the
  running container. Rebuild/restart first:
  `docker compose -f <file> -p <proj> up -d --build`
  Repo `HANDOFF.md`/`AGENTS.md` usually state this — read them before debugging
  "why isn't my change showing up".
- **Autologin demos / protected pages**: a nav-guard may bounce you to
  `/login` or the landing. To reach a protected page in the browser, either hit
  the auth route that sets the cookie (e.g. `POST /api/auth/login` via curl to
  grab a cookie jar, then reuse with `curl -b jar`), or just fill the login
  form in the browser with demo credentials. Don't debug layout while stuck in
  a redirect loop.
- **CSS `<link>` without `?v=` = rebuild never reaches the browser (real
  session, ~20 wasted iterations).** If the header serves
  `<link rel=stylesheet href="/css/main.css">` with NO query string, the browser
  caches the file in disk and NO container rebuild updates it — the DOM keeps
  measuring the old rule (e.g. `align-items: stretch`) even though the host file
  already says `start`. Fix: version the link like the footer already does —
  `href="/css/main.css?v=<%= assetVersion %>"` (the `assetVersion` is set in
  `app.locals` by the server; in an EJS *partial* use the bare global
  `<%= assetVersion %>`, NOT `app.locals.assetVersion` — that throws a runtime
  500). Then changing CSS and bumping `ASSET_VERSION` actually busts the cache.
- **Demo visual change invisible until you rebuild BOTH `app` and `app-demo`.**
  The browser requests `/css/main.css` (absolute, no `/demo/`), and nginx routes
  `/css/*` → `location /` → the **app principal**, NOT app-demo. So a CSS/header
  - **Demo visual change invisible until you rebuild BOTH `app` and `app-demo`, AND the browser loads `/css/main.css` from the PRINCIPAL, not the demo.** In the financas-app setup the page `/demo/app` references the stylesheet at `/css/main.css` (absolute, no `/demo/` prefix); nginx routes `/css/*` → `location /` → the **app principal** container, NOT `app-demo`. So even after you rebuild `app-demo`, the browser keeps showing the OLD CSS because the principal is still serving the previous file. Symptom that cost a full debug cycle: DevTools `document.styleSheets` listed `http://HOST/css/main.css` (no `/demo`), and a computed-style check reported the OLD `marginTop` even though `curl /demo/css/main.css` clearly had the new rule — the two URLs are DIFFERENT files. **Fix:** rebuild BOTH containers (`docker compose up -d --build app app-demo`) and verify the served bytes of the PRINCIPAL: `curl -s http://HOST/css/main.css?v=probe | grep -n 'your-new-token'`. If it still shows the old rule, `app` (principal) wasn't rebuilt — rebuilding only `app-demo` is not enough.
  - **ASSET_VERSION cache-bust is mandatory for the USER's browser, not just yours.** `header.ejs` already links `/css/main.css?v=<%= assetVersion %>` and `footer.ejs` versions the JS the same way (`app.locals.assetVersion = process.env.ASSET_VERSION || '1'`). When you ship a CSS fix, bump `ASSET_VERSION` in the compose env (`ASSET_VERSION: ${ASSET_VERSION:-1}` → pass `ASSET_VERSION=2 docker compose up -d --build app app-demo`) so the user's already-open tab actually re-fetches the new asset instead of using the cached `?v=1`. For YOUR OWN validation you can also just navigate the browser directly to the versioned URL (`/css/main.css?v=2`) to force a fresh fetch before measuring computed style.
  - **`/css/main.css` (principal) and `/demo/css/main.css` (app-demo) are DIFFERENT files — grep the one the browser actually loads.** In financas-app the page `/demo/app` requests the stylesheet at the *absolute* `/css/main.css` (no `/demo/`), so nginx routes it to `location /` → the **app principal** container. The `curl /demo/css/main.css` you may be checking is the demo's copy and can have your new rule while the browser still shows the old one. **Always cross-check the SAME url the browser fetches:** `curl -s http://HOST/css/main.css | grep -c 'your-new-token'`. If that shows 0 but `/demo/css/main.css` shows 2, the principal wasn't rebuilt — `docker compose up -d --build app app-demo` (both), then re-grep `/css/main.css`.
  - **Nested-card spacing pattern (financas-app dashboard).** Cards that are children of `.container`/`<main>` but whose preceding sibling is a `<div class="grid-2">` (not a `.card`) are NOT reached by the global `.card + .card { margin-top }`, so they "colam" no módulo anterior. Fix: `.container > .card { margin-top: 1.5rem }` + `.container > .card:first-child { margin-top: 0 }`. Cards *nested* inside another card (e.g. "Custo mensal" inside the Veículos card) also miss `.card + .card` → add `.card > .card { margin-top: 1.25rem }`. And restore `margin-top` inside `@media (max-width: 820px)` for `.grid-2 > .card + .card` / `.split > .card + .card` so stacked columns keep their gap.
  - **Rosca (donut) chart labels.** In financas-app the SVG donut is built in `app/public/js/financas-lib.js` (função `rosca`). It drew a fixed, oversized `<text>` percent label inside each slice — Pedro called this "feio" / "percentuais muito grandes". Fix: drop the fixed `<text>`, keep the native `<title>` (hover shows `label — % (R$ valor)`), and rely on the legend `<ul>` below the chart (already renders label + % + value). Verify by snapshot: center of donut should be empty (or show only the total), legend below carries the %s.

- **A `patch` can DUPLICATE a CSS rule and the browser silently applies the wrong one.** If you patch a `.foo { … }` block and the old_string didn't fully consume the original (e.g. a comment or adjacent line was left behind), you end up with TWO `.foo` rules — one old, one new. CSS cascades by LAST occurrence, but a `grep -c` for the property can hide the stale copy, and a stale container image serves the FIRST one. Symptom this session: `.grid-2` had both `align-items: stretch` (line 484) and `align-items: start` (line 491) — measured `stretch` in the DOM even though the file "looked fixed". **Fix the source to ONE rule, then verify the served asset shows exactly one base occurrence:**
  ```bash
  # served asset must show ONE base rule with the intended value:
  curl -s http://HOST/css/main.css?v=probe | grep -o '\.grid-2 { display: grid[^}]*align-items: [a-z]*' | head
  # expect exactly: .grid-2 { ... align-items: start   (no 'stretch' line)
  # also confirm host + container agree (no stale image):
  grep -c 'align-items: stretch' app/public/css/main.css          # expect 0 after fix
  docker exec <container> grep -c 'align-items: stretch' /app/public/css/main.css  # expect 0
  ```
  Rule of thumb: after any CSS patch, `grep -n` the EXACT selector you changed in BOTH the host file and the served asset; if you see it twice, the patch duplicated it — collapse to one rule before rebuilding.

## Server-side templates (EJS / SSR) — verify the RENDERED HTML

For server-rendered templates the bug isn't always "old asset": it can be that
the template compiled but produced wrong markup. Cross-check the *served HTML*,
not just the DOM/screenshot:

```bash
curl -s http://HOST/ | grep -c 'your-expected-text'
# or dump a section to inspect exact markup:
curl -s http://HOST/ | grep -o 'Veja funcionando[^<]*'
```

**EJS pitfall (cost real time this session):** `<%= expr %>` HTML-escapes its
output. If you put literal tags inside it — e.g.
`<%= stats ? \`<strong>2</strong><span>…</span>\` : '…' %>` — EJS escapes the
`<`/`>` and the browser shows `&lt;strong&gt;2&lt;/strong&gt;…` as *text*, not
markup. Tests that match `>2</strong><span>…` then fail even though `stats` is
correct. **Fix:** keep tags in the template body (`<% if (stats) { %><strong><%= val %></strong><span>…</span><% } %>`) and only interpolate *values* via `<%= %>`. Use `<%- %>` only for already-safe HTML.

Also re-run the suite after any template change — a subtly broken render can
flip a previously-green test (e.g. a landing test asserting on rendered copy).

### Verify an EJS page WITHOUT standing up the app (no DB / no server)

Many EJS routes pull data from the DB or middleware (i18n locals, auth, etc.),
so you can't just hit the URL to screenshot. **Don't stand up MongoDB just to
see the layout.** Render the template directly with `ejs` and open the result in
the browser tool. A ready-to-adapt harness lives in
`templates/ejs-standalone-render.js` (set `APP` to your project's `app/` dir and
fill `localsFor`).

```js
const ejs = require(require('path').join(APP, 'node_modules/ejs'));
const fs = require('fs'), path = require('path');
const VIEWS = path.join(APP, 'views');
function render(page, locals) {
  return ejs.render(fs.readFileSync(path.join(VIEWS, page), 'utf8'), locals,
    { views: [VIEWS], filename: path.join(VIEWS, page) });
}
const html = render(process.argv[2], localsFor(process.argv[2]));   // e.g. 'landing.ejs'
// escreve em /tmp/lp_pub/ com assets em caminho RELATIVO p/ funcionar via file://
fs.mkdirSync('/tmp/lp_pub/css', { recursive: true });
fs.mkdirSync('/tmp/lp_pub/js', { recursive: true });
fs.copyFileSync(path.join(APP,'public/css/main.css'), '/tmp/lp_pub/css/main.css');
fs.copyFileSync(path.join(APP,'public/js/common.js'), '/tmp/lp_pub/js/common.js');
fs.writeFileSync('/tmp/lp_pub/out.html', html.replace('/css/','css/').replace('/js/','js/'));
console.log('open file:///tmp/lp_pub/out.html');
```

Then `browser_navigate` to `file:///tmp/lp_pub/out.html` and `browser_vision`.

**Pitfalls específicos de verificação (custaram tempo real):**

- **Client-rendered table rows aren't in the served HTML — SSR check gives a false FAIL.** Pages like a Projects/Profissionais list deliver an EMPTY `<tbody>` from the server (the SSR only emits the shell: `<table>` + `<tbody id=...>`); the rows are built by `public/js/*.js` after the `fetch`. A `curl`/`http.get` on the served HTML will NOT find the `icon-btn js-edit` buttons — but the **browser** (post-JS) renders them. When verifying, assert (a) the shell in the SSR (`id="proj-rows"`, `class="dom-table"`) and (b) that the on-disk JS generates the buttons (`pjs.includes('icon-btn js-edit')`), OR navigate in the browser and read the snapshot. Do NOT mark it as a bug just because the raw HTML has no rows. Same root cause as "an ad-hoc `hermes-verify-*.js` that reads served HTML never sees the table" — it must read the JS or navigate.
- **Terminal/Node escaping makes CSS quotes look like a file defect.** `curl` piped through a shell, and `JSON.stringify` in a Node probe, render a CSS file's `"` as `\"` (e.g. `.board-col[data-status=\"em_andamento\"]`). That makes it LOOK like the served CSS has backslash-escaped quotes (and a broken selector) — it isn't. The file on disk is correct. To settle it: read the file with Node directly (`fs.readFileSync(p,'utf8')` and test `c.includes('\\"')` → should be `false`), or render the DOM in the browser and read computed style. Don't "fix" the CSS based on an escaped-print artifact — you'll corrupt a working file. (Same family as the "suspect the check before the code" rule.)
- **Não pré-fixe `<!DOCTYPE>` no resultado.** Se o `header.ejs` já emite
  `<!DOCTYPE html>…<body><main>` e o `footer.ejs` fecha, renderize **apenas a
  folha-folha** (ex.: `landing.ejs`, que faz `include` do header e footer). Se
  você também concatenar/prependar um doctype próprio, saem **dois topbars / dois
  `<body>`** — parecia bug de duplicação, mas era o harness.
- **Caminhos de asset relativos.** O browser resolve `/css/main.css` a partir da
  raiz do `file://`, não do seu `/tmp/lp_pub`. Use caminhos relativos
  (`css/main.css`) ou copie os assets para a mesma pasta do HTML.
- **`views` + `filename` são obrigatórios** para que `<%- include(...) %>` e
  `<%- include('partials/header') %>` resolvam. Sem `filename`, o include falha.
- O render standalone não exercita a lógica de rota (auth/i18n middleware). Para
  checar *conteúdo por idioma/ambiente*, monte os `locals` no próprio harness
  lendo os módulos de config (ex.: `landingFor(mode, lang)` de
  `config/landingContent.js`) — assim você valida o texto real sem o servidor.

### Config-key vs route-key mismatch (silent duplicate content)

When content/config lives in a module keyed one way but the route calls it with
a different key, `landingFor(mode)` returns `undefined` and falls back to a
default — so **two environments silently render the SAME content**. Seen here:
config keys were `producao`/`teste` but the route called `landingFor('production'…)`
and `landingFor('test'…)`, so production AND test both fell back to `producao`.
Always assert distinct output per key after renaming/mapping content keys:

```js
const titles = ['production','test','demo'].map(m => landingFor(m,'pt').title);
if (new Set(titles).size !== 3) throw new Error('fallback vazando entre ambientes');
```

## Self-hosted fonts

If you switched to a self-hosted font (woff2 served from `/fonts/*`, no CDN),
confirm the files actually serve — a missing/404 font silently falls back and
the "did the font apply?" question can't be answered by screenshot alone:

```bash
curl -s -o /dev/null -w '%{http_code}' http://HOST/fonts/Inter-400.woff2   # expect 200
curl -s http://HOST/css/main.css | grep -c "Inter"                          # @font-face present
```

## Ad-hoc verification script (when the suite doesn't cover the change)

If the canonical `jest`/`lint` run doesn't assert the exact behavior you
changed (e.g. a copy/CTA-text fix already deployed to a live container), write
a throwaway probe under `/tmp` with the `hermes-verify-` prefix, run it against
the *real* server, then delete it. Don't claim "verified" from the diff alone.

```bash
cat > "$(mktemp /tmp/hermes-verify-XXXX.sh)" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
H=$(curl -s http://127.0.0.1:4462/)
printf '%s' "$H" | grep -q 'meses de histórico</span>:' || { echo FAIL; exit 1; }
printf '%s' "$H" | grep -q 'meses de histórico de histórico' && { echo FAIL-dup; exit 1; }
echo PASS
EOF
chmod +x /tmp/hermes-verify-*.sh && /tmp/hermes-verify-*.sh; rm -f /tmp/hermes-verify-*.sh
```

## When to use this skill

- After editing CSS and needing visual confirmation at a specific resolution
  (e.g. Pedro verifies at 1920x1080 before approving).
- When a vision screenshot "lies" about layout that the DOM clearly has.
- Any frontend change served from a container or behind auth.
- When the page is an EJS/SSR view you can't easily hit (DB/auth gating the
  route) — render it standalone, see `templates/ejs-standalone-render.js`.

## References

- `references/cache-bust-recipe.md` — copy-paste commands for the triple-check
  and the cache-buster, including the curl cookie-jar login pattern.
- `templates/ejs-standalone-render.js` — copy/adapt harness to render an EJS view
  to `/tmp/lp_pub/out.html` without standing up the app (no DB/server), for
  screenshot verification.
