# Layout / width / spacing tips for the static portfolio

Reusable CSS patterns that emerged while widening the body and fixing broken cards.

## 1. Widening the body — but `max-width` alone breaks grids
`--maxw` (or `.page` in Quartz) controls the centered content width. Raising it (portfolio 1180→1800; Quartz `.page` 1500→1700→1850) pushes content toward the borders. BUT if the grids use `repeat(auto-fit, minmax(280px,1fr))`, a wide container now fits 4–5+ columns and cards look stretched/ugly. Fix by switching those grids to FIXED column counts once wide:

```css
.cards    { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.bolsas   { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.contact  { grid-template-columns: repeat(5, minmax(0, 1fr)); }  /* 9 items → 5+4 balanced */
```
`minmax(0, 1fr)` (NOT `minmax(220px,1fr)`) is essential: the `0` min lets children shrink so long text/values don't overflow the track. Keep responsive fallbacks:
```css
@media (max-width: 900px) { .contact { grid-template-columns: repeat(3, minmax(0,1fr)); } }
@media (max-width: 600px) { .cards,.bolsas,.contact { grid-template-columns: 1fr; } }
```

## 2. Contact cards clipping the last characters
Symptom: `pedroiff0@gmail.com` / `0009-0003-6724-4640` / `6818168089966785` cut off at the card edge (esp. when column count was high and cards were narrow).
Fix trio:
```css
.contact__item { min-width: 0; padding: 18px 22px; }
.contact__text { min-width: 0; overflow: hidden; }
.contact__value { overflow-wrap: anywhere; }
.contact__label { white-space: nowrap; }
```

## 3. Hiding the scrollbar while keeping scroll functional
User asked to "make the scrollbar disappear". Don't use `overflow: hidden` (kills scrolling). Use:
```css
body { scrollbar-width: none; -ms-overflow-style: none; }
body::-webkit-scrollbar { display: none; }
```
Scroll still works (wheel/trackpad/keyboard); only the visual thumb is gone.

## 4. Reducing excessive whitespace between sections
```css
.section       { padding: 54px clamp(16px,4vw,32px); }
.section__head { margin-bottom: 22px; }
.hero          { padding-top: 84px; }   /* was 110px */
```
Rule of thumb: section vertical padding 50–60px and head→content gap ~20px reads tight and modern; 80px+ feels empty on wide screens.

## 5. Quartz body width override (no motor edits)
The Quartz fork sets `.page { max-width: calc(desktop + 300px) }` (=1500px) in `quartz/styles/base.scss`. To widen WITHOUT touching the motor, override in `quartz/styles/custom.scss` (already `@use`d, loaded last):
```scss
.page { max-width: 1850px; }   /* ~35px side margin on 1920px */
```
Cautious progression the user accepted: 1500 → 1700 → 1850. Don't overshoot or side margins vanish on 1920 displays.
