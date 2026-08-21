#!/usr/bin/env python3
"""Generate a professional README.md from skills/**/SKILL.md, plugins/, and mcp/.

Produces: hero (badges + tagline), why-multi-tool table, interactive installer guide,
per-agent installation commands, master skill guide, plugins & MCP catalog, curated packs,
repo structure, and a per-category index with strict author attribution.
"""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
PLUGINS = ROOT / "plugins"
MCP = ROOT / "mcp"


def front_matter(path: Path) -> dict:
    txt = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if mm:
            data[mm.group(1)] = mm.group(2).strip().strip('"').strip("'")
    return data


def main(root: Path = ROOT) -> int:
    skills_dir = root / "skills"
    cats: dict[str, list[tuple[str, str, str, str]]] = {}
    for skill in sorted(skills_dir.rglob("SKILL.md")):
        rel = skill.relative_to(skills_dir)
        if len(rel.parts) >= 2:
            cat = rel.parts[0]
            fm = front_matter(skill)
            name = fm.get("name") or rel.parts[1]
            author = fm.get("author") or "Pedro Henrique Rocha de Andrade"
            desc = fm.get("description", "").replace("|", "\\|").replace("\n", " ")
            if len(desc) > 170:
                desc = desc[:167].rstrip() + "..."
            cats.setdefault(cat, []).append((name, desc, str(rel), author))

    total_skills = sum(len(v) for v in cats.values())

    # Count plugins & MCP
    plugin_dirs = [p for p in (root / "plugins").iterdir() if p.is_dir() and not p.name.startswith(".")] if (root / "plugins").exists() else []
    mcp_dirs = [m for m in (root / "mcp").iterdir() if m.is_dir() and not m.name.startswith(".")] if (root / "mcp").exists() else []

    out = []
    # ---- HERO ----
    out += [
        "<div align=\"center\">",
        "",
        "# awesome-skills",
        "",
        "![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)",
        f"![Skills](https://img.shields.io/badge/skills-{total_skills}-blue.svg)",
        f"![Plugins](https://img.shields.io/badge/plugins-{len(plugin_dirs)}-purple.svg)",
        f"![MCP](https://img.shields.io/badge/mcp--servers-{len(mcp_dirs)}-orange.svg)",
        f"![Categories](https://img.shields.io/badge/categories-{len(cats)}-blue.svg)",
        "![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)",
        "",
        "**The Universal Multi-Agent Catalog of Skills, Plugins & Model Context Protocol (MCP) Servers.**",
        "",
        "*Write once in `SKILL.md` — run on Google Antigravity, Claude Code, Hermes Agent, Cursor, Windsurf, Roo & Codex.*",
        "",
        "</div>",
        "",
        "---",
        "",
        "## 🧭 Autonomous Agent Setup (No CLI Required)",
        "",
        "If you are an **AI Agent** (or asked an agent to clone this repository), activate the Master Skill:",
        "",
        "> 🤖 **[`awesome-skills-master`](skills/autonomous-ai-agents/awesome-skills-master/SKILL.md)** — Fully autonomous procedural guide for agents to auto-detect their host environment (AGY, Claude, Cursor, Hermes, Roo), adapt rules (`.cursor/rules/*.mdc`, `CLAUDE.md`), link skills, configure MCP servers, and preserve strict author attribution without user prompts.",
        "",
        "---",
        "",
        "## ⚡ Quick Start: Interactive Installer (Caveman-style)",
        "",
        "Install skills interactively with a terminal TUI menu, skill-by-skill live browser, author credits, and curated packs:",
        "",
        "```bash",
        "# Run directly via curl (Interactive TUI)",
        "curl -fsSL https://raw.githubusercontent.com/pedroiff0/awesome-skills/main/install.sh | bash",
        "",
        "# Or clone and run locally",
        "git clone https://github.com/pedroiff0/awesome-skills.git",
        "cd awesome-skills",
        "./install.sh",
        "```",
        "",
        "---",
        "",
        "## 🤖 Installation by Agent (Direct 1-Liners)",
        "",
        "### 🪐 Google Antigravity (AGY)",
        "",
        "```bash",
        "# Global User Skills",
        "mkdir -p ~/.gemini/antigravity-cli/skills && cp -r skills/*/* ~/.gemini/antigravity-cli/skills/",
        "# Workspace Local Skills",
        "mkdir -p .agent/skills && cp -r skills/<category>/<skill> .agent/skills/",
        "```",
        "",
        "### 🏛️ Hermes Agent (Nous Research)",
        "",
        "```bash",
        "mkdir -p ~/.hermes/skills && cp -r skills/* ~/.hermes/skills/",
        "```",
        "",
        "### ⚡ Claude Code (Anthropic CLI)",
        "",
        "```bash",
        "mkdir -p ~/.claude/skills && cp -r skills/*/* ~/.claude/skills/",
        "```",
        "",
        "### 🎯 Cursor IDE (.mdc Rules)",
        "",
        "```bash",
        "./install.sh --agent cursor --scope local --pack fullstack",
        "```",
        "",
        "### 🌊 Windsurf & Roo Code / Cline",
        "",
        "```bash",
        "mkdir -p .windsurf/skills && cp -r skills/*/* .windsurf/skills/",
        "mkdir -p ~/.roo/skills && cp -r skills/*/* ~/.roo/skills/",
        "```",
        "",
        "---",
        "",
        "## 🔌 Model Context Protocol (MCP) & Plugins",
        "",
        "| Component | Description | Config Location |",
        "| :--- | :--- | :--- |",
        "| **[`mcp/context-mode`](mcp/context-mode)** | AST indexed search & token compression server | `mcp/context-mode/mcp.json` |",
        "| **[`mcp/sqlite-explorer`](mcp/sqlite-explorer)** | SQLite schema analysis & SQL executor | `mcp/sqlite-explorer/mcp.json` |",
        "| **[`mcp/puppeteer-browser`](mcp/puppeteer-browser)** | Headless browser rendering & screenshots | `mcp/puppeteer-browser/mcp.json` |",
        "| **[`mcp/filesystem-pro`](mcp/filesystem-pro)** | Granular scoped filesystem permissions | `mcp/filesystem-pro/mcp.json` |",
        "| **[`plugins/auto-git-checkpoint`](plugins/auto-git-checkpoint)** | Pre/post task automatic git atomic commits | `plugins/auto-git-checkpoint/plugin.json` |",
        "| **[`plugins/token-guardian`](plugins/token-guardian)** | Turn-by-turn context burn monitor | `plugins/token-guardian/plugin.json` |",
        "",
        "---",
        "",
        "## 📦 Curated Packs",
        "",
        "| Pack | Focus | Key Categories | Install Command |",
        "| :--- | :--- | :--- | :--- |",
        "| **🚀 Full-Stack Dev** | Web, APIs, Testing, Refactoring | `software-development`, `web`, `github` | `./install.sh --pack fullstack` |",
        "| **⚡ DevOps & Cloud** | Containers, Caddy, Cloudflare, CI/CD | `devops`, `github` | `./install.sh --pack devops` |",
        "| **🧠 Autonomous AI & MLOps** | Multi-Agent topologies, RAG, Token ops | `autonomous-ai-agents`, `mlops` | `./install.sh --pack ai` |",
        "| **📚 Academic & LaTeX** | Paper writing, LaTeX CVs, arXiv, i18n | `latex`, `research`, `content-i18n` | `./install.sh --pack academic` |",
        "| **🎨 Creative & Media** | Architecture diagrams, ASCII, Audio | `creative`, `media`, `desktop` | `./install.sh --pack creative` |",
        "| **📦 Complete Catalog** | All 124+ skills across 19 categories | All categories | `./install.sh --pack all` |",
        "",
        "---",
        "",
        "## 🗂️ Skills Catalog Index",
        "",
        f"> **{total_skills} skills** organized across **{len(cats)} categories** with strict attribution.",
        "",
    ]

    # ---- INDEX BY CATEGORY ----
    for cat in sorted(cats):
        out.append(f"### {cat}")
        out.append("")
        out.append("| Skill | Description | Author / Credits |")
        out.append("|---|---|---|")
        for name, desc, rel, author in sorted(cats[cat]):
            out.append(f"| [`{name}`](skills/{rel}) | {desc} | {author} |")
        out.append("")

    # ---- REPO STRUCTURE ----
    out += [
        "---",
        "",
        "## 📂 Repository Structure",
        "",
        "```",
        "awesome-skills/",
        "  ├── skills/<category>/<name>/   # Canonical SKILL.md + references/ + scripts/",
        "  ├── plugins/<name>/             # Reusable agent plugins & lifecycle hooks",
        "  ├── mcp/<name>/                 # Model Context Protocol (MCP) server definitions",
        "  ├── install.sh                  # Universal interactive installer (Caveman-style)",
        "  ├── tools/",
        "  │   ├── installer.py            # TUI & CLI installation engine",
        "  │   └── gen_index.py            # Regenerates README catalog index",
        "  ├── templates/                  # Starter kits: skill / agent / plugin / mcp",
        "  ├── packages/awesomeskills/     # Python package CLI (`awesomeskills install`)",
        "  ├── docs/CODE_REVIEW.md         # Review standard",
        "  └── .github/                    # Issue & PR templates + CI workflow",
        "```",
        "",
        "---",
        "",
        "## ⚖️ Author Credits & Attribution Standards",
        "",
        "awesome-skills strictly credits all original authors, community projects, and research creators:",
        "- **Anthropic & skills.sh Ecosystem**: Frontend design, tool calling specifications, and Claude skills.",
        "- **Nous Research**: Hermes Agent architecture, agent templates, and core skills.",
        "- **Matt Pocock**: `grill-me`, `grill-with-docs` requirement interview architectures.",
        "- **Vercel Labs**: `skills.sh` registry and discovery patterns.",
        "- **Guillaume Meyer**: `watermarks-remover` AI provenance hygiene tooling.",
        "- **Pedro Henrique Rocha de Andrade**: Architecture, catalog curation, Antigravity ecosystem, multi-agent installer, and DevOps skills.",
        "",
        "---",
        "",
        "## 📊 RepoActivity",
        "",
        "[![Star History Chart](https://api.star-history.com/svg?repos=pedroiff0/awesome-skills&type=Date)](https://www.star-history.com/#pedroiff0/awesome-skills&type=Date)",
        "",
        "---",
        "",
        "## 👨‍💻 Author & Maintainer",
        "",
        "<div align=\"center\">",
        "",
        "<img src=\"https://raw.githubusercontent.com/pedroiff0/pedroiff0/main/assets/pedroiff0.gif\" alt=\"pedroiff0\" width=\"900\"/>",
        "",
        "</div>",
        "",
        "<div align=\"center\">",
        "",
        "**2026 Awesome Skills**",
        "",
        "Made with ☕, code and ☄️ by **Pedro Henrique Rocha de Andrade**",
        "",
        "[![GitHub](https://img.shields.io/badge/GitHub-pedroiff0-181717?logo=github&logoColor=white)](https://github.com/pedroiff0)",
        "[![Site Oficial](https://img.shields.io/badge/Site-Oficial-22c55e?logo=googlechrome&logoColor=white)](https://phrandrade.com/)",
        "[![Portfólio](https://img.shields.io/badge/Portfólio-2563eb?logo=github&logoColor=white)](https://pedroiff0.github.io/webpage/)",
        "[![LinkedIn](https://img.shields.io/badge/LinkedIn-Pedro_Rocha-0077b5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedro-rocha-de-andrade)",
        "",
        "</div>",
        "",
    ]

    readme_path = root / "README.md"
    readme_path.write_text("\n".join(out), encoding="utf-8")
    print(f"Generated {readme_path} with {total_skills} skills, {len(plugin_dirs)} plugins, {len(mcp_dirs)} MCP servers across {len(cats)} categories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
