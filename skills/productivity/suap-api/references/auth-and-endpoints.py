#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Probe reutilizavel da API v2 do SUAP (instancia IFF / generica).
Faz login (matricula+senha -> JWT), depois:
  - imprime os periodos letivos
  - puxa /api/ensino/aluno-matriculado/
  - sonda /api/ensino/meu-boletim/ para os primeiros periodos
Nao depende de libs externas (so stdlib).

Uso:
  python3 auth-and-endpoints.py --base https://suap.iff.edu.br \
      --matricula 20232920049 --senha 'F4nt4st1c@' --token-out token.json
"""
import argparse, json, sys, urllib.request, urllib.error

def api(base, path, token=None, method="GET", data=None):
    url = base.rstrip("/") + path
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:  # noqa
        return None, str(e)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://suap.iff.edu.br")
    ap.add_argument("--matricula", required=True)
    ap.add_argument("--senha", required=True)
    ap.add_argument("--token-out", default="suap_token.json")
    ap.add_argument("--max-boletim", type=int, default=3)
    args = ap.parse_args()

    st, tok = api(args.base, "/api/v2/autenticacao/token/", method="POST",
                  data={"username": args.matricula, "password": args.senha})
    if st != 200:
        print(f"LOGIN FALHOU: {st} {tok}", file=sys.stderr)
        sys.exit(1)
    print(f"Login OK. access JWT len={len(tok['access'])}, refresh len={len(tok['refresh'])}")
    json.dump(tok, open(args.token_out, "w"), indent=1)
    print(f"Token salvo em {args.token_out}")

    # Periodos letivos
    st, per = api(args.base, "/api/ensino/meus-periodos-letivos/", tok["access"])
    periodos = []
    if st == 200:
        periodos = [(p["ano_letivo"], p["periodo_letivo"]) for p in per.get("results", [])]
        print(f"\nPeriodos letivos ({per.get('count')}): {periodos}")
    else:
        print(f"\nPeriodos: ERRO {st}")

    # Dados do aluno
    st, al = api(args.base, f"/api/ensino/aluno-matriculado/?matricula={args.matricula}", tok["access"])
    if st == 200:
        print(f"\nAluno: {al.get('nome')} | {al.get('curso')} | campus {al.get('campus')} | periodo {al.get('periodo_atual')}")
    else:
        print(f"\nAluno: ERRO {st} {al}")

    # Boletim (sonda os N primeiros periodos)
    print("\nBoletim:")
    for ano, p in periodos[:args.max_boletim]:
        st, b = api(args.base, f"/api/ensino/meu-boletim/{ano}/{p}/", tok["access"])
        if st == 200:
            print(f"  {ano}/{p}: {b.get('count', 0)} disciplinas")
        else:
            print(f"  {ano}/{p}: ERRO {st}")

if __name__ == "__main__":
    main()
