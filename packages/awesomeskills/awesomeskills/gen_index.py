#!/usr/bin/env python3
"""Generate a professional README.md from skills/**/SKILL.md.

Produces: hero (badges + tagline), why-multi-tool table, interactive installer guide,
per-agent installation commands, curated packs, repo structure, and a per-category index.
"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


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
    cats: dict[str, list[tuple[str, str, str]]] = {}
    for skill in sorted(skills_dir.rglob("SKILL.md")):
        rel = skill.relative_to(skills_dir)
        if len(rel.parts) >= 2:
            cat = rel.parts[0]
            fm = front_matter(skill)
            name = fm.get("name") or rel.parts[1]
            desc = fm.get("description", "").replace("|", "\\|").replace("\n", " ")
            if len(desc) > 180:
                desc = desc[:177].rstrip() + "..."
            cats.setdefault(cat, []).append((name, desc, str(rel)))

    total = sum(len(v) for v in cats.values())

    out = []
    # ---- HERO ----
    out += [
        "<div align=\"center\">",
        "",
        "# awesome-skills",
        "",
        "![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)",
        f"![Skills](https://img.shields.io/badge/skills-{total}-blue.svg)",
        f"![Categories](https://img.shields.io/badge/categories-{len(cats)}-blue.svg)",
        "![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)",
        "![Multi-Agent](https://img.shields.io/badge/Multi--Agent-AGY%20|%20Claude%20|%20Hermes%20|%20Cursor-8a2be2.svg)",
        "",
        "**Universal multi-agent library of reusable Skills, Agents & Rules.**",
        "",
        "*Write once in `SKILL.md` — run on Google Antigravity, Claude Code, Hermes Agent, Cursor, Windsurf & Cline.*",
        "",
        "</div>",
        "",
        "---",
        "",
        "## ⚡ Quick Start: Interactive Installer (Caveman-style)",
        "",
        "Install skills interactively with a TUI menu, fuzzy search, agent selector, and curated packs:",
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
        "Select your AI agent or IDE below for ready-to-run setup commands:",
        "",
        "### 🪐 Google Antigravity (AGY)",
        "",
        "```bash",
        "# Global User Skills (available in all workspaces)",
        "mkdir -p ~/.gemini/antigravity-cli/skills",
        "cp -r skills/*/* ~/.gemini/antigravity-cli/skills/",
        "",
        "# Or install into current workspace",
        "mkdir -p .agent/skills",
        "cp -r skills/<category>/<skill> .agent/skills/",
        "```",
        "",
        "### 🏛️ Hermes Agent (Nous Research)",
        "",
        "```bash",
        "# Global installation into Hermes catalog",
        "mkdir -p ~/.hermes/skills",
        "cp -r skills/* ~/.hermes/skills/",
        "",
        "# Install single category",
        "cp -r skills/devops ~/.hermes/skills/",
        "```",
        "",
        "### ⚡ Claude Code (Anthropic CLI)",
        "",
        "```bash",
        "# Global installation for Claude Code CLI",
        "mkdir -p ~/.claude/skills",
        "cp -r skills/*/* ~/.claude/skills/",
        "",
        "# Workspace installation",
        "mkdir -p .claude/skills",
        "cp -r skills/<category>/<skill> .claude/skills/",
        "```",
        "",
        "### 🎯 Cursor IDE (.mdc Rules)",
        "",
        "```bash",
        "# Automatically convert & install skills as Cursor rules (.cursor/rules/*.mdc)",
        "./install.sh --agent cursor --scope local --pack fullstack",
        "```",
        "",
        "### 🌊 Windsurf & Roo Code / Cline",
        "",
        "```bash",
        "# Windsurf Workspace Skills",
        "mkdir -p .windsurf/skills && cp -r skills/*/* .windsurf/skills/",
        "",
        "# Roo Code / Cline Skills",
        "mkdir -p ~/.roo/skills && cp -r skills/*/* ~/.roo/skills/",
        "```",
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
        "| **📦 Complete Catalog** | All 118+ skills across 19 categories | All categories | `./install.sh --pack all` |",
        "",
        "---",
        "",
        "## 🌐 Multi-Agent Architecture",
        "",
        "Every entry is a self-contained, versioned unit consumed — with thin adaptors — by the major agent runtimes:",
        "",
        "| Runtime | Loads From | Format |",
        "| :--- | :--- | :--- |",
        "| **Google Antigravity (AGY)** | `~/.gemini/antigravity-cli/skills/` or `.agent/skills/` | `SKILL.md` (native) |",
        "| **Hermes Agent** | `~/.hermes/skills/<cat>/<skill>/` | `SKILL.md` (native) |",
        "| **Claude Code** | `~/.claude/skills/<skill>/` | `SKILL.md` / `CLAUDE.md` |",
        "| **Cursor** | `.cursor/rules/<skill>.mdc` | MDC Rule with frontmatter |",
        "| **Windsurf** | `.windsurfrules` or `.windsurf/skills/` | Markdown Context |",
        "| **Roo Code / Cline** | `~/.roomodes` / `~/.roo/skills/` | `SKILL.md` (native) |",
        "| **OpenCode / Codex** | `~/.config/opencode/skills/` | Markdown Rule |",
        "",
        "> See [`templates/`](templates/) for starter kits (skill / agent / plugin).",
        "",
        "---",
        "",
        "## 🗂️ Skills Catalog Index",
        "",
        f"> **{total} skills** organized across **{len(cats)} categories**.",
        "",
    ]

    # ---- INDEX BY CATEGORY ----
    for cat in sorted(cats):
        out.append(f"### {cat}")
        out.append("")
        out.append("| Skill | Description |")
        out.append("|---|---|")
        for name, desc, rel in sorted(cats[cat]):
            out.append(f"| [`{name}`](skills/{rel}) | {desc} |")
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
        "  ├── install.sh                  # Universal interactive installer (Caveman-style)",
        "  ├── tools/",
        "  │   ├── installer.py            # TUI & CLI installation engine",
        "  │   └── gen_index.py            # Regenerates README catalog index",
        "  ├── templates/                  # Starter kits: skill / agent / plugin",
        "  ├── packages/awesomeskills/     # Python package CLI (`awesomeskills install`)",
        "  ├── docs/CODE_REVIEW.md         # Review standard",
        "  └── .github/                    # Issue & PR templates + CI workflow",
        "```",
        "",
        "---",
        "",
        "## 📊 RepoActivity",
        "",
        "[![Star History Chart](https://api.star-history.com/svg?repos=pedroiff0/awesome-skills&type=Date)](https://www.star-history.com/#pedroiff0/awesome-skills&type=Date)",
        "",
        "---",
        "",
        "## 👨‍💻 Author",
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
    print(f"Generated {readme_path} with {total} skills across {len(cats)} categories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
