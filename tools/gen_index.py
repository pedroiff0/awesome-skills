#!/usr/bin/env python3
"""Gera o índice de skills (README.md) a partir de skills/**/SKILL.md."""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def front_matter(path: Path) -> dict:
    txt = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    data = {}
    if not m:
        return data
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
        if len(desc) > 220:
            desc = desc[:217].rstrip() + "..."
        cats.setdefault(cat, []).append((name, desc, str(rel)))

    total = sum(len(v) for v in cats.values())
    out = [
        "# awesome-skills",
        "",
        "Coleção pessoal de **skills** (memória procedural) usadas pelo agente "
        "[Hermes](https://hermes-agent.nousresearch.com/docs).",
        "Cada skill é um diretório com `SKILL.md` (frontmatter YAML + instruções) e,",
        "opcionalmente, `references/`, `scripts/`, `templates/`, `assets/`.",
        "",
        f"**{total} skills** em {len(cats)} categorias.",
        "",
        "## Instalação",
        "",
        "```bash",
        "git clone https://github.com/pedroiff0/awesome-skills.git",
        "cp -r awesome-skills/skills/* ~/.hermes/skills/",
        "```",
        "",
        "Ou apenas uma categoria/skill: copie o diretório desejado para `~/.hermes/skills/`.",
        "",
        "## Índice",
        "",
    ]
    for cat in sorted(cats):
        out.append(f"### {cat}")
        out.append("")
        out.append("| Skill | Descrição |")
        out.append("|---|---|")
        for name, desc, rel in sorted(cats[cat]):
            out.append(f"| [`{name}`](skills/{rel}) | {desc} |")
        out.append("")
    out += [
        "## Contribuindo / adicionando skills",
        "",
        "1. Crie `skills/<categoria>/<nome-da-skill>/SKILL.md` com frontmatter:",
        "",
        "```yaml",
        "---",
        "name: minha-skill",
        'description: "Uma linha, imperativa, dizendo quando usar."',
        "version: 1.0.0",
        "license: MIT",
        "platforms: [linux, macos, windows]",
        "---",
        "```",
        "",
        "2. Rode `python3 tools/gen_index.py` para regenerar este README.",
        "3. Commit e push.",
        "",
        "> README gerado automaticamente — não edite à mão acima da seção Contribuindo.",
        "",
    ]
    (ROOT / "README.md").write_text("\n".join(out), encoding="utf-8")
    print(f"README.md gerado: {total} skills, {len(cats)} categorias")
    return 0


if __name__ == "__main__":
    sys.exit(main())
