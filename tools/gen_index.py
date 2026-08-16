#!/usr/bin/env python3
"""Generate a professional README.md from skills/**/SKILL.md.

Produces: hero (badges + tagline), why-multi-tool table, quick start,
repo structure, contribution standard, and a per-category index.
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


def main() -> int:
    cats: dict[str, list[tuple[str, str, str]]] = {}
    for skill in sorted(SKILLS.rglob("SKILL.md")):
        rel = skill.relative_to(SKILLS)
        cat = str(rel.parent.parent) if len(rel.parts) > 2 else "geral"
        fm = front_matter(skill)
        name = fm.get("name") or rel.parent.name
        desc = fm.get("description", "").replace("|", "\\|")
        if len(desc) > 200:
            desc = desc[:197].rstrip() + "..."
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
        "![Skills](https://img.shields.io/badge/skills-" + str(total) + "-blue.svg)",
        "![Categories](https://img.shields.io/badge/categories-" + str(len(cats)) + "-blue.svg)",
        "![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)",
        "![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)",
        "",
        "**Enterprise-grade library of reusable Skills, Agents & Plugins for AI agents.**",
        "",
        "*Write once in `SKILL.md` — run everywhere.*",
        "</div>",
        "",
        "---",
        "",
        "## Why multi-tool?",
        "",
        "Every entry is a self-contained, versioned unit consumed — with thin",
        "adaptors — by the major agent runtimes:",
        "",
        "| Runtime | Loads |",
        "|---|---|",
        "| **Hermes Agent** | `SKILL.md` → `~/.hermes/skills/` |",
        "| **Claude Code / Claude.ai** | `SKILL.md` / `CLAUDE.md` |",
        "| **Cursor** | `.cursor/rules/*.mdc` |",
        "| **Windsurf** | `.windsurfrules` / `skills/*.md` |",
        "| **OpenClaw / Roo / Cline / AGY** | `SKILL.md` / `manifest.json` |",
        "",
        "> See [`templates/`](templates/) for starter kits (skill / agent / plugin).",
        "",
        "## Quick start",
        "",
        "```bash",
        "git clone https://github.com/pedroiff0/awesome-skills.git",
        "",
        "# install the whole catalog into Hermes",
        "cp -r awesome-skills/skills/* ~/.hermes/skills/",
        "",
        "# or just one skill",
        "cp -r awesome-skills/skills/<category>/<skill> ~/.hermes/skills/<category>/",
        "```",
        "",
        "## Repository structure",
        "",
        "```",
        "awesome-skills/",
        "  skills/<category>/<name>/   # SKILL.md + references/ + scripts/",
        "  templates/                  # starter kits: skill / agent / plugin",
        "  docs/CODE_REVIEW.md         # review standard",
        "  tools/gen_index.py          # regenerates this index",
        "  .github/                    # ISSUE_TEMPLATE + PULL_REQUEST_TEMPLATE",
        "  CONTRIBUTING.md  SECURITY.md  CODE_OF_CONDUCT.md  LICENSE",
        "```",
        "",
        "## Standard workflow",
        "",
        "Every issue & PR uses the **seven standard assignment fields**",
        "(Assignee, Reviewer, Labels, Project, Milestone, Development, Relationship)",
        "via the templates in `.github/`. Reviews follow",
        "[`docs/CODE_REVIEW.md`](docs/CODE_REVIEW.md). Full standard in",
        "[`CONTRIBUTING.md`](CONTRIBUTING.md).",
        "",
        "## Index",
        "",
        f"> **{total} skills** across **{len(cats)} categories**.",
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

    # ---- REPOACTIVITY ----
    out += [
        "---",
        "",
        "## 📊 RepoActivity",
        "",
        "[![Star History Chart](https://star-history.dera.page/svg?repos=pedroiff0/awesome-skills&type=date&legend=top-left)](https://star-history.dera.page/#pedroiff0/awesome-skills&type=date&legend=top-left)",
        "",
        "---",
        "",
        "## 👨‍💻 Autor",
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
        "Feito com ☕, código e ☄️ por **Pedro Henrique Rocha de Andrade**",
        "",
        "[![GitHub](https://img.shields.io/badge/GitHub-pedroiff0-181717?logo=github&logoColor=white)](https://github.com/pedroiff0)",
        "[![Site Oficial](https://img.shields.io/badge/Site-Oficial-22c55e?logo=googlechrome&logoColor=white)](https://phrandrade.com/)",
        "[![Portfólio](https://img.shields.io/badge/Portfólio-2563eb?logo=github&logoColor=white)](https://pedroiff0.github.io/webpage/)",
        "",
        "</div>",
        "",
    ]

    # ---- CONTRIBUTING ----
    out += [
        "---",
        "",
        "## Contributing",
        "",
        "1. Branch from `main` (`feat/...`, `fix/...`, `docs/...`, `chore/...`).",
        "2. Build with `templates/` (multi-tool compatible).",
        "3. Verify: `python3 tools/gen_index.py` + lint the `SKILL.md` frontmatter.",
        "4. Open a PR with all assignments; review per `docs/CODE_REVIEW.md`.",
        "",
        "See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md),",
        "and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).",
        "",
        "<sub>README generated automatically by `tools/gen_index.py` — do not hand-edit",
        "above the Contributing sections.</sub>",
        "",
    ]

    (ROOT / "README.md").write_text("\n".join(out), encoding="utf-8")
    print(f"README.md gerado: {total} skills, {len(cats)} categorias")
    return 0


if __name__ == "__main__":
    sys.exit(main())
