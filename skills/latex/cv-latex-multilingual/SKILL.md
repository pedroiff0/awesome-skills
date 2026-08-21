---
name: cv-latex-multilingual
description: Manter o CV LaTeX multilíngue do usuário (classe altacv) em ~/Repositorios/pessoal/cv — PT (fonte), EN (espelho), ES/FR (gerados do EN via translate_cv.py). Abrange correções de conteúdo, build via Makefile, bugs do gerador e verificação de PDFs.
author: LaTeX Community
---

# CV LaTeX Multilíngue (altacv)

CV do usuário em LaTeX com a classe `altacv.cls`, em 4 idiomas (PT/EN/ES/FR). Usado para submissão a bolsas/eventos.

## Gatilhos
- "atualizar meu cv", "criar ES/FR do cv", "traduzir o cv", "corrigir o cv", "dar uma olhada no portuguese.tex".
- Qualquer pedido de editar projetos/bolsas/eventos no CV.

## LOCALIZAÇÃO (FONTE DE VERDADE)
`/home/pedro/Repositorios/pessoal/cv/` — é um REPO GIT e o CV REAL (mais completo: tem Resumo Acadêmico, Cursos Externos, dezenas de eventos com `\cite{...}`).

> ⚠️ PITFALL — NÃO EDITAR O TEMPLATE STALE: existe uma CÓPIA ANTIGA em
> `/home/pedro/Documentos/latex/modelos/geral/cv/modelo_cv/` (mesmos nomes de
> arquivo, mas sem o conteúdo extra e com os mesmos erros). Editar lá NÃO afeta o
> CV real. Sempre confirme o caminho antes de escrever — o usuário já corrigiu uma
> vez por causa disso ("Deveria ser em Repositorios pessoal cv").

## Estrutura
- `main.tex` — carrega `babel[brazilian,english,spanish,french]`; o Makefile gera `main_<lang>.tex` injetando `\input{<lang>.tex}`.
- `portuguese.tex` — FONTE DE CONTEÚDO (mais completo). Edite aqui primeiro.
- `english.tex` — espelho direto do PT; é o PIVÔ para gerar ES/FR.
- `spanish.tex`, `french.tex` — gerados por `translate_cv.py` a partir de `english.tex` (substituição literal de strings, NÃO tradução real).
- `translate_cv.py` — regenera ES/FR do EN.
- `Makefile`: `make portugueseCV | englishCV | spanishCV | frenchCV | all`.
- `page1sidebar.tex` (PT), `page1sidebarEN.tex`, `page1sidebarES.tex`, `page1sidebarFR.tex` — sidebar (Premiações/Estatísticas/Programação/Línguas) com cabeçalhos e termos traduzidos por idioma. Cada `<lang>.tex` aponta seu primeiro `\cvsection` para o arquivo correspondente via `[page1sidebar<SUFIXO>]`.
- `photo` usa `profile` (não `curriculo`).

