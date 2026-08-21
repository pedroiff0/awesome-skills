---
name: libretranslate-markdown-i18n
description: Machine-translate Markdown / Obsidian / Quartz content into other languages using a self-hosted LibreTranslate instance, preserving frontmatter, headings, emojis, bold/italic, wikilinks (![[...]]/[[...]]) and internal links. Use whenever a user wants to auto-translate a Markdown vault, Obsidian notes, or a Quartz/static-site content tree into other languages, especially pt-br -> en/es/fr. Covers the Docker setup, the markup-protection technique that prevents MT from corrupting the source, and the placeholder pitfalls that silently leak in some target languages.
author: LibreTranslate / Community
---

# LibreTranslate Markdown i18n

Self-host LibreTranslate (Docker) and translate Markdown/Obsidian content while keeping the
markup intact. The naive approach — sending raw Markdown to the MT engine — **corrupts the
output**: emojis vanish or get "translated" into words, `#`/`##` headings get rewritten,
`**bold**` grinds into the text, and Obsidian `![[embed]]` wikilinks turn into garbage
("Chapitre 1"). This skill encodes the protection technique that makes it safe.

## When to use
- "Translate this vault / these notes / the pt-br content into en/es/fr"
- Building i18n for a Quartz site, Obsidian publish, or static Markdown docs
- Any MT task where the source is Markdown with frontmatter and/or wikilinks

## 1. Stand up LibreTranslate (Docker)
```bash
docker run -d --name libretranslate -p 5000:5000 \
  -e LT_LOAD_ONLY=pt,en,es,fr \
  -e LT_UPDATE=false \
  libretranslate/libretranslate:latest
```
- `LT_LOAD_ONLY` limits downloaded models (faster first start; ~1-2 min to HTTP 200).
- `LT_UPDATE=false` stops it phoning home for updates.
- Wait for `curl -s -o /dev/null -w '%{http_code}' http://localhost:5000/` -> `200`.
- Translation endpoint: `POST http://localhost:5000/translate` with form fields
  `q`, `source`, `target`, `format=text`.

## 2. The protection technique (CORE)
Never send raw Markdown. Per line:
1. **Split frontmatter** (`---...---`) and preserve it verbatim, EXCEPT you MAY translate the
   display-only fields `title` and `description` per language (see 3c). Never translate
   `slug`/`aliases`/URL-bearing fields — those must stay IDENTICAL across languages so the
   language toggle keeps working. Preserve YAML key order and formatting where possible.
2. **Separate block prefix from text.** A heading/list/callout line like
   `## 🗓️ Sobre o evento` must be split into prefix `## 🗓️ ` (markup + adjacent emoji) and
   text `Sobre o evento`. Translate ONLY the text. The MT engine must never see `##` or the emoji.
   - Regex for the prefix: `^(?:#{1,6}\s+|>\s*|[-*]\s+|\d+\.\s+|!\s*)?<EMOJI_CLASS>*`
     where `EMOJI_CLASS` covers U+1F000–U+1FAFF, U+2600–U+27BF, U+2190–U+21FF, U+2B00–U+2BFF,
     U+FE00–U+FE0F, U+2700–U+27BF, `\u200d`, `\u20e3`.
3. **Wikilinks never reach the MT engine.** Extract `!?\[\[[^\]]+\]\]` from the text and keep
   them literal (split the line on them, translate only the text between). Do NOT use a
   placeholder for wikilinks — the engine sometimes deletes long wikilinks entirely.
4. **Bold/italic/internal links** (`**[...]**`, `*[...]*`, `[anchor](pt-br/...)`) use a
   placeholder `§N§` (see pitfalls).
5. **Rejoin** prefix + translated text. Guarantee one space after a heading/emoji prefix if the
   engine dropped it. Strip a leading `- `/`# `/`*` the engine may inject at line start.

## 3. Pitfalls (learned the hard way — DO NOT skip)
- **Do not send raw Markdown with `format=html`.** The engine eats emojis, headings, and bold.
- **Do NOT skip `index.md` files.** A naive `if p.name == "index.md": continue` in the file
  walker drops every section landing page (e.g. `research/index.md`, `media/2026/index.md`,
  `journal-clubs/index.md` — often the most important pages). List them like any other `.md`.
  If you DO generate an `index.md`, guard against slug collisions (next pitfall).
