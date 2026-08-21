#!/usr/bin/env python3
"""Interactive Multi-Agent Skills Installer for awesome-skills.

Inspired by Caveman & modern CLI package managers:
Provides an interactive terminal TUI / menu or CLI flags to install
skills across Google Antigravity (AGY), Hermes Agent, Claude Code,
Cursor, Windsurf, Roo Code / Cline, and OpenCode.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = REPO_ROOT / "skills"

# Supported Agents & Target Paths
AGENTS = {
    "agy": {
        "name": "Google Antigravity (AGY)",
        "global_dir": Path.home() / ".gemini" / "antigravity-cli" / "skills",
        "local_dir": Path(".agent") / "skills",
        "format": "skill_dir",  # <dir>/<name>/SKILL.md
    },
    "hermes": {
        "name": "Hermes Agent",
        "global_dir": Path.home() / ".hermes" / "skills",
        "local_dir": Path(".hermes") / "skills",
        "format": "categorized_dir",  # <dir>/<category>/<name>/SKILL.md
    },
    "claude": {
        "name": "Claude Code",
        "global_dir": Path.home() / ".claude" / "skills",
        "local_dir": Path(".claude") / "skills",
        "format": "skill_dir",
    },
    "cursor": {
        "name": "Cursor IDE Rules (.mdc)",
        "global_dir": Path.home() / ".cursor" / "rules",
        "local_dir": Path(".cursor") / "rules",
        "format": "cursor_mdc",  # <dir>/<name>.mdc
    },
    "windsurf": {
        "name": "Windsurf",
        "global_dir": Path.home() / ".codeium" / "windsurf" / "memories",
        "local_dir": Path(".windsurf") / "skills",
        "format": "skill_dir",
    },
    "roo": {
        "name": "Roo Code / Cline",
        "global_dir": Path.home() / ".roo" / "skills",
        "local_dir": Path(".roo") / "skills",
        "format": "skill_dir",
    },
    "opencode": {
        "name": "OpenCode / Codex",
        "global_dir": Path.home() / ".config" / "opencode" / "skills",
        "local_dir": Path(".codex") / "rules",
        "format": "skill_dir",
    },
}

# Curated Packs
PACKS = {
    "fullstack": {
        "title": "🚀 Full-Stack & Developer Essentials",
        "description": "Essential web, APIs, testing, refactoring, and code inspection",
        "categories": ["software-development", "web", "github"],
    },
    "devops": {
        "title": "⚡ DevOps, Docker & Cloud Infrastructure",
        "description": "Container orchestration, server ops, automation, and CI/CD",
        "categories": ["devops", "github"],
    },
    "ai": {
        "title": "🧠 Autonomous AI Agents & MLOps",
        "description": "Multi-agent workflows, token optimization, local RAG, and model ops",
        "categories": ["autonomous-ai-agents", "mlops"],
    },
    "academic": {
        "title": "📚 Academic, LaTeX & Research",
        "description": "Paper writing, LaTeX CVs, arXiv search, translation, and research tools",
        "categories": ["latex", "research", "content-i18n"],
    },
    "creative": {
        "title": "🎨 Creative, Media & Design",
        "description": "SVG diagrams, ASCII art/video, audio processing, and themes",
        "categories": ["creative", "media", "desktop"],
    },
    "all": {
        "title": "📦 Complete Catalog",
        "description": "Install every skill in the awesome-skills repository",
        "categories": "ALL",
    },
}

# ANSI colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def print_banner():
    banner = f"""{CYAN}{BOLD}
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗            ║
║  ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝            ║
║  ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗              ║
║  ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝              ║
║  ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗            ║
║                                                                            ║
║   AWESOME SKILLS — Interactive Multi-Agent Installer                       ║
║   Write once in SKILL.md — Run on all AI Agents                            ║
╚════════════════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)


