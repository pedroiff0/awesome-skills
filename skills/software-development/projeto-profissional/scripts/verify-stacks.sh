#!/usr/bin/env bash
# Verifica os invariantes estruturais do template projeto-profissional
# (ou de um projeto derivado dele) que o Jest nao alcanca: isolamento das
# duas stacks Docker, cenario k6, views CSP-safe e workflows.
#
# Uso: bash verify-stacks.sh [caminho-do-projeto]   (default: cwd)
#
# Complementa `npm test` — nao substitui. Sai != 0 se algo quebrar.

set -uo pipefail
R="${1:-$PWD}"
# O compose interpola vars do ambiente; sem isso `config` falha calado
# e qualquer grep contra saida vazia "passa" por acidente.
export JWT_SECRET="${JWT_SECRET:-placeholder-para-interpolacao-do-compose}"

f=0
ok(){ echo "  OK   $1"; }
nok(){ echo "  FALHA $1"; f=$((f+1)); }
uri(){ (cd "$R" && docker compose -f "$1" config 2>/dev/null | grep -oE 'mongodb://[^ ]+' | head -1); }

echo "[1] URI de producao"
p=$(uri docker-compose.yml)
case "$p" in
  *mongodb://mongo:27017/*) [[ "$p" != *test* ]] && ok "$p" || nok "producao aponta p/ teste: $p" ;;
  *) nok "inesperado: ${p:-<vazio>}" ;;
esac

echo "[2] URI de teste"
t=$(uri docker-compose.test.yml)
[[ "$t" == *test* ]] && ok "$t" || nok "inesperado: ${t:-<vazio>}"

# Comparacao por igualdade: 'app_db' e substring de 'app_test_db'.
echo "[3] hosts/bancos distintos"
[ -n "$p" ] && [ "$p" != "$t" ] && ok "stacks nao compartilham banco" || nok "mesmo banco nas duas stacks"

echo "[4] projetos e portas coexistem"
# Le a porta publicada do compose resolvido em vez de fixar o numero: o par
# de portas ja mudou uma vez (5000/5001 -> 4447/4446) e um literal aqui vira
# falso negativo. O que importa e serem distintas e mapearem p/ 5000 interno.
pub(){ (cd "$R" && docker compose -f "$1" config 2>/dev/null \
        | grep -oE 'published: "[0-9]+"' | grep -oE '[0-9]+' | head -1); }
pp=$(pub docker-compose.yml); pt=$(pub docker-compose.test.yml)
grep -q 'name: pp-test' "$R/docker-compose.test.yml" \
  && [ -n "$pp" ] && [ -n "$pt" ] && [ "$pp" != "$pt" ] \
  && ok "producao:$pp vs pp-test:$pt" || nok "conflito de porta/projeto (prod=$pp teste=$pt)"

echo "[5] RATE_LIMIT_DISABLED so na stack de teste"
grep -q 'RATE_LIMIT_DISABLED' "$R/docker-compose.test.yml" \
  && ! grep -q 'RATE_LIMIT_DISABLED' "$R/docker-compose.yml" \
  && ok "flag ausente da producao" || nok "flag vazou para producao"

echo "[6] guard: boot recusado com o flag em producao"
# Testa por exit code; casar a mensagem por grep e fragil (acentos/locale).
# cwd em /tmp para o dotenv nao sobrepor o ambiente com o .env do projeto.
if (cd /tmp && NODE_ENV=production JWT_SECRET=$(head -c48 /dev/urandom | base64) \
    RATE_LIMIT_DISABLED=true node -e "require('$R/app/src/config/env')" >/dev/null 2>&1)
then nok "bootou em producao com o limitador desligado"; else ok "boot recusado"; fi

echo "[7] guard: seed recusa banco que nao seja de teste"
if (cd /tmp && MONGO_URI=mongodb://localhost:27017/app_db \
    node "$R/app/scripts/seed-carga.js" 1 >/dev/null 2>&1)
then nok "seed aceitaria banco de producao"; else ok "seed recusa producao"; fi

echo "[8] cenario k6 completo"
node -e '
  const s=require("fs").readFileSync(process.argv[1],"utf8");
  ["smoke","carga","estresse","pico","auth"].forEach(p=>{if(!s.includes(p+":"))throw Error(p)});
  ["sessao.token","thresholds"].forEach(p=>{if(!s.includes(p))throw Error(p)});
' "$R/loadtest/carga.js" 2>/dev/null \
  && ok "5 perfis, sessao reutilizada, thresholds" || nok "cenario k6 incompleto"

echo "[9] views sem <script> inline (CSP)"
if grep -rlE '<script(?![^>]*src=)' "$R/app/views" --include='*.ejs' -P 2>/dev/null | grep -q .
then nok "script inline viola a CSP"; else ok "nenhum script inline"; fi

echo "[10] workflows YAML validos"
python3 -c 'import yaml,sys
[yaml.safe_load(open(p)) for p in sys.argv[1:]]' "$R"/.github/workflows/*.yml 2>/dev/null \
  && ok "workflows parseiam" || nok "YAML invalido"

echo
echo "=== falhas: $f ==="
exit $f
