#!/usr/bin/env python3
"""Interactive Multi-Agent Skills Installer for awesome-skills.

Features:
- Beautiful monospace terminal TUI with arrow navigation, spacebar toggle, and enter confirm.
- Re-attaches /dev/tty for direct curl | bash execution.
- Multi-agent targeting: Google Antigravity, Hermes Agent, Claude Code, Cursor (.mdc), Windsurf, Roo/Cline, OpenCode.
- Curated skill packs, category selection, fuzzy search, and full catalog installation.
"""
from __future__ import annotations

import argparse
import atexit
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
        "desc": "~/.gemini/antigravity-cli/skills/",
        "global_dir": Path.home() / ".gemini" / "antigravity-cli" / "skills",
        "local_dir": Path(".agent") / "skills",
        "format": "skill_dir",
    },
    "hermes": {
        "name": "Hermes Agent (Nous)",
        "desc": "~/.hermes/skills/",
        "global_dir": Path.home() / ".hermes" / "skills",
        "local_dir": Path(".hermes") / "skills",
        "format": "categorized_dir",
    },
    "claude": {
        "name": "Claude Code (Anthropic)",
        "desc": "~/.claude/skills/",
        "global_dir": Path.home() / ".claude" / "skills",
        "local_dir": Path(".claude") / "skills",
        "format": "skill_dir",
    },
    "cursor": {
        "name": "Cursor IDE Rules (.mdc)",
        "desc": ".cursor/rules/*.mdc",
        "global_dir": Path.home() / ".cursor" / "rules",
        "local_dir": Path(".cursor") / "rules",
        "format": "cursor_mdc",
    },
    "windsurf": {
        "name": "Windsurf (Codeium)",
        "desc": ".windsurf/skills/ or memories",
        "global_dir": Path.home() / ".codeium" / "windsurf" / "memories",
        "local_dir": Path(".windsurf") / "skills",
        "format": "skill_dir",
    },
    "roo": {
        "name": "Roo Code / Cline",
        "desc": "~/.roo/skills/",
        "global_dir": Path.home() / ".roo" / "skills",
        "local_dir": Path(".roo") / "skills",
        "format": "skill_dir",
    },
    "opencode": {
        "name": "OpenCode / Codex",
        "desc": "~/.config/opencode/skills/",
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

# ANSI Styling
ESC = "\033["
RESET = f"{ESC}0m"
BOLD = f"{ESC}1m"
DIM = f"{ESC}2m"
CYAN = f"{ESC}36m"
BRIGHT_CYAN = f"{ESC}96m"
GREEN = f"{ESC}32m"
BRIGHT_GREEN = f"{ESC}92m"
YELLOW = f"{ESC}33m"
BRIGHT_YELLOW = f"{ESC}93m"
BLUE = f"{ESC}34m"
BRIGHT_BLUE = f"{ESC}94m"
MAGENTA = f"{ESC}35m"
WHITE = f"{ESC}37m"
BG_BLUE = f"{ESC}44m"
BG_GRAY = f"{ESC}100m"
HIDE_CURSOR = f"{ESC}?25l"
SHOW_CURSOR = f"{ESC}?25h"


def restore_cursor():
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()


atexit.register(restore_cursor)


def ensure_tty():
    """Ensure stdin is connected to a tty if available (e.g. for curl | bash)."""
    if not sys.stdin.isatty():
        try:
            sys.stdin = open("/dev/tty", "r")
        except Exception:
            pass


def getch() -> str:
    """Read a single keypress or ANSI escape sequence on POSIX/Windows."""
    if os.name == "nt":
        import msvcrt
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):
            ch2 = msvcrt.getch()
            if ch2 == b"H":
                return "UP"
            if ch2 == b"P":
                return "DOWN"
            if ch2 == b"K":
                return "LEFT"
            if ch2 == b"M":
                return "RIGHT"
        if ch == b"\r":
            return "ENTER"
        if ch == b" ":
            return "SPACE"
        if ch == b"\x03":
            raise KeyboardInterrupt
        return ch.decode("utf-8", errors="ignore")

    import termios
    import tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            # Possible escape sequence
            seq = sys.stdin.read(2)
            if seq == "[A":
                return "UP"
            elif seq == "[B":
                return "DOWN"
            elif seq == "[C":
                return "RIGHT"
            elif seq == "[D":
                return "LEFT"
            elif seq.startswith("["):
                # Extended escape sequence like [1~
                _ = sys.stdin.read(1)
                return "ESC"
            return "ESC"
        elif ch in ("\r", "\n"):
            return "ENTER"
        elif ch == " ":
            return "SPACE"
        elif ch == "\x03":  # Ctrl+C
            raise KeyboardInterrupt
        elif ch == "\x04":  # Ctrl+D
            return "EOF"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def print_banner():
    banner = f"""{BRIGHT_CYAN}{BOLD}
  ╔══════════════════════════════════════════════════════════════════════╗
  ║   █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗      ║
  ║  ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝      ║
  ║  ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗        ║
  ║  ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝        ║
  ║  ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗      ║
  ║                                                                      ║
  ║   AWESOME SKILLS — Interactive Multi-Agent Installer v2.0            ║
  ║   Write once in SKILL.md — Run on all AI Agents                      ║
  ╚══════════════════════════════════════════════════════════════════════╝{RESET}
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


def tui_multiselect(
    title: str,
    options: list[tuple[str, str, str]],  # (key, label, subtitle)
    default_selected: list[str] | None = None,
) -> list[str]:
    """Interactive multi-select menu with arrow keys and spacebar."""
    if not sys.stdin.isatty():
        # Non-interactive fallback
        return [opt[0] for opt in options] if default_selected is None else default_selected

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    selected = set(default_selected if default_selected is not None else [options[0][0]])
    cursor = 0
    num_opts = len(options)
    lines_rendered = 0

    def render():
        nonlocal lines_rendered
        buf = []
        # Clear previous render
        if lines_rendered > 0:
            buf.append(f"{ESC}{lines_rendered}F")

        buf.append(f"{BOLD}{WHITE}┌── {title} {RESET}\n")
        lines = 1

        for idx, (key, label, sub) in enumerate(options):
            is_active = idx == cursor
            is_checked = key in selected
            box = f"{BRIGHT_GREEN}[✔]{RESET}" if is_checked else f"{DIM}[ ]{RESET}"
            ptr = f"{BRIGHT_CYAN}❯{RESET}" if is_active else " "

            sub_text = f" {DIM}({sub}){RESET}" if sub else ""
            if is_active:
                buf.append(f"  {ptr} {box} {BOLD}{BRIGHT_CYAN}{label}{RESET}{sub_text}{ESC}K\n")
            else:
                buf.append(f"  {ptr} {box} {label}{sub_text}{ESC}K\n")
            lines += 1

        footer = f"{DIM}└── [↑/↓/j/k: Navigate | Space: Toggle | a: Toggle All | Enter: Confirm | q: Quit]{RESET}"
        buf.append(f"{footer}{ESC}K\n")
        lines += 1

        lines_rendered = lines
        sys.stdout.write("".join(buf))
        sys.stdout.flush()

    try:
        while True:
            render()
            key = getch()
            if key in ("UP", "k"):
                cursor = (cursor - 1) % num_opts
            elif key in ("DOWN", "j"):
                cursor = (cursor + 1) % num_opts
            elif key == "SPACE":
                cur_key = options[cursor][0]
                if cur_key in selected:
                    selected.remove(cur_key)
                else:
                    selected.add(cur_key)
            elif key in ("a", "A"):
                if len(selected) == num_opts:
                    selected.clear()
                else:
                    selected = set(opt[0] for opt in options)
            elif key == "ENTER":
                if not selected:
                    selected.add(options[cursor][0])
                break
            elif key in ("q", "Q", "EOF"):
                print(f"\n{YELLOW}Installation cancelled by user.{RESET}")
                sys.exit(0)
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

    print()
    return [opt[0] for opt in options if opt[0] in selected]


def tui_single_select(
    title: str,
    options: list[tuple[str, str, str]],  # (key, label, subtitle)
    default_idx: int = 0,
) -> str:
    """Interactive single-choice menu with arrow keys."""
    if not sys.stdin.isatty():
        return options[default_idx][0]

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    cursor = default_idx
    num_opts = len(options)
    lines_rendered = 0

    def render():
        nonlocal lines_rendered
        buf = []
        if lines_rendered > 0:
            buf.append(f"{ESC}{lines_rendered}F")

        buf.append(f"{BOLD}{WHITE}┌── {title} {RESET}\n")
        lines = 1

        for idx, (key, label, sub) in enumerate(options):
            is_active = idx == cursor
            radio = f"{BRIGHT_CYAN}(•){RESET}" if is_active else f"{DIM}( ){RESET}"
            ptr = f"{BRIGHT_CYAN}❯{RESET}" if is_active else " "
            sub_text = f" {DIM}— {sub}{RESET}" if sub else ""

            if is_active:
                buf.append(f"  {ptr} {radio} {BOLD}{BRIGHT_CYAN}{label}{RESET}{sub_text}{ESC}K\n")
            else:
                buf.append(f"  {ptr} {radio} {label}{sub_text}{ESC}K\n")
            lines += 1

        footer = f"{DIM}└── [↑/↓/j/k: Navigate | Enter: Confirm | q: Quit]{RESET}"
        buf.append(f"{footer}{ESC}K\n")
        lines += 1

        lines_rendered = lines
        sys.stdout.write("".join(buf))
        sys.stdout.flush()

    try:
        while True:
            render()
            key = getch()
            if key in ("UP", "k"):
                cursor = (cursor - 1) % num_opts
            elif key in ("DOWN", "j"):
                cursor = (cursor + 1) % num_opts
            elif key in ("ENTER", "SPACE"):
                break
            elif key in ("q", "Q", "EOF"):
                print(f"\n{YELLOW}Installation cancelled by user.{RESET}")
                sys.exit(0)
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

    print()
    return options[cursor][0]


def convert_skill_to_cursor_mdc(skill_path: Path, target_dir: Path, skill_name: str):
    """Converts SKILL.md to .cursor/rules/<skill_name>.mdc with frontmatter."""
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
    ensure_tty()
    print_banner()

    catalog = discover_skills()
    total_skills = sum(len(s) for s in catalog.values())
    total_cats = len(catalog)

    print(f"  {BOLD}Catalog Status:{RESET} {BRIGHT_GREEN}{total_skills} skills{RESET} across {BRIGHT_CYAN}{total_cats} categories{RESET}.\n")

    # Step 1: Select Target Agents
    agent_opts = [(k, v["name"], v["desc"]) for k, v in AGENTS.items()]
    selected_agents = tui_multiselect(
        "Step 1: Select Target Agent(s) to Equip",
        agent_opts,
        default_selected=["agy", "claude", "hermes"],
    )

    # Step 2: Scope
    scope_opts = [
        ("global", "Global User Profile", "Installed in ~/.<agent> — available across all projects"),
        ("local", "Local Workspace Repository", "Installed in .agent/ or .cursor/ — scoped to current project"),
    ]
    selected_scope = tui_single_select("Step 2: Choose Installation Scope", scope_opts, default_idx=0)

    # Step 3: Selection Mode
    mode_opts = [
        ("pack_fullstack", PACKS["fullstack"]["title"], PACKS["fullstack"]["description"]),
        ("pack_devops", PACKS["devops"]["title"], PACKS["devops"]["description"]),
        ("pack_ai", PACKS["ai"]["title"], PACKS["ai"]["description"]),
        ("pack_academic", PACKS["academic"]["title"], PACKS["academic"]["description"]),
        ("pack_creative", PACKS["creative"]["title"], PACKS["creative"]["description"]),
        ("pack_all", PACKS["all"]["title"], f"All {total_skills} skills across {total_cats} categories"),
        ("categories", "🗂️  Select Categories Interactively", "Choose specific categories from a list"),
        ("search", "🔍 Search & Select Individual Skills", "Fuzzy search by name or keyword"),
    ]
    selected_mode = tui_single_select("Step 3: What Skills do you want to install?", mode_opts, default_idx=0)

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
        cat_opts = [(cat, cat, f"{len(sks)} skills") for cat, sks in sorted(catalog.items())]
        chosen_cats = tui_multiselect("Select Categories to Install", cat_opts, default_selected=[cat_opts[0][0]])
        for cat in chosen_cats:
            for name, path in catalog[cat].items():
                skills_to_install.append((cat, name, path))

    elif selected_mode == "search":
        print(f"{BOLD}{WHITE}Type search keyword (or press Enter to list all):{RESET}")
        try:
            query = input(f"{BRIGHT_YELLOW}Search: {RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            query = ""
        matched = []
        for cat, sks in catalog.items():
            for name, path in sks.items():
                if not query or query in name.lower() or query in cat.lower():
                    matched.append((name, f"[{cat}] {name}", str(path.relative_to(REPO_ROOT)), cat, path))
        if not matched:
            print(f"{YELLOW}No matches found for '{query}'. Loading full catalog.{RESET}")
            for cat, sks in catalog.items():
                for name, path in sks.items():
                    skills_to_install.append((cat, name, path))
        else:
            opts = [(m[0], m[1], m[2]) for m in matched]
            chosen = tui_multiselect(f"Select Skills to Install ({len(matched)} matches)", opts, default_selected=[opts[0][0]])
            for m_name in chosen:
                for item in matched:
                    if item[0] == m_name:
                        skills_to_install.append((item[3], item[0], item[4]))
                        break

    # Step 4: Installation Method
    method_opts = [
        ("symlink", "Symlink (Dynamic Link)", "Auto-updates instantly whenever repository is pulled"),
        ("copy", "Direct File Copy", "Independent snapshot clone"),
    ]
    selected_method = tui_single_select("Step 4: Choose Installation Mode", method_opts, default_idx=0)
    use_symlink = selected_method == "symlink"

    # Step 5: Execute
    print(f"{BOLD}{BRIGHT_CYAN}🚀 Installing {len(skills_to_install)} skill(s) across {len(selected_agents)} agent(s)...{RESET}\n")

    for agent_key in selected_agents:
        agent_info = AGENTS[agent_key]
        target_dir = agent_info["global_dir"] if selected_scope == "global" else agent_info["local_dir"]
        print(f"  {BOLD}Installing to {agent_info['name']}{RESET} -> {DIM}{target_dir}{RESET}")
        installed_count = 0
        for cat, name, path in skills_to_install:
            if install_skill_to_target(path, cat, name, agent_key, target_dir, use_symlink=use_symlink):
                installed_count += 1
        print(f"  {BRIGHT_GREEN}✔ Installed {installed_count} skills in {agent_info['name']}{RESET}\n")

    print(f"{BRIGHT_GREEN}{BOLD}══════════════════════════════════════════════════════════════════════{RESET}")
    print(f"  {BRIGHT_GREEN}{BOLD}🎉 Installation Complete!{RESET}")
    print(f"  {WHITE}Skills are active and ready for prompt triggers in your chosen runtimes.{RESET}")
    print(f"{BRIGHT_GREEN}{BOLD}══════════════════════════════════════════════════════════════════════{RESET}\n")


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
            print(f"\n{BOLD}{BRIGHT_CYAN}=== {cat} ({len(sks)} skills) ==={RESET}")
            for name, path in sorted(sks.items()):
                fm = parse_frontmatter(path / "SKILL.md")
                desc = fm.get("description", "")
                print(f"  • {BOLD}{name}{RESET}: {desc[:90]}{'...' if len(desc)>90 else ''}")
        return

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

    try:
        run_interactive()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{YELLOW}Installation cancelled by user.{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
