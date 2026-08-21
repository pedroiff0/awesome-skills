---
name: mt-markup-preserving-translation
description: Translate Markdown/Obsidian/Quartz content with LibreTranslate while preserving wikilinks, embeds, URLs, tables, HTML blocks, proper nouns, and canonical section titles. Use for any "translate this vault/site" task.
---

# Markup-preserving MT translation

The engine (LibreTranslate) WILL corrupt your source if you hand it raw Markdown. The fix is a single principle: **never let the engine see anything structural** — split the line, keep markup/URLs/wikilinks/proper-nouns/HTML literal, translate only the plain-text spans between them, rejoin.

## Core strategy (apply in this order, per line)

1. **Split positional, not placeholder.** Find protected spans (wikilinks, embeds, proper nouns, inline HTML) with `re.finditer`, keep them literal, translate the text BETWEEN them. Placeholders (`§N§`, `ZZNZZ`, `\x00N\x00`) are silently mangled by the engine (see references/libretranslate-notes.md) — do NOT use them for anything except bold/italic (which uses real HTML tags: `<strong>`/`<em>` with `format=html`).
2. **Wikilinks/embeds** — capture with `!?\[\s*\[\s*[^\[\]]*\]\s*\]\s*` (the FIRST `[` is mandatory so the `!` of embeds is kept; a leading `\s*` before `[` drops the `!` and yields broken `[[[`). Keep literal — engine turns `![[assets/b/b.pdf|B]]` into `[ [ [assets/b/b.pdf|Banner]]`.
3. **Internal links** — `\[([^\]]*)\]\(([^)]+)\)`; translate only the anchor text, re-emit with the ORIGINAL url. Engine mangles URLs (`integrra.iff.edu.br/p/x` -> `https: / / integrra ... / x`).
4. **Proper nouns** — positional, NOT to the engine. "Soja" -> "Soya", "Ana Cecília Soja" -> "Chapitre 1" if seen. Stash as literal spans (longest-first ordering matters).
5. **Tables** — split each row on `|`, translate per cell, rejoin. Engine drops inner `|` and merges columns if given the whole row.
6. **Bold/italic** — convert `**x**`->`<strong>x</strong>`, `*x*`->`<em>x</em>`, call engine with `format=html`, revert tags after. Engine preserves real HTML tags.
7. **Headings** — strip `## ` (+ emoji) as a prefix, re-prepend after translate; clean a leading `^[-\*#]\s+` the engine may inject.

## Inline HTML blocks (carousels etc.) — the hard one

**Non-greedy regex (`<\w+...>.*?</\w+>`) is NOT enough** for nested tags: it matches the smallest tag and leaves the outer wrapper (`<div class="media-carousel">`, `<a href=...>`) to be fed to the engine, which then corrupts attributes and spaces URLs (`< div classe = "media-carrousel" >`, `href = classe "/ pt-br / ... " = "carrousel-glide"`).

**Fix (see references/carousel-html.md):** extract balanced-HTML blocks by TAG DEPTH before translating the line, preserve them, then translate ONLY the inner text (e.g. `slide-caption` / `alt`) while keeping `href`/`src`/`class` literal. A depth-counting loop (push on open, pop on close, emit span when depth returns to 0) is the correct tool — regex cannot balance tags.

## Frontmatter titles & section titles

- Translate `title`/`description` per language, keep the slug/URL intact (only the DISPLAY changes).
- The engine mis-contexts academic terms: "Pesquisa" (pt) -> "Search" (en) when it should be "Research". For 1st-level `index.md` of known sections, force canonical titles via a `SECTION_TITLES` map (research->Research/Investigación/Recherche, media->Media/Medios/Médias, ...). Detect by `rel.name == "index.md"` and `rel.parent.name == section`.

## i18n slug rule (Quartz)

Keep slugs IDENTICAL across languages; only the language prefix in the URL changes. **Do NOT translate folder/file names** — the LanguageToggle swaps only the prefix segment, so renaming slugs breaks it (and causes "duplicate slug" build errors when `en/X.md` and `en/X/index.md` both exist). When emitting `en/<dir>/index.md`, skip if `en/<dir>.md` already exists (manual page at that slug).

## Disclaimer

Append a per-language "translated automatically" notice (citing the translator, e.g. `tools/translate_quartz.py`) AFTER the last section. Do not translate it.

## Guardrails when emitting

- Never overwrite existing `en/*.md` flat files (manual pages) even with `--overwrite`; skip them (`lang == "en" and out_path.name != "index.md"`).
- Sanitize spacing AFTER translate but NEVER insert a space between `[[` or `![` (breaks embeds): space before `[` only if the preceding char is a letter or `)` (not `!` or `[`).

## Support files
- `scripts/translate_quartz.py` — worked, validated example for a Quartz/Obsidian vault (the full pipeline above).
- `references/libretranslate-notes.md` — engine quirks (placeholder failures, emoji, headings, tables, format=text vs html, Docker).
- `references/verified-regexes.md` — the exact regexes that survived real runs.
- `references/carousel-html.md` — balanced-HTML extraction + translate-inner-text for carousels.
- `references/html-blocks-titles.md` — carrossel/HTML-by-depth protection, canonical
  section titles (Pesquisa->Research, not Search), fix_bold post-process, and the
  "verify TSX with `npm run check`; the GitHub deploy transpile is permissive" pitfall.