## Workflow de correção
1. Edite `portuguese.tex` (fonte) E `english.tex` (espelho) com o mesmo conteúdo.
2. `cd ~/Repositorios/pessoal/cv && python3 translate_cv.py` → regera `spanish.tex`/`french.tex` do EN já corrigido.
3. Conserte os BUGS conhecidos do `translate_cv.py` em `spanish.tex`/`french.tex` (ver `references/translate_cv_pitfalls.md`). Se for traduzir TODOS os eventos (pedido explícito do usuário em 2026-08), use `scripts/translate_events.py` — rode DENTRO do `terminal` (ver Pitfall #6).
4. `make all` (ou por idioma) para gerar os 4 PDFs.
5. Verifique com `scripts/verify_cv_pdfs.py` (normaliza acentos/en-dash/apóstrofo/quebras de linha).

> ⚠️ PITFALL #6 — `execute_code` (hermes_tools) NÃO persiste arquivos no disco.
> Edições em massa de `.tex` devem ser feitas via Python REAL no `terminal`
> (`io.open`), NUNCA via `read_file`/`write_file` de `hermes_tools` dentro de
> `execute_code`. Edits pontuais: use a tool `patch` (grava de fato).

## LAYOUT / ESPAÇAMENTO (altacv) — pitfalls de quebra de página

Estes bugs apareceram e custaram várias iterações; registre para não repetir:

1. **Sidebar `[page1sidebar]` atrelada à seção ERADA → espaço em branco em Eventos.**
   O argumento opcional do `\cvsection` (`\cvsection[page1sidebar]{...}`) faz `\marginpar{\input{page1sidebar.tex}}`
   na PRIMEIRA página onde esse comando aparece. Se a sidebar for ALTA (~49 linhas, como a deste CV)
   e estiver atrelada a uma seção LONGA (ex.: `Publicações` com bibliografia de 14 refs), o LaTeX
   reserva uma página inteira para a marginpar e joga a seção para a página seguinte — isolando a
   seção ANTERIOR (Eventos) com ~metade da página em branco.
   **FIX:** atrele `[page1sidebar]` ao PRIMEIRO `\cvsection` da página 1 (o "Resumo Acadêmico" /
   "Academic Background" / "Resumen Académico" / "Résumé Académique"). Assim a sidebar vai para a
   pág 1 e Eventos preenche a pág 2 sem espaço em branco. Remova qualquer `\clearpage`/`\pagebreak`
   que force Eventos para página própria.

2. **`\pagebreak` espúrio antes de "Áreas de Interesse"** também isola Eventos. Se a pág 1 termina
   cortada e a pág 2 tem Áreas de Interesse + Eventos com espaço embaixo, remova o `\pagebreak`
   entre `Cursos Externos` e `Áreas de Interesse` para o conteúdo fluir.

3. **Sobreposição entre subtítulos de bibliografia** ("Resumos em Congressos" vs "Artigos"):
   `\printbibliography[heading=none,type=inproceedings]` termina COLADO no `\cvsubsection{Artigos}`
   seguinte. **FIX:** insira `\medskip` após cada `\printbibliography[heading=none,...]` antes do
   próximo `\cvsubsection`. Aplica em PT/EN/ES/FR.

4. **Sidebar por idioma (NÃO mais compartilhada):** o CV agora tem `page1sidebar.tex` (PT),
   `page1sidebarEN.tex` (AWARDS/STATISTICS/PROGRAMMING/LANGUAGES), `page1sidebarES.tex`
   (Premiaciones/Estadísticas/Programación/Lenguas), `page1sidebarFR.tex` (Prix/Statistiques/
   Programmation/Langues). Em cada `<lang>.tex`, aponte o primeiro cvsection para o arquivo do
   idioma: `\cvsection[page1sidebarEN]{Academic Background}`, etc. Mantenha nomes próprios de
   prêmios/siglas; traduza só cabeçalhos e termos genéricos. (Atualiza também a seção Estrutura
   acima: `page1sidebar.tex` é só o PT; os outros são dedicados por idioma.)

5. **Verificação de layout é VISUAL.** `pdftotext` + normalizador confirmam PRESENÇA de texto, mas
   NÃO detectam espaço em branco nem sobreposição. Gere PNGs (`pdftoppm -png -r 90 X.pdf /tmp/X`) e
   inspecione com visão (vision_analyze) para confirmar: sidebar na pág 1 sem sobreposição, Eventos
   preenchendo a pág 2, e Referências sem colisão. Esta é a única forma confiável de fechar esses bugs.

## Commit & push (repo git)
- ANTES de `git add`, limpe lixo de build do macOS: `rm -f ._*.pdf` (o `make` e o
  preview do macOS criam `._<nome>.pdf` que não devem ser versionados).
- `git add` dos `.tex` modificados + dos 4 `*CV.pdf` (2 modificados + 2 novos) +
  `git rm` dos auxiliares órfãos (`main_spanish.tex`, `spanishCV.aux/.fls/.log/.fdb_latexmk`).
- `git commit -m "..."` e `git push origin main`. O remote é `github.com/pedroiff0/cv`.

## Verificação de PDFs (pós-build)
`pdftotext <lang>CV.pdf -` e confira substrings. Cuidado com armadilhas do `pdftotext`:
- emite en-dash (U+2013) para `--` e apóstrofo tipográfico (U+2019) para `'`.
- títulos longos quebram em linha nova.
- Normalize antes de comparar: NFD → remove Mn (acentos) → lowercase → não-alfanum→espaço → colapse espaços. Isso junta quebras de linha e neutraliza en-dash/apóstrofo.
- Script reutilizável: `scripts/verify_cv_pdfs.py [DIR_DO_CV]`.

## Support files
- `scripts/verify_cv_pdfs.py` — verificação pós-build dos 4 PDFs (normaliza acentos/en-dash/apóstrofo/quebras; rode `python3 scripts/verify_cv_pdfs.py [DIR]`).
- `scripts/translate_events.py` — traduz TODOS os nomes de eventos/congressos em ES/FR (rode DENTRO do `terminal`, nunca via execute_code). Ajuste os dicts conforme o conteúdo corrente; reporta alvos não encontrados.
- `references/translate_cv_pitfalls.md` — bugs do `translate_cv.py` (portunhol, "Brasilian", títulos de projeto em inglês, eventos em inglês, PITFALL #6 execute_code, PITFALL #7 grep LC_ALL=C) e correções de ano/título recorrentes.

## Relacionado
- `lattes-xml-projetos`: gerar XML de importação Lattes (bolsas/projetos) — frequentemente usado junto com o CV.
