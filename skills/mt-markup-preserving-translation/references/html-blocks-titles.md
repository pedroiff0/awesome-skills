# HTML blocks, section titles, and bold — extra Quartz lessons

Patterns added after the carrossel/section-title incidents. The base
regexes live in `verified-regexes.md`; these are the follow-on fixes.

## HTML BLOCKS — protect by TAG DEPTH, never regex
LibreTranslate DESTROYS inline HTML. Observed on a `<div class="media-carousel">`
block (carrossel): it rewrote `class="media-carousel"` -> `classe = "media-carrousel"`,
shuffled `href` with `class` (`href = classe "/ pt-br / recherche / anomalie / détection" = "carrousel-glide"`),
injected spaces into URLs (`assets` -> `actifs`, `/ pt-br / recherche`), and
`<img ... />` -> `< img ... / >`. The page layout breaks.

A single non-greedy `HTML_RE = <tag>.*?</tag>` MISSES nested blocks
(carousel = `<div><a><div>..</div></a></div>`) and corrupts the outer tags.
Use depth counting to extract top-level blocks before translating:

```python
import re
def find_balanced_html(text):
    spans=[]; stack=[]; opens=[]
    i=0
    while i < len(text):
        if text[i] == "<":
            m = re.match(r"<\s*(/?)\s*([a-zA-Z][\w-]*)([^>]*?)(/?)>", text[i:])
            if m:
                closing, tag, attrs, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
                j = m.end()
                if closing:
                    if opens: opens.pop()
                    if not opens:
                        start = stack.pop(); spans.append((start, j))
                elif selfclose:
                    pass
                else:
                    if not opens: stack.append(i)
                    opens.append((tag, i))
                i = j; continue
        i += 1
    return spans

def translate_carousel(html, target):
    # translate ONLY inner text (slide-caption / alt); keep href/src/class literal
    html = re.sub(r'<div class="slide-caption">(.*?)</div>',
                  lambda m: f'<div class="slide-caption">{translate_line(m.group(1), target).strip()}</div>',
                  html, flags=re.S)
    html = re.sub(r'alt="(.*?)"',
                  lambda m: f'alt="{translate_line(m.group(1), target).strip()}"', html)
    return html
```
In `translate_body`: extract top-level HTML blocks FIRST, translate the text
between them line-by-line, and for each block run `translate_carousel` (do NOT
feed the whole block to LT). Names proper (ReLaTeX, Journal Clubs) stay literal.

## Section titles — canonical, NOT engine output
LT mis-translates by context: PT "Pesquisa" -> EN "Search" (should be
"Research"); "Mídia" -> "Means"/"Moyens" (should be "Media"/"Médias");
"Pesquisa" -> FR "Recherche" but EN "Search". Force canonical titles for
1st-level `index.md` by language:

```python
SECTION_TITLES = {
  "research": {"pt-br":"Pesquisa","en":"Research","es":"Investigación","fr":"Recherche"},
  "media":    {"pt-br":"Mídia","en":"Media","es":"Medios","fr":"Médias"},
}
# rel is relative to content/<SRC>: rel="research/index.md" -> rel.parent.name
# == "research", rel.name == "index.md". (NOT rel.parent.name == "content".)
if field == "title" and rel.name == "index.md":
    sec = rel.parent.name
    if sec in SECTION_TITLES and lang in SECTION_TITLES[sec]:
        tr = SECTION_TITLES[sec][lang]   # skip LT entirely
```

## Bold grudado — post-process the whole body
LT glues spaces inside bold: `* * méthode * *` (kept) or `** Informatique **`.
Normalize AFTER translation on the FULL body (covers callouts/tables that
`sanitize()` per-line does not reach):

```python
def fix_bold(text):
    text = re.sub(r"\*\*\s+(.+?)\s+\*\*", r"**\1**", text)   # ** texto **
    text = re.sub(r"\*\*\s+(.+?)\*\*", r"**\1**", text)      # ** texto**
    text = re.sub(r"\*\*(.+?)\s+\*\*", r"**\1**", text)      # **texto **
    text = re.sub(r"\*\s+\*\s+(.+?)\s+\*\s+\*", r"**\1**", text)  # * * x * *
    text = re.sub(r"(?<!\*)\*\s+(.+?)\s+\*(?!\*)", r"*\1*", text)  # * x *
    return text
```

## VERIFY TSX with `npm run check`, not just the deploy
The Quartz GitHub Actions deploy uses a PERMISSIVE transpile and PASSES even
when `tsc --noEmit` (the `npm run check` script) fails. Real errors caught
only by `npm run check`:
- unused import (`'i18n' is declared but its value is never read` TS6133)
- `onError="..."` string on an `<img>` — Preact wants a function
  `GenericEventHandler`, not an inline string. Use
  `onError={(e) => { e.currentTarget.style.display="none"; ... }}`.
If `node_modules` is present, run `npm run check` locally before pushing —
the deploy success is NOT proof the TSX type-checks. (The repo's
`quartz/i18n/locales/*.ts` have PRE-EXISTING unrelated TS errors; ignore those.)
