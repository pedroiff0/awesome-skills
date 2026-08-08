---
name: latex-cv-maintenance
description: Use when reviewing, updating, or keeping consistent a multi-language LaTeX CV (altacv.cls). Covers treating Portuguese as source of truth and mirroring to other languages, cross-checking project/date/role data against the Lattes export, and verifying edits by compiling (latexmk/Makefile) and grepping pdftotext output.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [latex, cv, curriculo, altacv, lattes, consistencia, revisao]
    related_skills: [lattes-xml-projetos]
---

# LaTeX CV Maintenance (multi-language, altacv)

## Overview
Mantém um currículo em LaTeX baseado em altacv.cls quando há versões em múltiplos idiomas
(ex.: portuguese.tex + english.tex) e um Lattes como fonte autoritativa de dados de projetos.
Usado para revisar o CV em busca de itens faltando ou inconsistentes, espelhar edições entre
idiomas e confirmar que as mudanças realmente entraram no PDF.

## When to Use
- Usuário pede para "revisar o CV", "atualizar o currículo", "conferir inconsistências".
- Há um .tex por idioma e os outros são "tradução direta" de um deles (PT = fonte da verdade).
- Precisa garantir que projetos/datas/cargos batem com o Lattes.
- **Criar novos idiomas** (ex.: "cadê o ES e FR? crie-os traduzidamente") — o CV deste usuário
  já tem 4 idiomas (PT/EN/ES/FR), cada um com wrapper `*CV.tex` + `page1sidebarXX.tex` dedicados.
- Não usar para gerar o XML de importação do Lattes (ver skill `lattes-xml-projetos`).

## Workflow
1. **Localize os arquivos**: o main (ex.: portugueseCV.tex) faz `\input{portuguese.tex}`;
   há um .tex por idioma e sidebars (ex.: page1sidebar.tex / page2sidebar.tex) para a barra lateral.
   O build costuma ser um Makefile (`make portugueseCV` / `make englishCV`) com `latexmk -lualatex`.
2. **PT é a fonte da verdade.** Edite primeiro o portuguese.tex; espelhe cada mudança em TODOS os
   outros idiomas (english.tex, spanish.tex, french.tex — tradução literal, sem inventar conteúdo).
   Trate como edição atômica em todas as línguas. Se o CV tiver 2 idiomas só (PT/EN), espelhe PT<->EN.
2b. **Para CRIAR um novo idioma** (ex.: ES/FR a partir do PT), replique a estrutura de um idioma existente:
    - `XX.tex`: copie `portuguese.tex`, troque `\selectlanguage{brazilian}` pelo idioma alvo
      (`\selectlanguage{spanish}` / `\selectlanguage{french}`) e traduza o corpo. Ajuste `hl=XX` nos links
      (Google Scholar etc.) para o idioma.
    - `page1sidebarXX.tex`: copie `page1sidebar.tex` e traduza (Premiações→Premios/Prix, Línguas→Idiomas/Langues...).
    - `XXCV.tex`: wrapper que copia `portugueseCV.tex`/`englishCV.tex`, mas com
      `\usepackage[brazilian,<idioma>]{babel}` (KEEP `brazilian` primeiro — o `\selectlanguage` do `\today`
      no corpo depende dele) e `\input{XX.tex}`.
    - `Makefile`: adicione `XX_PDF := XXCV.pdf`, `XX_SRC := XXCV.tex`, target `XXCV` e `$(XX_PDF)` e inclua
      em `all`. Veja o padrão dos targets `spanishCV`/`frenchCV` já existentes.
    Tradução é DIRETA (não adapte conteúdo). Não invente dados.
3. **Cross-check com o Lattes** (XML ou export): confira título, período (ano/mês), cargo
   (Bolsista vs Voluntário), orientador(es) e natureza (Pesquisa/Extensão) de cada projeto.
   O CV tende a defasar quando o projeto é renomeado ou a data muda no Lattes.
4. **Aplique nas duas línguas** e nos sidebars se a informação aparecer lá (ex.: premiações citam
   o título de um projeto — o título deve bater em ambos os lados).
5. **Verifique (obrigatório)**: compile e extraia o texto para confirmar que a edição entrou no PDF.
   Receita em `references/verify-recipe.md`.
