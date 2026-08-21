# 📖 Multi-Agent Skills Installer Guide

The **awesome-skills** catalog features a universal, interactive installer inspired by modern package managers (like Caveman, Gum, and npm). It allows developers and AI engineers to install skills across multiple AI agent runtimes seamlessly.

---

## 🚀 Quick Start

### Interactive Terminal TUI Mode

Run directly from any machine without cloning:

```bash
curl -fsSL https://raw.githubusercontent.com/pedroiff0/awesome-skills/main/install.sh | bash
```

Or from a local clone:

```bash
git clone https://github.com/pedroiff0/awesome-skills.git
cd awesome-skills
./install.sh
```

---

## 🤖 Supported Agents & Routing

The installer automatically recognizes the appropriate target directory and configuration format for each runtime:

| Agent / IDE | Global Path | Workspace Local Path | Installation Format |
| :--- | :--- | :--- | :--- |
| **Google Antigravity (AGY)** | `~/.gemini/antigravity-cli/skills/` | `.agent/skills/` | `SKILL.md` (Native) |
| **Hermes Agent (Nous)** | `~/.hermes/skills/<category>/` | `.hermes/skills/` | `SKILL.md` (Categorized) |
| **Claude Code (Anthropic)** | `~/.claude/skills/` | `.claude/skills/` | `SKILL.md` / `CLAUDE.md` |
| **Cursor IDE** | `~/.cursor/rules/` | `.cursor/rules/` | `.mdc` Rule format |
| **Windsurf (Codeium)** | `~/.codeium/windsurf/memories/` | `.windsurf/skills/` | Context Markdown |
| **Roo Code / Cline** | `~/.roo/skills/` | `.roo/skills/` | `SKILL.md` (Native) |
| **OpenCode / Codex** | `~/.config/opencode/skills/` | `.codex/rules/` | Context Markdown |

---

## 📦 Curated Skill Packs

You can select a curated pack to get started quickly with the most essential tools:

| Pack Flag | Pack Name | Focus & Included Categories |
| :--- | :--- | :--- |
| `--pack fullstack` | **🚀 Full-Stack & Developer Essentials** | `software-development`, `web`, `github` |
| `--pack devops` | **⚡ DevOps, Docker & Cloud Infrastructure** | `devops`, `github` |
| `--pack ai` | **🧠 Autonomous AI Agents & MLOps** | `autonomous-ai-agents`, `mlops` |
| `--pack academic` | **📚 Academic, LaTeX & Research** | `latex`, `research`, `content-i18n` |
| `--pack creative` | **🎨 Creative, Media & Design** | `creative`, `media`, `desktop` |
| `--pack all` | **📦 Complete Catalog** | All 118+ skills across 19 categories |

---

## 💻 Non-Interactive CLI Automation (CI/CD & Dotfiles)

You can script skill installation directly using command-line arguments:

```bash
# 1. Install Full-Stack pack for Google Antigravity & Claude Code globally
./install.sh --agent agy,claude --pack fullstack --symlink

# 2. Convert and install all DevOps skills as Cursor IDE rules locally
./install.sh --agent cursor --scope local --category devops

# 3. Install specific skills by name
./install.sh --agent hermes --skills hybrid-desktop-server-ops,financas-app

# 4. List all available skills and descriptions in terminal
./install.sh --list
```

---

## 🔗 Symlink vs Hard Copy

- **Symlinks (`--symlink`, default)**: Creates symbolic links pointing to your clone of `awesome-skills`. Whenever you run `git pull` in the repository, all your installed skills across all agents are updated automatically.
- **Hard Copy (`--copy`)**: Creates independent file snapshots in the target directories without linking back to the repository.
