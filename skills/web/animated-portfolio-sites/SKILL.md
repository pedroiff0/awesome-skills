---
name: animated-portfolio-sites
description: Build a one-page animated personal or portfolio site (canvas starfield, rotating galaxies with mouse parallax, hidden accordion/card content, anchor nav) and publish it free on GitHub Pages. Covers the canvas technique and the Pages permission wall, not just one task.
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [web, portfolio, github-pages, canvas, animation, single-page, ui]
platforms: [linux, macos, windows]
triggers:
  - build a portfolio site
  - personal page / CV site / resumé site
  - one-page website with anchors
  - animated background (stars, galaxies, particles)
  - rotating galaxies / starfield canvas
  - constellations, Cruzeiro do Sul, Orion, Escorpião, Cassiopeia, Big Dipper
  - background blur + opaque text layering
  - SVG icons instead of emoji (tofu boxes)
  - mouse REPULSION background (push away from cursor, slow self-movement)
  - multi-language site (PT/EN/ES/FR flag selector, i18n, persisted)
  - responsive mobile menu (hamburger + in-menu language switch)
  - publish on github pages
  - GitHub Pages 422 / private repo pages
---

# Animated Portfolio Sites

Build a single-page, anchor-navigated personal/portfolio site with a "wow" animated
background, hidden-on-click content, and publish it free on GitHub Pages.

For visual tokens (color palettes, typography, component CSS) of known brands, pair
with the `popular-web-designs` skill (Stripe/Linear/Vercel/etc.). This skill covers the
**structure, canvas animation technique, and the Pages publishing wall**.

## When to use
- User wants a "cool" personal site, portfolio, CV, or short-resumé page.
- Astronomy/space/dark theme is requested (or you choose it for impact).
- They want it on GitHub Pages.

## Architecture (single file, no build step)
- `index.html` — page + sections with `#anchor` ids; nav links to them.
- `assets/css/style.css` — theme via CSS custom properties (`--accent`, `--grad`…).
- `assets/js/projects.js` — `window.PORTFOLIO_DATA = { REPOS, FEATURED, RESEARCH, BOLSAS, CONTACTS, FULL_NAME, ORCID }` (data-driven; list public AND private repos with short briefs without touching HTML).
- `assets/js/main.js` — renders cards/accordions/contacts, canvas animation, scroll reveal, nav.

## Hidden-until-click content
CSS `max-height` transition, toggled by a class:
```css
.detail { max-height:0; overflow:hidden; opacity:0; transition:max-height .5s, opacity .4s; }
.card.open .detail { max-height:520px; opacity:1; }
```
JS: on card click, `card.classList.toggle('open')`, but `if (e.target.closest('a')) return;`
so inner repo links still work. Accordions use the same trick (`.acc.open .acc__body`).

## Canvas background (starfield + rotating galaxies)
Two stacked `<canvas>` (`#galaxies` behind, `#starfield` front), both
`position:fixed; inset:0; z-index:0; pointer-events:none`.

Galaxy per frame, per galaxy:
- Nucleus: radial gradient white→hueA→hueB→transparent, plus a small bright core glow.
- Spiral arms: for each star, `arm = floor(a/(2π/arms))*(2π/arms)`;
  `ang = arm + rad*3.4 + rot`; `x=cx+cos(ang)*rad`; `y=cy+sin(ang)*rad*0.42`
  (×0.42 squashes into a disk). `rot += spin` each frame → rotation.

  **More realistic galaxies (dust + halo + bright core):** add a soft halo
  `radial(cx,cy, R*0.1 → R*1.05)` light blue `rgba(180,200,255,0.12)` → transparent; mark
  ~35% of arm stars as `dust` and draw them `rgba(255,190,150,…)` (reddish, mimicking dust
  lanes). BULGE: a brighter core gradient `radial(0 → R*0.28)` white 0.98 → hueA → hueB →
  transparent, drawn AFTER the arms so the center pops. Reads far more like a real spiral
  than a flat disk.
