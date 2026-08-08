# Markdown→static-site pipeline (condensed)

Goal: edit a data-driven static site in Markdown/Obsidian; site renders IDENTICALLY.

## Seam
Site = `index.html` + `style.css` + `main.js` (render engine) + `data.js` (`window.X = {...}`).
`main.js` reads `window.X` and builds the DOM. `data.js` is the ONLY thing that changes.

## Files
- `src/<site>.md` — source (YAML frontmatter). One field per language: `brief: {pt, en, es, fr}`.
- `tools/seed.js` (1x) — load original `data.js` (shim `window`/`module`), dump parsed object to MD.
- `tools/build.py` — MD → `data.js`. Real JS-literal emitter (NOT yaml).
- `tools/verify.js` — Node deep-equal(generated, original). Exit 1 on diff.
- `data.js.orig` — baseline for verify.
- `.git/hooks/pre-commit` — runs build.py; `git add data.js`.

## Emitter rules (Python → JS)
- str: `"..."` with `\` `\\` `\"` `\n` `\t` escaped.
- bool → true/false; None → null; list/dict → `[...]`/`{...}` (multi-line when long).
- Inline variables the original referenced (e.g. `ORCID`) → literal values, so runtime object equals original.
- Mirror i18n nesting EXACTLY (per-language objects vs per-field objects).

## Verify (the real test)
```js
const fn = new Function('window', src + '\nreturn window.X');
const w = {}; fn(w);
// deepEqual(w.X, originalParsed)
```
Byte `diff` is a FALSE positive — only the parsed object matters.

## Round-trip proof
seed → build → verify == pass → (edit one field) → build → field present in data.js →
revert → verify == pass. Then `git tag stable-display HEAD` before committing the pipeline.
