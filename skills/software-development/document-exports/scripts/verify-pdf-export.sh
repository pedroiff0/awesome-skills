#!/usr/bin/env bash
# Verifica a DIAGRAMACAO de um PDF de extrato servido por HTTP real.
#
# Por que existe: a suite Jest gera o PDF dentro do processo de teste e afirma
# "200 + %PDF + frase presente". Quatro bugs reais passaram por isso — 3 paginas
# em vez de 1, cabecalho "VALOR" virando "V", texto sem acento e data quebrando
# em duas linhas. Nenhum deles e visivel sem ABRIR o arquivo.
#
# Uso:
#   verify-pdf-export.sh <base-url> <path-do-pdf> [--cookie-from <path-de-login>]
# Ex.:
#   verify-pdf-export.sh http://127.0.0.1:4452 \
#     "/api/exportacao/extrato.pdf?month=$(date +%Y-%m)" --cookie-from /app
#
# Requer: curl, python3 com pymupdf
#   pip install --break-system-packages pymupdf
set -uo pipefail

BASE="${1:?informe a base url, ex.: http://127.0.0.1:4452}"
PDF_PATH="${2:?informe o path do pdf, ex.: /api/exportacao/extrato.pdf?month=2026-08}"
COOKIE_FROM=""
[ "${3:-}" = "--cookie-from" ] && COOKIE_FROM="${4:-/app}"

JAR=$(mktemp -t hermes-verify-jar.XXXXXX)
PDF=$(mktemp -t hermes-verify-pdf.XXXXXX).pdf
trap 'rm -f "$JAR" "$PDF"' EXIT

# Instancias com autologin so emitem o cookie ao navegar numa pagina.
[ -n "$COOKIE_FROM" ] && curl -s -c "$JAR" -o /dev/null --max-time 10 "$BASE$COOKIE_FROM"

code=$(curl -s -b "$JAR" -o "$PDF" -w '%{http_code}' --max-time 20 "$BASE$PDF_PATH")
[ "$code" = "200" ] || { echo "FALHA: download retornou $code"; exit 1; }

PAGINAS_ESPERADAS="${PAGINAS_ESPERADAS:-1}" python3 - "$PDF" <<'PY'
import os, re, sys, pymupdf

doc = pymupdf.open(sys.argv[1])
texto = "\n".join(p.get_text() for p in doc)
esperado = int(os.environ.get("PAGINAS_ESPERADAS", "1"))
ok = falhou = 0

def checa(desc, cond):
    global ok, falhou
    print(f"  {'ok  ' if cond else 'FALHA'} {desc}")
    ok, falhou = (ok + 1, falhou) if cond else (ok, falhou + 1)

print("1) paginacao (rodape fora da area util inventa paginas)")
checa(f"{esperado} pagina(s) (obtido: {doc.page_count})", doc.page_count == esperado)
# Uma pagina contendo SO texto de rodape e a assinatura do bug.
for i, p in enumerate(doc):
    t = p.get_text().strip()
    checa(f"pagina {i+1} tem conteudo alem do rodape",
          len(t) > 40 or not re.fullmatch(r"(P.gina \d+ de \d+|Gerado em .*)", t))

print("2) acentuacao (strings-fonte ou dados do seed sem diacritico)")
checa("ha algum diacritico no documento", re.search(r"[áàâãéêíóôõúüç]", texto, re.I) is not None)

print("3) cabecalhos completos (coluna estreita trunca para 1 letra)")
for linha in texto.splitlines():
    s = linha.strip()
    if s.isupper() and len(s) == 1:
        checa(f"cabecalho truncado encontrado: {s!r}", False)

print("4) celulas em uma linha so")
checa("sem data ISO partida (ex.: '2026-08-' sozinho)",
      re.search(r"\d{4}-\d{2}-\s*$", texto, re.M) is None)

print(f"\npassaram: {ok} · falharam: {falhou}")
sys.exit(1 if falhou else 0)
PY

echo "PDF OK"
