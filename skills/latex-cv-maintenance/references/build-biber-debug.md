# Build + Biber + Debug (altacv CV multi-idioma)

## Makefile correto (ciclo explicito lualatex -> biber)
`latexmk -lualatex` NAO dispara biber de forma confiavel neste repo — o PDF sai sem a lista
bibliografica. Use o ciclo explicito. Exemplo de receita por idioma (substitua `portuguese`):

```
LUALATEX := lualatex -interaction=nonstopmode
portugueseCV.pdf: main.tex portuguese.tex sample.bib
	grep -v "\\input{" main.tex | sed 's/\\end{document}/\\input{portuguese.tex}\\n\\end{document}/' > main_portuguese.tex
	$(LUALATEX) -jobname=portugueseCV main_portuguese.tex
	biber portugueseCV
	$(LUALATEX) -jobname=portugueseCV main_portuguese.tex
	$(LUALATEX) -jobname=portugueseCV main_portuguese.tex
	rm -f main_portuguese.tex *.aux *.log *.fdb_latexmk *.fls *.out *.toc *.synctex.gz *.run.xml *.bcf *.bbl *.blg
```

Notas:
- O `grep -v "\\input{"` remove os `\input{<lang>.tex}` do main.tex; o `sed` re-insere o
  idioma alvo antes de `\end{document}`.
- NAO use `-halt-on-error` no lualatex do Makefile: ele para no PRIMEIRO erro e nao escreve o
  `.aux`, deixando o biber sem dados (`.bbl` vazio). Prefira `-interaction=nonstopmode` e verifique
  o exit code depois.
- `main_<lang>.tex` e artifact — ja esta no `.gitignore`.

## Diagnostico de "Empty bibliography" / referencias sumiram
1. Compile o ciclo acima e confira `biber <jobname>` retorna 0.
2. `pdftotext <job>.pdf - | grep -c '\[\d+\]'` -> deve ser > 0. Se 0:
   - `LaTeX Warning: Empty bibliography` no log -> o `.bbl` esta vazio.
   - Causa raiz quase sempre: o PRIMEIRO lualatex falhou (exit 1) por um erro fatal
     ("Undefined control sequence" / fullwidth desbalanceado), entao o `.aux`/`.bcf` nao foi
     escrito e o biber nao achou citacoes ("Found 0 citekeys"). Corrija o erro fatal primeiro.
   - PT tem `\nocite{*}` COMENTADO (so entradas citadas aparecem); EN/ES/FR tem `\nocite{*}` ativo.

## Isolar "Undefined control sequence" escondido pelo \input
O `\input{portuguese.tex}` faz o LaTeX atribuir o erro a linha do `\input`, escondendo a linha real.
Para achar:

```bash
python3 - <<'PY'
body=open('portuguese.tex',encoding='utf-8').read()
pre=open('main.tex',encoding='utf-8').read()
pre=pre[:pre.index('\\begin{document}')+len('\\begin{document}')]
open('main_PORT.tex','w',encoding='utf-8').write(pre+'\n'+body+'\n\\end{document}\n')
PY
lualatex -interaction=nonstopmode -jobname=portugueseCV main_PORT.tex
# se EXIT=0 aqui mas falha via \input -> BOM/caractere invisivel no .tex
rm -f main_PORT.tex portugueseCV.*
```

Se inline compila mas `\input` nao: caractere invisivel/BOM no inicio do arquivo de conteudo.
Confirme: `od -c portuguese.tex | head`. Limpe: `sed -i '1s/^\xEF\xBB\xBF//' portuguese.tex`
(remove BOM UTF-8) ou reescreva o arquivo via write_file.

Isolamento binario (sem adivinhar): comente secoes do fim pro inicio e recompile ate o erro sumir.
A ultima secao removida e a culpada. Teste minimo: so cabecalho (`\makecvheader`) — se ainda der
erro, o problema e no preambulo (main.tex) ou no `\personalinfo`.

## fullwidth desbalanceado (erro fatal)
`\begin{fullwidth}` sem `\end{fullwidth}` -> `! LaTeX Error: \begin{list} on input line N ended by
\end{document}`. Conte os pares `begin{fullwidth}` / `end{fullwidth}` (ignorando os comentados com
`% \begin{fullwidth}` — o grep conta a string mesmo comentada, use `grep -n "fullwidth"` e olhe o
`%`). Ao reescrever Eventos, se removeu o `\end{fullwidth}` antigo, reinsira `\end{fullwidth}`
logo antes de `\newpage`/Publicacoes.
