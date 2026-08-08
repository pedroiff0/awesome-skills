# Makefile canônico — altacv CV multi-idioma com biber (awk, NÃO sed)

Este é o Makefile que corrige o bug do `\n` literal (Pitfall 16). Gera `main_<lang>.tex`
a partir de `main.tex` (remove os `\input{<lang>.tex}` originais via `grep -v` e reinsere
o `\input{<lang>}` com newline REAL via `awk`), depois roda o ciclo
`lualatex → biber → lualatex → lualatex`.

```makefile
SHELL := /bin/bash
MAIN := main.tex
LUALATEX := lualatex -interaction=nonstopmode
BIBER := biber
LANGS := portuguese english spanish french

.PHONY: all clean $(LANGS)

all: $(addsuffix CV.pdf,$(LANGS))

%CV.pdf: $(MAIN) %.tex
	@echo "Building $@..."
	@grep -v '\\input{' $(MAIN) > main_$*.tex
	@awk '/\\end\{document\}/{print "\\input{$*}"} {print}' main_$*.tex > main_$*.tex.tmp && mv main_$*.tex.tmp main_$*.tex
	$(LUALATEX) -jobname=$(basename $@) main_$*.tex
	$(BIBER) $(basename $@)
	$(LUALATEX) -jobname=$(basename $@) main_$*.tex
	$(LUALATEX) -jobname=$(basename $@) main_$*.tex
	@echo "Generated $@"
	@rm -f main_$*.tex *.aux *.log *.fdb_latexmk *.fls *.out *.toc *.synctex.gz *.run.xml *.bcf *.bbl *.blg

portuguese: portugueseCV.pdf
english: englishCV.pdf
spanish: spanishCV.pdf
french: frenchCV.pdf

clean:
	rm -f main_*.tex *.aux *.log *.fdb_latexmk *.fls *.out *.toc *.synctex.gz *.run.xml *.bcf *.bbl *.blg *CV.pdf
```

## Pontos críticos
- `awk '/\\end\{document\}/{print "\\input{$*}"} {print}'` — o `$*` é expandido pelo make
  (vira `portuguese` etc.) ANTES do shell chamar o awk. O awk imprime `\input{portuguese}`
  numa linha própria e DEPOIS reimprime a linha `\end{document}` (via `{print}`).
  NÃO use `sed 's/...\n.../'` — o `\n` vira texto literal e quebra tudo (Pitfall 16).
- O recipe usa `$(LUALATEX)` SEM `-halt-on-error`: com `-halt-on-error`, um warning vira
  erro fatal e o `.aux` não é escrito → biber vazio. `nonstopmode` continua e escreve o aux.
- Build artifacts `main_<lang>.tex` são dinâmicos — já no `.gitignore`, não versionar.

## Verificação rápida de que o biber rodou
```bash
for t in portugueseCV englishCV spanishCV frenchCV; do
  echo "$t: $(pdftotext $t.pdf - 2>/dev/null | grep -cE '\[[0-9]+\]') refs"
done
```
Se 0 em algum idioma → o primeiro lualatex quebrou (grep `undefined` no log) ou o
`\nocite{*}` está comentado e os `\cite{}` sumiram (Pitfall 17).
