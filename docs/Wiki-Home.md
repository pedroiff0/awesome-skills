# Awesome Skills — Wiki Home

Welcome to the **awesome-skills** wiki!

This is the community-maintained catalog of reusable Skills, Agents & Plugins for AI agents. Every entry is procedural memory that works across multiple runtimes from a single canonical `SKILL.md`.

## Universal Multi-Agent Interactive Installer

Install skills interactively with a TUI menu, fuzzy search, agent selector, and curated packs:

```bash
# Direct run via curl (TUI menu)
curl -fsSL https://raw.githubusercontent.com/pedroiff0/awesome-skills/main/install.sh | bash

# Or clone and run locally
git clone https://github.com/pedroiff0/awesome-skills.git
cd awesome-skills
./install.sh
```

## What's a Skill?

A **skill** is a self-contained, versioned unit of procedural memory for AI agents. Each skill lives in `skills/<category>/<name>/` and contains:

- `SKILL.md` — canonical definition (Hermes/Multi-Agent format)
- `references/` — supporting docs, API specs, examples
- `scripts/` — helper scripts, validators, generators
- `templates/` — starter kits for new skills/agents/plugins

## Multi-Tool Compatibility

Every skill is designed to work across runtimes with thin adaptors:

| Runtime | Loads From | Format |
|---|---|---|
| **Google Antigravity (AGY)** | `~/.gemini/antigravity-cli/skills/` or `.agent/skills/` | `SKILL.md` (native) |
| **Hermes Agent** | `~/.hermes/skills/<cat>/<skill>/` | `SKILL.md` (native) |
| **Claude Code** | `~/.claude/skills/<skill>/` | `SKILL.md` / `CLAUDE.md` |
| **Cursor** | `.cursor/rules/<skill>.mdc` | MDC Rule with frontmatter |
| **Windsurf** | `.windsurfrules` or `.windsurf/skills/` | Markdown Context |
| **Roo Code / Cline** | `~/.roomodes` / `~/.roo/skills/` | `SKILL.md` (native) |
| **OpenCode / Codex** | `~/.config/opencode/skills/` | Markdown Rule |

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
- [MULTI_AGENT_INSTALLER_GUIDE.md](https://github.com/pedroiff0/awesome-skills/blob/main/docs/MULTI_AGENT_INSTALLER_GUIDE.md)
