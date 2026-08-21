# Verified regexes & patterns (from real LibreTranslate Quartz runs)

These are the exact patterns that worked after multiple broken attempts. Use them;
do not fall back to `§N§`/`ZZ` placeholder stashing for anything except bold/italic
(which uses real HTML tags, not placeholders).

## Wikilinks / embeds — MUST capture the `!`
```python
# FIRST [ is MANDATORY (no \s* before it) so the `!` of embeds is kept.
# Tolerates spaces the engine inserts between inner brackets.
WIKI_RE = re.compile(r"!?\[\s*\[\s*[^\]]*\]\s*\]\s*")
# Broken version that DROPPED the `!` (match started after `!`):
#   r"!?\s*\[\s*\[..."   -> produced `[[[assets/..]]` (3 brackets), broke embed
```

## Proper nouns — positional, never to engine
```python
PROPER_NAMES = ["Ana Cecília Soja", "Soja", "Maycon Jorge Deláqua da Silva",
                "Deláqua", "Maria Luiza Linhares Dantas", "Linhares Dantas", ...]
PROPER_RE = re.compile("|".join(re.escape(n) for n in PROPER_NAMES))
# Combine for the split:
PROT_RE = re.compile(WIKI_RE.pattern + r"|" + PROPER_RE.pattern)
# In translate_spans: finditer PROT_RE, keep literal spans, translate BETWEEN them.
# Engine rewrites "Soja"->"Soya"/"Chapitre 1" if it ever sees the name.
```

## Links — split, keep url literal
```python
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")   # any [text](url)
# translate anchor only; re-emit with ORIGINAL url. Engine mangles URLs:
# integra.iff.edu.br/p/ana-cecilia-soja -> "https: / / integrra... / p / ana-cecilia-soya"
```

## Tables — per-cell
```python
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:\-|]+\|\s*$")  # | :--- | :--- | -> verbatim
# split row on |, translate each cell, rejoin "| "+" | ".join(cells)+" |"
```

## Bold/italic — HTML tags (engine preserves real tags)
```python
BOLD_RE = re.compile(r"\*\*(?<!\\*)\*([^*]+)\*\*")   # avoid tri-greedy
ITAL_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
# -> <strong> / <em>, call LT with format=html
# revert: <\s*strong\s*> -> ** , <\s*em\s*> -> * , <\s*br\s*/?\\s*> -> <br>
```

## Sanitize (append to each translated line; do NOT space wikilink/embed brackets)
```python
# space before [ ONLY if char before is letter or ) — never ! or [
line = re.sub(r"(?<=[A-Za-zÀ-ÿ])\[", r" [", line)
line = re.sub(r"(?<=[\])])\[", r" [", line)
# ) followed by letter (not *) -> space
line = re.sub(r"\)(?=[A-Za-zÀ-ÿ])(?!\*)", r") ", line)
# French apostrophe spaced out -> rejoin
line = re.sub(r"(?<=[A-Za-zÀ-ÿ]) ' (?=[A-Za-zÀ-ÿ])", "'", line)
# Naive "any non-space before [" corrupts ![[..]] into ! [ [ .. -> BROKEN.
```

## index.md + slug collision
```python
# Do NOT `if p.name == "index.md": continue` — skips principal pages.
# When emitting en/<dir>/index.md, skip if en/<dir>.md exists (dup slug, build breaks).
sibling = out_path.parent.with_suffix(".md")
if out_path.name == "index.md" and sibling.exists():
    skip("conflito de slug com " + sibling.name)
```

## Disclaimer (append to every translated page, in target language)
```
> [!abstract] <title>
> <text citing the translator, e.g. tools/translate_quartz.py>
```
Append AFTER the last section (References / Correlatos). Do not translate the disclaimer.