- **Slugs/parent folders stay IDENTICAL across languages BY DESIGN.** The i18n language toggle
  (e.g. Quartz `LanguageToggle` / `translatePath`) only swaps the language *prefix*
  (`/pt-br/x` -> `/en/x`) — it does NOT remap folder names. Therefore the folder/file slug must
  be the same in every `content/<lang>/` tree. **Do NOT translate folder or file names**
  (e.g. don't rename `research/` to `es/investigacion/`). The page CONTENT and the frontmatter
  `title` get translated; the URL does not. If a user asks "why didn't the folder names change
  per language?", explain this is intentional and required for the toggle to work — offering to
  translate slugs would mean re-engineering the toggle + every internal wikilink (a big, risky
  change). Confirm before doing that.
- **`index.md` vs sibling `.md` slug collision.** If the source has both `research/foo/index.md`
  and `research/foo.md` (or the target lang already has a hand-authored `research/foo.md`),
  Quartz resolves both to the SAME slug and the build conflicts. When generating `index.md`,
  skip it if a sibling `<dir>.md` already exists at the same target path.
  leaving `\u00000` / `0` in the output. Use a VISIBLE stable token `§N§` instead.
- **Even `§N§` gets spaced by the engine** (`§0§` -> `§ 0 §`), so a naive `.replace("§0§")`
  fails to restore. Restore with a tolerant regex: `re.sub(r"§\s*(\d+)\s*§", repl, text)` where
  `repl` looks up `§<n>§` in the store.
- **Wikilinks must be positionally extracted, not placeholder-protected.** The engine deleted a
  `![[assets/banners/X.pdf|Y]]` and returned "Chapitre 1". Split on wikilinks and keep them literal.
- **WIKILINK REGEX BUG (critical):** `!?\s*\[\s*\[` lets the match START AFTER the `!` (the `\s*`
  before the first `[` swallows the `!`), so the `!` is left outside, the embed loses it and gains a
  stray bracket (`[[[`). The first `[` must be MANDATORY: `!?\[\s*\[`. And when extracting the body,
  account for the `!`: `body = raw[3:-2] if raw.startswith("!") else raw[2:-2]`, then re-emit with
  `![[` when `has_bang`. Also tolerate spaces the engine may inject between the inner brackets:
  `!?\[\s*\[\s*[^\]]*\]\s*\]\s*`.
- **Emoji in heading text gets "translated"** (👋 -> "Argicos"). Fix: the prefix regex must consume
  the emoji that immediately follows the markup token, so it is excluded from translation.
- **`format=text` still rewrites markup.** The protection above is what makes it safe, not the format.
- **Internal links `pt-br/...` must stay literal** (only the anchor text is translated). They are the
  language-toggle routes in Quartz — translating the path breaks the site.
- **Embed/link callouts:** a line `> ![[...]]` is NOT a `[!note]` callout (it's `![[`, not `[!`),
  so it falls through to the prefix branch; make sure the wikilink split still catches it and the
  sanitize step (below) does not insert a space between `!` and `[[` or between the two `[[`.

## 3b. Advanced pitfalls (production use — these bit hard)
- **Proper names get translated.** LibreTranslate turns "Soja" into French "soya" and
  "Ana Cecília Soja" into "Chapitre 1". Build a `PROPER_NAMES` list (surnames, people) and split
  them positionally EXACTLY like wikilinks — never as a placeholder (the `§N§` for a name goes to
  the engine and comes back translated). Combined regex for the protected split:
  `PROT_RE = re.compile(WIKI_RE.pattern + r"|" + PROPER_RE.pattern)`; loop, translate only the text
  BETWEEN matches, re-emit matches literally. Guarantee a space when rejoining if the translated
  chunk ends in a letter and the name starts with a letter (the engine eats the space before a name).
- **Markdown TABLES.** Sending a whole table row `| a | b | c |` to the engine destroys the `|`
  delimiters (it rewrites cell-by-cell into free text). Detect table rows (`^\s*\|.*\|\s*$`, ignoring
  the separator `| :--- | :--- |`) and translate CELL BY CELL, re-joining with `| `.
- **Bold is safer as HTML than as a placeholder.** Convert `**x**`->`<strong>x</strong>` and
  `*x*`->`<em>x</em>` BEFORE sending, use `format=html` for those calls (the engine preserves tags
  and translates only the inner text), then restore `<strong>`->`**`. Do NOT use `format=html` for
  whole lines/headings — it eats emojis/`##`. So: decide `fmt = "html" if has_bold else "text"` per
  span. `<br>` is also preserved by `format=html`; normalize `<br/>`->`<br>` on restore.
- **Residual bold spacing — apply `fix_bold()` on the WHOLE body, not per-line.** The per-line
  `sanitize` does not reach bold inside callouts (`> [!note] **x**`) or table cells, so leftover
  `** texto **` / `* * x * *` survives. After re-joining the body, run a global pass:
  ```python
  def fix_bold(text):
      text = re.sub(r"\*\*\s+(.+?)\s+\*\*", r"**\1**", text)   # ** texto **
      text = re.sub(r"\*\*\s+(.+?)\*\*",   r"**\1**", text)    # ** texto**
      text = re.sub(r"\*\*(.+?)\s+\*\*",   r"**\1**", text)    # **texto **
      text = re.sub(r"\*\s+\*\s+(.+?)\s+\*\s+\*", r"**\1**", text)  # * * x * *
      text = re.sub(r"(?<!\*)\*\s+(.+?)\s+\*(?!\*)", r"*\1*", text)  # * x *
      return text
  ```
  Verify with a precise checker (false positives are common): real grudge = `**` OPENING followed by
  space, i.e. `(?<![\*\w])\*\*\s+\S` — NOT `**texto**` (valid) and NOT `**texto** (` (space is OUTSIDE
  the bold, after the closing `**`). Naive `\*\*\s` or `\s\*\*` checkers flag valid markdown.
- **External URLs in `[text](url)` get corrupted** (`https://` -> `https: / / integrra`). Extract the
  full `[anchor](url)` pair, translate ONLY the anchor, re-emit with the literal `url`. Never let the
  engine see `http`.
- **Local-link fallback.** If a link points at `pt-br/foo` but `foo` does not exist in the target lang
  (`content/<target>/foo.md` missing), repoint to `en/foo` (the fallback lang) and append a tag to the
  anchor like `(en français)`; if even `en/foo` is missing, keep the original url (don't break the link).
- **Sanitize spacing the engine drops/merges** (run AFTER translation, per line):
  - `)et` -> `) et`: `re.sub(r"\)(?=[A-Za-zÀ-ÿ])(?!\*)", r") ", line)`
  - `apresentação[Link` -> `apresentação [Link`: insert space before `[` ONLY if the preceding char is
    a letter or `)` — NEVER before `[[` (wikilink) or `![` (embed):
    `re.sub(r"(?<=[A-Za-zÀ-ÿ])\[", r" [", line)` and `re.sub(r"(?<=[\])])\[", r" [", line)`
  - French apostrophe `l ' état` -> `l'état`: `re.sub(r"(?<=[A-Za-zÀ-ÿ]) ' (?=[A-Za-zÀ-ÿ])", "'", line)`

- **Display-only frontmatter + `--overwrite` safety (Quartz rollout)** — see §3c.
- **Raw HTML blocks (carousels, `<div>` layouts) are DESTROYED by the engine** if they
  reach it (the engine even mixes `href` with `class` and injects spaces into URLs).
  The naive per-line + non-greedy-regex protection misses nested blocks. Use a
  depth-counting parser at BODY level — full recipe in `references/html-block-preservation.md`.
- **Canonical section titles.** The engine MISSES academic context: pt "Pesquisa" -> en "Search"
  (should be "Research"). For the 1st-level section `index.md` (research/media/resource/
  projects/blog), force a canonical title per language instead of letting the engine translate —
  `SECTION_TITLES = {"research": {"en":"Research","es":"Investigación","fr":"Recherche"}, ...}`
  and apply when `rel.name == "index.md"` and `rel.parent.name` is the section key.
  (A wrong detection `rel.parent.name == "content"` is a real bug — the rel path is relative to
  `content/<SRC>`, so `rel.parent.name` IS the section, e.g. "research".)
- **Translate `title`/`description`, not `slug`.** The page H1 and nav label come from the
  frontmatter `title`, which the user expects in the page's own language. Translate `title` (and
  `description` if present) per target lang using `translate_line` (reuse the same proper-name /
  wikilink protection so "Soja" stays). Re-emit wrapped in quotes (`title: "..."`) for YAML safety
  (titles may contain `:` or `#`). **Never translate `slug`/`aliases`** — those drive the URL.
  Skip for the SRC language (leave it untouched). This is how you satisfy "show it in the language
  on the page, but keep the URL/slug the same".
- **`--overwrite` must still protect hand-authored files.** When retrofitting (disclaimer, title
  translation) with `--overwrite`, the source tree may already contain MANUAL translations in the
  target lang (e.g. `en/research/satellite-trail-removal.md` authored by the user). A blanket
  overwrite destroys that work. Rule: even with `--overwrite`, SKIP a target file if it is a
  top-level `.md` in the SRC-equivalent manual lang (e.g. `en/*.md` plain files) — i.e.
  `if args.overwrite and lang == "en" and out_path.name != "index.md" and out_path.exists(): skip`,
  while still overwriting `index.md` and `articles/*.md` (machine-generated) to update titles.
- **If the title didn't change**, verify with a grep like
  `re.search(r"(?m)^title:\s*(.*)$", text)` per generated file; expect 0 remaining PT phrases in
  en/es/fr (use a phrase-level heuristic, not single words like "Simulando" which is valid ES too).

## 4. Rollout discipline (for real sites)
- **Dry-run first**: translate 1 representative file and eyeball all targets before `--apply`.
- **Translate only the source language tree** (`pt-br/...`) into mirrored slugs in the other langs.
  Folder/file NAMES stay identical across langs (see §3 pitfalls: slugs mirrored by design); only
  page CONTENT + frontmatter `title` are translated.
- **Retrofitting (`--overwrite`)**: when re-running to add a disclaimer or translate titles on
  already-generated pages, pass `--overwrite` BUT keep the manual-file protection from §3c (skip
  hand-authored `en/*.md` plain files). Otherwise you clobber human work.
- **Check the publish config before push.** Quartz `ignorePatterns` may NOT exclude `es/`/`fr/` —
  if so, translated files go live on push. Prefer a manual `git commit`+`push` (the Quartz Syncer
  plugin has a known mass-deletion bug; see `quartz-multilang-site-maintenance`).
- **MT is a draft.** Heading labels and domain terms (astrophysics, etc.) come out rough. Review
  before exposing on a public site, or commit locally without push for human review.
- **Two MORE production pieces this class needs (added from the quartz-site rollout):**
  - **Auto-disclaimer.** Append a per-language notice to the END of every machine-translated page
    (after the last section / "Referências e correlatos"), stating it was auto-translated and citing
    the translator mechanism (e.g. `tools/translate_quartz.py`). Keep it in the page's own language.
    Implement as a `DISCLAIMER = {lang: "..."}` dict appended in `translate_body` after re-joining.
    Re-run with `--overwrite` on already-generated pages to retrofit the disclaimer.
  - **Missing-translation issue watcher.** A static site (GitHub Pages) CANNOT open an issue on
    every 404 visit (no backend → would spam issues). Instead use a **scheduled GitHub Action**
    (`cron` daily) that scans `content/` for slugs present in `pt-br/` but missing in `en/es/fr`,
    opens a labeled issue per gap (idempotent: skip if an open issue with the same title exists),
    using the repo `GITHUB_TOKEN`. Separately, the `404.tsx` shows the "translation missing" message
    + a pre-filled "open issue" link + a 5s redirect to the `pt-br` equivalent (client-side only).
    Create the issue label once via `gh label create`.

## 5. Verification (no test suite for this)
- `python3 -m py_compile script.py` (syntax)
- `python3 script.py --check` (engine reachable: `LT OK -> Hello test world!`)
- After `--apply`: `grep -rl '§[0-9]*§' <outdir>` must return 0 (no leaked placeholders);
  `grep -rl '!\\[\\[' <outdir>` should show embeds preserved; spot-check frontmatter unchanged.
- **Disclaimer present:** every generated page should contain the citation string
  (e.g. `grep -rl 'translate_quartz.py' <outdir>` == number of generated pages).
- **Don't claim `npm run check`/`test` as verification** for a standalone Python translator — those
  are the Quartz/Node build, not the translator. State the Python-level checks above instead.

## 5. Verification (no test suite for this)
- `python3 -m py_compile script.py` (syntax)
- `python3 script.py --check` (engine reachable: `LT OK -> Hello test world!`)
- After `--apply`: `grep -rl '§[0-9]*§' <outdir>` must return 0 (no leaked placeholders);
  `grep -rl '!\[\[' <outdir>` should show embeds preserved; spot-check frontmatter unchanged.

## Files in this skill
- `scripts/translate_markdown.py` — generalized, re-runnable template. Customize `CONTENT_ROOT`,
  `SRC_LANG`, `SECTIONS`, `TARGETS` near the top. Has `--check`/`--dry-run`/`--apply`,
  `--lang`, `--section`.
- `references/libretranslate-pitfalls.md` — the full iteration transcript of what broke and why.
- `references/advanced-patterns.md` — copy-pasteable code for the §3b advanced pitfalls
  (proper-name split, cell-by-cell tables, HTML-bold spans, local-link fallback, post-MT
  sanitize, external-URL protection, verification greps). START HERE when implementing.
- `references/html-block-preservation.md` — depth-counting parser + BODY-level extraction to
  keep raw HTML (carousels, `<div>` layouts) literal. USE when the source has embedded HTML.

> **Load this skill FIRST** for any "translate pt-br Markdown/Obsidian/Quartz into en/es/fr"
> task. Skipping it costs many rediscovery cycles (wikilink regex bug, proper-name
> translation, table corruption, post-MT spacing all bit before this was written down).
