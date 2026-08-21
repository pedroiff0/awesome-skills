---
name: portfolio-github-pages
description: Build and deploy a personal/academic PORTFOLIO as a single-page STATIC site (no build step) to GitHub Pages via the gh CLI. Use when the user asks for a portfolio, landing page, "pagina de portfólio", professional site, or "site estatico pro GitHub Pages", especially with a theme (astronomy/space is a known good pattern) and with sections revealed on click (accordions/cards). Covers scanning their real repos for truthful content, the single-page anchor layout, the space/glassmorphism design ingredients, and the gh CLI Pages activation gotchas (public-repo requirement, unarchiving, REST API enable).
author: Open Source Community
---

# Portfolio → GitHub Pages (static, single-page)

## When to use
- "criar um portfólio", "página de portfólio", "site profissional", "site estático pro GitHub Pages".
- Any request for a one-page site with anchor navigation and "invisible content shown when clicked".
- This user (pedro) owns several webpage/page/portfolio repos — reuse an existing one when possible.

## Workflow (ordered)
1. **Scan for truthful content first.** Do NOT invent projects. Read their real repos:
   `gh repo list <user> --limit 60`, then `gh api repos/<u>/<r>/readme` to enumerate ALL repos
   (public + private) **without cloning**; read each README for the real stack/description.
   Also mine local vaults for personal facts: `hardcore-life/99 - Meta/INDICE_VAULT.md`
   (PARA structure, course grade), `page/content/pt-br/index.md` (Sobre mim, Instagram
   handle, hobby), `cv/*.tex` (bolsas de pesquisa, ORCID, áreas de interesse). Pull full
   name, Lattes ID, ORCID, Instagram, hobby straight from there. If a brief is uncertain,
   say so — never fabricate. For a "short resumé" of ALL GitHub work, list every repo
   (private ones get a short brief too — no secrets, just what it does).
   For the animated canvas/constellation/SVG-icon build, see the `animated-portfolio-sites`
   skill (it covers that class of technique).
2. **Pick or reuse a repo.** If a `portfolio`/`webpage` repo exists and is archived, it must be
   unarchived before push (see references). Clone it, strip any old scaffold (Jekyll, etc.) if replacing.
3. **Build a single `index.html`** + `assets/css/style.css` + `assets/js/*.js`. Pure HTML/CSS/JS — NO
   build step, so GitHub Pages serves it directly from root. Put project/research data in a JS file
   (`window.PORTFOLIO_DATA`) so content is easy to edit.
4. **Single-page, anchor nav.** One `<section id="...">` per topic (sobre, projetos, pesquisa,
   curriculo, lattes, contato). A fixed top nav with `href="#id"` + `scroll-behavior: smooth`.
5. **"Invisible content revealed on click" = accordion / toggle cards.**
   - Cards: `.card` with a `.card__detail` that has `max-height:0; overflow:hidden;` and transitions to
     a fixed `max-height` when `.card.open` is toggled (JS adds/removes the class on click).
   - Accordions: same `max-height` technique inside `.acc.open`.
   - Reveal-on-scroll: `IntersectionObserver` adds `.visible` to `.reveal` elements.
6. **Space/astronomy theme (known-good design):**
   - Starfield: `<canvas>` + `requestAnimationFrame`; handle `devicePixelRatio`; twinkle via `Math.sin`;
     respect `prefers-reduced-motion` (draw a static frame instead).
   - Glassmorphism: `background: rgba(...); backdrop-filter: blur(...); border: 1px solid rgba(...)`.
   - Gradient text on the name: `background: linear-gradient(...); -webkit-background-clip: text; color: transparent`.
   - Soft nebulas: large blurred radial-gradient divs, slow `drift` keyframe.
   - Orbital hero: concentric `border-radius:50%` rings rotating (`@keyframes spin`) with small "moons".
   - Fonts: Space Grotesk (display) + Inter (body) from Google Fonts.
7b. **Multi-language (PT/EN/ES/FR) with flag selector.** Put ALL UI strings in a JS dict
    `I18N = { pt:{nav:[...], hero:{...}, sections:{...}, about:[...], contactLabels:{...}, footer:...}, en:{...}, es:{...}, fr:{...} }`.
    - Barra: `.lang-switch` with 4 `<button data-lang="pt|en|es|fr">` each an inline SVG flag + label
      (`PT-BR`/`EN`/`ES`/`FR`). On click set `localStorage.lang`, `document.documentElement.lang`,
      apply `data-i18n="chave"` texts, and re-render data-driven cards/contacts/bolsas (they read a `pick(obj,key)`
      helper that falls back to `obj[key]` if no `obj.i18n[lang]`). Keep PT as default.
    - Data objects may carry `i18n:{en:{title,desc,...},es:{...},fr:{...}}` (PLANO: `obj.i18n[lang].title`).
      Make `pick(x,k)` = `x.i18n && x.i18n[lang] && x.i18n[lang][k] ? x.i18n[lang][k] : (x[k]||"")`.
