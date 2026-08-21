---
name: static-site-md-source
description: Turn an EXISTING static site (HTML/CSS/JS) into a Markdown-editable source WITHOUT changing its rendered output. Use when the user likes the current site ("muito bom, não mexa no HTML") but wants to edit content in Obsidian/Markdown and have commit+push republish the same look. Covers the data-object extraction pattern, a JS serializer (YAML/JSON does NOT produce valid JS), semantic deep-equal verification (not byte-equal), and a pre-commit hook that regenerates the compiled asset.
author: Static Site Community
---

# Static site → Markdown source (render-identical)

## When to use
The user has a working static site they love and does NOT want the HTML/CSS/JS
touched, but wants to edit content in Markdown (Obsidian) and have
`commit`+`push` republish the site unchanged in appearance.

Classic signal: "reescreva esse site em markdown mas que renderize EXATAMENTE
como o HTML atual; não quero editar o html, só o markdown."

## Core pattern (what worked)
1. **Find the single source of truth.** Most hand-written static sites keep
   content in one JS file as a global object, e.g. `assets/js/projects.js`
   exposing `window.PORTFOLIO_DATA = { REPOS, BOLSAS, CONTACTS, I18N, ... }`.
   The `index.html` + `main.js` are a *template/engine* that reads that object
   and builds the DOM. Editing that object is what changes the site.
   → Make the JS object the **compiled output**, and Markdown the **source**.
2. **Source = ONE clean Markdown file, NOT YAML frontmatter** (`src/portfolio.md`).
   Pedro REJECTED nested YAML frontmatter as "muito ruim de editar". Use prose Markdown:
   - One `### Title` per item (project/bolsa/contact).
   - Single-line fields: `repo:`, `stack:`, `tags:`, `cat:`, `visibility:`, `icon:` (comma-separated lists).
   - Multilingual text as flag-prefixed paragraphs: `🇧🇷 pt`, `🇺🇸 en`, `🇪🇸 es`, `🇫🇷 fr`. Missing langs INHERIT 🇧🇷.
   - **Separate rarely-edited interface/menu i18n** (nav, hero, section titles, about, labels, footer) into its OWN file `src/interface.yaml`. The editable MD then holds ONLY content the user touches (Metadados, Projetos, Bolsas, Contatos, Extra). The generator reads BOTH files. Pedro found the trailing i18n YAML block inside the MD still "muito dificil" — isolating it in its own file is what made the MD tractable.
   See sibling skill `markdown-site-source-pipeline` for the concrete format.
3. **Generator** (`tools/build.py`) parses the YAML and rewrites the JS object.
4. **Verifier** (`tools/verify.js`, Node) does a SEMANTIC deep-equal of the
   generated `window.PORTFOLIO_DATA` against a captured baseline
   (`*.js.orig`). The generated file does NOT need to be byte-equal — only the
   consumed object must match, because that is what drives rendering.
5. **Pre-commit hook** runs the generator so a plain `git commit` republishes.

Why this guarantees identical render: the engine (`main.js`) still reads the
same `PORTFOLIO_DATA` shape. You only swapped the *authoring format*, not the
consumed structure.

## CRITICAL pitfalls (caught and fixed this session)
- **Do NOT use `json.dumps` or YAML emitters to produce the JS.** They emit
  `{ "a": 1 }` / `a: 1` syntax that is INVALID JavaScript (no `const X =`,
  no `,` between object entries in flow style issues, no trailing commas in
  some engines). Write a dedicated JS serializer that emits real JS literals:
  `const NAME = <literal>;`, valid `,`-separated object/array entries, proper
  string escaping (`\"`, `\\`, `\n`). See `scripts/js_serializer.py` snippet.
- **i18n nesting direction.** If the original nests per-language
  (`i18n: { en: { title, kind, desc }, es: {...} }`), reproduce THAT shape —
  do NOT transpose to per-field (`i18n: { title: { en, es } }`). The verifier
  will catch a mismatch, but design the normalizer to match the original's
  structure exactly. When seeding MD→JS for the first time, preserve the
  original nesting.
- **Constants referenced by the object:** if the JS uses `ORCID` / `INSTAGRAM`
  as variables (e.g. `href: "https://orcid.org/" + ORCID`), your generator must
  re-emit those `const`s or inline them. Missing constants → `ReferenceError`
  at load. Capture them in the MD (e.g. `orcid:` / `instagram:`) and emit as
  top-level `const`.
- **Baseline must be the real current JS.** Save `projects.js.orig` BEFORE you
  first overwrite it. The deep-equal verifier depends on it. If you overwrite
  the original with a broken generator output, restore from `.orig` before
  re-seeding (you cannot re-seed from a corrupted JS).
- **Verify by running, not by reading.** After building, load the generated JS
  in Node (`new Function('window', src + 'return window.X')`) and deep-compare
  to the baseline. A pure text `diff` will show huge differences (formatting)
  even when the object is identical — that is expected and fine.

## Workflow
1. Locate the content object; save `X.js.orig`.
2. Write `seed.js` (Node) that loads `X.js.orig` (with a `window` shim) and
   emits `src/portfolio.md` (YAML). Run once.
3. Write `build.py` (Python + PyYAML) → regenerates `X.js`.
4. Write `verify.js` (Node) → deep-equal generated vs `.orig`.
5. Add `.git/hooks/pre-commit` that runs `build.py` and `git add`s the output.
6. Prove it: edit the MD (change one string), run build, confirm the change
   appears in `X.js`; revert, confirm verify passes again.

## Verification recipe (ad-hoc, re-runnable)
See `scripts/verify_pipeline.sh` — checks baseline exists, JS parses in Node,
deep-equal passes, hook is executable, and an edit propagates + reverts.

## Conventions for THIS user (Pedro)
- He edits in Obsidian; the portfolio repo is `/home/pedro/portfolio`
  (branch `master`, published at portfolio.phrandrade.com, no CI).
- Plain terminal text, no markdown in replies. Multilingual PT/EN/ES/FR.
- Do NOT edit `index.html` / `assets/css/*.css` / `assets/js/main.js`.
