# Animated Portfolio — extras (constellations, layering, SVG icons)

Condensed, copy-modify-ready snippets that extend SKILL.md.

## 1. Constellation coordinate data (relative 0–1 viewport)
```js
const C = {
  cruz: { // Cruzeiro do Sul — lower right
    stars: [[0.80,0.80],[0.83,0.70],[0.86,0.60],[0.84,0.50],[0.82,0.40]],
    lines: [[0,1],[1,2],[2,3],[3,4]] },
  ori: { // Orion / Três Marias — center
    stars: [[0.42,0.30],[0.46,0.38],[0.50,0.46],[0.40,0.55],[0.56,0.58],[0.36,0.70],[0.60,0.72]],
    lines: [[0,1],[1,2],[3,4],[0,3],[2,4],[3,5],[4,6],[5,6]] },
  escorp: { // Escorpião — lower left
    stars: [[0.12,0.55],[0.16,0.62],[0.20,0.68],[0.25,0.72],[0.30,0.74],[0.33,0.70],[0.32,0.64],[0.29,0.60]],
    lines: [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]] },
  cas: { // Cassiopeia (W) — upper left
    stars: [[0.10,0.18],[0.18,0.24],[0.26,0.16],[0.34,0.23],[0.42,0.15]],
    lines: [[0,1],[1,2],[2,3],[3,4]] },
  ursa: { // Big Dipper / Ursa Maior — upper right
    stars: [[0.62,0.14],[0.70,0.17],[0.78,0.16],[0.85,0.20],[0.88,0.27],[0.82,0.30],[0.74,0.28]],
    lines: [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,1]] }
};
```
Draw: for each constellation, `stars` = map coords to `{x,y,tw,r}`; `lines` connect indices.
Draw a synchronous frame at init: `drawConstel(performance.now())` before `requestAnimationFrame`.

## 2. Layering CSS (sky visible + text opaque)
```css
#starfield { position:fixed; inset:0; z-index:0; pointer-events:none; }
#galaxies  { position:fixed; inset:0; z-index:1.4; pointer-events:none;
             opacity:1; mix-blend-mode:screen; }
#constel   { position:fixed; inset:0; z-index:1.7; pointer-events:none; opacity:.95; }
.bg-veil   { position:fixed; inset:0; z-index:1; pointer-events:none;
             backdrop-filter:blur(2px); -webkit-backdrop-filter:blur(2px);
             background: linear-gradient(180deg, rgba(8,11,26,.30), rgba(8,11,26,.45)); }
nav, main, .footer { position:relative; z-index:2; }   /* content on top */
:root { --panel: rgba(17,21,46,0.82); }                 /* opaque cards */
```
Pitfall: a dark veil gradient >=0.7 hides the constellations. Keep it ~0.3-0.45.

## 4. Multi-language flag selector (PT/EN/ES/FR)
Top-bar markup (each button = inline SVG flag + label). Put it in `.nav` before the hamburger:
```html
<div class="lang-switch" role="group" aria-label="Idioma / Language / Idioma / Langue">
  <button class="lang-btn" data-lang="pt"><svg class="flag" viewBox="0 0 20 14"><rect width="20" height="14" fill="#009b3a"/><path d="M10 2.2 17.6 7 10 11.8 2.4 7z" fill="#ffdf00"/><circle cx="10" cy="7" r="2.4" fill="#002776"/></svg><span>PT-BR</span></button>
  <button class="lang-btn" data-lang="en"><svg class="flag" viewBox="0 0 20 14"><rect width="20" height="14" fill="#fff"/><g fill="#b22234"><rect width="20" height="1.4"/><rect y="2.8" width="20" height="1.4"/><rect y="5.6" width="20" height="1.4"/><rect y="8.4" width="20" height="1.4"/><rect y="11.2" width="20" height="1.4"/></g><rect width="8" height="7.6" fill="#3c3b6e"/></svg><span>EN</span></button>
  <button class="lang-btn" data-lang="es"><svg class="flag" viewBox="0 0 20 14"><rect width="20" height="14" fill="#aa151b"/><rect y="3.5" width="20" height="7" fill="#f1bf00"/><rect y="0" width="20" height="3.5" fill="#aa151b"/><rect y="10.5" width="20" height="3.5" fill="#aa151b"/></svg><span>ES</span></button>
  <button class="lang-btn" data-lang="fr"><svg class="flag" viewBox="0 0 20 14"><rect width="6.6" height="14" fill="#0055A4"/><rect x="6.6" width="6.8" height="14" fill="#fff"/><rect x="13.4" width="6.6" height="14" fill="#EF4135"/></svg><span>FR</span></button>
</div>
```
Logic (`applyLang` + `applyI18n`): keep `I18N` dict keyed by lang; re-render cards/bolsas/contatos
on switch. Persist with `localStorage.setItem('lang',l)`; read on load. On mobile, show the
switch inside the open menu: `.nav__links.open ~ .lang-switch { order:5; flex-basis:100%; display:flex; justify-content:center; }`.

