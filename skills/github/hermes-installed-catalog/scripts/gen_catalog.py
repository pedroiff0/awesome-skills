#!/usr/bin/env python3
"""Generate the Hermes installed catalog from the live server.

Scans ~/.hermes/skills (+ profiles/*/skills) and hermes-agent/plugins, then
writes references/installed-inventory.md and references/installed.json next to
this script.

Usage:
  python3 gen_catalog.py
"""
from __future__ import annotations
import json, os, pathlib
from collections import defaultdict

HOME = pathlib.Path(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")))


def list_skills(base: pathlib.Path) -> list[str]:
    d = base / "skills"
    if not d.exists():
        return []
    return sorted(p.name for p in d.glob("*") if (p / "SKILL.md").exists())


def main() -> int:
    default_skills = list_skills(HOME)
    profiles = sorted(p.name for p in (HOME / "profiles").glob("*") if p.is_dir())
    profile_skills = {p: list_skills(HOME / f"profiles/{p}") for p in profiles}

    plugins_dir = HOME / "hermes-agent" / "plugins"
    plugins = sorted(p.name for p in plugins_dir.iterdir()
                     if p.is_dir() and not p.name.startswith("_")
                     and p.name not in ("__pycache__",))

    groups = defaultdict(list)
    for s in default_skills:
        if s.startswith("agency-"):
            parts = s.split("-")
            grp = "agency:" + parts[1] if len(parts) > 1 else "agency"
        else:
            grp = s.split("-")[0].split("/")[0]
        groups[grp].append(s)

    here = pathlib.Path(__file__).resolve().parent
    cat: list[str] = []
    cat.append("# Catálogo de Skills/plugins/agents instalados (Hermes — servidor de pedroiff0)")
    cat.append("")
    cat.append(f"Gerado a partir de `{HOME}` (profile: **default**"
               + (f" + {', '.join(profiles)}" if profiles else "") + ").")
    cat.append("")
    cat.append(f"- **Skills instaladas:** {len(default_skills)} (default)"
               + (f" + {sum(len(v) for v in profile_skills.values())} em profiles" if profiles else ""))
    cat.append(f"- **Plugins instalados:** {len(plugins)}")
    cat.append("- **Agent definitions custom:** 0 (subagentes são runtime leaf/orchestrator)")
    cat.append("")
    cat.append("## Plugins\n")
    cat.append("| Plugin | |")
    cat.append("|---|---|")
    for p in plugins:
        cat.append(f"| `{p}` | |")
    cat.append("")
    cat.append("## Skills por grupo (default)\n")
    cat.append("| Grupo | Qtd | Exemplos |")
    cat.append("|---|---|---|")
    for g in sorted(groups, key=lambda k: -len(groups[k])):
        items = groups[g]
        ex = ", ".join(f"`{x}`" for x in items[:3])
        if len(items) > 3:
            ex += ", …"
        cat.append(f"| {g} | {len(items)} | {ex} |")
    cat.append("")
    cat.append("## Lista completa de skills (default)\n")
    for s in default_skills:
        cat.append(f"- `{s}`")
    cat.append("")
    if profiles:
        cat.append("## Skills por profile\n")
        for p, sk in profile_skills.items():
            cat.append(f"### {p} ({len(sk)})")
            for s in sk:
                cat.append(f"- `{s}`")
            cat.append("")

    ref_dir = here.parent / "references"
    (ref_dir / "installed-inventory.md").write_text("\n".join(cat) + "\n", encoding="utf-8")
    meta = {"skills_default": default_skills, "profiles": profiles,
             "profile_skills": profile_skills, "plugins": plugins}
    (ref_dir / "installed.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"skills={len(default_skills)} plugins={len(plugins)} grupos={len(groups)}")
    print(f"-> {here/'references/installed-inventory.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
