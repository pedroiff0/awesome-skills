# Inline HTML blocks (carousels) — the hard MT case

## The failure

Quartz pages often embed a carousel as an inline HTML block:

```
<div class="media-carousel">
  <a href="/pt-br/research/x" class="carousel-slide">
    <img src="/assets/x/y.png" alt="Texto PT" />
    <div class="slide-caption">Texto PT</div>
  </a>
  ...
</div>
```

Feeding this line-by-line to LibreTranslate corrupts it because the engine
treats HTML as text to "translate":
- `class="media-carousel"` -> `classe = "media-carrousel"` (with stray spaces)
- `href="/pt-br/research/x" class="carousel-slide"` -> `href = classe "/ pt-br / recherche / x" = "carrousel-glide"` (the engine MIXES `href` and `class` attributes!)
- `/assets/x/y.png` -> `/ actifs / x / y.png` (spaces injected into the URL, "assets"->"actifs")
- `<img ... />` -> `< img ... / >`

A naive non-greedy regex `<\w+...>.*?</\w+>` makes it worse: it matches only
the smallest tag (`<div class="slide-caption">...</div>` and `<img .../>`),
leaving the OUTER `<div class="media-carousel">` and `<a href=...>` to be sent
to the engine — which then mangles them.

## The fix: balanced-HTML extraction by tag depth

Do NOT use regex for nested HTML. Walk the text with a depth counter:

```python
HTML_TAG_RE = re.compile(r"<\s*(/?)\s*([a-zA-Z][\w-]*)([^>]*?)(/?)>")

def find_balanced_html(text):
    """Return (start, end) spans of HTML blocks that BEGIN at depth 0
    (e.g. the outer <div class="media-carousel"> ... </div>)."""
    spans = []
    opens = []          # stack of (tag, start) at depth > 0
    root_starts = []    # starts of blocks at depth 0
    i = 0
    while i < len(text):
        if text[i] != "<":
            i += 1; continue
        m = HTML_TAG_RE.match(text, i)
        if not m:
            i += 1; continue
        closing, tag, selfclose = m.group(1), m.group(2).lower(), m.group(4)
        j = m.end()
        if closing:
            if opens:
                opens.pop()
                if not opens:               # returned to depth 0
                    start = root_starts.pop()
                    spans.append((start, j))
        elif selfclose:
            pass                            # <img .../> doesn't push
        else:
            if not opens:
                root_starts.append(i)
            opens.append((tag, i))
        i = j
    return spans
```

In `translate_body`, extract these spans BEFORE line-by-line translation,
re-emit them literally (the whole block is preserved), and translate the
text BETWEEN blocks normally. This keeps `href`/`src`/`class` 100% intact.

## Then translate the INNER text only

A preserved block still shows captions/alt in the SOURCE language. To make
the carousel follow the page language, translate only `slide-caption` and
`alt` text, keeping attributes literal:

```python
def translate_carousel(html, target):
    def _cap(m):
        return f'<div class="slide-caption">{translate_line(m.group(1), target).strip()}</div>'
    html = re.sub(r'<div class="slide-caption">(.*?)</div>', _cap, html, flags=re.S)
    def _alt(m):
        return f'alt="{translate_line(m.group(1), target).strip()}"'
    html = re.sub(r'alt="(.*?)"', _alt, html)
    return html
```

Apply `translate_carousel` to each extracted block instead of keeping it raw.
Result: FR captions ("Clubs de revues"), ES ("Impacto de Satélites en
Observaciones"), EN ("ReLaTeX (LaTeX class)"), with `href="/pt-br/..."` and
`src="/assets/..."` untouched. Proper nouns inside (ReLaTeX, Journal Clubs)
survive because `translate_line` still applies the proper-noun protection.

## Gotcha

`.strip()` the translated caption/alt — the engine tends to prepend a space
(`alt=" Détection..."`). Without `.strip()` the space leaks into the attribute.
