# Bouncing orbs + realistic galaxies — verify pattern

Condensed from a portfolio session where the user replaced mouse-repulsion galaxies
with slow particles that bounce off screen edges, and wanted more realistic spirals.

## Realistic spiral galaxy (per galaxy object)
```js
{ cx, cy, R, arms: 2 + (i%2), rot, spin, hueA, hueB,
  stars: Array.from({length:320}, () => ({
    a, rad: Math.pow(Math.random(),0.55), sz, tw,
    dust: Math.random() < 0.35            // reddish dust-lane stars
  })) }
```
Draw order per frame: halo -> arm stars (dust = rgba(255,190,150,...), rest =
rgba(225,235,255,...)) -> bright bulge core radial(0 -> R*0.28) white 0.98->hueA->hueB->transparent.
Halo: radial(cx,cy, R*0.1 -> R*1.05) rgba(180,200,255,0.12)->transparent.
Arm math: arm = floor(a/(2PI/arms))*(2PI/arms); ang = arm + rad*4.2 + rot;
x=cx+cos(ang)*rad; y=cy+sin(ang)*rad*0.45. rot += spin each frame.

## Bouncing orbs (the settled interaction)
```js
function buildOrbs() {
  const count = Math.min(26, Math.floor((innerWidth*innerHeight)/52000));
  orbs = Array.from({length:count}, () => ({
    x: Math.random()*gw, y: Math.random()*gh,
    vx: (Math.random()*2-1)*0.55*gdpr, vy: (Math.random()*2-1)*0.55*gdpr,
    r: (2+Math.random()*3.5)*gdpr, tw: Math.random()*Math.PI*2,
    hue: Math.random()<0.3?275:(Math.random()<0.5?210:175)
  }));
}
// per frame
for (const o of orbs) {
  o.x += o.vx; o.y += o.vy;
  if (o.x-o.r<0){o.x=o.r; o.vx=Math.abs(o.vx);}
  else if (o.x+o.r>gw){o.x=gw-o.r; o.vx=-Math.abs(o.vx);}
  if (o.y-o.r<0){o.y=o.r; o.vy=Math.abs(o.vy);}
  else if (o.y+o.r>gh){o.y=gh-o.r; o.vy=-Math.abs(o.vy);}
  o.tw += 0.05; /* draw glow with hsla + twinkle */
}
```
Speed ~0.5 px/frame => slow but a bounce shows in ~15-20s on a full screen.
Remove tmx/tmy mousemove + mouseleave listeners and the mx/my ease when using orbs.

## Objective browser verification (headless)
Expose temporarily (REMOVE before commit): window.__test = { orbs, galaxies };
Then in browser_console:
```js
const orbs = window.__test.orbs;
const o = orbs[0]; const s0 = {x:o.x, y:o.y, vx:o.vx, vy:o.vy};
await new Promise(r=>setTimeout(r,800));
const moved = Math.hypot(o.x-s0.x, o.y-s0.y);   // >0 => moving
// detect bounce: sample vx/vy flips over ~80 frames @40ms; any sign change = edge hit
```
Proving motion cheaply without exposing internals:
fingerprint = sum of getImageData(...).data at t and t+600ms; relative diff >0 => animating.
Browser cache trap: the browser tool keeps the old JS across navigate in one session -
navigate to about:blank then back, or use a NEW port, to actually re-fetch the edited file.

## i18n per-object nesting MUST be flat (silent translation bug)
When adding translations to FEATURED / RESEARCH / BOLSAS items, use the SAME flat shape
as the cards use, or the translation silently won't render:

```js
// CORRECT (flat) — pick(obj,"title") reads obj.i18n[lang].title
b: { title:"…", i18n:{ en:{title:"…", desc:"…", kind:"…"}, es:{…}, fr:{…} } }

// WRONG (nested) — pick reads obj.i18n[lang].title, but here it's obj.i18n.title[lang]
b: { title:"…", i18n:{ title:{ en:"…", es:"…", fr:"…" }, desc:{…} } }   // stays PT!
```
Symptom seen this session: after switching to EN/FR, cards translated but bolsas stayed
in PT — because bolsas used the nested shape. Unify ALL translated objects to flat
`i18n.en.X` and the bug disappears. Verify with `pick` reading `obj.i18n?.[lang]?.[key]`.
