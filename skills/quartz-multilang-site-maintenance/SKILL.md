---
name: quartz-multilang-site-maintenance
description: Maintain and edit a Quartz static site (Quartz Syncer / quartz-site fork) that publishes to GitHub Pages — especially editing the 4-language home/index pages (pt-br/en/es/fr), cross-referencing sections, removing items, and verifying publication through the CDN/cache/redirect maze. Covers the two CLAUDE.md conventions, the deletion trap, and how to confirm a deploy actually went live.
version: 1.0.0
author: Hermes Agent
license: MIT
related_skills: [mt-markup-preserving-translation]
tags: [web, quartz, github-pages, static-site, i18n, content, astro-like]
platforms: [linux, macos, windows]
triggers:
  - edit the home/index of a Quartz site
  - add/remove a section such as Blog or Projects from a Quartz index
  - cross-reference pages on a Quartz site (portfolio versus official site)
  - Quartz Syncer or quartz-site vault maintenance
  - publish to GitHub Pages via Quartz and verify it went live
  - edits to the phrandrade site or the pedroiff0/page repository
---

# Quartz Multilingual Site Maintenance

Maintain a Quartz (jackyzha0 fork) personal/academic site that publishes to GitHub Pages
from a vault of Markdown notes. The distinctive part is NOT building Quartz — it's the
**conventions of THIS vault** and the **verification maze** (CDN redirect + Varnish cache
that makes "is it live yet?" hard to answer).

## Vault layout and two CLAUDE.md files
This repo has TWO CLAUDE.md files and you must respect both:
- CLAUDE.md (root) — motor/build/deploy (quartz-site fork, commands, i18n systems,
  media, deploy workflow, deletion guard).
- content/CLAUDE.md — vault authoring (bilingual mirror, status of language rollout,
  frontmatter rules, the deletion trap, media note structure).

The content/ folder IS the real Obsidian vault the user edits AND the folder Quartz
consumes. Edits made here are not a copy.

## Language rollout status (important — do not over-build)
- pt-br — primary, always complete.
- en — partial; translated as time allows.
- es, fr — ONLY the index.md exists (welcome stub with translation-in-preparation note
  plus a link back to pt-br). Do NOT author new content in es/ or fr/ unless asked; those
  pages 404 to a friendly translation-coming notice (quartz/components/pages/404.tsx).
