# Animated single-page portfolio / CV pattern (condensed)

Built and verified for a GitHub-Pages personal site (astronomy theme). Reusable
recipe — copy the structure, swap copy/data.

## Layout shape
- One `index.html`, single page, sections reached by `#anchor` nav (Sobre, Projetos,
  Trabalhos, Pesquisa, Bolsas, Currículo, Lattes, Contato).
- "Hidden until click" content via CSS `max-height` transition:
  - Cards: `.card__detail { max-height:0; overflow:hidden; opacity:0 }` → `.card.open .card__detail { max-height:520px; opacity:1 }`. Toggle `.open` on click (ignore clicks on inner `<a>`).
  - Accordions: same trick with `.acc.open .acc__body`.
- Scroll reveal: `IntersectionObserver` adds `.visible` to `.reveal` elements.

## Canvas background (starfield + rotating galaxies)
Two stacked `<canvas>` (`#galaxies` behind, `#starfield` front), both
`position:fixed; inset:0; z-index:0; pointer-events:none`.

Galaxy draw (per frame, per galaxy):
- radial gradient nucleus: white core → `hueA` → `hueB` → transparent; plus a small
  bright core glow.
- spiral arms: for each star, `arm = floor(a/(2π/arms))*(2π/arms)`,
  `ang = arm + rad*3.4 + rot`; `x=cx+cos(ang)*rad`, `y=cy+sin(ang)*rad*0.42`
  (the *0.42 squashes it into a disk). `rot += spin` each frame → rotation.
- Mouse parallax: track `tmx/tmy` from `mousemove` (normalized −1..1), ease `mx += (tmx-mx)*0.06`,
  offset galaxy centers by `mx*parallax`. `mouseleave` → tmx=tmy=0.
- `mix-blend-mode: screen` + `opacity:1` so galaxies glow over the dark gradient.
- Respect `prefers-reduced-motion`: if set, draw one static frame, skip `requestAnimationFrame` loop.
- Resize: recompute canvas size with `devicePixelRatio` (cap at 2) on `resize`.

Gotcha: `node --check` won't catch canvas logic; verify in a real browser via
`browser_vision` + `browser_console` `getImageData(...).data` non-zero check to prove
pixels are drawn. Screenshots alone under-report subtle `screen`-blend canvases.

## Data-driven rendering
Keep content in one JS object (`window.PORTFOLIO_DATA = { REPOS, FEATURED, RESEARCH,
BOLSAS, CONTACTS, FULL_NAME, ORCID }`) and render with `innerHTML` templates +
`wireCards()`. Lets you list ALL repos (public + private) with short briefs without
touching HTML. Categorize with a `cat` field; group sections by category.

## GitHub Pages free-plan gotchas (the wall)
1. **Repo MUST be public** for Pages on the free plan — private repo →
   `422 "Your current plan does not support GitHub Pages for this repository."`
   Fix: `gh api -X PATCH repos/<owner>/<repo> -f private=false`.
2. **Archived repos can't be pushed/pages-activated.** Unarchive first:
   `gh api -X PATCH repos/<owner>/<repo> -f archived=false`.
3. Activate Pages: `gh api -X POST repos/<owner>/<repo>/pages -f build_type=legacy
   -f "source[branch]=master" -f "source[path]="/`.
4. If the repo was renamed (e.g. `portfolio`→`webpage`), `git push` to the old remote
   URL auto-redirects and still works; the canonical URL changes.
5. Build takes ~1 min; poll with `curl -sI https://<user>.github.io/<repo>/`.
6. Verify locally with `python3 -m http.server` + `browser_navigate`, then publish.

## Verification checklist (ad-hoc, not a suite)
- `node --check` on every JS file.
- `node -e 'global.window={}; require(...); ...'` to assert data shape/counts.
- `curl` each asset for HTTP 200 on the published URL.
- `grep` the served HTML for the new container ids / link.
- Browser: `getImageData` pixel check for canvases; click a card/accordion and confirm
  class toggles via `querySelector('.open')`.

## Useful gh commands (copy-paste)
```
gh repo view <owner>/<repo> --json name,isArchived,isPrivate,url
gh api -X PATCH repos/<owner>/<repo> -f archived=false
gh api -X PATCH repos/<owner>/<repo> -f private=false
gh api -X POST repos/<owner>/<repo>/pages -f build_type=legacy -f "source[branch]=master" -f "source[path]=/"
# update a README:
SHA=$(gh api repos/<owner>/<repo>/contents/README.md --jq '.sha')
gh api -X PUT repos/<owner>/<repo>/contents/README.md -f message="..." -f content="$(base64 -w0 file.md)" -f sha="$SHA"
```
