# Awesome Skills — Wiki Home

Welcome to the **awesome-skills** wiki!

This is the community-maintained catalog of reusable Skills, Agents & Plugins for AI agents. Every entry is procedural memory that works across multiple runtimes from a single canonical `SKILL.md`.

## Getting Started

```bash
git clone https://github.com/pedroiff0/awesome-skills.git

# install the whole catalog into Hermes
cp -r awesome-skills/skills/* ~/.hermes/skills/

# or just one skill
cp -r awesome-skills/skills/<category>/<skill> ~/.hermes/skills/<category>/
```

## What's a Skill?

A **skill** is a self-contained, versioned unit of procedural memory for AI agents. Each skill lives in `skills/<category>/<name>/` and contains:

- `SKILL.md` — canonical definition (Hermes format)
- `references/` — supporting docs, API specs, examples
- `scripts/` — helper scripts, validators, generators
- `templates/` — starter kits for new skills/agents/plugins

## Multi-Tool Compatibility

Every skill is designed to work across runtimes with thin adaptors:

| Runtime | Loads |
|---|---|
| **Hermes Agent** | `SKILL.md` → `~/.hermes/skills/` |
| **Claude Code / Claude.ai** | `SKILL.md` / `CLAUDE.md` |
| **Cursor** | `.cursor/rules/*.mdc` |
| **Windsurf** | `.windsurfrules` / `skills/*.md` |
| **OpenClaw / Roo / Cline / AGY** | `SKILL.md` / `manifest.json` |

## Contributing

1. Branch from `main` (`feat/...`, `fix/...`, `docs/...`, `chore/...`).
2. Follow `templates/` for new skills/agents/plugins.
3. Run `python3 tools/gen_index.py` to regenerate the README.
4. Open a PR with all seven standard assignment fields.

See [CONTRIBUTING.md](https://github.com/pedroiff0/awesome-skills/blob/main/CONTRIBUTING.md) for the full standard.

## Governance

- [CODE_OF_CONDUCT.md](https://github.com/pedroiff0/awesome-skills/blob/main/CODE_OF_CONDUCT.md)
- [SECURITY.md](https://github.com/pedroiff0/awesome-skills/blob/main/SECURITY.md)
- [AGENTS.md](https://github.com/pedroiff0/awesome-skills/blob/main/AGENTS.md)

## Categories

Skills are organized by domain:

- **apple** — macOS integrations (Notes, Reminders, iMessage, FindMy)
- **autonomous-ai-agents** — Claude Code, Codex, OpenCode, Hermes
- **content-i18n** — Markdown translation, localization
- **creative** — ASCII art, diagrams, design, video, music
- **data-science** — Jupyter, SUAP API
- **desktop** — Linux desktop theming
- **devops** — Docker, multi-instance
- **email** — Himalaya CLI
- **geral** — Portfolio, LaTeX, Markdown sites, static sites
- **github** — Auth, issues, PRs, code review, profile README
- **latex** — CV maintenance, multilingual
- **media** — GIF search, audio, YouTube
- **mlops** — GPU setup, HuggingFace, LLMs, evaluation
- **note-taking** — Obsidian
- **productivity** — Airtable, Google Workspace, Notion, PowerPoint
- **research** — arXiv, blogwatcher, Polymarket
- **smart-home** — OpenHue
- **social-media** — X/Twitter
- **software-development** — Debugging, TDD, Docker, financas-app
- **web** — CSP, visual verification, GitHub Pages

## Releases

See [CHANGELOG.md](https://github.com/pedroiff0/awesome-skills/blob/main/CHANGELOG.md) for the release history.

## License

This project is licensed under the **MIT License**. See [LICENSE](https://github.com/pedroiff0/awesome-skills/blob/main/LICENSE).
