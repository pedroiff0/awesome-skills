#!/usr/bin/env python3
"""Interactive Multi-Agent Skills Installer for awesome-skills.

Features:
- Beautiful monospace terminal TUI with arrow navigation, spacebar toggle, and enter confirm.
- Skill-by-skill browsing with live metadata, author, GitHub links, stars, and descriptions.
- Instant ESC key cancellation at any step.
- Scrollable viewport with pagination and search/sort support.
- Multi-agent targeting: Google Antigravity, Hermes Agent, Claude Code, Cursor (.mdc), Windsurf, Roo/Cline, OpenCode.
- Curated skill packs, category selection, and full catalog installation.
"""
from __future__ import annotations

import argparse
import atexit
import os
import re
import select
import shutil
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = REPO_ROOT / "skills"
GITHUB_BASE_URL = "https://github.com/pedroiff0/awesome-skills/tree/main/skills"

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
HIDE_CURSOR = f"{ESC}?25l"
SHOW_CURSOR = f"{ESC}?25h"


def restore_cursor():
    try:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()
    except Exception:
        pass


atexit.register(restore_cursor)


def cancel_and_exit():
    restore_cursor()
    print(f"\n{BRIGHT_YELLOW}🟡 Operação cancelada pelo usuário (ESC/Ctrl+C).{RESET}\n")
    sys.exit(0)


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
        if ch == b"\x1b":
            return "ESC"
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
            # Check if there are more characters arriving immediately (arrow keys)
            r, _, _ = select.select([sys.stdin], [], [], 0.05)
            if not r:
                return "ESC"  # Standalone ESC key pressed!
            seq1 = sys.stdin.read(1)
            if seq1 == "[":
                r2, _, _ = select.select([sys.stdin], [], [], 0.05)
                if not r2:
                    return "ESC"
                seq2 = sys.stdin.read(1)
                if seq2 == "A":
                    return "UP"
                elif seq2 == "B":
                    return "DOWN"
                elif seq2 == "C":
                    return "RIGHT"
                elif seq2 == "D":
                    return "LEFT"
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
    """Interactive multi-select menu with arrow keys, spacebar, and ESC support."""
    if not sys.stdin.isatty():
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

        footer = f"{DIM}└── [↑/↓/j/k: Mover | Espaço: Marcar | a: Todos | Enter: Confirmar | Esc/q: Cancelar]{RESET}"
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
            elif key in ("ESC", "q", "Q", "EOF"):
                cancel_and_exit()
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
    """Interactive single-choice menu with arrow keys and ESC support."""
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

        footer = f"{DIM}└── [↑/↓/j/k: Mover | Enter: Confirmar | Esc/q: Cancelar]{RESET}"
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
            elif key in ("ESC", "q", "Q", "EOF"):
                cancel_and_exit()
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

    print()
    return options[cursor][0]