7c. **Canvas background — galaxies + bouncing orbs (known-good for this user).**
    - Galaxies: real-ish spirals — a bright core radial-gradient (white→hue→transparent), stars placed along
      `arms` logarithmic-spiral arms (some flagged `dust` = warmer/rgba), slow `g.rot += g.spin` rotation.
    - Orbs: N particles (`vx,vy ~0.5px/frame`, capped speed) that travel straight and BOUNCE off all 4 edges
      (`if (x-r<0){x=r; vx=Math.abs(vx)}` etc.) — calm but visibly bouncing. Each has a pulsing glow.
    - NOTE: this user wants MOUSE REPULSION on the field, NOT attraction. If you add mouse interaction,
      push galaxies AWAY from the cursor (per-galaxy eased offset), don't parallax-pull them.
    - Respect `prefers-reduced-motion` (static frame).
7. **Verify locally** (see "Verification" below) BEFORE deploying.
8. **Deploy to GitHub Pages** (see references/github-pages-cli.md for exact commands + gotchas).

## Pitfalls
- **Free GitHub plan: Pages ONLY works on PUBLIC repos.** A private repo returns
  `422 "Your current plan does not support GitHub Pages for this repository."` when you POST /pages.
  Fix: `gh api -X PATCH repos/OWNER/REPO -f private=false` (the static content has no secrets — fine).
- **Archived repos can't receive push or Pages.** Unarchive: `gh api -X PATCH repos/OWNER/REPO -f archived=false`.
- **The UI "Pages" toggle may demand GitHub Pro.** Use the REST API instead (legacy build type) — it works on free.
- **Repo rename redirects pushes** ("This repository moved…") but the push still succeeds; trust the final `master -> master`.
- **Browser-click verification quirk:** the `browser_click` tool sometimes misses a nested `<button>` inside
  an accordion, so the accordion won't toggle and you'll falsely think it's broken. Verify the handler by
  dispatching a real event in `browser_console`:
  `new MouseEvent('click',{bubbles:true}); head.dispatchEvent(ev)` and re-check the `.open` class.
  A real user click works — don't "fix" working code based on the tool's miss.
- **Browser ASSET CACHE across navigations (silent staleness).** The `browser_navigate` tool reuses the same
  page context and caches JS/CSS between `navigate`s in one session — after editing an asset, re-navigating
  still runs the OLD JS (you'll see stale behavior and think your fix didn't land). Two reliable fixes:
  (a) navigate to `about:blank` then back to the URL, or (b) serve on a FRESH port (`python3 -m http.server 81XX`)
  so the asset URL changes and forces a fresh fetch. Always confirm a behavioral fix against a reload-clean page
  before declaring it done. To inspect internals, temporarily expose `window.__test = {…}` at the end of the IIFE,
  verify, then REMOVE it before commit (never ship `__test`).
- **Quartz deploy is async + CDN-cached.** After `git push` to the Quartz repo, the GitHub Pages build takes
  ~1–7 min and the CDN (Varnish) serves stale HTML for a while (`age:` header). Confirm the deploy actually ran
  with `gh run list --repo <u>/<r>` / `gh run watch <id>` and check `gh api repos/<u>/<r>/deployments` — the
  latest deployment `sha` must match your commit. Only then trust a "still shows old content" curl as real.
- 7d. **Sibling Quartz site (this user owns one).** The portfolio is a SHORT RESUMÉ; the official site is a
    Quartz vault (Obsidian) at `www.phrandrade.com` / `pedroiff0.github.io/page` with full content
    (research, classes, media, blog). Cross-link it from the portfolio and add a DISCLAIMER on the portfolio
    that it's a summary (e.g. a `.disclaimer` block with 4 lang spans shown via
    `html[lang=...] .disclaimer .lang-X{display:block}`). When editing the Quartz `content/<lang>/index.md`:
    inline HTML + Obsidian callouts (`> [!abstract]`) compile fine; don't DELETE files from `content/` (the
    Pages deploy has a mass-deletion guard and the Quartz Syncer can wipe drafts); a push just edits index md.
**Keep it KISS.** No framework/bundler for a portfolio; a 3-file static site is more robust on Pages.

## Verification (ad-hoc, run before declaring done)
- `node --check assets/js/*.js`
- Serve on a FRESH port (`python3 -m http.server 81XX`, background), then `curl -o /dev/null -w "%{http_code}"` for `/`,
  each asset, and finally the published URL (`https://<user>.github.io/<repo>/`) — expect 200.
- Prefer a temp script `/tmp/hermes-verify-<name>.sh` that checks files + `node --check` + data shape + served HTML
  markers, prints PASS/FAIL, and self-removes. Run it; report it explicitly as ad-hoc (not a suite).
- Browser verification: navigate `about:blank`→back (or fresh port) to defeat asset cache before asserting a fix landed.
  Use `browser_console` to read `window.PORTFOLIO_DATA` / dispatch events / measure canvas state when the DOM isn't enough.
- Optional: browser screenshot to confirm visual theme.
- After enabling Pages (or pushing to Quartz), wait for the deploy (`gh run watch <id>`) before curling the published URL.

## References
- `references/github-pages-cli.md` — exact gh CLI commands + JSON responses for the deployment gotchas.
