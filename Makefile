.PHONY: help install validate lint test

help: ## Exibe a lista de comandos disponíveis
	@echo "Comandos disponíveis em Awesome Skills:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Dá permissão de execução ao instalador
	chmod +x install.sh

validate: ## Valida sintaxe e frontmatter de todas as skills
	python3 -c "import glob, yaml, sys; [yaml.safe_load(open(f).read().split('---')[1]) for f in glob.glob('skills/**/SKILL.md')]; print('Todas as skills são válidas!')"

lint: validate ## Executa validação de sintaxe e estrutura

test: validate ## Executa testes do catálogo
