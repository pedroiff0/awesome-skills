#!/usr/bin/env python3
"""Verifica conteudo dos 4 PDFs do CV apos o build.

Uso: python3 verify_cv_pdfs.py [DIR_DO_CV]
  (default: /home/pedro/Repositorios/pessoal/cv)

Checa substrings normalizadas (acentos/en-dash/apostrofo/quebras de linha
removidos) para sobreviver a: en-dash (--), apóstrofo tipografico (') e
quebra de linha no meio de titulos longos que o pdftotext emite.

Ajuste os `checks` abaixo conforme o conteudo corrente do CV.
"""
import subprocess, sys, unicodedata, os, re

DIR = sys.argv[1] if len(sys.argv) > 1 else "/home/pedro/Repositorios/pessoal/cv"

def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")  # tira acentos
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)   # remove tudo que nao e alfanum
    return re.sub(r"\s+", " ", s)

def text(pdf: str) -> str:
    r = subprocess.run(["pdftotext", os.path.join(DIR, pdf), "-"],
                       capture_output=True, text=True)
    return norm(r.stdout)

# (pdf, [(label, needle, must_contain_bool), ...])
checks = {
    "portugueseCV.pdf": [
        ("PT titulo 2022-2023", "analise de simulacoes dinamicas de aglomerados de galaxias em fusao", True),
        ("PT satelites", "simulando o impacto de satelites em observacoes astronomicas", True),
        ("PT bolsista cnpq", "bolsista no projeto de iniciacao cientifica cnpq", True),
        ("PT anomalias", "deteccao de anomalias em estrelas da via lactea", True),
        ("PT data 2024", "2024 presente", True),
        ("PT sem materia escura", "entendendo a materia escura", False),
        ("PT sem voluntario", "voluntario no projeto", False),
        ("PT extra XLVIII", "xlviii reuniao anual da sociedade astronomica brasileira", True),
    ],
    "englishCV.pdf": [
        ("EN titulo 2022-2023", "analysis of dynamical simulations of merging galaxy clusters", True),
        ("EN satelites completo", "simulating the impact of satellites on astronomical observations", True),
        ("EN scholarship cnpq", "scholarship in the scientific initiation project cnpq", True),
        ("EN anomalias", "anomaly detection in stars of the milky way", True),
        ("EN data 2024", "2024 present", True),
        ("EN sem dark matter", "understanding dark matter", False),
        ("EN sem volunteer", "volunteer in the scientific initiation", False),
    ],
    "spanishCV.pdf": [
        ("ES titulo 2022-2023", "analisis de simulaciones dinamicas de cumulos de galaxias en fusion", True),
        ("ES satelites", "simulando el impacto de satelites en observaciones astronomicas", True),
        ("ES anomalias", "deteccion de anomalias en estrellas de la via lactea", True),
        ("ES resumo", "actualmente soy estudiante de ingenieria informatica", True),
        ("ES sem portunhol", "i'm currently a ingenieria informatica", False),
        ("ES brazilian", "brazilian astronomical society", True),
        ("ES sem brasilian", "brasilian", False),
        ("ES sem ingles proj", "analysis of dynamical simulations", False),
    ],
    "frenchCV.pdf": [
        ("FR titulo 2022-2023", "analyse de simulations dynamiques d amas de galaxies en fusion", True),
        ("FR satelites", "simulation de l impact des satellites sur les observations astronomiques", True),
        ("FR anomalias", "detection d anomalies dans les etoiles de la voie lactee", True),
        ("FR resumo", "je suis actuellement etudiant en ingenierie informatique", True),
        ("FR sem portunhol", "i'm currently a ingenierie informatique", False),
        ("FR bresilienne", "bresilienne astronomical society", True),
        ("FR sem bresilian", "bresilian", False),
        ("FR sem ingles proj", "analysis of dynamical simulations", False),
    ],
}

fail = 0
for pdf, items in checks.items():
    path = os.path.join(DIR, pdf)
    if not os.path.exists(path):
        print(f"FAIL {pdf} NAO EXISTE"); fail = 1; continue
    t = text(pdf)
    print(f"=== {pdf} ===")
    for label, needle, must in items:
        present = norm(needle) in t
        ok = present if must else (not present)
        print(("OK   " if ok else "FAIL ") + label)
        if not ok:
            fail = 1

print("=== RESULTADO ===", "ALL_OK" if fail == 0 else "HOUVE_FALHAS")
sys.exit(fail)
