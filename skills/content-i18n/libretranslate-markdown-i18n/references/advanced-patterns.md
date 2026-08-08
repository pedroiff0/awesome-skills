# Advanced patterns — LibreTranslate Markdown i18n (production)

Condensed, copy-pasteable patterns discovered the hard way. Pair with SKILL.md §3b.

## 1. Protected split: wikilinks + proper names (NEVER go to the engine)

```python
import re
WIKI_RE = re.compile(r"!?\[\s*\[\s*[^\]]*\]\s*\]\s*")   # mandatory first [, tolerate inner spaces
PROPER_NAMES = ["Ana Cecília Soja", "Soja", "Maycon Jorge Deláqua da Silva", "Deláqua", ...]
PROPER_RE = re.compile("|".join(re.escape(n) for n in PROPER_NAMES))
PROT_RE = re.compile(WIKI_RE.pattern + r"|" + PROPER_RE.pattern)

def translate_spans(text, target):
    if not text.strip():
        return text
    parts, last = [], 0
    for mm in PROT_RE.finditer(text):
        before = text[last:mm.start()]
        if before:
            parts.append(_translate_bold(before, target))          # translate the gap
            if parts[-1] and not parts[-1][-1].isspace() and mm.group(0)[0].isalpha():
                parts.append(" ")                                   # keep space before a name
        parts.append(mm.group(0))                                   # literal wikilink/name
        last = mm.end()
    if last < len(text):
        after = text[last:]
        if after:
            parts.append(_translate_bold(after, target))
    return "".join(parts)
```

## 2. Bold/italic as HTML (per span, not whole-doc)

```python
def _translate_bold(text, target):
    # protect() converts **x**-><strong>x</strong>, *x*-><em>x</em>; restore reverses
    prot, store, html = protect(text)
    fmt = "html" if html else "text"          # NEVER format=html for headings/whole lines
    out = lt_translate(prot, target, fmt=fmt)
    return restore(out, store)                # restore: <strong>->**, <em>->*, <br/>-><br>
```

## 3. Tables — translate cell by cell

```python
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:\-|]+\|\s*$")   # | :--- | :--- |
def translate_line(line, target):
    if TABLE_ROW_RE.match(line):
        if TABLE_SEP_RE.match(line):
            return line                        # separator untouched
        cells = [c for c in line.strip().strip("|").split("|")]
        tr = [translate_text_preserving_wiki(c, target) for c in cells]
        return "| " + " | ".join(tr) + " |"
```

## 4. Local-link fallback (pt-br/foo -> en/foo + tag, if missing in target)

```python
LOCAL_PREFIXES = ("pt-br/", "en/", "es/", "fr/")
FALLBACK_LANG = "en"
FALLBACK_TAG = {"en": "(in English)", "es": "(en español)", "fr": "(en français)"}

def _slug_exists(lang, slug):
    base = CONTENT / lang / slug
    return base.with_suffix(".md").exists() or (base / "index.md").exists()

def local_link(url, target):
    if not url.startswith(LOCAL_PREFIXES):
        return url, False
    _, slug = url.split("/", 1)
    if _slug_exists(target, slug):
        return f"{target}/{slug}", False
    if _slug_exists(FALLBACK_LANG, slug):
        return f"{FALLBACK_LANG}/{slug}", True     # signal fallback for the anchor tag
    return url, False                                        # keep original if even fallback missing
```

## 5. Sanitize spacing (AFTER translation, per line)

```python
def sanitize(line):
    line = re.sub(r"\)(?=[A-Za-zÀ-ÿ])(?!\*)", r") ", line)              # )et -> ) et
    line = re.sub(r"(?<=[A-Za-zÀ-ÿ])\[", r" [", line)                  # word[Link -> word [Link
    line = re.sub(r"(?<=[\])])\[", r" [", line)                        # )[Link -> ) [Link
    # NOTE: the two rules above intentionally do NOT fire on `[[` (wikilink) or `![` (embed)
    line = re.sub(r"(?<=[A-Za-zÀ-ÿ]) ' (?=[A-Za-zÀ-ÿ])", "'", line)    # l ' état -> l'état
    return line
```

## 6. External URLs in `[anchor](url)` — keep url literal

In `translate_with_links`, for each `[anchor](url)` match: translate ONLY `anchor`
(`translate_spans(anchor, target)`), re-emit `[{anchor_tr}]({url})`. The engine never
sees `http`. Verified failure when skipped: `https://integra.iff.edu.br/...` became
`https: / / integrra.iff.edu.br / p / ana-cecilia-soya`.

## 7. Verify after --apply
```bash
grep -rl '§[0-9]*§' <outdir>      # must be 0 (no leaked placeholders)
grep -rl 'ZZ[0-9]' <outdir>       # must be 0 (old token scheme)
# embeds intact:
grep -rn '!\[\[assets/' <outdir>  # should show ![[assets/...]] with NO space in ![[ or [[
# names preserved:
grep -rln 'Soya\|Chapitre 1' <outdir>   # must be 0
```
