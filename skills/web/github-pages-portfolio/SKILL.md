---
name: github-pages-portfolio
description: Build, update, and verify a single-page static portfolio / intro site on GitHub Pages (pure HTML+CSS+JS, no build step). Covers sourcing content read-only from the user's existing GitHub repos (public AND private), the free-tier public-repo requirement, anchor+accordion single-page design (hidden content revealed on click), and an ad-hoc verification recipe. Use when the user asks for a portfolio, personal/landing/intro/"short resumé" page, or to publish/refresh a static site on GitHub Pages.
---

# GitHub Pages Portfolio

## When to use
- "crie um portfólio", "página de portfólio", "site pessoal no GitHub Pages", "landing / intro / resumé site".
- Updating an existing Pages repo (e.g. pedro's `webpage` = short resumé vs `page` = official Quartz site).
- Need to list a user's GitHub repos (public AND private) on one page.

## Key distinctions (ask or infer)
- **Short resumé / intro (portfolio):** one eye-catching page for introduction / client acquisition. For pedro this is `pedroiff0/webpage` → https://pedroiff0.github.io/webpage/.
- **Official full site:** deep content, often Quartz/Obsidian (pedro's `pedroiff0/page`). The portfolio should *link to* the official site, not replace it.
- If both already exist, confirm which you're editing before writing.

## Cross-linking a static portfolio WITH a Quartz site (pedro's two-repo reality)
When both `webpage` (portfolio) and `page` (Quartz, published at `www.phrandrade.com`, but GitHub Pages still serves `pedroiff0.github.io/page` with a 301 → phrandrade) exist:
- Add a reciprocal callout on EACH side:
  - In the Quartz `content/<lang>/index.md` (all 4: pt-br/en/es/fr), add a `> [!abstract]` callout: "Se você veio do meu **[portfólio de projetos](https://pedroiff0.github.io/webpage/)**…" (translate per language). This satisfies "referencie o portfólio nas index de cada idioma".
  - The portfolio already links out to the official site.
- **Quartz index MD conventions (Obsidian/Quartz markdown):** callouts use `> [!type]`; inline HTML with `style="..."` works (used for `.cv-cards-grid`); embedded PDFs use `![[assets/curriculo/x.pdf]]` wikilinks; links must be full path from content root (`pt-br/research/`), never `./relativo`.
- **Per-language CV + repo card (what the user wanted instead of a 4-language list):** replace the "download CV in every language" list with exactly TWO cards in a `.cv-cards-grid`: (1) the CV PDF for THAT page's language only (`/assets/curriculo/<lang>CV.pdf` — portugueseCV/englishCV/spanishCV/frenchCV) and (2) a "Repositório do CV" card linking to `https://github.com/pedroiff0/curriculo`. Drop the Lattes-PDF link and the embedded `![[...CV.pdf]]` viewer, and don't explain compilation. One card per idiom, repo beside it.
- **i18n note:** es/fr Quartz indexes are intentionally stub (only "tradução em preparação" + back-link to pt-br); don't over-translate them beyond the cross-link callout + the per-language CV card.

## Deploying edits to a Quartz repo (`pedroiff0/page`)
- Push to `main`; GitHub Actions rebuilds + redeploys Pages automatically.
- **Non-fast-forward reject** (Syncthing/Obsidian may have pushed in between): `git pull --rebase origin main` THEN push. Use rebase (NOT merge) so you don't create a merge commit, and the CLAUDE.md "guarda contra deleção em massa" only fires on >20 deleted `content/` files — a rebase of 4 index edits is safe (status must show only `M content/<lang>/index.md`, no deletions).
- **Verification after deploy is slow/cache-prone — and the user will say "não chegou".** Both Pages repos now have custom domains: `pedroiff0.github.io/page` 301→`www.phrandrade.com` and `pedroiff0.github.io/webpage` 301→`portfolio.phrandrade.com`. The CDN/Varnish serves stale copies for up to `Cache-Control: max-age=600` (10 min) and `curl` of the live URL often returns OLD content or times out right after a push. **The user-perceived "ainda não chegou / não mudou" is almost always browser+CDN cache, NOT a lost edit.** Don't treat a stale/empty grep as "edit lost". Confirm success deterministically by:
  1. `git log --oneline -1` shows your commit on `origin/master` (webpage) or `origin/main` (page).
  2. Wait ~1–3 min for the Actions build to finish.
  3. **Curl the SERVED ASSET with a cache-bust query and loop until it shows the new value** — this is the real proof the deploy propagated:
     ```bash
     for i in $(seq 1 6); do
       mw=$(curl -s -m 25 -L "https://pedroiff0.github.io/webpage/assets/css/style.css?t=$(date +%s)" | grep -o -- '--maxw: [0-9]*px' | head -1)
       echo "tentativa $i: $mw"; [ "$mw" = "--maxw: 1800px" ] && break; sleep 30
     done
     ```
     If the served asset shows the new value, the deploy is done — tell the user to **hard-refresh** (Ctrl+F5 / Cmd+Shift+R) or open an incognito tab; the served CSS is correct even if their browser still shows old.
  4. If the CDN keeps timing out, trust the committed+remote state — the build is deterministic on push.
- **`npm run check` / `npm test` / `npm run format` are NOT runnable here** (and not needed for static CSS changes): `npm run check` fails with `tsc: not found` (exit 127) because there is no `node_modules`. Running it would require `npm install` + `npx quartz plugin install` (which CLAUDE.md documents as broken/slow) just to lint one `max-width`. For CSS/SCSS edits, use **evidential verification** (served-asset grep above + `node --check` for any JS) — that is the correct bar, not the suite.
- `npx quartz build` locally is NOT a good smoke test here: CLAUDE.md says `npm run install-plugins` is broken and `npx quartz plugin install` is required first (slow). Prefer the live-build + commit check over a local build.

## Workflow
1. **Scan existing content — read-only, never clone or modify the user's repos:**
   - List all: `gh repo list USER --limit 100 --json name,description,isPrivate,isArchived,updatedAt,url`
   - Read a README without cloning: `gh api repos/USER/REPO/readme --jq '.content' | base64 -d`
   - Profile README: `gh api repos/USER/USER/readme --jq '.content' | base64 -d`
2. **Reuse an existing Pages repo if present.** Clone it. NOTE: on push GitHub may have *renamed* it — the push still redirects, but verify the canonical name with `gh repo view USER/REPO --json name,isPrivate,isArchived`.
3. **Build a single static page (no build step — Pages serves raw files):**
   - `index.html` with anchor sections (`#sobre #projetos #trabalhos #pesquisa #curriculo #lattes #contato`) + a fixed nav.
   - `assets/css/style.css`, `assets/js/*.js`. Dark/space theme, glassmorphism, canvas starfield, IntersectionObserver scroll-reveal, mobile hamburger nav.
   - **Hidden-content pattern:** cartões/accordions whose `.detail`/`.acc__body` start collapsed (`max-height:0; overflow:hidden`) and reveal on click via a toggled class. This is the "conteúdo invisível que aparece ao clicar" requirement.
   - Keep all content in one JS object (`window.PORTFOLIO_DATA = { REPOS, FEATURED, RESEARCH }`) so cards/accordions render from a single source; list private repos too with a "Privado" tag + short brief.
4. **Verify (ad-hoc — see scripts/verify_portfolio.sh):**
   - `node --check` every JS file (there is NO bundler; don't add npm/build).
   - Serve locally: `python3 -m http.server 8123 &` then `curl -o /dev/null -w '%{http_code}'` each asset → expect 200.
   - Browser screenshot + snapshot; confirm accordion/cards toggle (dispatch a real `MouseEvent('click',{bubbles:true})` to prove handlers fire — the tool's synthetic click sometimes misses nested buttons).
   - After push, re-curl the live Pages URL and grep served HTML for the new section ids.
5. **Commit & push**, then **enable Pages:** `gh api -X POST repos/USER/REPO/pages -f build_type=legacy -f "source[branch]=master" -f "source[path]=/"`. Build ~1 min; poll with curl for 200.

## Pitfalls
- **Free GitHub Pages needs a PUBLIC repo.** Private repo → API returns `422 "Your current plan does not support GitHub Pages for this repository."` Fix: confirm with user, then `gh api -X PATCH repos/USER/REPO -f private=false`. A portfolio is usually fine to expose (no secrets in a static site).
- **Archived repo blocks pushes AND Pages creation.** Unarchive: `gh api -X PATCH repos/USER/REPO -f archived=false`.
- **Push rejected (non-fast-forward)** after enabling Pages or a rename: `git pull --rebase origin <branch>` then push again.
- **Don't link private-repo raw PDFs as if public** — `raw.githubusercontent.com/...` of a private repo 404s. Use only public mirrors (or make repo public).
- **Keep it KISS:** pure static files. No React/webpack. node --check is the only "build" check needed.

## Support files
- `references/github-pages-gotchas.md` — durable platform facts (public-repo rule, archived block, rename redirect, enable command).
- `references/quartz-page-index.md` — recipe for cross-linking the portfolio from the Quartz `page` index.md (4-language callout + per-language CV card + repo card).
- `references/layout-width-tips.md` — widening body without breaking grids, fixing clipped contact cards, hiding scrollbar, tightening section whitespace, Quartz `.page` width override.
- `scripts/verify_portfolio.sh` — copy/run ad-hoc verification (assets 200, JS syntax, live-HTML section check).
