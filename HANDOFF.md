# HANDOFF — Awesome Skills

## 1. Contexto Rápido
- **Repositório:** `pedroiff0/awesome-skills` (`~/Repositorios/pessoal/awesome-skills`).
- **Função Principal:** Catálogo curado e padronizado de skills de IA, plugins, servidores MCP e extensões para Antigravity, Claude Desktop, Cursor e agentes LLM.
- **Estrutura:** `skills/` (Skills canônicas), `mcp/` (Servidores MCP), `plugins/` (Extensões), `templates/` (Scaffolding).

## 2. Arquitetura do Catálogo
- Toda skill deve possuir `SKILL.md` com YAML frontmatter válido (`name`, `description`, `version`, `author`, `license`).
- Validação automática executada via script embutido no CI.

## 3. Estado Atual & Diretrizes Operacionais
- **Governança:** AGENTS.md, DESIGN.md, Makefile e templates do GitHub ativos.
- **Comandos Principais:**
  - `make install`: Configura ferramentas locais e permissões.
  - `make validate`: Valida metadados e YAML frontmatters de todas as skills.
  - `make lint`: Verifica integridade de sintaxe.
- **Próximos Passos:**
  - Expandir suíte de MCP servers com ferramentas adicionais para automação de ambiente local.