def discover_skills() -> dict[str, dict[str, Path]]:
    """Return dict of category -> {skill_name: skill_path}."""
    catalog: dict[str, dict[str, Path]] = {}
    for skill_file in sorted(SKILLS_DIR.rglob("SKILL.md")):
        rel = skill_file.relative_to(SKILLS_DIR)
        if len(rel.parts) >= 2:
            cat = rel.parts[0]
            name = rel.parts[1]
            catalog.setdefault(cat, {})[name] = skill_file.parent
    return catalog


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    txt = skill_md.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if mm:
            data[mm.group(1)] = mm.group(2).strip().strip('"').strip("'")
    return data


def prompt_choice(prompt: str, options: list[tuple[str, str]], default: int = 1) -> str:
    """Prompt user to select one option by number."""
    print(f"\n{BOLD}{prompt}{RESET}")
    for idx, (key, label) in enumerate(options, 1):
        def_marker = f" {DIM}(default){RESET}" if idx == default else ""
        print(f"  {CYAN}[{idx}]{RESET} {label}{def_marker}")
    while True:
        try:
            val = input(f"\n{YELLOW}Choose [1-{len(options)}] (default {default}): {RESET}").strip()
            if not val:
                return options[default - 1][0]
            n = int(val)
            if 1 <= n <= len(options):
                return options[n - 1][0]
        except (ValueError, IndexError):
            pass
        print(f"Invalid choice. Please enter a number between 1 and {len(options)}.")


def prompt_multiselect(
    prompt: str, options: list[tuple[str, str]], preselect_all: bool = False
) -> list[str]:
    """Interactive multi-select list."""
    print(f"\n{BOLD}{prompt}{RESET}")
    print(f"{DIM}Enter numbers separated by space/comma, 'a' for all, or press Enter for selection:{RESET}")
    for idx, (key, label) in enumerate(options, 1):
        print(f"  {CYAN}[{idx:2d}]{RESET} {label}")

    while True:
        try:
            val = input(f"\n{YELLOW}Select options [e.g. 1 3 4 or 'a' for all]: {RESET}").strip().lower()
            if not val or val == "a" or val == "all":
                return [opt[0] for opt in options]
            selected_indices = set(int(x.strip()) for x in re.split(r"[\s,]+", val) if x.strip())
            valid = [options[i - 1][0] for i in selected_indices if 1 <= i <= len(options)]
            if valid:
                return valid
        except Exception:
            pass
        print("Invalid selection. Try again.")


def convert_skill_to_cursor_mdc(skill_path: Path, target_dir: Path, skill_name: str):
    """Converts SKILL.md to .cursor/rules/<skill_name>.mdc with appropriate cursor frontmatter."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return
    fm = parse_frontmatter(skill_md)
    desc = fm.get("description", f"Skill rules for {skill_name}")
    content = skill_md.read_text(encoding="utf-8", errors="replace")
    body = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.S).strip()

    mdc_content = f"""---
description: "{desc}"
globs: "*"
alwaysApply: false
---