## 5. Mouse REPULSION for galaxies (user-corrected; NOT attraction)
```js
mx += (tmx - mx) * 0.06; my += (tmy - my) * 0.06;
const mpx = (mx*0.5+0.5)*gw, mpy = (my*0.5+0.5)*gh;
const radius = Math.min(gw,gh)*0.7, maxPush = 160*gdpr;
for (const g of galaxies) {
  const bx = g.cx*gw, by = g.cy*gh;
  let tx=0, ty=0;
  const dx = bx-mpx, dy = by-mpy, dist = Math.hypot(dx,dy) || 1;
  if (dist < radius) { const f = 1 - dist/radius; const push = f*f*maxPush;
    tx = (dx/dist)*push; ty = (dy/dist)*push; }
  g.ox = (g.ox||0) + (tx-(g.ox||0))*0.08;
  g.oy = (g.oy||0) + (ty-(g.oy||0))*0.08;
  const cx = bx + g.ox, cy = by + g.oy;   // draw at offset center
}
```
Objective verify: `window.__test={galaxies}`; dispatch `mousemove` at a galaxy's center;
after ~600ms assert `ox` grows away (~ -35px). Remove exposure before commit.

## 6. Slow constellation drift (self-movement)
Each star: `ph: Math.random()*2π, amp: 4+Math.random()*6`. Per frame `t=now*0.00018`:
```js
const pos = c.stars.map(s => ({
  x: s.x*cw + Math.sin(t + s.ph)*s.amp*dpr,
  y: s.y*ch + Math.cos(t*0.8 + s.ph)*s.amp*dpr*0.6 }));
// draw lines + glow using `pos[a]`/`pos[b]` instead of `s.x*cw`
```

## 7. Contact box grouping (fixes mis-aligned label/value)
```html
<a class="contact__item" href="…">
  <svg class="contact__ico">…</svg>
  <span class="contact__text"><span class="contact__label">Email</span><span class="contact__value">…</span></span>
</a>
```
```css
.contact__item { display:flex; align-items:center; gap:14px; }
.contact__text { display:flex; flex-direction:column; gap:2px; min-width:0; }
.contact__value { overflow-wrap:anywhere; }
```
(Do NOT make label + value three flat siblings — nest them in `.contact__text`.)

## 3. SVG icon map (replace emoji)
Key the data file by icon name (`icon:"star"`), render with `iconSVG(p.icon)`.
`.ico{width:1.5em;height:1.5em;flex:none;display:block}`; `.contact__ico{width:22px;color:var(--accent)}`.
Use `currentColor` stroke so icons inherit text color. ~24 keys cover software/pesquisa/
academico/pessoal + contact channels (github, linkedin, scholar, orcid, lattes, instagram,
mail, pin, globe). Fallback `ICONS.star` for unknown keys.
