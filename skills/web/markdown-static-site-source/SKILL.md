---
name: markdown-static-site-source
description: Make a data-driven static site (content lives in a JS/JSON object consumed by a render script) editable from Markdown/Obsidian. Generate the data file from a YAML-frontmatter MD source and verify fidelity with SEMANTIC deep-equal (not byte comparison), keeping the HTML/CSS/render engine untouched so the site renders identically.
author: Static Site Community
---

# Markdown as the source of truth for a JS-data-driven static site

## When to use
- A static site (plain HTML/CSS/JS, no build framework) renders content from a data object in a JS file, e.g. `window.PORTFOLIO_DATA = {...}` consumed by a render script (`main.js`) that builds the DOM.
- The user wants to edit content in Markdown / Obsidian and have the site update, WITHOUT touching the HTML/template/CSS.
- The render must stay EXACTLY the same (pixel/semantics identical to today).

## Core idea
Find the "data seam": the single JS object the render engine reads. Make a Markdown file with YAML frontmatter the SOURCE OF TRUTH. Write a tiny generator that emits that same JS object. The render engine never changes → output is identical by construction. Verify the emitted object is semantically equal to the original, NOT byte-equal (formatting differs, meaning must not).

## Steps
1. Locate the data object. Grep for `window.<X> =` / `const PORTFOLIO_DATA`. Confirm what consumes it (e.g. `main.js` reads `window.X` and builds DOM).
2. Snapshot the original data file to `*.orig` — this is your verification baseline.
3. (Optional, one-time) `seed.js`: load the original JS (shim `window` / `module.exports`), dump the parsed object to a YAML-frontmatter MD. Freezes today's content as the source.
4. `build.py`: read the MD, emit valid JS reconstructing the SAME object:
   - Serialize with a real JS-literal emitter (objects/arrays as `{}/[]`, strings double-quoted with `\"` and `\n` escapes). Do NOT emit YAML — the browser must evaluate it.
   - Preserve structure exactly: same keys, same nesting, same field order where the consumer relies on it.
   - Resolve constants: if the original referenced variables inside the data (e.g. `"https://orcid.org/" + ORCID`), inline the values so the generated object equals the original at runtime.
   - For i18n, mirror the EXACT nesting of the original (e.g. bolsas may nest `i18n.en = {title,kind,desc}` per language). Match it; don't transpose unless you also change the consumer.
5. `verify.js` (Node): load BOTH the generated file and `*.orig` via `new Function('window', src + 'return window.X')`, then deep-equal the objects. Exit 1 on diff. This is the real test — a byte `diff` will always show false positives.
6. Pre-commit hook: run `build.py` so `git commit` always recompiles; `git add` the generated file.
7. User workflow: edit `src/<site>.md` in Obsidian → `python3 tools/build.py` → `git add -A && git commit && git push`.

## Pitfalls
- Emitting YAML instead of JS: the browser can't consume it. Use a JS-literal emitter.
- Comparing generated vs original by `diff`/bytes: formatting always differs → false alarms. Compare the PARSED OBJECT.
- Transposed i18n: if you restructure how translations are stored in the MD, the generator must re-nest to the consumer's expected shape, or the render breaks. Keep the consumer untouched.
- Round-trip drift: after `seed`, immediately `build` + `verify` and confirm deep-equal BEFORE editing. If not equal, fix the serializer first.
- Never hand-edit the generated data file — it's a build artifact the hook overwrites.
- Version the stable display first: `git tag stable-display HEAD` before introducing the pipeline, so the user can revert if the round-trip isn't faithful.

## Verification (ad-hoc, run after changes)
`node tools/verify.js` must print "<VAR> gerado == original". Also: edit one field in the MD, rebuild, confirm it appears in the generated file, then revert and re-verify.

## References
- `references/pipeline-pattern.md` — condensed walkthrough of the seed→build→verify sequence.
- `scripts/generate_js_data.py` — generalized MD(frontmatter)→JS generator skeleton (adapt `normalize()` to the site's schema; emits valid JS).
- `scripts/verify_deep_equal.js` — generalized Node deep-equal verifier for two JS data files.
