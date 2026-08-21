---
name: markdown-site-source-pipeline
description: Keep a static HTML/JS site's content in an editable Markdown source file; generate the data artifact (JS/JSON) the site consumes; guarantee identical render via semantic deep-equal verification. Use when a user wants to edit a static site (portfolio, docs) in Markdown/Obsidian instead of hand-editing generated data files, OR when building a "write in MD, publish identical HTML" workflow.
---

# Markdown → Static Site Source Pipeline

## When to use
- A static site (HTML + CSS + JS) renders content from a data file (e.g. `window.PORTFOLIO_DATA` in `assets/js/*.js`, or a JSON fed to a template).
- The user wants to author content in Markdown/Obsidian, not in JS/YAML/JSON.
- Goal: edits to the Markdown must produce a byte-faithful (semantically identical) artifact so the rendered site is UNCHANGED in structure/appearance.

## Core principle
Treat the data artifact (JS/JSON) as a **build output**, never as source. The site's render logic (HTML/CSS/`main.js`) stays untouched. Markdown is the source of truth. This guarantees "render exactly the same" because the consumer reads the same object shape.

## Pipeline shape
1. `src/<site>.md` — editable source (clean Markdown, see format below).
2. `tools/build.py` (or .js) — parses the MD, emits the data artifact.
3. `tools/verify.<js|py>` — loads BOTH the generated artifact and a stable baseline, deep-equals the parsed object (semantic, NOT byte diff). Fails the build if different.
4. `tools/seed.<js>` — one-off generator that freezes the CURRENT site content into the MD source (run when bootstrapping or re-syncing).
5. `.git/hooks/pre-commit` — runs `build.py` so every commit recompiles the artifact.

## Source format (USER PREFERENCE — do not violate)
This user (Pedro) REJECTED nested YAML frontmatter as "muito ruim de editar". Use **clean Markdown**, not a YAML document:
- One `### Title` per item (project/bolsa/contact).
- Single-line fields: `repo:`, `stack:`, `tags:`, `cat:`, `visibility:`, `icon:`.
- Multilingual text via inline flag prefixes, one paragraph each:
  `🇧🇷 pt text` / `🇺🇸 en text` / `🇪🇸 es text` / `🇫🇷 fr text`.
- If a translation is missing, INHERIT the 🇧🇷 text (don't force all 4 languages).
- Keep rarely-edited interface/i18n menus in a SEPARATE file (`src/interface.yaml`), NOT inside the editable MD. The generator reads both `src/portfolio.md` and `src/interface.yaml`. Pedro found a trailing i18n block inside the MD still "muito dificil" — isolating it in its own file is what made editing tractable.
See `templates/portfolio.source.md` for a concrete example.

## Build/verify rules
- Verify by **deep-equal of the parsed object** the site actually consumes (e.g. load both JS files in a `new Function('window', src+'return window.X')` shim and `deepEqual`). Byte-identical output is NOT required and usually impossible (key order, quoting). Semantic equality is what guarantees identical render.
- The generator's JS serializer must emit VALID JS literals (`py_to_js` that handles strings/arrays/dicts/null/bool, with proper quoting + multiline when long). A YAML-style emitter will produce `const X = key: ...` which is a SyntaxError.
- Multilingual nesting must match the original: if the source object is `i18n.en = {title,kind,desc}`, the MD must re-emit that shape (don't transpose to `i18n.title = {en,es,fr}` unless the generator transposes back).

## Pitfalls (see references/pitfalls.md)
- **Seed must read a STABLE baseline (`.orig`), never the generated artifact.** A generator that writes `projects.js` and a seed that reads `projects.js` will poison itself: one bad build corrupts all future seeds. Keep `assets/js/*.js.orig` as the frozen reference.
- A Python module whose `main()` runs at import (no proper `if __name__=='__main__'` guard, or a stray top-level call) double-executes during `python3 -c "import x"` debugging and overwrites the very file you're inspecting — confusing. Always guard `main()`.
- Don't `git push` until `verify` is green AND the artifact on disk matches the baseline. A corrupted intermediate (e.g. `CONTACTS = []`) will publish broken.
- **KEY-NAME CONSISTENCY (PT vs EN):** the parser and the emitter MUST use the SAME key language. A `parse_source` that returns `data["contatos"]` (PT) while `build` reads `data.get("contacts")` (EN) silently yields `[]` for that whole section — `id(data)` stays identical, so it looks like phantom corruption. Pick one language for internal dict keys (here: Portuguese, matching `##` headers) and use it everywhere. When a section comes out empty, print `list(data.keys())` inside `build` before anything else. (See pitfalls.md #6.)
- **Pull rarely-edited config OUT of the editable MD.** Menu/hero/section/footer i18n is large and changes almost never. Keep it in a separate `src/interface.yaml` (or `.json`) that the generator merges in; the user edits only `src/portfolio.md`. This single move turned an "impossible to edit" MD into a tractable one for Pedro. (See pitfalls.md #8.)

## Commit/push discipline
- Tag the original display version (`git tag stable-display <base_commit>`) before introducing the pipeline, so the user can roll back.
- Commit the MD + tooling + `.orig`. Don't push a render unless verify passes.