6. **Mantenha também as versões em Markdown sincronizadas** (preferência do usuário): o repo tem
   `README.md` (com o CV embutido em md na seção "CV em Markdown") e `curriculo.md` (CV standalone em
   md). Ao mudar conteúdo no LaTeX, replique a mesma alteração nesses .md — o usuário os usa como
   fonte legível/portátil. O `README.md` também documenta o build multi-idioma (tabela de arquivos
   por idioma + targets do Makefile).

## Estrutura altacv relevante
- `\cvevent{Título}{Instituição}{Período}{Local}` — o Período usa `{Mês. Ano -- presente}`
  (hífen duplo; em inglês `present`, em português `presente`). Ano-only também ok: `{2024 -- presente}`.
- Sidebar: `\\cvsection`, `\\cvachievement`, `\\cvtag`, `\\cvskill`.
- Build (Makefile, `latexmk -lualatex`): `make portugueseCV` / `make englishCV` / `make spanishCV`
  / `make frenchCV` / `make all`. Cada idioma tem wrapper `*CV.tex` + `page1sidebarXX.tex`.

## Layout / espaçamento (ajustes comuns de altacv)
altacv deixa o layout "quebradico" em 3 situações típicas — corrija assim:
1. **Colunas `multicols` esticadas (espaço em branco entre itens)**: o ambiente `multicols`
   equaliza a altura das colunas esticando o espaço vertical. Adicione `\raggedcolumns`
   logo após cada `\begin{multicols}{2}` (Formação, Projetos, Eventos). Isso alinha pelo
   topo e elimina o espaço extra. Ex.: `\begin{multicols}{2}\raggedcolumns`.
2. **Espaço solto entre um sub-cabeçalho e o conteúdo** (ex.: "Proceedings" → referência da
   bibliografia): o `\cvsubsection` insere `\medskip` depois do título. Substitua por um
   cabeçalho compacto inline:
   `\textbf{\large\color{emphasis}Proceedings}\par\vspace{0.2\baselineskip}` seguido do conteúdo.
   (Use para seções de Publicações; para sub-cabeçalhos de Eventos, manter `\cvsubsection` é OK.)
3. **Página 2 com 2/3 vazios** (ex.: Publicações + sidebar, coluna esquerda curta): mova uma
   seção da página 1 para depois das Publicações (página 2) para balancear. Neste CV, as
   "Áreas de Interesse / Research Interests / Domaines d'Intérêt / Áreas de Interés" foram
   movidas do final da página 1 para após a bibliografia na página 2 — equilibrou a coluna.
4. **`\divider` redundante antes de `\cvsubsection`**: em Eventos, o `\divider` antes do
   sub-cabeçalho "Congressos" cria um buraco grande. Remova-o; o `\cvsubsection` já separa
   visualmente. (Mantenha os `\divider` entre itens do mesmo sub-cabeçalho.)
5. **Disclaimer de tradução automática**: em idiomas DERIVADOS (não o PT fonte), o usuário quer
   um rodapé itálico informando tradução por IA. Ex. (ES, no final do arquivo, antes de `\clearpage`):
   `\vspace{1em}\footnotesize\itshape Traducción automática generada por IA a partir de la versión en portugués del currículo.`
   (FR): `...Traduction automatique générée par IA à partir de la version portugaise du curriculum vitae.`
   PT e EN não levam disclaimer.

## Pitfalls
1. **"Voluntário ... CNPq"** é contraditório — CNPq concede bolsa, não voluntariado. Use "Bolsista CNPq".
   (No EN: "Scholarship ... CNPq", nunca "Volunteer".)
2. **Drift de data**: o CV costuma ficar 1-2 anos atrás do Lattes quando o projeto é renomeado/mudado.
   Sempre cruze com a fonte antes de "consertar" só o texto solto.
3. **Título grudado no ano**: `"... com Aprendizado de Máquina 2025"` — o "2025" é typo dentro do
   título; removê-lo e usar o campo de período.
4. **Mirror drift**: se editou só o PT e esqueceu o EN (ou vice-versa), as versões divergem.
5. **Título truncado na tradução**: ex.: "Astronomical" deveria ser "Astronomical Observations".
   Revise o EN com cuidado, não só copie.
6. **hl=pt-BR em links do EN** (ex.: Google Scholar `hl=pt-BR`) — cosmetic, mas no EN prefira `hl=en`.
7. **Não confie só no "up-to-date" do latexmk**: após editar, force rebuild (`rm` dos aux) e confira o PDF.
8. **babel em novo idioma**: mantenha `brazilian` PRIMEIRO em `\usepackage[brazilian,<idioma>]{babel}`
   mesmo no wrapper de outro idioma — o `\selectlanguage{<idioma>}` no corpo (e o `\today` formatado)
   depende de o brazilian estar carregado. Sem isso, `\today` não formata ou quebra o build.