- Mouse REPULSION (not parallax-toward — user corrected this): `mousemove` → normalized
  `tmx/tmy` (−1..1); ease `mx += (tmx-mx)*0.06`. Per galaxy push the center AWAY from the
  cursor: `dx=bx-mpx, dy=by-mpy, dist=hypot`; if `dist<radius` { `f=1-dist/radius; push=f*f*maxPush;
  tx=dx/dist*push; ty=dy/dist*push` }; ease `g.ox += (tx-g.ox)*0.08`; draw at `bx+g.ox`.
  This makes the sky shrink away from the pointer. (Attraction/parallax-toward is the WRONG
  default here — the user explicitly wanted repulsion.)

  **ALT background interaction the user actually settled on — "bouncing orbs":** the user
  disliked the mouse-repulsion galaxies and asked for self-moving particles that
  **bounce off the screen edges** (slowly). Replace the mouse handler entirely with:
  ```js
  let orbs = [];
  function buildOrbs() {
    const count = Math.min(26, Math.floor((innerWidth*innerHeight)/52000));
    orbs = Array.from({length:count}, () => {
      const r = (2+Math.random()*3.5)*gdpr;
      return { x:Math.random()*gw, y:Math.random()*gh,
        vx:(Math.random()*2-1)*0.55*gdpr, vy:(Math.random()*2-1)*0.55*gdpr,
        r, tw:Math.random()*Math.PI*2,
        hue: Math.random()<0.3?275:(Math.random()<0.5?210:175) };
    });
  }
  // per frame:
  for (const o of orbs) {
    o.x += o.vx; o.y += o.vy;
    if (o.x-o.r<0){o.x=o.r; o.vx=Math.abs(o.vx);} else if(o.x+o.r>gw){o.x=gw-o.r; o.vx=-Math.abs(o.vx);}
    if (o.y-o.r<0){o.y=o.r; o.vy=Math.abs(o.vy);} else if(o.y+o.r>gh){o.y=gh-o.r; o.vy=-Math.abs(o.vy);}
    o.tw += 0.05;
    const tw = 0.5+0.5*Math.sin(o.tw);
    const g = ctx.createRadialGradient(o.x,o.y,0,o.x,o.y,o.r*3.2);
    g.addColorStop(0,`hsla(${o.hue},90%,85%,${0.8*tw+0.2})`);
    g.addColorStop(0.4,`hsla(${o.hue},90%,75%,${0.35*tw})`);
    g.addColorStop(1,`hsla(${o.hue},90%,75%,0)`);
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(o.x,o.y,o.r*3.2,0,Math.PI*2); ctx.fill();
  }
  ```
  Keep `vx/vy` small (~0.5 px/frame) so it's "slow" but a bounce is still visible within
  ~15–20s on a full screen. Remove the `tmx/tmy` mousemove + `mouseleave` listeners and the
  `mx/my` easing when using orbs. Still respect `prefers-reduced-motion`.
- `#galaxies { mix-blend-mode:screen; opacity:1 }` so it glows over the dark gradient.
- Respect `prefers-reduced-motion`: draw one static frame, skip the rAF loop.
- On `resize` recompute size with `devicePixelRatio` capped at 2.

Gotcha: `node --check` won't validate canvas logic. Verify in a real browser:
`browser_vision` + a `browser_console` `getImageData(...).data` non-zero check proves
pixels are drawn. Screenshots alone *under-report* subtle `screen`-blend canvases — trust
the pixel check over the screenshot when confirming the effect exists.

