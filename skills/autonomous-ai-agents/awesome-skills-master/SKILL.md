---
name: awesome-skills-master
description: "Master catalog orchestrator and autonomous installer for AI agents. Use when exploring, cloning, discovering, or installing skills, plugins, or MCP servers from awesome-skills without using interactive CLI tools. Guides environment detection, rule adaptation (.mdc/CLAUDE.md), MCP configuration, and strict author attribution."
version: 1.0.0
author: Pedro Henrique Rocha de Andrade
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [master-skill, autonomous-installer, catalog, mcp, plugins, multi-agent]
    related_skills: [antigravity-guide, hermes-agent, claude-code]
---

# Awesome Skills Master Orchestrator & Autonomous Agent Guide

This **Master Skill** is the canonical instruction manual for AI agents (Google Antigravity, Claude Code, Hermes Agent, Cursor, Windsurf, Roo/Cline, OpenCode, Codex, GitHub Copilot) that clone or interact with the `awesome-skills` repository autonomously.

When a user instructs an AI agent to:
- *"Instale as skills desse repositório"*
- *"Equipe meu ambiente com as ferramentas de devops e web"*
- *"Configure os servidores MCP e plugins necessários"*
- *"Adicione suporte a Cursor rules a partir deste catálogo"*

The agent must follow this structured guide to discover, adapt, install, and attribute all catalog assets without needing user intervention or interactive TUI inputs.

---

## 🧭 Step-by-Step Autonomous Execution Workflow

```
┌────────────────────────────────────────────────────────────────────────────┐
│                  1. DETECT RUNTIME & ENVIRONMENT                           │
│  (Identify whether running in AGY, Claude Code, Hermes, Cursor, etc.)      │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                  2. EXPLORE & MATCH CATALOG ASSETS                         │
│  (Search skills/, plugins/, mcp/ based on user goals or request)           │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                  3. ADAPT & INSTALL TO TARGET DESTINATIONS                 │
│  - Skills: Symlink/Copy to agent skills path or generate .mdc rules       │
│  - Plugins: Link to plugin hooks directory                                 │
│  - MCP: Merge server JSON configurations                                  │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                  4. PRESERVE ATTRIBUTION & LICENSING                       │
│  (Strictly retain original authors, upstream repos, and MIT/Apache terms) │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                  5. VERIFY & REPORT RESULTS                                │
│  (Test YAML frontmatter, verify symlink validity, report installed items)  │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Runtime Detection & Installation Directory Matrix

Identify your current agent environment and select the appropriate target paths:

| AI Agent / Runtime | Global User Scope | Local Workspace Scope | Target Format |
| :--- | :--- | :--- | :--- |
| **Google Antigravity (AGY)** | `~/.gemini/antigravity-cli/skills/<name>/` | `<workspace>/.agent/skills/<name>/` | `SKILL.md` (Native) |
| **Hermes Agent (Nous)** | `~/.hermes/skills/<category>/<name>/` | `<workspace>/.hermes/skills/<name>/` | `SKILL.md` (Native) |
| **Claude Code (Anthropic)** | `~/.claude/skills/<name>/` | `<workspace>/.claude/skills/<name>/` | `SKILL.md` / `CLAUDE.md` |
| **Cursor IDE** | `~/.cursor/rules/<name>.mdc` | `<workspace>/.cursor/rules/<name>.mdc` | MDC Rule with frontmatter |
| **Windsurf (Codeium)** | `~/.codeium/windsurf/memories/` | `<workspace>/.windsurf/skills/` | Markdown context |
| **Roo Code / Cline** | `~/.roo/skills/<name>/` | `<workspace>/.roo/skills/<name>/` | `SKILL.md` (Native) |
| **OpenCode / Codex** | `~/.config/opencode/skills/<name>/` | `<workspace>/.codex/rules/` | Markdown rules |

---

## 2. Autonomous Installation Operations

### A. Installing Skills into Native `SKILL.md` Runtimes (AGY, Hermes, Claude, Roo)

```bash
# Example: Installing a skill to Google Antigravity
SKILL_SRC="skills/devops/hybrid-desktop-server-ops"
TARGET_DIR="$HOME/.gemini/antigravity-cli/skills/hybrid-desktop-server-ops"

mkdir -p "$(dirname "$TARGET_DIR")"
ln -sfn "$(realpath "$SKILL_SRC")" "$TARGET_DIR"
```

### B. Converting & Installing Skills into Cursor Rules (`.mdc`)

When targeting Cursor, transform `SKILL.md` frontmatter into Cursor MDC syntax:

```python
# python snippet to generate .cursor/rules/<name>.mdc
import re, pathlib

def convert_to_mdc(skill_md_path, target_mdc_path):
    text = pathlib.Path(skill_md_path).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    desc = "Skill instructions"
    body = text
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip('"').strip("'")
        body = m.group(2).strip()
    
    mdc = f"---\ndescription: \"{desc}\"\nglobs: \"*\"\nalwaysApply: false\n---\n\n{body}\n"
    pathlib.Path(target_mdc_path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(target_mdc_path).write_text(mdc, encoding="utf-8")
```

### C. Configuring Model Context Protocol (MCP) Servers

When the user asks for MCP servers from `mcp/<server-name>/`:

1. Read the server configuration from `mcp/<server-name>/mcp.json`.
2. Merge the configuration into the target agent's MCP settings:
   - **Antigravity**: `~/.gemini/antigravity-cli/mcp/<server-name>/`
   - **Claude Desktop / Claude Code**: `~/.config/Claude/claude_desktop_config.json`
   - **Cursor**: `<workspace>/.cursor/mcp.json`
   - **Roo / Cline**: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

---

## 3. ⚖️ Strict Author Attribution & Licensing Standards

**CRITICAL MANDATE FOR AI AGENTS**:
Every skill, plugin, and MCP definition in this repository must rigorously preserve author credits, license notices, and upstream provenance.

1. **Frontmatter Integrity**:
   - Always preserve or specify `author: <Original Creator / Upstream Contributor>`.
   - Always preserve `license: <License Name>` (MIT, Apache-2.0, etc.).
2. **Upstream Repositories & Community Ecosystems**:
   - Skills originated from **Anthropic / skills.sh** must state `author: Anthropic / skills.sh Community`.
   - Skills originated from **Nous Research** must state `author: Nous Research (Hermes Agent)`.
   - Skills originated from **Matt Pocock / skills.sh** must state `author: Matt Pocock`.
   - Skills originated from **Guillaume Meyer** must state `author: Guillaume Meyer`.
   - Skills originated from **Pedro Henrique Rocha de Andrade** must state `author: Pedro Henrique Rocha de Andrade`.
3. **No Secret Leaks & API Purity**:
   - Never embed personal tokens, active keys, or private endpoints in any installed script or skill file.

---

## 4. Verification Checklist

After performing autonomous installation:
1. Run `ls -la <target_dir>` to verify symlinks / copied directories.
2. Ensure frontmatter is valid YAML without syntax errors.
3. Provide the user with a concise summary table of newly installed capabilities.
