#!/usr/bin/env python3
"""Regenerate README.md with an automated catalog index of skills, plugins, and MCP servers.

Supports:
- OS Compatibility Matrix with Auto-Detection status.
- Sponsor and Support section.
- Open Contributions guideline.
- Open Source repository author attribution.
- Enriched categorization and statistics.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


def parse_frontmatter(file_path: Path) -> dict[str, str]:
    content = file_path.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.S)
    if not match:
        return {}
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if m:
            meta[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return meta


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    plugins_dir = root / "plugins"
    mcp_dir = root / "mcp"

    cats: dict[str, list[tuple[str, str, str, str]]] = defaultdict(list)
    total_skills = 0

    for skill_file in sorted(skills_dir.rglob("SKILL.md")):
        rel = skill_file.relative_to(skills_dir)
        if len(rel.parts) < 2:
            continue
        cat = rel.parts[0]
        name = rel.parts[1]
        fm = parse_frontmatter(skill_file)
        desc = fm.get("description", "").strip()
        if len(desc) > 170:
            desc = desc[:167] + "..."
        author = fm.get("author", "Open Source Community").strip()
        cats[cat].append((name, desc, f"{cat}/{name}/SKILL.md", author))
        total_skills += 1

    # Plugins
    plugin_dirs = [p for p in sorted(plugins_dir.glob("*")) if p.is_dir()] if plugins_dir.exists() else []
    # MCP
    mcp_dirs = [m for m in sorted(mcp_dir.glob("*")) if m.is_dir()] if mcp_dir.exists() else []

    out = [
        "# 🪐 awesome-skills",
        "",
        '<div align="center">',
        "",
        "![Awesome Skills Banner](assets/banner.svg)",
        "",
        "**The Universal, Community-Maintained Catalog of Procedural AI Agent Skills, MCP Servers & Plugins.**",
        "",
        "*Write once in canonical `SKILL.md` — Equip instantly across Google Antigravity, Hermes Agent, Claude Code, Cursor, Windsurf, Roo/Cline & OpenCode.*",
        "",
        "[![CI](https://github.com/pedroiff0/awesome-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/pedroiff0/awesome-skills/actions/workflows/ci.yml)",
        f"![Skills Count](https://img.shields.io/badge/Skills-{total_skills}-blueviolet?style=flat-square&logo=speedtest&logoColor=white)",
        f"![Plugins Count](https://img.shields.io/badge/Plugins-{len(plugin_dirs)}-purple?style=flat-square&logo=puzzle&logoColor=white)",
        f"![MCP Servers](https://img.shields.io/badge/MCP_Servers-{len(mcp_dirs)}-indigo?style=flat-square&logo=server&logoColor=white)",
        "![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-blue?style=flat-square&logo=linux&logoColor=white)",
        "![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)",
        "[![Sponsor](https://img.shields.io/badge/Sponsor-Open_for_Sponsors-ea4aaa?style=flat-square&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/pedroiff0)",
        "",
        "</div>",
        "",
        "---",
        "",
        "## ☕ Quick Cosmic Install (One-Liner)",
        "",
        "Equip your AI agents instantly using our interactive TUI installer:",
        "",
        "```bash",
        "curl -fsSL https://raw.githubusercontent.com/pedroiff0/awesome-skills/main/install.sh | bash",
        "```",
        "",
        "Or install and manage via the dedicated Python CLI:",
        "",
        "```bash",
        "pip install awesomeskills",
        "awesomeskills install",
        "```",
        "",
        "---",
        "",
        "## 🖥️ Operating System Support & Auto-Detection",
        "",
        "The installer automatically detects your operating system and dynamically configures agent target directories, symlinks, and file copy strategies:",
        "",
        "| Operating System | Tier / Support Status | Auto-Detection Mechanism | Target Paths Adapted |",
        "| :--- | :--- | :--- | :--- |",
        "| 🐧 **Linux (Ubuntu, Debian, Arch, Fedora, etc.)** | 🟢 **Tier 1 (Primary & Fully Verified)** | Native POSIX & Linux syscalls | `~/.gemini`, `~/.claude`, `~/.hermes`, `~/.cursor` |",
        "| 🍎 **macOS (Darwin / Apple Silicon & Intel)** | 🟡 **Supported (Paths Adapted)** | `platform.system() == 'Darwin'` | `~/Library/Application Support/...` + dotfiles |",
        "| 🪟 **Windows (WSL / Native / PowerShell)** | 🟡 **Supported (Paths Adapted / WSL Recommended)** | Detects Windows/NT + `%APPDATA%` | `%USERPROFILE%\\...`, `%APPDATA%\\...` (copy fallback) |",
        "",
        "> **Note**: Linux is our primary verified development and testing platform. On macOS and Windows, paths and symlink fallbacks are auto-configured. For Windows users, running inside **WSL (Windows Subsystem for Linux)** is highly recommended.",
        "",
        "---",
        "",
        "## 🌐 Ecosystem Highlights",
        "",
        "- 🎯 **[Explore Open-Source Repositories](references/open-source-repos.md)**: Curated top-starred GitHub projects (100k+ ⭐) enriched via [OpenCurious](https://www.opencurious.com/explore-open-source).",
        "- 🦙 **[Local Ollama Models Catalog](references/ollama-models.md)**: 4 hardware tiers from lightweight (0.5B) to datacenter flagships (70B+) with direct library links.",
        "- 🧩 **[Plugins Directory](plugins/)**: Reusable lifecycle hooks and agent extensions.",
        "- 🔌 **[MCP Servers](mcp/)**: Model Context Protocol servers for enhanced database, filesystem, and context capabilities.",
        "",
        "---",
        "",
        "## 📚 Skills Catalog Index",
        "",
    ]

    for cat in sorted(cats.keys()):
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
        "  ├── install.sh                  # Universal interactive installer with OS detection",
        "  ├── tools/",
        "  │   ├── installer.py            # TUI & CLI installation engine (with OS detector)",
        "  │   └── gen_index.py            # Regenerates README catalog index",
        "  ├── references/                 # Open-Source repositories & Ollama models registries",
        "  ├── templates/                  # Starter kits: skill / agent / plugin / mcp",
        "  ├── packages/awesomeskills/     # Python package CLI (`awesomeskills install`)",
        "  ├── docs/CODE_REVIEW.md         # Review standard",
        "  └── .github/                    # Issue & PR templates + CI workflow",
        "```",
        "",
        "---",
        "",
        "## 💖 Sponsor & Support",
        "",
        "Maintaining and expanding the largest universal multi-agent skills catalog requires continuous testing across model APIs, local hardware benchmarks, and community curation.",
        "",
        "If **awesome-skills** helps accelerate your AI coding workflows, consider sponsoring the project:",
        "",
        "<div align=\"center\">",
        "",
        "[![GitHub Sponsors](https://img.shields.io/badge/Sponsor_on-GitHub_Sponsors-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/pedroiff0)",
        "",
        "*Your sponsorship helps fund open-weight model testing, server infrastructure, and daily catalog expansion.*",
        "",
        "</div>",
        "",
        "---",
        "",
        "## 🤝 Contributing & Submissions",
        "",
        "Contributions are warmly welcomed from the entire open-source community!",
        "",
        "- 💡 **Add New Skills**: Submit a PR following `templates/skill/SKILL.md`.",
        "- 🔌 **Add Plugins / MCP**: Provide structured definitions in `plugins/` or `mcp/`.",
        "- 🌐 **Translations & Fixes**: Enhance documentation, multi-OS support, and model catalogs.",
        "",
        "Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/CODE_REVIEW.md](docs/CODE_REVIEW.md) before submitting.",
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
        "- **Open Source Community**: Open-source tools, Playwright, Pandas, Next.js, Docker, LaTeX, and Linux ecosystem skills.",
        "- **Pedro Henrique Rocha de Andrade**: Repository architecture, catalog curation, and universal multi-agent installer.",
        "",
        "---",
        "",
        "## 📊 RepoActivity",
        "",
        "[![Star History Chart](https://api.star-history.com/svg?repos=pedroiff0/awesome-skills&type=Date)](https://www.star-history.com/#pedroiff0/awesome-skills&type=Date)",
        "",
        "---",
        "",
        "## 👨‍💻 Maintainer & Curator",
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
        "Curated with ☕, code and ☄️ by **Pedro Henrique Rocha de Andrade**",
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
