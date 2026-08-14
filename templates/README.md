# awesome-skills — Templates de Skill / Agent / Plugin (multi-tool)

Este diretório contém **templates de fósforo** (starter kits) para você criar
habilidades que funcionam em múltiplos agentes de IA, não só no Hermes.

## Por que multi-tool?

A comunicação entre agentes de IA está convergindo em **poucos formatos de
instrução legível por máquina**. Um único `SKILL.md` bem escrito já é consumido,
com pequenos ajustes, por:

| Ferramenta | Formato aceito | Onde colocar |
|---|---|---|
| **Hermes Agent** | `SKILL.md` (frontmatter YAML + corpo) | `~/.hermes/skills/<cat>/<nome>/` |
| **Claude Code / Claude.ai** | `CLAUDE.md` ou `SKILL.md` (estilo Anthropic) | `.claude/skills/` ou repo |
| **Cursor** | `.cursor/rules/*.mdc` ou `@include` de md | `.cursor/rules/` |
| **Windsurf** | `.windsurfrules` ou `skills/*.md` | `.windsurf/` |
| **OpenClaw / Roo / Cline** | `SKILL.md` / `AGENT.md` | config do agente |
| **AGY** e derivados | `SKILL.md` / manifesto JSON | conforme o loader |

> Princípio: **escreva uma vez em `SKILL.md`** (formato canônico), e forneça
> adaptadores mínimos (`CLAUDE.md`, `.mdc`, manifesto) que apenas re-referenciam
> ou traduzem o conteúdo. Não duplique lógica.

## Estrutura de uma skill multi-tool

```
minha-skill/
  SKILL.md            # canônico (Hermes + compatíveis que leem SKILL.md)
  CLAUDE.md           # adaptador p/ Claude (pode ser só um include/resumo)
  CONVENTIONS.md      # regras que valem p/ todos os loaders
  references/         # markdown de apoio (não executável)
  scripts/            # scripts reutilizáveis (python/bash)
  templates/          # arquivos copiáveis
  manifest.json       # metadados p/ loaders que exigem JSON (AGY, etc.)
  README.md           # como instalar em cada ferramenta
```

## Como usar os templates desta pasta

- `skill-template/` — starter de skill canônica.
- `agent-template/` — starter de agent definition (system prompt + tools + restrições).
- `plugin-template/` — starter de plugin (hooks/commands/ferramentas estendidas).

Copie a pasta desejada, renomeie, edite o `SKILL.md`, e siga o `README.md`
dentro de cada um para publicar em cada ferramenta.

## Regras de ouro (compartilháveis)

1. **Frontmatter versionado** — `version: X.Y.Z` em todo `SKILL.md`.
2. **Sem segredos** — tokens vão em `.env` / secret store, nunca no corpo.
3. **Idempotente** — scripts podem rodar mais de uma vez sem quebrar.
4. **Verificável** — inclua um modo de checagem (lint/test) ou descreva o blocker.
5. **Triggers explícitos** — diga em que frases a skill deve disparar.
6. **KISS/DRY** — instrução enxuta, exemplos concretos, sem ruído.
