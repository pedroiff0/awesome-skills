#!/usr/bin/env bash
# Ad-hoc verification for a static GitHub Pages portfolio (NOT a committed suite).
# Usage: bash /tmp/verify_portfolio.sh  (edit ROOT / LIVE / BASE below)
set -u
ROOT=/home/pedro/portfolio
LIVE=https://pedroiff0.github.io/webpage
echo "== 1. Essential files =="
for f in index.html assets/css/style.css assets/js/main.js assets/js/projects.js favicon.svg; do
  [ -f "$ROOT/$f" ] && echo "OK  $f" || echo "MISSING $f"
done
echo; echo "== 2. JS syntax (node --check) =="
for f in assets/js/main.js assets/js/projects.js; do
  node --check "$ROOT/$f" 2>/tmp/e && echo "OK  $f" || { echo "FAIL $f"; cat /tmp/e; }
done
echo; echo "== 3. Data shape =="
node -e 'global.window={}; require("/home/pedro/portfolio/assets/js/projects.js"); const d=window.PORTFOLIO_DATA; console.log("REPOS:", d.REPOS.length, "| FEATURED:", d.FEATURED.length, "| RESEARCH:", d.RESEARCH.length); const c={}; d.REPOS.forEach(r=>c[r.cat]=(c[r.cat]||0)+1); console.log("cats:", JSON.stringify(c));'
echo; echo "== 4. index.html containers =="
grep -oE 'id="projectGrid"|id="allRepos"|id="researchList"|id="trabalhos"|href="#trabalhos"' "$ROOT/index.html" | sort -u
echo; echo "== 5. Live site =="
for f in "" assets/css/style.css assets/js/projects.js; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' -L $LIVE/$f)  /$f"
done
curl -s -L $LIVE/ | grep -oE 'Tudo o que eu faço no GitHub|id="allRepos"' | sort -u
echo; echo "== 6. Clones in Repositorios =="
find /home/pedro/Repositorios -type d -name .git 2>/dev/null | wc -l | xargs echo "git dirs:"
