# Preserving raw HTML blocks (carousels, `<div>` layouts) in MT

## Problem (bit hard)
LibreTranslate translates raw HTML blocks and DESTROYS them:
- `class="media-carousel"` -> `classe = "media-carrousel"` with spaces scattered
- `href="/pt-br/research/anomaly-detection" class="carousel-slide"` ->
  `href = classe "/ pt-br / recherche / anomalie / détection" = "carrousel-glide"`
  (the engine MIXES `href` with `class`!)
- `src="/assets/...png"` -> `src = "/ actifs / anomalie -détection / ..."`
  (spaces injected into URLs, "assets"->"actifs")
- `<img ... />` -> `< img ... / >`

## Why the naive regex fails
A single non-greedy regex like `<\w+...>.*?</\w+>|<...\/>` matches only the
SMALLEST tag. For a nested block `<div class="media-carousel"><a>...</a><div>..</div></div>`
it stops at the first inner `</div>` and never protects the outer wrapper, the
`<a>`, or the closing tags. Those leak to the LT and get mangled.

## Correct fix: depth-counting parser, applied at BODY level (not per-line)
The translator splits the body into LINES before translating, so a multi-line
HTML block is never seen whole by the line-level protector. Extract balanced
HTML blocks of depth 0 from the FULL body first, translate only the non-HTML
parts line-by-line, then re-insert the blocks literally.

```python
import re
HTML_TAG_RE = re.compile(r"<\s*(/?)\s*([a-zA-Z][\w-]*)([^>]*?)(/?)>")

def find_balanced_html(text: str):
    """Intervals (start,end) of HTML blocks that OPEN at depth 0
    (e.g. the <div class="media-carousel"> through its matching </div>)."""
    spans, opens, roots = [], [], []
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
                if not opens:               # back to depth 0
                    spans.append((roots.pop(), j))
        elif selfclose:
            pass                            # <img/> does not push
        else:
            if not opens:
                roots.append(i)
            opens.append((tag, i))
        i = j
    return spans

def translate_body(body, target):
    blocks = find_balanced_html(body)
    if blocks:
        parts, last = [], 0
        for (s, e) in blocks:
            before = body[last:s]
            if before:
                parts.append("\n".join(translate_line(l, target) for l in before.split("\n")))
            parts.append(body[s:e])        # literal HTML
            last = e
        if last < len(body):
            after = body[last:]
            parts.append("\n".join(translate_line(l, target) for l in after.split("\n")))
        out = "\n".join(parts)
    else:
        out = "\n".join(translate_line(l, target) for l in body.split("\n"))
    return fix_bold(out)
```

## Notes
- Self-closing tags (`<img .../>`, `<br/>`) are NOT pushed onto the depth stack,
  so inner `<div class="slide-caption">..</div>` (depth 1) is captured INSIDE the
  outer carousel block — exactly what we want.
- The preserved HTML keeps its captions in the SOURCE language (they live inside
  the protected block). That is acceptable cosmetically; if you need them
  translated, parse the caption text out and translate only that, then re-wrap.
- Sanitize the result with `fix_bold()` (see SKILL §3b/§fix_bold) AFTER re-joining,
  so bold inside AND outside HTML blocks is cleaned in one pass.