- i18n is TWO separate systems: (1) quartz/i18n/locales/* for UI chrome (fixed to pt-BR
  for the whole site — a known limitation), (2) content/<lang>/ folders for real page
  content with mirrored slugs (en/x <-> pt-br/x). The LanguageToggle only swaps the
  language URL segment.
- To AUTO-TRANSLATE content/<lang>/ folders (pt-br media/research -> en/es/fr) preserving
  Markdown markup (headings, emojis, tables, bold, wikilinks), use the
  `mt-markup-preserving-translation` skill (self-hosted LibreTranslate + a parser that
  blinds markup). Remember es/fr are published on push (see ignorePatterns above).

## Editing the 4 home/index pages
Root landing (content/index.md) is the language-chooser at /. Each content/<lang>/index.md
is that language's home. To keep them in sync:
- Use Obsidian callouts > [!abstract] / > [!info] / > [!tip] — they render natively in
  Quartz. Inline HTML (<div style=…>) also works.
- Cross-reference pattern the user wanted: a callout on each home linking to an external
  short-resume portfolio, e.g. "Se veio do meu [portfólio de projetos](https://…/webpage/)
  (…)". Keep the SAME callout on all 4 language index pages, translated.
- For a SINGLE combined notice on the root index, put all 4 languages in ONE callout with
  4 bulleted lines (BR/US/ES/FR flags) — that is what the user asked for the root alertinha.
- To show ONLY one language's CV next to its repo card (not a list of all languages), use a
  2-card grid: one card = <a href="/assets/curriculo/<lang>CV.pdf">, the other =
  <a href="https://github.com/<user>/curriculo">Repositório do CV</a>. Do not explain LaTeX
  compilation in the page body.
- Removing a section (e.g. Blog + Projects) from a home = delete the carousel
  <a class="carousel-slide"> block AND the matching list item. Do it on all 4 languages so
  the carousels stay consistent.

## WORKING DIRECTORY — confirm the REAL vault path before writing
The repo can exist as MULTIPLE clones on disk (e.g. `~/Repositorios/pessoal/page/` AND
`~/Repositorios/pessoal/quartz-site/`, both pointing at the same GitHub remote
`pedroiff0/page`). The user's Obsidian/vault opens ONE of them (here: `quartz-site/`).
If you write generated content into the wrong clone, the user "does not see it".
- BEFORE any file-generating task, ask or verify which directory the user actually edits.
  A quick `ls -ld` + `git remote -v` on the candidates disambiguates (different inodes =
  separate clones; same origin = pick the one the vault uses).
- If asked to remove a directory that holds UNCOMMITTED work (e.g. "remove page/, work
  only in quartz-site"), COPY the valuable files to the surviving dir FIRST, verify the
  copy, THEN `rm -rf`. Never delete before copying — untracked generated output is
  unrecoverable once removed.
- After copying between clones, confirm counts (`find ... -name '*.md' | wc -l`) match.

## ignorePatterns — es/ and fr/ are NOT ignored
The build (`quartz.config.yaml` → ignorePatterns) ignores only `private`, `templates`,
`.obsidian`. It does NOT ignore `es/` or `fr/`. So any file you drop into
`content/es/...` or `content/fr/...` WILL be built and published on the next push —
even machine-translated (MT) drafts. If you generate es/fr content, either (a) commit
locally and let the user review before pushing (recommended for MT drafts), or (b) expect
it to go live as-is. Do not assume an untranslated language folder is "safe" from publish.

## THE DELETION TRAP (has wiped the repo twice)
Quartz Syncer treats content/ as a mirror of the PUBLISHED subset. Everything in the repo
that is not publishable shows as a candidate to unpublish/delete and the plugin WILL remove
it from the repo on publish. This produced Deleted 216 files and Deleted 222 files commits
historically (110/111 were publish:false, but the site went live empty once).
- Guard: CI deploy has a "Guarda contra deleção em massa" step that HALTS deploy if a push
  removes >20 content/ files. It warns but does NOT undo — you revert the commit.
- Rule: never use the plugin to publish after editing here via git directly without checking
  git status / git log --stat -1 for unexpected deletions. Prefer git push (manual) or
  npx quartz sync over the plugin's publish button when you have made direct file edits.
- Syncthing syncs content/ as its own folder (.stfolder); .git is NOT synced. Edits here
  arrive on other devices fast but do NOT auto-publish.

## Publishing and verification maze (this is the tricky part)
Deploy = .github/workflows/deploy-gh-pages.yaml, runs npx quartz plugin install (the
npm run install-plugins prebuild script is BROKEN — scss import error, do not use it) then
build then Pages deploy, on every push to main.

Problem: https://pedroiff0.github.io/page/ does a 301 redirect to the custom domain
(www.phrandrade.com), so you cannot read the built body via the github.io URL. And the
custom domain sits behind Varnish (CDN) with age: 30–50s caching, so right after a push the
served HTML is STILL the old version even though the build succeeded.

Reliable verification recipe:
1. Confirm the commit is on the remote: git push then git log --oneline -1 shows your SHA.
2. Confirm the deploy actually ran: gh run list --repo <owner>/<repo> --limit 3 — look for
   the Deploy to GitHub Pages workflow; gh run watch <id> to block until done, then
   gh run view <id> --json conclusion,status → must be success.
3. Confirm the deployment points at YOUR commit: gh api repos/<owner>/<repo>/deployments
   --jq '.[0] | {created_at, sha}' → SHA should match your push (may lag by one commit if a
   rebase happened; both are the same content).
4. ONLY THEN check the live site: curl -sL "https://www.phrandrade.com/<lang>/?t=$(date +%s)"
   (the ?t= cache-buster helps but Varnish may still serve stale; expect up to ~1–2 min).
   Grep for the markers you added/removed (e.g. Blog</div>, carousel-slide count, the new
   callout text). If the site is slow/timing out, that is the CDN, NOT your files — trust the
   gh API checks (steps 1–3) as the source of truth.
5. Do not claim verified live from a stale curl. State explicitly: commit pushed, deploy
   success, deployment SHA matches; live reflection pending CDN cache expiry.

## Missing-translation UX: 404 fallback + redirect + issue watcher
When a page is accessed in a language that has no translation (es/fr are stubs; en is
partial), the visitor hits `quartz/components/pages/404.tsx`. The desired behavior
(implemented here) is:
1. **Multilingual notice** that the translation was not found and "will be translated soon"
   (one string per language, keyed off the URL's language segment).
2. **"Open an issue to request this translation" link** — a pre-filled GitHub issue URL
   (`https://github.com/<repo>/issues/new?title=...&body=...&labels=translation`) injected
   into the 404 page. The user clicks to file it; no backend needed.
3. **Auto-redirect after ~5s to the pt-br equivalent** (which always exists). Compute
   `pt-br/<rest-of-slug>` and only redirect if that path is in the client-side `index`
   built by Quartz; otherwise just show the notice. Uses the same `fetchData`/`index`
   lookup the stock 404 already uses for case-insensitive slug fixes.

**Why a "watcher that opens an issue on every visit" is NOT done:** GitHub Pages is static;
the 404 runs in the visitor's browser — there is no server to call the GitHub API, and
doing it client-side would leak the token or spam issues (one per visit). Instead use a
**scheduled GitHub Action** (`.github/workflows/translation-issues.yml`, cron daily) that:
- walks `content/pt-br/**/*.md` (minus `index.md`),
- for each slug missing in `en`/`es`/`fr`, opens an issue titled `Tradução em falta:
  <lang>/<slug>` with label `translation`,
- de-dupes via `gh issue list --search <title> --state open` (skips if already open),
- uses the repo `GITHUB_TOKEN` (no secret to leak). Safe, no per-visit spam.
Create the `translation` label once: `gh label create translation --repo <owner>/<repo>
--description "Pagina sem traducao" --color 0E8A16`.

Editing `404.tsx` / adding the Action: **run `npm run check` locally FIRST** — node_modules
is present in the repo, so `npm run check` (tsc --noEmit + prettier --check) runs and
catches TSX type errors. The BROKEN part is ONLY `npm run install-plugins` / `npx quartz
plugin install` (scss import error) — that is the plugin-cache step the deploy workflow
runs for you; you never need it locally. This session, `npm run check` caught two real
bugs the deploy's permissive transpile missed: an unused `i18n` import, and `onError` must
be a function (not a string inline handler). So: validate TSX by `npm run check` locally,
THEN confirm the deploy (steps 1–3) went green. Do NOT skip local tsc.

### CLIENT-SIDE JS in ANY Quartz component — three pitfalls, one is site-breaking
The 404 text (and any client-side behavior you add to a component) runs from a string you
assign to `NotFound.afterDOMLoaded`. Three wrong ways, ranked by damage:

- **WRONG (site-breaking, silent): a regex inside the string with `\/`.** The Quartz build
  minifies these strings with esbuild. esbuild "optimizes" `\/` to `/` inside a regex literal,
  turning `/^\//` into `/^//` — an INVALID regex. The browser then fails to parse the ENTIRE
  module (`static/scripts/script-N-<hash>.js`). `postscript.js` imports all scripts via
  `Promise.all([import(...), ...])`; one rejected import rejects the whole `Promise.all`, so
  every script AFTER yours never runs. The toolbar (search, darkmode, explorer, readermode)
  and the SPA router are typically script-12+ — they never register handlers → **every button
  on the whole site stops working** (mobile AND desktop; you notice on mobile because the
  toolbar is the only interaction path there). Symptom: clicking Pesquisar/Tema/Explorador
  does nothing. Symptom is identical to a normal JS error — isolate by downloading the built
  `postscript.js`, then `node --check` each `static/scripts/script-N-*.js` (see
  `scripts/verify-quartz-scripts.mjs`). FIX: NEVER put `\/` in a regex inside `afterDOMLoaded`.
  Use string methods instead: `str.startsWith("/") ? str.slice(1) : str`,
  `str.endsWith("/index") ? str.slice(0, -6) : str`, `str.split("/").filter(Boolean)`.
  Confirm locally with `npx esbuild --minify` on the extracted string + `node --check` — the
  corruption reproduces exactly. (This is the bug that broke all buttons; `npm run check` and
  the deploy's permissive transpile BOTH miss it.)
- **WRONG: `<script dangerouslySetInnerHTML={...}>` inside the JSX.** Scripts inserted via
  `innerHTML` do NOT execute in the Quartz SPA — so nothing fills in.
- **WRONG: `afterDOMLoaded` as a bare IIFE that runs once.** It IS injected as a real
  `<script>` and runs on hard load, BUT Quartz does NOT re-run `afterDOMLoaded` on SPA
  navigation — it only dispatches a `nav` CustomEvent. Clicking a dead link inside the site
  leaves placeholders empty.
- **RIGHT:** assign `NotFound.afterDOMLoaded` to a string whose body is a named function
  `fill404()` that you (a) call immediately and (b) register on `document.addEventListener(
  "nav", fill404)`. Matches the built-in analytics scripts. The logic lives in
  `static/scripts/script-N-<hash>.js` (imported by `postscript.js`), NOT inline in the HTML
  body — expected. Inspect the external .js, not the inline HTML, when debugging.

Also: the issue-link slug comes from `window.location.pathname`, percent-encoded
(`engenharia-de-computa%C3%A7%C3%A3o`). `decodeURIComponent()` it before building the issue
URL, or the GitHub issue shows mojibake.

Verify client-JS health WITHOUT a browser: `node scripts/verify-quartz-scripts.mjs` (downloads
the live `postscript.js`, `node --check`s every `static/scripts/script-N-*.js`, exits non-zero
if any fail). Run it after any edit to client JS in a component. See
`references/404-client-js.md` for the full pattern + the curl debugging recipe.

## Frontmatter gotchas (publish:true required)
- Every published note needs publish: true in frontmatter or it stays local.
- title frontmatter NEVER carries decorative emoji (emoji only in the H1 body).
- type: blog enables Giscus comments; used in blog/ and all media/ notes.
- Section index.md files need order: N (Explorer order).
- Internal links use full path from content root (pt-br/research/x), never ./relative.
- markdownLinkResolution: shortest ignores .. dots — ./foo only works if foo.md exists at
  root. Ambiguous asset names → use full path (e.g. ![[assets/banners/X.pdf]]).

## Verification (ad-hoc, not a suite)
- git status --short after edits → expect ONLY the files you touched (no deletions beyond
  intended). A deletion spike = stop and inspect the deletion trap.
- git diff --stat to sanity-check scope.
- gh run list / gh api .../deployments for deploy truth (see maze above).
- curl + grep the live URL for added/removed markers.
- If a build seems to have failed, the artifact-size warning (exceeds 1GB) is usually just a
  warning — check conclusion:success, not the warning text.