9. **Verificação frágil via grep/pdftotext dá FALSO-NEGATIVO**: `pdftotext` exporta cabeçalhos de
   `\\cvsection` em MAIÚSCULAS, converte apóstrofo reto em tipográfico (’) e QUEBRA LINHAS no meio de
   títulos longos. Greps case-sensitive ou com apóstrofo reto falham. Use o script de normalização em
   `references/verify-recipe.md` (remove acentos via NFD, casefold, colapsa pontuação/espaço) — assim
   substrings sobrevivem a quebras e apóstrofos. Nunca declare "FALHOU" sem antes confirmar com o
   texto extraído cru (ex.: `pdftotext X.pdf - | grep -i "trecho" | cat -A`).
10. **Mover seção entre páginas apaga o `\end{multicols}` vizinho** (BUG REAL desta sessão): ao cortar
   uma seção do final da página 1 (ex.: remover "Áreas de Interesse" de antes do `\end{fullwidth}`),
   é fácil incluir o `\end{multicols}` da seção ANTERIOR (Eventos) no bloco removido. Sintoma:
   `! LaTeX Error: \begin{multicols} on input line N ended by \end{list}` e o PDF some. Sempre
   reinsira o `\end{multicols}` imediatamente antes do `\end{fullwidth}` da seção cuja coluna você
 mexeu. Dica: após qualquer remoção de bloco, confira se cada `\begin{multicols}{2}` tem seu
 `\end{multicols}` correspondente (conte os pares).
 11. **`\begin{fullwidth}` órfão quebra TODO o documento**: se você removeu um `\end{fullwidth}`
 (ex.: ao reescrever uma seção) mas deixou o `\begin{fullwidth}` correspondente, o ambiente
 `list` interno do fullwidth fica aberto até `\end{document}` →
 `! LaTeX Error: \begin{list} on input line N ended by \end{document}` + erro fatal
 "Undefined control sequence". Isso TRAVA o primeiro lualatex (exit 1), o `.aux`/`.bcf` não é
 escrito e, em cascata, o biber gera `.bbl` vazio ("Empty bibliography") — por isso as
 referências somem. SEMPRE mantenha begin/end de fullwidth balanceados (conte os pares).
 Ao reescrever Eventos removendo o `\end{fullwidth}` antigo, reinsira `\end{fullwidth}` logo
 antes de `\newpage`/Publicações.
 12. **`\\` solto dentro de `\cvtag{...}`**: `\cvtag{Física Computacional} \\` (double backslash
 no fim da linha, fora de contexto de quebra de linha) causa "Undefined control sequence" ou
 "There's no line here to end". Remova o `\\` — o altacv já quebra os cvtags sozinho.
 13. **`\\` dentro de `\tagline{...}`** (cabeçalho): o altacv processa o tagline como texto; um
 `\\` no meio pode quebrar. Prefira texto corrido ou `\newline` dentro de grupo se preciso.
 14. **"Undefined control sequence" que só aparece VIA `\input` (não inline) — técnica de isolar**:
 Quando o corpo é incluído por `\input{portuguese.tex}` (padrão do Makefile), o LaTeX atribui
 o erro à linha do `\input` e ESCONDE a linha real do comando indefinido, dificultando o debug.
 Para achar a linha real: gere um `main_TEST.tex` com o PREÂMBULO do main.tex (até
 `\begin{document}`) + o CONTEÚDO do corpo embutido (sem `\input`) e compile. Se compilar
 limpo inline mas quebrar via `\input`, o culpado é um caractere invisível/BOM no início do
 arquivo de conteúdo (o Python normaliza ao ler/gravar, o `\input` não). Confirme com `od -c`
 no início do .tex e limpe com `sed -i '1s/^\xEF\xBB\xBF//'` ou reescreva o arquivo.
 Isolamento binário: comente seções progressivamente (do fim pro início) e recompile até o
 erro sumir — a última seção removida é a culpada.
 15. **Não declare "compilou" só porque `make` imprimiu "Generated"**: com `>/dev/null 2>&1` e
 `|| true` no recipe, o make esconde exit≠0 e um PDF de fallback (incompleto) é escrito. Sempre
 cheque `echo $?` ou rode uma passada de lualatex visível e confirme `EXIT=0` + conte as
 citações no PDF (`pdftotext X.pdf - | grep -c '\[\\d+\]'`).
 16. **BUG CRÍTICO do Makefile: `sed` que insere `\\n` LITERAL (barra-n como texto)** — bug raiz
 desta sessão; faz as referências SUMIREM silenciosamente. O padrão
 `sed 's/\\end{document}/\\input{<lang>}\\n\\end{document}/'` NÃO interpreta `\n` como newline em
 muito sed/GNU — escreve a string literal `\n`. No main_<lang>.tex resulta
 `\\input{portuguese.tex}\\n\\end{document}` onde o `\n` é o comando `\n` (undefined) →
 `! Undefined control sequence` FATAL no PRIMEIRO lualatex (exit 1). O `.aux`/`.bcf` não é escrito,
 o biber lê 0 citekeys → `.bbl` vazio → "Empty bibliography" + 0 referências no PDF. O corpo
 embutido INLINE (sem `\\input`) compila limpo — só falha via `\\input`, o que confunde o debug.
 **CORREÇÃO**: never use `sed '...\n...'` p/ newline. Use `awk` p/ inserir o `\\input` com newline
 REAL antes de `\\end{document}`:
 `awk '/\\end\\{document\\}/{print "\\input{'$*'}"} {print}' main_$*.tex > tmp && mv tmp main_$*.tex`
 (`$*` expandido pelo make; awk imprime `\\input{portuguese}` em linha própria, `{print}` reimprime
 `\\end{document}`). Makefile canônico em `references/makefile-biber-awk.md`.
 DICA diagnóstico: se `make` diz "Generated" mas o PDF tem 0 citações, rode passada visível
 `lualatex -interaction=nonstopmode -jobname=X main_X.tex 2>&1 | grep -i undefined`; se aparecer,
 o main_X.tex tem `\n` literal ou comando inválido — confirme com `grep -n '\\input' main_X.tex`.
 17. **`\\nocite{*}` vs citações nos eventos**: ao reescrever uma seção (ex.: Eventos) com comando
 custom (`\\evento`), é fácil PERDER os `\\cite{...}` que vinculavam o evento à referência. Se o PT
 tem `\\nocite{*}` comentado e os `\\cite{}` sumiram, o biber acha 0 citekeys → bibliografia vazia.
 Opções: (a) reativar `\\nocite{*}` no PT (mostra TODAS as entradas do .bib — o que o usuário quer),
 ou (b) reinserir os `\\cite{Chave}` nos args do `\\evento`. `\\nocite{*}` é a mais robusta.
 18. **Layout de Publicações em 2 colunas (publicações + sidebar) — substitua `[page1sidebar]`**:
 `\\cvsection[page1sidebarXX]{Publicações}` usa `\\marginpar`, que SOME se a página estiver quase
 vazia (ex.: após `\\newpage`, a pág final só tem o resto das referências). Para GARANTIR a sidebar
 na última página DIVIDINDO o espaço, use `minipage` explícito DENTRO de `fullwidth`:
 `\\begin{fullwidth}\\cvsection{\\faFile*\\ Publicações}\\begin{minipage}[t]{0.63\\linewidth}
 <link ADS + \\nocite{*} + \\printbibliography...> \\end{minipage}\\hfill
 \\begin{minipage}[t]{0.33\\linewidth}\\input{page1sidebarXX}\\end{minipage}\\end{fullwidth}`.
 Fixa publicações à esquerda e sidebar à direita, sem depender de marginpar. Verificado PT/EN/ES/FR.
 19. **Corrupção de escaping em edições de `.tex` via `patch` tool**: ao usar a tool `patch`
 num arquivo denso em barras invertidas (ex.: definição de `\\evento` em `main.tex`), o `patch`
 pode DEVOLVER barras DOBRADAS (`\\` → `\\\\`) em vez de substituir — especialmente quando o
 `old_string`/`new_string` também contém `\\`. Sintoma: `! Undefined control sequence` ou
 `! LaTeX Error: There's no line here to end` em TODAS as entradas que usam o comando.
 **FIX**: reescreva o arquivo inteiro com `write_file` (sobrescreve tudo, barras corretas) ou
 use `execute_code` com `io.open` (Pitfall #6 do `cv-latex-multilingual`). NUNCA confie em
 `patch` para trocar trechos densos em `\\`; valide com `grep -n '\\\\\\\\' arquivo.tex` após editar.
 20. **Espaçamento entre entradas de comando customizado + título de seção colado no conteúdo**:
 - Entre itens de uma lista custom (`\\evento`, `\\cvevent`): use `\\par\\medskip` no fim de cada
   entrada (não só `\\smallskip`) — dá o "respiro"/breakline que o usuário pediu. Confirmado por
   inspeção visual (PT pág 2: eventos não colados).
 - Título de seção isolado do conteúdo (ex.: "Publicações" numa página, referências na seguinte):
   o `\\cvsection{...}` + bloco grande abaixo transborda. **FIX**: insira `\\nopagebreak` logo
   após o `\\cvsection{...}` (antes do `\\begin{minipage}`), e remova `\\newpage` DUPLICADO que
   cria a quebra errada. Assim título e conteúdo ficam na mesma página.

## Build: ciclo de bibliografia (BIBER) e Makefile
O CV usa biblatex (backend biber) com `\addbibresource{sample.bib}` + `\printbibliography`.
A referência SÓ aparece no PDF se o ciclo rodar biber ENTRE as passadas do lualatex:
`lualatex → biber <jobname> → lualatex → lualatex`.
- **`latexmk -lualatex` NÃO dispara biber de forma confiável** neste repo (o PDF sai sem a
  lista bibliográfica / "Empty bibliography"). Use o ciclo explícito no Makefile (Makefile
  canônico com `awk` em `references/makefile-biber-awk.md` — NÃO use `sed` com `\n`, ver Pitfall 16).
  Se usar `latexmk`, force `-bibtex` ou rode biber à mão.
- Sintoma de biber não rodado: `LaTeX Warning: Empty bibliography on input line N` e 0 citações
  no PDF (o `\nocite{*}` comentado em PT significa que só entradas citadas aparecem; EN/ES/FR têm
  `\nocite{*}` ativo).
- Build artifacts `main_<lang>.tex` são gerados dinamicamente pelo Makefile (sed em cima do
  main.tex) — NÃO versionar (já no `.gitignore`).

## Sidebar ([page1sidebar]) e página da bibliografia
- `\cvsection[page1sidebar]{Publicações}` injeta o arquivo como `\marginpar` (lado direito).
  Se a página estiver CHEIA de referências, a marginpar não cabe e a sidebar SOME (lado direito
  em branco). Para garantir a sidebar na ÚLTIMA página junto das Publicações, insira
  `\clearpage` (ou `\newpage`) ANTES do `\cvsection[page1sidebar]{...}`.
- **Sidebar multi-idioma**: o argumento `[page1sidebar]` aponta SEMPRE para `page1sidebar.tex`
  (português). Para traduzir a sidebar, crie `page1sidebarEN.tex` / `page1sidebarES.tex` /
  `page1sidebarFR.tex` e use `\cvsection[page1sidebarEN]{...}` etc. em cada idioma. Reverter a
  sidebar para "Publicações" (saindo do "Resumo Acadêmico") exige trocar o argumento em TODOS os
  4 idiomas — não esqueça de apontar para o arquivo traduzido.
- Para seção de Publicações em página dedicada: `\end{fullwidth}` (fecha o fullwidth do corpo)
  + `\newpage` + `\cvsection[page1sidebarXX]{Publicações}`.

## Verification (ad-hoc, via pdftotext — método robusto)
Veja `references/verify-recipe.md` para o script Python de normalização e
`references/build-biber-debug.md` para o ciclo de Makefile com biber e a técnica de isolar
"Undefined control sequence" escondido pelo `\input`. Em resumo:
- Compile todos os idiomas tocados: `make portugueseCV englishCV spanishCV frenchCV` (exit 0 = compila).
- Confirme o texto novo no PDF com o script normalizado (acentos/apóstrofo/quebra de linha não quebram a busca).
- Sem `pdftotext`/Python, abra o PDF ou use inspeção visual — mas NÃO use grep case-sensitive cru,
  pois `pdftotext` emite cabeçalhos em MAIÚSCULAS e apóstrofo tipográfico (ver Pitfall 9).

## Related
- `lattes-xml-projetos`: gera/valida o XML de importação do Lattes (mesma fonte de dados de projetos;
  o gerador `gerar_projeto_lattes.py` embute a lista canônica de projetos — use-a como referência
  antes de mexer no CV).