### Constellations layer (lines connecting stars)
Above the galaxies, add a `#constel` canvas so the sky reads as a sky, not random dots.
Data-driven: each constellation = array of stars in **relative viewport coords (0–1)**
+ an index-pair `lines` array. Draw once per frame:
```js
ctx.strokeStyle = "rgba(180,205,255,0.55)"; ctx.lineWidth = 1.6*dpr;
ctx.shadowColor = "rgba(150,180,255,0.6)"; ctx.shadowBlur = 6*dpr;
ctx.beginPath();
c.lines.forEach(([a,b]) => { ctx.moveTo(sx[a],sy[a]); ctx.lineTo(sx[b],sy[b]); });
ctx.stroke(); ctx.shadowBlur = 0;
// stars: radial-gradient glow, twinkle via Math.sin(t*0.0012)
```
Good southern/astronomy set: **Cruzeiro do Sul** (lower-right), **Orion/Três Marias**
(center), **Escorpião** (lower-left), **Cassiopeia** (W, upper-left), **Big Dipper/Ursa
Maior** (upper-right). Draw a synchronous frame at init (`drawConstel(performance.now())`
before the rAF loop) so headless screenshots still capture it. Confirm via
`canvas.toDataURL('image/png')` length (~150 KB PNG ⇒ full of content) when the visual
layer is hard to read.

**Slow self-movement (user requirement):** constellations must drift on their own, not sit
static. Give each star `ph` (phase) + `amp` (px). Per frame `t = now*0.00018` and offset:
`x = s.x*cw + sin(t+s.ph)*s.amp*dpr; y = s.y*ch + cos(t*0.8+s.ph)*s.amp*dpr*0.6`. Galaxies
already self-rotate via `rot += spin`; constellations now "breathe" slowly too. Respect
`prefers-reduced-motion`: one static frame, skip rAF.

