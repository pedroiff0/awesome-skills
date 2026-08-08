# LibreTranslate quirks — learned the hard way

## Placeholders DO NOT survive the engine
Tried, all failed in at least one language (en/es/fr):
- Invisible control chars `\x00`/`\x01` → engine DELETES them (leak: literal `0`/`01`).
- `§N§` → engine spaces it (`§ 0 §`) or deletes it (`2§`).
- `ZZNZZ` → engine corrupts (`2ZZ`, `Z0ZZ`).
Root cause: the MT engine normalizes/strips "weird" tokens. Restore-by-key then can't
match. **Fix: never rely on placeholders for anything the engine might touch.** Use HTML
tags (`<strong>`, `<em>`) for bold/italic — the engine is built to preserve HTML and only
translates text inside. For wikilinks, exclude them from the request entirely (split the
line and keep them literal).

## Emojis
If an emoji is in the string sent to the engine, it gets "translated": 👋 -> "Argicos"
(es), "Apocalíptico" (es), etc. Always pull the emoji into a non-translated prefix so the
engine never sees it.

## Headings
Engine rewrites `##` -> `#` and may inject a leading `- ` or `# ` into the translation.
Strip the `## ` (and any emoji) as a prefix; re-prepend after translate; regex-clean a
leading `^[\-\*\#]\s+` from the result.

## Tables
Sending a whole `| a | b | c |` row → engine drops the inner `|` and returns loose text
with the columns merged. Must split on `|`, translate per cell, rejoin. Separator row
`| :--- | :--- |` returned verbatim.

## format=text vs format=html
- Plain text lines: `format=text` is fine and keeps things stable.
- Lines containing `**`/`*`/`**`/`*`: convert to `<strong>`/`<em>` and use `format=html`.
  The engine preserves the tags. After translate, revert tags to markdown.
- Do NOT use format=html for the WHOLE file — it mangles headings/emojis (collapses `##`,
  drops emojis). Use it only on the bold-containing spans.

## Docker
- Image `libretranslate/libretranslate:latest`. `LT_LOAD_ONLY=pt,en,es,fr` limits models
  (faster startup, less RAM). `LT_UPDATE=false` avoids auto model downloads on each run.
- Models download on first start (~1-2 min). Poll HTTP 200 before translating.
- ~6 CPU / 16GB RAM machine handled it fine alongside other work.

## Performance
~1 file per 3-4s (multiple LT calls per file: per body line + per table cell). 42 files
(en/es/fr × 14 media) took ~4-5 min. Run with --apply in background and poll.
