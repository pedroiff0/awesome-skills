# LibreTranslate Markdown i18n — pitfall transcript

What broke across 6 iterations of translating a Quartz/Obsidian vault (pt-br -> en/es/fr),
and the fix for each. Captured so the next session does not re-discover them.

## Attempt 1 — raw Markdown, format=html
Sent the whole `.md` body to `POST /translate` with `format=html`.
- EN: H1 became empty (`# `), H2 emojis vanished, `**` ground into text (`Society (SAB 2026)**,`).
- ES: 👋 became "apocalíptico" (`## apocalíptico Mi participación`).
- FR: H1 corrupted to `▼`, `[!note]` lost the `!`, `##` -> `# #`, bold glued.
Lesson: never hand raw Markdown to MT.

## Attempt 2 — text-only per line, but markup still inline
Extracted text after block prefix but still let the engine see emojis and `**`.
- Bold still glued; emoji in heading still "translated" (👋 -> "Argicos" in ES/FR).
Lesson: emojis adjacent to markup must be excluded from the translated span.

## Attempt 3 — invisible-control placeholders \x00/\x01
Protected bold/emoji/wikilink as `\x00N\x01` before sending.
- EN worked. ES/FR STRIPPED the control chars -> output had `\u00000`, `01`, `0` where emojis were.
Lesson: invisible placeholders leak in some target languages. Use a VISIBLE token.

## Attempt 4 — visible token §N§
Replaced with `§N§`.
- ES showed `🗓1§` (engine spaced/reordered), FR showed `§ 0 §` and the restore
  `.replace("§0§")` did NOT match `§ 0 §` -> placeholder leaked into output.
- FR wikilink `![[assets/banners/X.pdf|Y]]` was DELETED by the engine -> "Chapitre 1".
Lesson: restore with tolerant regex `§\s*(\d+)\s*§`; extract wikilinks positionally, never placeholder them.

## Attempt 5 — emoji into prefix + wikilink positional split
Prefix regex consumed emoji after markup; wikilinks kept literal via split.
- Markup 100% intact, embeds preserved, zero leaks. Remaining: emoji glued to text
  (`## 🗓️About` no space) and FR injected a stray `-` at heading start (`## - À propos`).
Lesson: rejoin with a guaranteed space after prefix; strip leading `- `/`# `/`*` from translated text.

## Attempt 6 (FINAL) — clean
`## 🗓️ About the event`, `## 📎 Bannière`, embeds literal, bold/links preserved, 0 leaks.
Validated on 42 files (14 media x 3 langs): `grep -rl '§[0-9]*§'` -> 0; embeds present.

## Operational notes
- LT first-start downloads models; poll `curl .../ ` for HTTP 200 (up to ~2 min).
- `LT_LOAD_ONLY=pt,en,es,fr` + `LT_UPDATE=false` keeps the image lean.
- 42 files took ~4 min single-threaded (one HTTP call per text span). Run `--apply`
  in background with notify; it exceeds a 60s foreground timeout.
- Quartz `ignorePatterns` did NOT exclude es/fr -> translated files go live on push.
  Commit locally (no push) for human review, or accept MT-draft quality on the public site.
  Use manual `git commit`+`push`, NOT Quartz Syncer (known mass-deletion bug).
