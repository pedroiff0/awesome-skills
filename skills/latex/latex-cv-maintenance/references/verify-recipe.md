# Verificação ad-hoc de CV LaTeX (altacv) — método robusto

Após editar os `.tex` de qualquer idioma e seus sidebars, confirme que a edição
realmente entrou no PDF. O `grep`/`pdftotext` CRU dá falso-negativo por três motivos:
1. `pdftotext` emite cabeçalhos de `\cvsection` em **MAIÚSCULAS**.
2. Converte apóstrofo reto (') em tipográfico (’) — seus greps com ' não casam.
3. **Quebra linhas** no meio de títulos longos (ex.: "...Merging Galaxy\nClusters").

=> Use normalização: remova acentos (NFD + drop Mn), `casefold`, e descarte tudo que
não seja alfanumérico. Assim substrings sobrevivem a maiúsculas, apóstrofos e quebras.

## Script Python reutilizável (salve em /tmp e remova depois)
```python
import subprocess, sys, unicodedata, os, re
DIR = "/home/pedro/Documentos/latex/modelos/geral/cv/modelo_cv"

def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")  # tira acentos
    s = s.casefold()
    s = re.sub(r"[^a-z0-9]", "", s)                                # sobra so alfanum
    return s

def pdf_text(pdf):
    return subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout

checks = {
  "portugueseCV.pdf": [("Formacao","formacao academica"),
                       ("2022-2023","analise de simulacoes dinamicas de aglomerados de galaxias em fusao"),
                       ("satelites","simulando o impacto de satelites em observacoes astronomicas"),
                       ("anomalias","deteccao de anomalias em estrelas da via lactea")],
  "englishCV.pdf":    [("Academic","academic background"),
                       ("2022-2023","analysis of dynamical simulations of merging galaxy clusters"),
                       ("satellites","simulating the impact of satellites on astronomical observations"),
                       ("anomalies","anomaly detection in stars of the milky way")],
  "spanishCV.pdf":    [("Formacion","formacion academica"),
                       ("2022-2023","analisis de simulaciones dinamicas de cumulos de galaxias en fusion"),
                       ("satelites","simulando el impacto de satelites en observaciones astronomicas"),
                       ("anomalias","deteccion de anomalias en estrellas de la via lactea")],
  "frenchCV.pdf":     [("Formation","formation academique"),
                       ("2022-2023","analyse de simulations dynamiques d amas de galaxies en fusion"),
                       ("satellites","simulation de l impact des satellites sur les observations astronomiques"),
                       ("anomalias","detection d anomalies dans les etoiles de la voie lactee")],
}
fail = 0
for pdf, items in checks.items():
    t = norm(pdf_text(os.path.join(DIR, pdf)))
    for label, needle in items:
        ok = norm(needle) in t
        print(("OK   " if ok else "FAIL ") + f"{pdf}: {label}")
        fail |= (not ok)
print("ALL_OK" if not fail else "HOUVE_FALHAS")
sys.exit(fail)
```
> Obs: o cabeçalho EN é "Academic Background" (não "Academic Education") — use o termo real do `.tex`.

## Passos manuais (fallback sem Python)
```bash
DIR=/home/pedro/Documentos/latex/modelos/geral/cv/modelo_cv
cd "$DIR"
# Force rebuild limpo (latexmk diz "up-to-date" se os aux não sumiram)
rm -f *.pdf *.aux *.log *.fdb_latexmk *.fls *.out *.toc *.bbl *.bcf *.xml *.synctex.gz *.run 2>/dev/null
make all
# Inspeção crua (confirme com cat -A para ver apóstrofo/quebra antes de declarar FAIL)
pdftotext spanishCV.pdf - | grep -i "cumulos de galaxias" | cat -A
pdftotext frenchCV.pdf  - | grep -i "amas de galaxies"    | cat -A
```

Checklist:
- [ ] `make all` retorna exit 0 para PT/EN/ES/FR
- [ ] títulos novos presentes no pdftotext normalizado de CADA idioma tocado
- [ ] anos/períodos corretos no PDF (confira `2024`, `2025`, `presente`/`present`)
- [ ] sidebars (premiações) ainda batem com os títulos de projeto citados em todas as línguas
- [ ] datas `\today` formatadas no idioma (PT "4 de agosto de 2026", ES "4 de agosto de 2026",
      FR "4 aout 2026", EN "August 4, 2026")

Nota: `pdftotext` vem do pacote `poppler-utils`. Se ausente, instale ou use inspeção visual.
Ao escrever um script de verificação temporário, use `/tmp/hermes-verify-*.py` e remova-o depois.
