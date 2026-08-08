# translate_cv.py — armadilhas conhecidas

`translate_cv.py` faz `str.replace` de strings fixas em `english.tex` → `spanish.tex`/`french.tex`. NÃO é tradutor: só troca o que está na lista. Sintomas recorrentes após rodar o script (corrigir manualmente em `spanish.tex`/`french.tex`):

1. **Resumo em portunhol/frenglish.** O script troca `Computer Engineering`→`Ingeniería Informática`/`Ingénierie Informatique`, mas a frase "I'm currently a Computer Engineering student" vira "I'm currently a Ingeniería Informática student" (semble inglês+espanhol). Troque a frase toda por uma tradução real:
   - ES: `Actualmente soy estudiante de Ingeniería Informática con una pasión por la astronomía y la ciencia de datos. ...`
   - FR: `Je suis actuellement étudiant en ingénierie informatique avec une passion pour l'astronomie et la science des données. ...`

2. **"Brasilian"/"Brésilian"** (grafia errada). O script troca `Brazil`→`Brasil`/`Brésil`, mas `Brazilian` vira `Brasilian`/`Brésilian`. Corrija:
   - ES: `Brazilian` (ex.: "XLVIII Annual Meeting of the Brazilian Astronomical Society").
   - FR: `Brésilienne` (concorda com "Société").

3. **Títulos de projeto (`\cvevent{...}`) ficam em INGLÊS.** O script NÃO tem replace para os títulos específicos de projeto, então eles são copiados do EN para ES/FR. Traduza os 3 títulos de projeto manualmente (alinhados ao PT):
   - 2022-2023: "Analysis of Dynamical Simulations of Merging Galaxy Clusters" → ES `Análisis de simulaciones dinámicas de cúmulos de galaxias en fusión` / FR `Analyse de simulations dynamiques d'amas de galaxies en fusion`.
   - Satélites: "Simulating the Impact of Satellites on Astronomical Observations" → ES `Simulando el Impacto de Satélites en Observaciones Astronómicas` / FR `Simulation de l'Impact des Satellites sur les Observations Astronomiques`.
   - Anomalias: "Anomaly Detection in Stars of the Milky Way: ..." → ES `Detección de Anomalías en Estrellas de la Vía Láctea: Explorando Datos de Gaia y Otros Surveys con Aprendizaje Automático` / FR `Détection d'Anomalies dans les Étoiles de la Voie Lactée : Exploration des Données de Gaia et d'autres Surveys par Apprentissage Automatique`.

4. **"Bachelor in Ingeniería/Ingénierie Informatique"** no EN→ES/FR. O script só troca o grau se a string exata bater; corrija para `Grado en Ingeniería Informática` (ES) / `Licence en Ingénierie Informatique` (FR).

5. **Nomes de eventos/congressos ficam em INGLÊS** em ES/FR (o script não os traduz). Em 2026-08 o usuário pediu explicitamente para traduzir TODOS os nomes de congressos, exceto internacionais já em inglês por natureza (só a IAU, que fica em inglês). Aplicado e aprovado. Regras:
   - Mantenha siglas-próprias/com-nomes-próprios: `44º CONUBES`, `CONEPE`, `MobFog at IFFMaker`, `Açaí Institute`, `Fluminense`.
   - O script JÁ aplica substituições parciais nos títulos de evento (ex.: `Brazilian`→`Brésilienne`/`Brasilian`, `Computer Engineering`→`Ingeniería Informática`/`Ingénierie Informatique`), então as strings-alvo em ES/FR NÃO são idênticas ao inglês. Ex.: em FR o alvo é `21st Brésilienne Science and Engineering Fair` (não `21st Brazilian...`); em ES `I Week of Ingeniería Informática and Management` (não `Computer Engineering`). Faça o replace das strings exatas que estão no arquivo, não as do inglês.
   - Use o apóstrofo tipográfico (U+2019, `'`) nos títulos FR (ex.: `d’Initiation`, `l’Institut`, `d’Ingénierie`).
   - As linhas de evento comentadas (`% \cvevent{...}`) não renderizam; opcional traduzi-las para consistência do fonte.
   - Traduza toda a seção de Eventos (feiras, congressos, reuniões, escolas, semanas acadêmicas) — não só os projetos.

6. **`execute_code` (hermes_tools) NÃO persiste arquivos no disco.** Ler/escrever `.tex` via `read_file`/`write_file` de `hermes_tools` DENTRO de `execute_code` roda em sandbox e o `write_file` não grava de fato (silencioso — o arquivo fica igual). Sintoma: script reporta "atualizado" mas `grep`/`sed` mostra o conteúdo antigo. **Corrija fazendo as edições em massa via Python REAL no `terminal`** (`io.open(path, encoding="utf-8")` para ler e gravar), nunca via `hermes_tools` dentro de `execute_code`. Para edições pontuais, prefira a tool `patch` (modo replace) — ela grava de fato.

7. **Verificação de PDF por `grep` no terminal precisa de `LC_ALL=C`.** O `grep` com locale padrão silencia matches com acento (ex.: `grep "reunion"` não acha `Reunión`). Use `export LC_ALL=C` antes do `grep -inE` no texto do `pdftotext`, ou confie no `scripts/verify_cv_pdfs.py` (que normaliza acentos em Python).

## Correções de "ano/título" recorrentes no conteúdo (aplicar em PT e EN)
- Título 2022-2023: "Entendendo a Matéria Escura a partir de Choques ExtraGalácticos" → "Análise de simulações dinâmicas de aglomerados de galáxias em fusão".
- Satélites: ano 2023→2025; "Voluntário/Volunteer"→"Bolsista/Scholarship" (CNPq).
- Detecção de Anomalias: remover "2025" grudado no título; ano Out/2025→2024.
