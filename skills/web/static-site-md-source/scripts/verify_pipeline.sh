#!/bin/sh
# Ad-hoc verification of a static-site MD->JS pipeline.
# Args: ROOT = repo root (default /home/pedro/portfolio)
# Checks: baseline exists, generated JS parses in Node, deep-equal vs .orig,
# pre-commit hook executable, an edit propagates + reverts cleanly.
set -e
ROOT="${1:-/home/pedro/portfolio}"
ORIG=$ROOT/assets/js/projects.js.orig
WORK=$ROOT/assets/js/projects.js
MD=$ROOT/src/portfolio.md
PASS=0; FAIL=0
ok(){ echo "PASS: $1"; PASS=$((PASS+1)); }
bad(){ echo "FAIL: $1"; FAIL=$((FAIL+1)); }

[ -f "$ORIG" ] && ok "baseline .orig existe" || bad "falta baseline .orig"
python3 "$ROOT/tools/build.py" >/dev/null
node -e "new Function('window', require('fs').readFileSync('$WORK','utf8')+'return window.PORTFOLIO_DATA');" \
  && ok "build.py gera JS válido" || bad "JS inválido"
node "$ROOT/tools/verify.js" >/dev/null 2>&1 && ok "verify: objeto == original" || bad "verify falhou"
[ -x "$ROOT/.git/hooks/pre-commit" ] && ok "pre-commit executável" || bad "hook não executável"

cp "$MD" "$MD.bak"
python3 - "$MD" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
s=s.replace('"PROBEXYZ"','')  # limpa
s=s.replace('"🏆 IAAC 2024 & 2025"','"🏆 IAAC 2024 & 2025 [PROBEXYZ]"',1)
open(p,'w').write(s)
PY
python3 "$ROOT/tools/build.py" >/dev/null
grep -q PROBEXYZ "$WORK" && ok "edição propaga p/ JS" || bad "edição NÃO propagou"
mv "$MD.bak" "$MD"
python3 "$ROOT/tools/build.py" >/dev/null
! grep -q PROBEXYZ "$WORK" && ok "revert restaura" || bad "revert falhou"
node "$ROOT/tools/verify.js" >/dev/null 2>&1 && ok "após revert verify ok" || bad "após revert verify falha"

echo "----"; echo "RESULTADO: $PASS passou, $FAIL falhou"; [ "$FAIL" -eq 0 ]