{body}
"""
    target_file = target_dir / f"{skill_name}.mdc"
    target_file.write_text(mdc_content, encoding="utf-8")


def install_skill_to_target(
    skill_path: Path,
    category: str,
    skill_name: str,
    agent_key: str,
    target_base: Path,
    use_symlink: bool = True,
) -> bool:
    """Install a skill to a specific agent directory."""
    agent_info = AGENTS[agent_key]
    fmt = agent_info["format"]

    try:
        target_base.mkdir(parents=True, exist_ok=True)

        if fmt == "cursor_mdc":
            convert_skill_to_cursor_mdc(skill_path, target_base, skill_name)
            return True

        if fmt == "categorized_dir":
            dest_dir = target_base / category
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_skill = dest_dir / skill_name
        else:  # skill_dir
            dest_skill = target_base / skill_name

        # Clean existing link or dir
        if dest_skill.is_symlink() or dest_skill.exists():
            if dest_skill.is_symlink() or dest_skill.is_file():
                dest_skill.unlink()
            else:
                shutil.rmtree(dest_skill)

        if use_symlink:
            dest_skill.symlink_to(skill_path.resolve(), target_is_directory=True)
        else:
            shutil.copytree(skill_path, dest_skill)
        return True
    except Exception as e:
        print(f"{YELLOW}Warning installing {skill_name} to {agent_key}: {e}{RESET}")
        return False


def run_interactive():
    print_banner()
    catalog = discover_skills()
    total_skills = sum(len(s) for s in catalog.values())
    total_cats = len(catalog)

    print(f"Loaded {GREEN}{total_skills} skills{RESET} across {BLUE}{total_cats} categories{RESET}.\n")

    # Step 1: Select Target Agents
    agent_options = [(k, v["name"]) for k, v in AGENTS.items()]
    selected_agents = prompt_multiselect("🤖 Step 1: Select Target Agent(s)", agent_options)

    # Step 2: Select Scope
    scope_options = [
        ("global", "Global (User Home directory `~/.` - available everywhere)"),
        ("local", "Local Workspace (Current project repository)"),
    ]
    selected_scope = prompt_choice("📍 Step 2: Select Installation Scope", scope_options, default=1)

    # Step 3: Selection Mode
    mode_options = [
        ("pack_fullstack", f"{PACKS['fullstack']['title']} — {PACKS['fullstack']['description']}"),
        ("pack_devops", f"{PACKS['devops']['title']} — {PACKS['devops']['description']}"),
        ("pack_ai", f"{PACKS['ai']['title']} — {PACKS['ai']['description']}"),
        ("pack_academic", f"{PACKS['academic']['title']} — {PACKS['academic']['description']}"),
        ("pack_creative", f"{PACKS['creative']['title']} — {PACKS['creative']['description']}"),
        ("pack_all", f"{PACKS['all']['title']} ({total_skills} skills) — {PACKS['all']['description']}"),
        ("categories", "🗂️  Select Specific Categories (Interactive Category List)"),
        ("search", "🔍 Search & Select Individual Skills"),
    ]
    selected_mode = prompt_choice("📦 Step 3: How would you like to select skills?", mode_options, default=1)

    skills_to_install: list[tuple[str, str, Path]] = []

    if selected_mode.startswith("pack_"):
        pack_key = selected_mode.replace("pack_", "")
        pack_cats = PACKS[pack_key]["categories"]
        if pack_cats == "ALL":
            for cat, sks in catalog.items():
                for name, path in sks.items():
                    skills_to_install.append((cat, name, path))
        else:
            for cat in pack_cats:
                if cat in catalog:
                    for name, path in catalog[cat].items():
                        skills_to_install.append((cat, name, path))

    elif selected_mode == "categories":
        cat_options = [(cat, f"{cat} ({len(sks)} skills)") for cat, sks in sorted(catalog.items())]
        chosen_cats = prompt_multiselect("Select Categories to install", cat_options)
        for cat in chosen_cats:
            for name, path in catalog[cat].items():
                skills_to_install.append((cat, name, path))

    elif selected_mode == "search":
        print(f"\n{BOLD}Type search terms to filter skills (or press enter to list all):{RESET}")
        query = input(f"{YELLOW}Search term: {RESET}").strip().lower()
        matched = []
        for cat, sks in catalog.items():
            for name, path in sks.items():
                if not query or query in name.lower() or query in cat.lower():
                    matched.append((name, f"[{cat}] {name}", cat, path))
        if not matched:
            print(f"{YELLOW}No skills found matching '{query}'. Installing all.{RESET}")
            for cat, sks in catalog.items():
                for name, path in sks.items():
                    skills_to_install.append((cat, name, path))
        else:
            chosen = prompt_multiselect(
                f"Found {len(matched)} matching skills:", [(m[0], m[1]) for m in matched]
            )
            for m_name in chosen:
                for item in matched:
                    if item[0] == m_name:
                        skills_to_install.append((item[2], item[0], item[3]))
                        break

    # Step 4: Installation Method
    method_options = [
        ("symlink", "Symlink (Recommended — auto-updates when repository is pulled)"),
        ("copy", "Hard Copy (Isolated snapshot)"),
    ]
    selected_method = prompt_choice("🔗 Step 4: Choose Installation Method", method_options, default=1)
    use_symlink = selected_method == "symlink"

    # Step 5: Install
    print(f"\n{BOLD}{CYAN}🚀 Installing {len(skills_to_install)} skill(s) across {len(selected_agents)} agent(s)...{RESET}\n")

    for agent_key in selected_agents:
        agent_info = AGENTS[agent_key]
        target_dir = agent_info["global_dir"] if selected_scope == "global" else agent_info["local_dir"]
        print(f"  {BOLD}Installing to {agent_info['name']}{RESET} ({target_dir})...")
        installed_count = 0
        for cat, name, path in skills_to_install:
            if install_skill_to_target(path, cat, name, agent_key, target_dir, use_symlink=use_symlink):
                installed_count += 1
        print(f"  {GREEN}✔ Installed {installed_count} skills in {agent_info['name']}{RESET}\n")

    print(f"{GREEN}{BOLD}🎉 Installation Complete!{RESET}")
    print(f"{DIM}All selected skills are immediately available in your chosen agent runtime(s).{RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        prog="awesome-skills installer",
        description="Multi-Agent Skill Installer for awesome-skills",
    )
    parser.add_argument(
        "--agent",
        help="Target agent(s) comma-separated (agy, hermes, claude, cursor, windsurf, roo, opencode, all)",
    )
    parser.add_argument(
        "--scope",
        choices=["global", "local"],
        default="global",
        help="Installation scope (default: global)",
    )
    parser.add_argument(
        "--pack",
        choices=["fullstack", "devops", "ai", "academic", "creative", "all"],
        help="Install a curated pack",
    )
    parser.add_argument(
        "--category",
        help="Install specific categories comma-separated",
    )
    parser.add_argument(
        "--skills",
        help="Install specific skills comma-separated",
    )
    parser.add_argument(
        "--symlink",
        action="store_true",
        default=True,
        help="Use symlinks (default)",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy files instead of symlinks",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available skills",
    )

    args = parser.parse_args()

    catalog = discover_skills()

    if args.list:
        print_banner()
        for cat, sks in sorted(catalog.items()):
            print(f"\n{BOLD}{CYAN}=== {cat} ({len(sks)} skills) ==={RESET}")
            for name, path in sorted(sks.items()):
                fm = parse_frontmatter(path / "SKILL.md")
                desc = fm.get("description", "")
                print(f"  • {BOLD}{name}{RESET}: {desc[:90]}{'...' if len(desc)>90 else ''}")
        return

    # Non-interactive CLI flags mode
    if args.agent or args.pack or args.category or args.skills:
        selected_agents = list(AGENTS.keys()) if args.agent == "all" else (args.agent.split(",") if args.agent else ["agy"])
        use_symlink = not args.copy

        skills_to_install: list[tuple[str, str, Path]] = []

        if args.pack:
            pack_cats = PACKS[args.pack]["categories"]
            if pack_cats == "ALL":
                for cat, sks in catalog.items():
                    for name, path in sks.items():
                        skills_to_install.append((cat, name, path))
            else:
                for cat in pack_cats:
                    if cat in catalog:
                        for name, path in catalog[cat].items():
                            skills_to_install.append((cat, name, path))

        elif args.category:
            cats = [c.strip() for c in args.category.split(",")]
            for cat in cats:
                if cat in catalog:
                    for name, path in catalog[cat].items():
                        skills_to_install.append((cat, name, path))

        elif args.skills:
            req_skills = set(s.strip() for s in args.skills.split(","))
            for cat, sks in catalog.items():
                for name, path in sks.items():
                    if name in req_skills:
                        skills_to_install.append((cat, name, path))
        else:
            for cat, sks in catalog.items():
                for name, path in sks.items():
                    skills_to_install.append((cat, name, path))

        print(f"Installing {len(skills_to_install)} skill(s) to {selected_agents}...")
        for agent_key in selected_agents:
            if agent_key not in AGENTS:
                continue
            agent_info = AGENTS[agent_key]
            target_dir = agent_info["global_dir"] if args.scope == "global" else agent_info["local_dir"]
            for cat, name, path in skills_to_install:
                install_skill_to_target(path, cat, name, agent_key, target_dir, use_symlink=use_symlink)
            print(f"✔ Installed to {agent_info['name']} ({target_dir})")
        return

    # Fallback to interactive mode
    run_interactive()


if __name__ == "__main__":
    main()
