# 404.tsx client-side JS — pattern + debugging recipe

## The RIGHT shape (assign to `NotFound.afterDOMLoaded`)

```ts
NotFound.afterDOMLoaded = `
function fill404() {
  var root = document.querySelector(".notfound");
  if (!root) return;                 // critical: no-op on every non-404 page
  var I18N = { /* pt/en/es/fr objects with title/msg/home/request/redirect/issueTitle/issueBody */ };
  function detectLang() {
    var segs = window.location.pathname.split("/").filter(Boolean);
    var first = segs[0] || "";
    if (["pt-br", "en", "es", "fr"].indexOf(first) !== -1) return first === "pt-br" ? "pt" : first;
    return "pt";
  }
  var lang = detectLang();
  var T = I18N[lang] || I18N.pt;
  var slug = window.location.pathname;
  if (slug.startsWith("/")) slug = slug.slice(1);
  if (slug.endsWith("/index")) slug = slug.slice(0, -6);
  if (slug.endsWith(".html")) slug = slug.slice(0, -5);
}
fill404();
document.addEventListener("nav", fill404);
`;
```

## Pitfall 1 — esbuild minifier corrupts `\/` in regex (SITE-BREAKING)
Regex with `\/` inside `afterDOMLoaded` gets the slash optimized away by esbuild minify:
`/^\//` -> `/^//` (INVALID). The whole `script-N-<hash>.js` fails to parse; `postscript.js`'s
`Promise.all([import(...)])` rejects, so every later script (toolbar search/darkmode/explorer/
readermode + SPA router) never registers handlers -> ALL buttons dead (mobile + desktop).
RULE: never use `\/` in a regex inside `afterDOMLoaded`. Use string methods:
`startsWith("/") ? slice(1) : str`, `endsWith("/index") ? slice(0,-6) : str`,
`split("/").filter(Boolean)` for the language segment.
Reproduce: `npx esbuild /tmp/s11_in.ts --minify` then `node --check` -> must pass, no `/^//`.

## Pitfall 2 — `<script dangerouslySetInnerHTML>` does not run in SPA (innerHTML scripts don't execute).

## Pitfall 3 — bare IIFE runs once, not on SPA nav. Quartz only dispatches `nav` CustomEvent;
register `document.addEventListener("nav", fill404)`.

## Where the logic lives after build
In `static/scripts/script-N-<hash>.js` (imported by `postscript.js`), NOT inline in the HTML.

## Deterministic verification (no browser)
`node scripts/verify-quartz-scripts.mjs https://pedroiff0.github.io/page`
Downloads live postscript, `node --check`s every `static/scripts/script-N-*.js`, exits
non-zero if any fail. Run after ANY edit to client JS in a component.

## Manual curl recipe
```
base=https://pedroiff0.github.io/page
post=$(curl -sL $base/pt-br/ | grep -o 'src="[^"]*postscript[^"]*\.js"' | head -1 | sed 's/src="//;s/"//')
curl -sL $base/$post > /tmp/post.js
for s in $(grep -o 'static/scripts/script-[0-9]*-[a-f0-9]*\.js' /tmp/post.js | sort -u); do
  curl -sL $base/$s > /tmp/c.js; node --check /tmp/c.js && echo "$s OK" || echo "$s ERRO"
done
```