def tui_skill_browser(
    all_skills: list[dict],  # dict with name, category, path, author, desc, github_url
) -> list[tuple[str, str, Path]]:
    """Interactive Skill-by-Skill browser with viewport scrolling, details box, search, and sort."""
    if not sys.stdin.isatty():
        return [(s["category"], s["name"], s["path"]) for s in all_skills]

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    sort_modes = ["name", "category", "author"]
    sort_idx = 0
    search_query = ""

    def get_filtered_skills():
        items = all_skills
        if search_query:
            q = search_query.lower()
            items = [
                s for s in items
                if q in s["name"].lower() or q in s["category"].lower() or q in s["author"].lower() or q in s["desc"].lower()
            ]
        sm = sort_modes[sort_idx]
        if sm == "name":
            return sorted(items, key=lambda x: x["name"])
        elif sm == "category":
            return sorted(items, key=lambda x: (x["category"], x["name"]))
        elif sm == "author":
            return sorted(items, key=lambda x: (x["author"], x["name"]))
        return items

    selected_names = set()
    cursor = 0
    page_size = 10
    lines_rendered = 0

    try:
        while True:
            items = get_filtered_skills()
            if not items:
                items = all_skills
                search_query = ""

            num_items = len(items)
            cursor = max(0, min(cursor, num_items - 1))

            # Calculate scroll window
            start_idx = max(0, min(cursor - page_size // 2, num_items - page_size))
            end_idx = min(start_idx + page_size, num_items)
            visible_items = items[start_idx:end_idx]

            focused = items[cursor]

            buf = []
            if lines_rendered > 0:
                buf.append(f"{ESC}{lines_rendered}F")

            header = f"{BOLD}{WHITE}┌── 🎯 Seleção Skill por Skill [Selecionadas: {len(selected_names)}/{len(all_skills)}] {RESET}"
            if search_query:
                header += f" {BRIGHT_YELLOW}(Filtro: '{search_query}'){RESET}"
            buf.append(f"{header}{ESC}K\n")
            lines = 1

            for rel_i, item in enumerate(visible_items):
                abs_i = start_idx + rel_i
                is_active = abs_i == cursor
                is_checked = item["name"] in selected_names

                box = f"{BRIGHT_GREEN}[✔]{RESET}" if is_checked else f"{DIM}[ ]{RESET}"
                ptr = f"{BRIGHT_CYAN}❯{RESET}" if is_active else " "

                name_fmt = f"{BOLD}{BRIGHT_CYAN}{item['name']:<28}{RESET}" if is_active else f"{item['name']:<28}"
                cat_fmt = f"{DIM}[{item['category']}]{RESET}"
                author_fmt = f"{DIM}by {item['author'][:18]}{RESET}"

                buf.append(f"  {ptr} {box} {name_fmt} {cat_fmt:<32} {author_fmt}{ESC}K\n")
                lines += 1

            # Viewport scroll indicator
            sort_label = f"Sort: {sort_modes[sort_idx].capitalize()}"
            scroll_info = f"Exibindo {start_idx+1}-{end_idx} de {num_items} skills [{sort_label}]"
            buf.append(f"  {DIM}── {scroll_info} ──{RESET}{ESC}K\n")
            lines += 1

            # Detailed metadata box for focused skill
            desc_wrapped = focused["desc"][:160] + "..." if len(focused["desc"]) > 160 else focused["desc"]
            buf.append(f"{BOLD}{WHITE}┌─ 🔍 Detalhes da Skill Selecionada ─────────────────────────────────{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Nome:{RESET}        {BRIGHT_CYAN}{focused['name']}{RESET} ({focused['category']}){ESC}K\n")
            buf.append(f"│ {BOLD}Autor:{RESET}       {WHITE}{focused['author']}{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Descrição:{RESET}   {DIM}{desc_wrapped}{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}GitHub URL:{RESET}  {BLUE}{focused['github_url']}{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Repositório:{RESET} ⭐ {BRIGHT_YELLOW}pedroiff0/awesome-skills{RESET} | MIT License{ESC}K\n")
            buf.append(f"{BOLD}{WHITE}└────────────────────────────────────────────────────────────────────{RESET}{ESC}K\n")
            lines += 7

            # Controls footer
            footer = f"{DIM}└── [↑/↓/j/k: Navegar | Espaço: Marcar | a: Todos | /: Filtrar | s: Ordenar | Enter: Confirmar | Esc: Cancelar]{RESET}"
            buf.append(f"{footer}{ESC}K\n")
            lines += 1

            lines_rendered = lines
            sys.stdout.write("".join(buf))
            sys.stdout.flush()

            key = getch()
            if key in ("UP", "k"):
                cursor = (cursor - 1) % num_items
            elif key in ("DOWN", "j"):
                cursor = (cursor + 1) % num_items
            elif key == "SPACE":
                cur_name = items[cursor]["name"]
                if cur_name in selected_names:
                    selected_names.remove(cur_name)
                else:
                    selected_names.add(cur_name)
            elif key in ("a", "A"):
                if len(selected_names) == len(all_skills):
                    selected_names.clear()
                else:
                    selected_names = set(s["name"] for s in all_skills)
            elif key == "s":
                sort_idx = (sort_idx + 1) % len(sort_modes)
            elif key == "/":
                restore_cursor()
                sys.stdout.write(f"\n{BOLD}{BRIGHT_YELLOW}Filtrar skills por texto (Enter para limpar): {RESET}")
                sys.stdout.flush()
                try:
                    search_query = input().strip()
                except (EOFError, KeyboardInterrupt):
                    search_query = ""
                cursor = 0
                lines_rendered = 0  # Redraw cleanly
                sys.stdout.write(HIDE_CURSOR)
            elif key == "ENTER":
                if not selected_names and items:
                    selected_names.add(items[cursor]["name"])
                break
            elif key in ("ESC", "q", "Q", "EOF"):
                cancel_and_exit()

    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

    print()
    return [(s["category"], s["name"], s["path"]) for s in all_skills if s["name"] in selected_names]


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

    # Build rich skill metadata list
    all_skills_flat = []
    for cat, sks in catalog.items():
        for name, path in sks.items():
            fm = parse_frontmatter(path / "SKILL.md")
            author = fm.get("author") or "Pedro Henrique Rocha de Andrade"
            desc = fm.get("description") or f"Reusable {name} skill"
            all_skills_flat.append({
                "name": name,
                "category": cat,
                "path": path,
                "author": author,
                "desc": desc,
                "github_url": f"{GITHUB_BASE_URL}/{cat}/{name}",
            })

    print(f"  {BOLD}Catálogo:{RESET} {BRIGHT_GREEN}{total_skills} skills{RESET} em {BRIGHT_CYAN}{total_cats} categorias{RESET}.\n")

    # Step 1: Select Target Agents
    agent_opts = [(k, v["name"], v["desc"]) for k, v in AGENTS.items()]
    selected_agents = tui_multiselect(
        "Passo 1: Selecione os Agentes de IA Alvo",
        agent_opts,
        default_selected=["agy", "claude", "hermes"],
    )

    # Step 2: Scope
    scope_opts = [
        ("global", "Perfil Global do Usuário", "Instalado em ~/.<agente> — disponível em todos os projetos"),
        ("local", "Repositório Local (Workspace)", "Instalado em .agent/ ou .cursor/ — restrito a este projeto"),
    ]
    selected_scope = tui_single_select("Passo 2: Escolha o Escopo de Instalação", scope_opts, default_idx=0)

    # Step 3: Selection Mode
    mode_opts = [
        ("skill_by_skill", "🎯 Selecionar Skill por Skill (Navegação Completa)", "Ver detalhes, autor, GitHub, stars e escolher individualmente"),
        ("pack_fullstack", PACKS["fullstack"]["title"], PACKS["fullstack"]["description"]),
        ("pack_devops", PACKS["devops"]["title"], PACKS["devops"]["description"]),
        ("pack_ai", PACKS["ai"]["title"], PACKS["ai"]["description"]),
        ("pack_academic", PACKS["academic"]["title"], PACKS["academic"]["description"]),
        ("pack_creative", PACKS["creative"]["title"], PACKS["creative"]["description"]),
        ("pack_all", PACKS["all"]["title"], f"Todas as {total_skills} skills em {total_cats} categorias"),
        ("categories", "🗂️  Selecionar por Categoria", "Escolha categorias completas da lista"),
    ]
    selected_mode = tui_single_select("Passo 3: Quais Skills você deseja instalar?", mode_opts, default_idx=0)

    skills_to_install: list[tuple[str, str, Path]] = []

    if selected_mode == "skill_by_skill":
        skills_to_install = tui_skill_browser(all_skills_flat)

    elif selected_mode.startswith("pack_"):
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
        chosen_cats = tui_multiselect("Selecione as Categorias Desejadas", cat_opts, default_selected=[cat_opts[0][0]])
        for cat in chosen_cats:
            for name, path in catalog[cat].items():
                skills_to_install.append((cat, name, path))

    # Step 4: Installation Method
    method_opts = [
        ("symlink", "Link Simbólico (Symlink Dinâmico)", "Atualiza automaticamente ao rodar git pull"),
        ("copy", "Cópia Direta de Arquivos", "Snapshot independente e isolado"),
    ]
    selected_method = tui_single_select("Passo 4: Escolha o Modo de Instalação", method_opts, default_idx=0)
    use_symlink = selected_method == "symlink"

    if not skills_to_install:
        print(f"\n{YELLOW}Nenhuma skill selecionada para instalação.{RESET}")
        return

    # Step 5: Execute
    print(f"\n{BOLD}{BRIGHT_CYAN}🚀 Instalando {len(skills_to_install)} skill(s) em {len(selected_agents)} agente(s)...{RESET}\n")

    for agent_key in selected_agents:
        agent_info = AGENTS[agent_key]
        target_dir = agent_info["global_dir"] if selected_scope == "global" else agent_info["local_dir"]
        print(f"  {BOLD}Instalando em {agent_info['name']}{RESET} -> {DIM}{target_dir}{RESET}")
        installed_count = 0
        for cat, name, path in skills_to_install:
            if install_skill_to_target(path, cat, name, agent_key, target_dir, use_symlink=use_symlink):
                installed_count += 1
        print(f"  {BRIGHT_GREEN}✔ {installed_count} skill(s) instalada(s) em {agent_info['name']}{RESET}\n")

    print(f"{BRIGHT_GREEN}{BOLD}══════════════════════════════════════════════════════════════════════{RESET}")
    print(f"  {BRIGHT_GREEN}{BOLD}🎉 Instalação Concluída com Sucesso!{RESET}")
    print(f"  {WHITE}As skills estão prontas para serem acionadas nos seus agentes de IA.{RESET}")
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
                author = fm.get("author", "Pedro Henrique Rocha de Andrade")
                desc = fm.get("description", "")
                print(f"  • {BOLD}{name}{RESET} (by {author}): {desc[:80]}{'...' if len(desc)>80 else ''}")
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
        cancel_and_exit()


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(0)
