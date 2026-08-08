#!/usr/bin/env bash
# Prova, contra stacks REAIS, que a protecao de forca bruta esta ativa.
# O Jest nao alcanca isto: os limiters sao desligados em NODE_ENV=test.
#
# Uso:  bash verify-bruteforce.sh [repo] [tentativas] [minutos]
#       bash verify-bruteforce.sh /home/pedro/Repositorios/templates/projeto-profissional 3 30
set -uo pipefail

R="${1:-/home/pedro/Repositorios/templates/projeto-profissional}"
N="${2:-3}"          # tentativas permitidas antes do bloqueio
MIN="${3:-30}"       # janela de bloqueio em minutos
PROD=4447; TESTE=4446
SENHA_ADMIN='AdminProd123ok'

cd "$R" || exit 1
f=0; ok(){ echo "  OK   $1"; }; nok(){ echo "  FALHA $1"; f=$((f+1)); }
export JWT_SECRET="$(openssl rand -base64 48)" ADMIN_PASSWORD="$SENHA_ADMIN"

limpar(){ docker compose -f docker-compose.test.yml -p pp-test down -v >/dev/null 2>&1
          docker compose -f docker-compose.yml      -p pp      down -v >/dev/null 2>&1; }
trap limpar EXIT   # derruba as stacks mesmo se o script morrer no meio
limpar

echo "[0] subindo producao ($PROD) e teste ($TESTE)"
docker compose -f docker-compose.test.yml -p pp-test up -d >/dev/null 2>&1
docker compose -f docker-compose.yml      -p pp      up -d >/dev/null 2>&1
for _ in $(seq 1 40); do
  curl -sf "localhost:$TESTE/api/health/ready" >/dev/null 2>&1 &&
  curl -sf "localhost:$PROD/api/health/ready"  >/dev/null 2>&1 && break
  sleep 2
done

login(){ curl -s -o /dev/null -w '%{http_code}' -X POST "localhost:$1/api/auth/login" \
         -H 'Content-Type: application/json' \
         -d "{\"email\":\"admin@example.com\",\"password\":\"$2\"}"; }

echo "[1] as duas portas respondem simultaneamente"
a=$(curl -s -o /dev/null -w '%{http_code}' "localhost:$TESTE/")
b=$(curl -s -o /dev/null -w '%{http_code}' "localhost:$PROD/")
[ "$a" = 200 ] && [ "$b" = 200 ] && ok "$TESTE=$a $PROD=$b" || nok "$TESTE=$a $PROD=$b"

echo "[2] bloqueia na tentativa $((N+1)) — sequencia EXATA"
esperado=""; for _ in $(seq 1 "$N"); do esperado="${esperado}401 "; done; esperado="${esperado}429 "
obtido=""; for _ in $(seq 1 $((N+1))); do obtido="${obtido}$(login "$PROD" errada123456) "; done
[ "$obtido" = "$esperado" ] && ok "sequencia: $obtido" || nok "esperado '$esperado', veio '$obtido'"

echo "[3] senha CORRETA continua barrada (bloqueio real, nao contagem)"
[ "$(login "$PROD" "$SENHA_ADMIN")" = 429 ] \
  && ok "credencial valida rejeitada durante o bloqueio" || nok "bloqueio nao resiste"

echo "[4] header anuncia a politica"
pol=$(curl -sD- -o /dev/null -X POST "localhost:$PROD/api/auth/login" \
      -H 'Content-Type: application/json' -d '{"email":"x@y.z","password":"a"}' \
      | grep -i 'ratelimit-policy' | tr -d '\r')
echo "$pol" | grep -q "$N;w=$((MIN*60))" && ok "$pol" || nok "esperado $N;w=$((MIN*60)) — veio: $pol"

echo "[5] lockout de CONTA gravado no banco (~$MIN min)"
m=$(docker compose -p pp exec -T mongo mongosh app_db --quiet --eval \
   'const u=db.users.findOne({email:"admin@example.com"});
    print(u&&u.lockedUntil?Math.round((new Date(u.lockedUntil)-Date.now())/60000):"nulo")' 2>/dev/null | tr -d '\r')
[ "$m" -ge $((MIN-5)) ] 2>/dev/null && [ "$m" -le "$MIN" ] 2>/dev/null \
  && ok "conta travada por ${m} min" || nok "lockedUntil: $m"

echo "[6] stack de TESTE sem limiter (carga honesta)"
s=""; for _ in 1 2 3 4 5; do s="${s}$(login "$TESTE" errada123456) "; done
echo "$s" | grep -q 429 && nok "limiter ativo em teste: $s" || ok "5 tentativas sem 429: $s"

echo; echo "=== falhas: $f ==="; exit "$f"