**MOUSE INTERACTION = REPULSION, not attraction (user corrected this):** the background must
PUSH AWAY from the cursor. Per galaxy, push away from the mouse proportional to closeness:
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
  const cx = bx + g.ox, cy = by + g.oy;  // draw nucleus + arms at (cx,cy)
}
```
Verify objectively: temporarily expose `window.__test={galaxies}`, dispatch
`MouseEvent('mousemove',{clientX:g.cx*innerWidth, clientY:g.cy*innerHeight})`, wait ~600ms,
assert `galaxies[i].ox` moves away (~ -35px). REMOVE the exposure before committing.

### z-index + backdrop-filter layering (sky visible AND text opaque)
User explicitly required: animated sky visible, background lightly blurred, but **text
must NOT be transparent**. Stack (back→front), all `position:fixed; inset:0; pointer-events:none`:
- `#starfield` `z-index:0`
- `#galaxies` `z-index:1.4` (`mix-blend-mode:screen`)
- `#constel` `z-index:1.7` (above galaxies so lines aren't eaten by the blend)
- `.bg-veil` `z-index:1` with `backdrop-filter:blur(2px)` + a *light* gradient
  (`rgba(8,11,26,0.30–0.45)` — NOT 0.72, which hides the constellations)
- content wrapper (`nav/main/footer`) `position:relative; z-index:2` on top.
Make cards/sections opaque: `--panel: rgba(17,21,46,0.82)` (not 0.45) so text never
transparesces. Rule: keep the veil's dark gradient light enough that constellation pixels
(drawn brighter, above the veil) still show through.

### SVG icon map (fixes emojis that render as empty boxes)
Emojis (🪐🛰️🌌) render as tofu on systems lacking the glyph. Prefer inline `iconSVG(key)`:
```js
const ICONS = { star:'<path d="M12 3l2.5 5.5L20 9l-4 4 1 6-5-3-5 3 1-6-4-4 5.5-.5z"/>',
  github:'<path d="M12 2a10 …Z"/>', instagram:'<rect …/><circle …/>', /* ~24 keys */ };
const iconSVG = (k,cls) => `<svg class="ico ${cls||''}" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="1.7" stroke-linecap="round"
  stroke-linejoin="round">${ICONS[k]||ICONS.star}</svg>`;
```
Key the data file by icon name (`icon:"star"`) not an emoji; render with `iconSVG(p.icon)`
in cards, bolsas, and contacts. Style `.ico{width:1.5em}`. More robust + themeable than emoji.

### Multi-language UI (flag selector, persisted) — PT/EN/ES/FR pattern
User asked for 4 selectable languages with flag+label buttons in the top bar. Structure:
- `projects.js`: add `I18N = { pt:{...}, en:{...}, es:{...}, fr:{...} }` with every interface
  string (nav[], hero{eyebrow,sub,badges[],hobbyLabel}, sections.*{title,lead},
  about[3 paragraphs], vis{}, cat{}, contactLabels{}, bolsas{orientLabel,periodLabel},
  footer). Keep PT as default. Mark static text in `index.html` with `data-i18n="path"`
  and nav links with `data-i18n-nav="0..6"`.
- Per-object translations: add `i18n:{en:{...},es:{...},fr:{...}}` to FEATURED/RESEARCH/BOLSAS
  items — FLAT shape (`i18n.en.title`, NOT `i18n.title.en`). `pick(obj,key)` reads
  `obj.i18n[lang] && obj.i18n[lang][key]`. Mismatched nesting = silent bug (bolsas stayed PT
  until the shape was unified to flat).
- Top bar: `.lang-switch` with 4 `<button class="lang-btn" data-lang="pt|en|es|fr">`, each
  an inline `<svg class="flag">` (Brasil/EUA/Espanha/França) + `<span>PT-BR|EN|ES|FR</span>`.
- `applyLang(l)`: set `localStorage.lang`, update `document.documentElement.lang`, run
  `applyI18n()` (text via `data-i18n` + `[data-html]` for the about block), then re-render
  cards/bolsas/contatos/research so translated briefs refresh. Load: `localStorage.getItem('lang')||'pt'`.
- CSS: in the mobile menu, show the 4 languages INSIDE the open dropdown
  (`.nav__links.open ~ .lang-switch`) so the selector is reachable on small screens.

### Footer name duplication (silent i18n bug)
Footer text like `© 2026 Pedro Henrique Rocha de Andrade — Pedro Rocha — feito com…`
means the `I18N.pt.footer` string itself contains the name (e.g. `"Pedro Rocha — feito
com…"`) while the HTML `<a>` already shows the full name. Fix: keep `I18N.*.footer` =
just the trailing phrase (`"feito com café, código e um céu estrelado."`) and let the HTML
`<a href="https://phrandrade.com/pt-br/">Pedro Henrique Rocha de Andrade</a>` carry the name.
One source of truth for the name — never embed it in both.

### Contact boxes: group label+value or they mis-align (user-reported bug)
`.contact__item` is `display:flex; align-items:center; gap`. Icon + label + value must NOT be
three flat siblings — wrap label+value in one `.contact__text` (flex column) so they stack
cleanly beside the icon. Bug symptom: `item > span:not(.contact__ico){flex-direction:column}`
left the value floating beside the label. Fix = nest them in `.contact__text`.

### Body width + hide scrollbar (layout polish, user-requested)
- **Widen content:** the layout is driven by a single token `--maxw` (e.g. `1180px`)
  applied as `max-width: var(--maxw); margin: 0 auto` on every section + the lateral
  `padding: clamp(16px,5vw,56px)`. To push the left/right columns toward the screen edges
  (with a safe margin), just bump `--maxw` (e.g. → `1480px`). Do NOT add per-section
  overrides — the token is the single source of truth. Telas < maxw keep the clamped padding.
- **Hide the scrollbar but keep scrolling:** user wanted the vertical scrollbar invisible.
  Pure CSS, scroll still works:
  ```css
  body { scrollbar-width: none; -ms-overflow-style: none; } /* Firefox / legacy Edge */
  body::-webkit-scrollbar { display: none; }                 /* Chrome / Safari / Edge */
  ```
  Don't use `overflow:hidden` on `<html>`/`<body>` — that disables scrolling entirely.
  Verify in-browser: screenshot shows no scrollbar but the page is long and "back to top"
  works.

### Sourcing truthful content from the user's home (no fabrication)
Before writing any brief, mine real sources (read-only):
- `gh repo list <user> --limit 60` + `gh api repos/<u>/<r>/readme` to enumerate ALL repos
  (public + private) without cloning; read each README for real stack/description.
- Local vaults: `hardcore-life/99 - Meta/INDICE_VAULT.md` (PARA, grade),
  `page/content/pt-br/index.md` (Sobre mim, Instagram, hobby), `cv/*.tex` (bolsas,
  ORCID, interesses). Pull full name, Lattes ID, ORCID, Instagram, hobby straight from
  there. Never invent; if unsure, say so.
- For a "short resumé" of ALL GitHub work, list every repo (private ones get a short
  brief too — no secrets, just what it does). Make it public for free Pages ONLY after
  stripping any scaffold with real secrets.

### Post-edit "verification: stale" banner is often WRONG — re-run fresh
The harness attaches a stale banner showing an OLD data snapshot (e.g. `PROJECTS: 4`)
from a previous file version after every edit. Treat it as untrusted. Always re-run a
fresh `node --check` + `node -e '...'` data-shape assertion + `curl` of the published URL
+ `grep` of served HTML for new ids, and label it explicitly *ad-hoc verification* (not
"suite green"). Refreshing it is on you, not the harness.

## GitHub Pages free-plan wall (the part that blocks everyone)
1. **Repo MUST be public.** Private repo →
   `422 "Your current plan does not support GitHub Pages for this repository."`
   Fix: `gh api -X PATCH repos/<owner>/<repo> -f private=false`.
2. **Archived repos can't push / activate Pages.** Unarchive first:
   `gh api -X PATCH repos/<owner>/<repo> -f archived=false`.
3. Activate: `gh api -X POST repos/<owner>/<repo>/pages -f build_type=legacy
   -f "source[branch]=master" -f "source[path]="/`.
4. Renamed repo (`portfolio`→`webpage`) still accepts `git push` to the old URL
   (redirects); canonical URL changes — don't panic.
5. Build ~1 min; poll `curl -sI https://<user>.github.io/<repo>/` for HTTP 200.
6. Local check first: `python3 -m http.server 8123` + `browser_navigate`.

## Verification (ad-hoc, not a suite)
- `node --check` every JS file.
- `node -e 'global.window={}; require("assets/js/projects.js"); ...'` assert data shape/counts.
- `curl` each asset for HTTP 200 on the published URL.
- `grep` served HTML for new container ids / links.
- Browser: `getImageData` pixel check for canvases; click a card/accordion, assert
  `querySelector('.open')` exists.

### Headless-browser cache trap (wastes a verification round)
The browser tool **preserves the loaded JS/canvas module across `browser_navigate` calls in
the same session** — even navigating to the same URL re-runs the OLD script from memory, so
after you edit `main.js`/`projects.js` and re-navigate, `getImageData`/`window.PORTFOLIO_DATA`
still reflect the pre-edit code (you'll see stale strings like an old `I18N.footer`). Two
reliable ways to force a fresh fetch:
  1. `browser_navigate('about:blank')` then `browser_navigate(siteURL)` — wipes the page so the
     next load re-fetches assets; OR
  2. serve on a **new port** (`python3 -m http.server 8151`) and navigate there — the asset
     URL changes, bypassing the cached one. Confirm with `curl` of the served file that the
     new content is actually there; only then trust the browser check.
Always REMOVE any temporary `window.__test = {...}` exposure before committing (it's only for
the measurement round).

See `references/animated-portfolio-pattern.md` for the full condensed technique
(canvas math, mouse parallax, Pages gotchas, verification snippets).
See `references/animated-portfolio-extras.md` for constellation coords, the z-index/blur
layering CSS, and the SVG icon-map snippet.
See `references/bouncing-orbs-verify.md` for the realistic-galaxy + bouncing-orbs code and
the objective headless verification recipe (including the browser-cache trap).
