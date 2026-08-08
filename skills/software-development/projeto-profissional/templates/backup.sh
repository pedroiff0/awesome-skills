#!/usr/bin/env bash
# Backup do banco de PRODUCAO em um unico .zip.
#
# Template para projetos derivados do projeto-profissional. Copie para
# <repo>/scripts/backup.sh, ajuste os defaults de PROJETO/BANCO e chmod +x.
#
# Faz mongodump DENTRO do container do Mongo (nao exige mongo-tools no host),
# copia o dump para o host e compacta. Nome com timestamp UTC para nunca
# sobrescrever um backup anterior.
#
#   ./scripts/backup.sh                  # zip em ./backups/
#   ./scripts/backup.sh /mnt/hd/backups  # zip em outro destino
#
# Restauracao (tambem descrita no MANIFEST.txt dentro do zip):
#   unzip -o financas-backup-AAAAMMDD-HHMMSS.zip -d /tmp/restore
#   docker cp /tmp/restore/dump $(docker compose -p fa ps -q mongo):/tmp/dump
#   docker compose -p fa exec -T mongo mongorestore --drop /tmp/dump

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

PROJETO="${COMPOSE_PROJECT:-fa}"
SERVICO_MONGO="${MONGO_SERVICE:-mongo}"
BANCO="${MONGO_DB:-financas_db}"
DESTINO="${1:-$REPO_DIR/backups}"
STAMP="$(date -u +%Y%m%d-%H%M%S)"
NOME="financas-backup-${STAMP}"

command -v docker >/dev/null || { echo "docker nao encontrado" >&2; exit 1; }
command -v zip    >/dev/null || { echo "zip nao encontrado (apt install zip)" >&2; exit 1; }

# Falhar cedo e com mensagem clara: sem isso o mongodump erra de um jeito
# criptico quando o stack esta parado.
if ! docker compose -p "$PROJETO" ps --status running --services 2>/dev/null | grep -qx "$SERVICO_MONGO"; then
  echo "Servico '$SERVICO_MONGO' do projeto '$PROJETO' nao esta rodando." >&2
  exit 1
fi

mkdir -p "$DESTINO"
TMP="$(mktemp -d)"
# Limpa o temporario mesmo se o script morrer no meio.
trap 'rm -rf "$TMP"' EXIT

echo "==> mongodump do banco '$BANCO'"
docker compose -p "$PROJETO" exec -T "$SERVICO_MONGO" \
  sh -c "rm -rf /tmp/dump && mongodump --quiet --db='$BANCO' --out=/tmp/dump"

CID="$(docker compose -p "$PROJETO" ps -q "$SERVICO_MONGO")"
docker cp "$CID:/tmp/dump" "$TMP/dump"
docker compose -p "$PROJETO" exec -T "$SERVICO_MONGO" rm -rf /tmp/dump

# Manifesto: sem isso um zip antigo vira adivinhacao na hora de restaurar.
cat > "$TMP/MANIFEST.txt" <<EOF
backup   : $NOME
gerado   : $(date -u +"%Y-%m-%dT%H:%M:%SZ") (UTC)
host     : $(hostname)
projeto  : $PROJETO
banco    : $BANCO
colecoes : $(find "$TMP/dump" -name '*.bson' | wc -l)

Restaurar:
  unzip -o ${NOME}.zip -d /tmp/restore
  docker cp /tmp/restore/dump \$(docker compose -p $PROJETO ps -q $SERVICO_MONGO):/tmp/dump
  docker compose -p $PROJETO exec -T $SERVICO_MONGO mongorestore --drop /tmp/dump
EOF

echo "==> compactando"
( cd "$TMP" && zip -qr "$NOME.zip" dump MANIFEST.txt )
mv "$TMP/$NOME.zip" "$DESTINO/"
# O dump tem dado pessoal: 600 para nao ficar legivel por outros usuarios.
chmod 600 "$DESTINO/$NOME.zip"

TAMANHO="$(du -h "$DESTINO/$NOME.zip" | cut -f1)"
echo "==> pronto: $DESTINO/$NOME.zip ($TAMANHO)"

# Retencao: mantem os N mais recentes (0 = manter todos).
RETENCAO="${BACKUP_KEEP:-14}"
if [ "$RETENCAO" -gt 0 ]; then
  # shellcheck disable=SC2012
  ls -1t "$DESTINO"/financas-backup-*.zip 2>/dev/null | tail -n "+$((RETENCAO + 1))" | while read -r velho; do
    echo "==> removendo backup antigo: $(basename "$velho")"
    rm -f "$velho"
  done
fi
