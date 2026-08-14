# awesome-skills — Wiki (conteúdo de fallback)

> Esta página espelha o conteúdo planejado para a Wiki do GitHub.
> A aba Wiki está habilitada; o GitHub provisiona o repo `*.wiki.git` no
> primeiro edit via UI. Até lá, use este arquivo como referência.

## Visão rápida

- Repositório: [README](../README.md)
- Como contribuir: [CONTRIBUTING](../CONTRIBUTING.md)
- Padrão de revisão: [docs/CODE_REVIEW.md](../docs/CODE_REVIEW.md)
- Templates multi-tool: [templates/](../templates/)

## Como usar as skills

1. Clone o repo.
2. Copie `skills/<categoria>/<nome>` para `~/.hermes/skills/`.
3. Rode `python3 tools/gen_index.py` após alterações.

## FAQ

**Posso usar em outro agente além do Hermes?**
Sim — `SKILL.md` é canônico; adaptadores (`CLAUDE.md`, `manifest.json`) traduzem
para Claude/Cursor/Windsurf/OpenClaw/AGY.
