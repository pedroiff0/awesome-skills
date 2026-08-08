#!/usr/bin/env python3
"""Extrai o historico de disciplinas cursadas do SUAP (IFF) via scraping da
pagina web autenticada (aba Historico). A API v2 NAO expoe historico, entao
fazemos login web (matricula+senha, contorna o reCAPTCHA) e parseamos a tabela.

Uso:
  pip install requests beautifulsoup4 lxml
  export SUAP_MATRICULA=20232920049 SUAP_SENHA=...
  python scrape-historico.py [--csv saida.csv]
"""
import os
import re
import json
import csv
import argparse
import requests
from bs4 import BeautifulSoup

BASE = "https://suap.iff.edu.br"
UA = "Mozilla/5.0"
MATRICULA = os.environ.get("SUAP_MATRICULA", "20232920049")
SENHA = os.environ.get("SUAP_SENHA", "")


def login_session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    pg = s.get(f"{BASE}/accounts/login/", timeout=30)
    csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', pg.text)
    csrf = csrf.group(1) if csrf else ""
    r = s.post(
        f"{BASE}/accounts/login/",
        data={"csrfmiddlewaretoken": csrf, "username": MATRICULA,
              "password": SENHA, "next": f"/edu/aluno/{MATRICULA}/?tab=historico"},
        headers={"Referer": f"{BASE}/accounts/login/"},
        allow_redirects=False, timeout=30,
    )
    if r.status_code not in (302, 303):
        raise RuntimeError(f"Login falhou (status {r.status_code}): {r.text[:200]}")
    return s


def extrair(s):
    url = f"{BASE}/edu/aluno/{MATRICULA}/?tab=historico"
    html = s.get(url, timeout=30).text
    start = html.find('data-tab="historico"')
    if start == -1:
        raise RuntimeError("Aba de historico nao encontrada (sessao expirou?)")
    soup = BeautifulSoup(html[start:start + 200000], "lxml")
    linhas = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 9:
            continue
        vals = [td.get_text(" ", strip=True) for td in tds]
        ano = vals[0]
        if not re.match(r"^\d{4}/\d$", ano):
            continue
        codigo = vals[3]
        componente = tds[4].get_text(" ", strip=True)
        mtit = re.search(r"\s*\([^)]*\)\s*$", componente)
        if mtit:
            componente = componente[:mtit.start()].strip()
        mcap = re.match(r"^([A-ZÀ-Ú0-9\s.\-]+?)(?=[A-ZÀ-Ú][a-zà-ú])", componente)
        prof = ""
        if mcap:
            disciplina = mcap.group(1).strip()
            prof = componente[mcap.end():].strip()
            componente = disciplina
        linhas.append({
            "ano_letivo": ano,
            "periodo_curso": vals[1],
            "codigo": codigo,
            "componente": componente,
            "professor": prof,
            "carga_horaria": vals[5],
            "nota_conceito": vals[6],
            "freq_percent": vals[7],
            "situacao": vals[8] if len(vals) > 8 else "",
        })
    return linhas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", metavar="ARQUIVO", help="salvar tambem em CSV")
    args = ap.parse_args()
    if not SENHA:
        print("ERRO: defina SUAP_SENHA (export) ou edite a constante no topo.", file=__import__("sys").stderr)
        raise SystemExit(2)
    s = login_session()
    linhas = extrair(s)
    print(json.dumps(linhas, indent=2, ensure_ascii=False))
    print(f"\nTotal de disciplinas no historico: {len(linhas)}", file=__import__("sys").stderr)
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()))
            w.writeheader()
            w.writerows(linhas)
        print(f"CSV salvo em {args.csv}", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
