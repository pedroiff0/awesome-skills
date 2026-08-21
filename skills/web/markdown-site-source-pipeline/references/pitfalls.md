# Pitfalls — Markdown → Static Site Source Pipeline

## 1. Seed reads generated artifact (self-poisoning loop)
**Symptom:** after one bad `build.py`, every subsequent `seed_md.js` produces an
empty/partial `src/portfolio.md`, and the site loses sections (e.g. `CONTACTS = []`,
`EXTRA = {}`).
**Root cause:** seed loads `assets/js/projects.js` (the GENERATED file) to rebuild the
Markdown. When a build run corrupts that file, the seed freezes the corruption back
into the source, which the next build corrupts again. Circular.
**Fix:** seed MUST read a frozen baseline `assets/js/projects.js.orig` (snapshot of the
known-good site), never the generated artifact. Restore `projects.js` from `.orig`
before re-seeding.
```js
const SRC = fs.readFileSync(path.join(ROOT, 'assets/js/projects.js.orig'), 'utf8');
global.window = {};
new Function('window', SRC + '\nwindow.PORTFOLIO_DATA = window.PORTFOLIO_DATA || PORTFOLIO_DATA;')(global.window);
const D = global.window.PORTFOLIO_DATA;
```

## 2. Python module runs main() on import (double-execution)
**Symptom:** running `python3 -c "import build"` prints "Gerado: ..." and rewrites the
artifact, even though you only wanted to inspect a function. Two DEBUG lines appear.
**Root cause:** a top-level `main()` call or a malformed guard (`if "__main__" == "__main__":`
is fine, but a stray `generated = build(data)` at module scope is not) executes during
import, overwriting the file you're trying to debug.
**Fix:** keep ALL execution behind `if __name__ == "__main__": main()`. During debugging,
prefer a wrapper that monkey-patches the function and prints `id(data)` to confirm which
object the callee receives.

## 3. "Same dict, different value" illusion
When `len(data['contatos'])` is 9 in the caller but 0 inside `build(data)` despite
`id(data)` being EQUAL: the artifact on disk was already corrupted by pitfall #1, so the
`on-disk` file the build writes reflects the bad state even though an in-memory
`parse_source()` of the (good) Markdown returns 9. Always re-verify against `.orig`, and
restore the artifact from `.orig` before trusting any round-trip test.

## 4. JS serializer must emit valid JS, not YAML
A serializer that prints `key: value` without braces/commas/quotes produces
`const X = key: ...` → SyntaxError when the site loads it. Emit real JS literals:
strings double-quoted+escaped, arrays `[ ... ]`, objects `{ key: ... }`, `null`, `true/false`.
Multiline is fine for readability; the site only cares about the parsed object.

## 5. Verify semantically, not by bytes
The generated `projects.js` will NEVER be byte-identical to the original (key order,
quoting, formatting differ). What matters is `window.PORTFOLIO_DATA` being equal. Load
both files in a shim and deep-equal the object:
```js
function loadData(file){ const src=fs.readFileSync(file,'utf8');
  const w={}; new Function('window', src+'\nreturn window.PORTFOLIO_DATA;')(w); return w.PORTFOLIO_DATA; }
function deepEqual(a,b){ /* recursive: arrays length, dict keys, scalars === */ }
```
Any difference → fail the pre-commit.

## 6. KEY-NAME MISMATCH (PT vs EN) silently empties a section — THE REAL "same dict, different value" cause
**Symptom:** `parse_source()` returns `data['contatos']` with 9 items, but inside
`build(data)` the SAME object (`id(data)` identical) yields `data.get('contacts', []) == []`.
The artifact is written with `const CONTACTS = []` and the verify reports that section as
empty — even though `assets/js/projects.js.orig` is intact and the Markdown is correct.
**Root cause:** the parser emits the key in Portuguese (`"contatos"`), but the generator
reads it in English (`data.get("contacts")`). Mismatch → always defaults to `[]`. The
`id()` is identical because it IS the same dict; only the key string differs, so the value
lookup fails silently. (Pitfall #3 blames corruption; this is the more common root cause.)
**Fix:** keep key names IDENTICAL between `parse_source` return and `build()` consumption.
Pick ONE language for internal keys and use it everywhere (here: Portuguese dict keys like
`"contatos"`, `"bolsas"`, `"repos"` matching the `##` section headers). When debugging,
print `list(data.keys())` inside `build` AND `len(data['contatos'])` (not `.get`) to see
the mismatch immediately instead of chasing phantom corruption.

## 7. Omit redundant i18n so verify reaches 100% AND stays faithful
**Symptom:** verify reports `DIFERENÇA em REPOS` but every card's text looks identical
between generated and original.
**Root cause:** the parser heredits the 🇧🇷 text into en/es/fr when a translation is missing,
so `norm_repo( )` emits `i18n: {en,es,fr}` DUPLICATING the PT brief. The original site object
has NO `i18n` key for repos that were never translated — so the objects differ structurally.
**Fix:** in the normalizer, only emit `i18n[lang]` when it DIFFERS from the PT brief:
```python
i18n = {}
for l in LANGS:
    if l == "pt": continue
    if l in brief and brief[l] and brief[l] != brief.get("pt", ""):
        i18n[l] = brief[l]
if i18n: obj["i18n"] = i18n
```
This reproduces the `.orig` exactly (no fabricated translations) and the verify goes green.
Also regenerate the Markdown source (seed) after this change so the MD itself stops carrying
the redundant inherited translations — cleaner for the user to edit.

