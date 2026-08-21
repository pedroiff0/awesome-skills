#!/usr/bin/env python3
"""Universal Multi-Agent Skills Installer for awesome-skills (Cosmic Purple Dev Edition).

Features:
- Full Step-by-Step Back Navigation (press 'b', '←' Left Arrow, or 'Backspace' to go back and modify).
- Preserves user selections when navigating backward and forward.
- Aesthetic Purple, Astronomy & Developer Theme with Cosmic Coffee intro ☕ 🪐 🌌.
- Step 0: Quick Install (with verification of agents & skills), Custom Manual Setup, Uninstall / Clean, Open-Source Hub, and Ollama Hub.
- Strict selection validation: Users CANNOT proceed with 0 items selected (requires explicit [Space] check).
- Uninstaller module: Safely scans, selects, and removes installed skills/rules across agents with Back support.
- Robust key handling: Left arrow acts as Back; standalone ESC cancels immediately.
- Live Skill-by-Skill browser with viewport scrolling, metadata, author credits, and GitHub links.
- Multi-agent targeting: Google Antigravity, Hermes Agent, Claude Code, Cursor (.mdc), Windsurf, Roo/Cline, OpenCode.
"""
from __future__ import annotations

import argparse
import atexit
import fcntl
import os
import re
import shutil
import subprocess
import sys
import termios
import tty
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = REPO_ROOT / "skills"
PLUGINS_DIR = REPO_ROOT / "plugins"
MCP_DIR = REPO_ROOT / "mcp"
GITHUB_BASE_URL = "https://github.com/pedroiff0/awesome-skills/tree/main/skills"

# Supported Agents & Target Paths
AGENTS = {
    "agy": {
        "name": "🪐 Google Antigravity (AGY)",
        "desc": "~/.gemini/antigravity-cli/skills/",
        "global_dir": Path.home() / ".gemini" / "antigravity-cli" / "skills",
        "local_dir": Path(".agent") / "skills",
        "format": "skill_dir",
    },
    "hermes": {
        "name": "🏛️  Hermes Agent (Nous)",
        "desc": "~/.hermes/skills/",
        "global_dir": Path.home() / ".hermes" / "skills",
        "local_dir": Path(".hermes") / "skills",
        "format": "categorized_dir",
    },
    "claude": {
        "name": "⚡ Claude Code (Anthropic)",
        "desc": "~/.claude/skills/",
        "global_dir": Path.home() / ".claude" / "skills",
        "local_dir": Path(".claude") / "skills",
        "format": "skill_dir",
    },
    "cursor": {
        "name": "🎯 Cursor IDE Rules (.mdc)",
        "desc": ".cursor/rules/*.mdc",
        "global_dir": Path.home() / ".cursor" / "rules",
        "local_dir": Path(".cursor") / "rules",
        "format": "cursor_mdc",
    },
    "windsurf": {
        "name": "🌊 Windsurf (Codeium)",
        "desc": ".windsurf/skills/ or memories",
        "global_dir": Path.home() / ".codeium" / "windsurf" / "memories",
        "local_dir": Path(".windsurf") / "skills",
        "format": "skill_dir",
    },
    "roo": {
        "name": "🦘 Roo Code / Cline",
        "desc": "~/.roo/skills/",
        "global_dir": Path.home() / ".roo" / "skills",
        "local_dir": Path(".roo") / "skills",
        "format": "skill_dir",
    },
    "opencode": {
        "name": "💻 OpenCode / Codex",
        "desc": "~/.config/opencode/skills/",
        "global_dir": Path.home() / ".config" / "opencode" / "skills",
        "local_dir": Path(".codex") / "rules",
        "format": "skill_dir",
    },
}

# Elite Quick-Install Skills (Most Starred & Essential)
ELITE_SKILLS = [
    "antigravity-guide",
    "awesome-skills-master",
    "context-mode",
    "frontend-design-systems",
    "hybrid-desktop-server-ops",
    "docker-single-port-multi-instance",
    "git-conventional-commits",
    "security-sast-audit",
    "playwright-browser-automation",
    "grill-me-interview",
    "watermarks-remover",
    "docx-analysis-conversion",
    "xlsx-data-wrangling",
]

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
        "title": "📦 Complete Cosmic Catalog",
        "description": "Install every skill in the awesome-skills repository",
        "categories": "ALL",
    },
}

# Open Source Repositories (Curated with OpenCurious & GitHub Stars)
OPEN_SOURCE_REPOS = [
    {"repo": "openclaw/openclaw", "stars": "100k+", "cat": "AI Agents", "desc": "Personal AI assistant for any OS (The lobster way 🦞)"},
    {"repo": "ollama/ollama", "stars": "110k+", "cat": "Local LLMs", "desc": "Run Llama 3, DeepSeek, Qwen 2.5 locally on CPU & GPU"},
    {"repo": "NousResearch/hermes-agent", "stars": "25k+", "cat": "AI Agents", "desc": "The open agent that grows with you & runs skills"},
    {"repo": "anomalyco/opencode", "stars": "20k+", "cat": "Coding Agent", "desc": "Terminal-native open-source coding agent"},
    {"repo": "Significant-Gravitas/AutoGPT", "stars": "170k+", "cat": "AI Agents", "desc": "Vision of accessible autonomous AI agents"},
    {"repo": "langflow-ai/langflow", "stars": "55k+", "cat": "Visual AI", "desc": "Visual IDE for building & orchestrating AI workflows"},
    {"repo": "langgenius/dify", "stars": "65k+", "cat": "AI Workflows", "desc": "Production-ready LLM application & agent platform"},
    {"repo": "firecrawl/firecrawl", "stars": "25k+", "cat": "Web Scraping", "desc": "Turn websites into clean LLM-ready markdown for RAG"},
    {"repo": "codecrafters-io/build-your-own-x", "stars": "320k+", "cat": "Learning", "desc": "Master programming by recreating tech from scratch"},
    {"repo": "donnemartin/system-design-primer", "stars": "280k+", "cat": "Architecture", "desc": "Design large-scale systems & interview prep"},
    {"repo": "trimstray/the-book-of-secret-knowledge", "stars": "150k+", "cat": "Security", "desc": "CLI tools, one-liners, security cheatsheets"},
    {"repo": "shadcn-ui/ui", "stars": "75k+", "cat": "Frontend", "desc": "Accessible React & Tailwind CSS component primitives"},
    {"repo": "rustdesk/rustdesk", "stars": "78k+", "cat": "Remote Desktop", "desc": "Open-source self-hosted remote desktop alternative"},
]

# Ollama Models Hub
OLLAMA_MODELS = [
    {"tag": "qwen2.5:1.5b", "size": "1.5B", "tier": "🪶 Ultra-Light", "vram": "~1.5 GB", "desc": "Ultra-fast, JSON parsing and background workers"},
    {"tag": "deepseek-r1:1.5b", "size": "1.5B", "tier": "🪶 Ultra-Light", "vram": "~1.8 GB", "desc": "Lightweight reasoning and math on pure CPU"},
    {"tag": "llama3.2:1b", "size": "1.2B", "tier": "🪶 Ultra-Light", "vram": "~1.3 GB", "desc": "Instant text classification and fast routing"},
    {"tag": "llama3.2:3b", "size": "3.2B", "tier": "🪶 Ultra-Light", "vram": "~2.8 GB", "desc": "Best lightweight balance for daily chat"},
    {"tag": "phi3.5:3.8b", "size": "3.8B", "tier": "🪶 Ultra-Light", "vram": "~3.2 GB", "desc": "Microsoft Phi-3.5 Mini - high instruction accuracy"},
    {"tag": "qwen2.5-coder:7b", "size": "7.6B", "tier": "⚡ Balanced", "vram": "~5.5 GB", "desc": "🏆 Top tier for code generation & refactoring"},
    {"tag": "deepseek-r1:7b", "size": "7.6B", "tier": "⚡ Balanced", "vram": "~6.0 GB", "desc": "Step-by-step reasoning and debugging"},
    {"tag": "llama3.1:8b", "size": "8.0B", "tier": "⚡ Balanced", "vram": "~6.2 GB", "desc": "Solid general model for diverse tasks"},
    {"tag": "gemma2:9b", "size": "9.2B", "tier": "⚡ Balanced", "vram": "~7.5 GB", "desc": "Google Gemma 2 - high synthesis quality"},
    {"tag": "mistral:7b", "size": "7.2B", "tier": "⚡ Balanced", "vram": "~5.8 GB", "desc": "Fast and direct for structured prompts"},
    {"tag": "qwen2.5-coder:14b", "size": "14.7B", "tier": "🚀 Advanced", "vram": "~10.5 GB", "desc": "Quality matching proprietary models"},
    {"tag": "deepseek-r1:14b", "size": "14.7B", "tier": "🚀 Advanced", "vram": "~11.0 GB", "desc": "Deep mathematical & algorithmic reasoning"},
    {"tag": "qwen2.5-coder:32b", "size": "32.5B", "tier": "🚀 Advanced", "vram": "~20.0 GB", "desc": "👑 State-of-the-art in software engineering"},
    {"tag": "deepseek-r1:32b", "size": "32.5B", "tier": "🚀 Advanced", "vram": "~21.0 GB", "desc": "Extreme logical reasoning for complex bugs"},
    {"tag": "command-r:35b", "size": "35.0B", "tier": "🚀 Advanced", "vram": "~22.0 GB", "desc": "Master in Tool Use function calling and RAG"},
    {"tag": "deepseek-r1:70b", "size": "70B", "tier": "🧠 Heavyweight", "vram": "~42.0 GB", "desc": "🧠 Absolute top reasoning in code and logic"},
    {"tag": "llama3.3:70b", "size": "70B", "tier": "🧠 Heavyweight", "vram": "~42.0 GB", "desc": "Meta flagship general open source model"},
    {"tag": "qwen2.5:72b", "size": "72B", "tier": "🧠 Heavyweight", "vram": "~44.0 GB", "desc": "Maximum performance in global benchmarks"},
]

# ANSI Styling (Purple / Cosmic Astronomy & Dev Theme)
ESC = "\033["
RESET = f"{ESC}0m"
BOLD = f"{ESC}1m"
DIM = f"{ESC}2m"

# Cosmic Purple Palette
PURPLE = "\033[38;5;141m"       # Soft Lavender Purple
VIOLET = "\033[38;5;99m"        # Deep Space Violet
NEBULA = "\033[38;5;183m"       # Light Nebula
MAGENTA = "\033[38;5;201m"      # Cyber Magenta
STARLIGHT = "\033[38;5;159m"    # Ice-blue Star Glow
COSMIC_GREEN = "\033[38;5;120m" # Aurora Green
GOLD_STAR = "\033[38;5;220m"    # Cosmic Gold / Coffee Crema
CYAN_DEV = "\033[38;5;87m"      # Hacker Cyan
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
    print(f"\n{GOLD_STAR}🟡 Cosmic Mission Aborted by User (ESC/Ctrl+C).{RESET}\n")
    sys.exit(0)


def ensure_tty():
    if not sys.stdin.isatty():
        try:
            sys.stdin = open("/dev/tty", "r")
        except Exception:
            pass


def getch() -> str:
    """Read a single keypress or ANSI escape sequence reliably on POSIX/Windows."""
    if os.name == "nt":
        import msvcrt
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):
            ch2 = msvcrt.getch()
            if ch2 == b"H": return "UP"
            if ch2 == b"P": return "DOWN"
            if ch2 == b"K": return "LEFT"
            if ch2 == b"M": return "RIGHT"
        if ch == b"\x1b": return "ESC"
        if ch in (b"\x08",): return "BACKSPACE"
        if ch in (b"\r", b"\n"): return "ENTER"
        if ch == b" ": return "SPACE"
        if ch == b"\x03": raise KeyboardInterrupt
        return ch.decode("utf-8", errors="ignore")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)
            try:
                rest = sys.stdin.read(10)
            except (IOError, TypeError):
                rest = ""
            finally:
                fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)

            if not rest:
                return "ESC"
            if rest in ("[A", "OA") or rest.endswith("A"): return "UP"
            elif rest in ("[B", "OB") or rest.endswith("B"): return "DOWN"
            elif rest in ("[C", "OC") or rest.endswith("C"): return "RIGHT"
            elif rest in ("[D", "OD") or rest.endswith("D"): return "LEFT"
            elif rest in ("[H", "[1~"): return "HOME"
            elif rest in ("[F", "[4~"): return "END"
            return "IGNORE"
        elif ch in ("\x7f", "\x08"):
            return "BACKSPACE"
        elif ch in ("\r", "\n"):
            return "ENTER"
        elif ch == " ":
            return "SPACE"
        elif ch == "\x03":
            raise KeyboardInterrupt
        elif ch == "\x04":
            return "EOF"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def print_banner():
    banner = f"""{PURPLE}{BOLD}
          .      *       .     (  )   (   )  )       *       .      .
    *        .       .          ) (   )  (  (     .       .      *
       .         *       .     ( )  (    ) )        .        .
   .       *   ┌───────────────────────────────┐     *      .       *
             * │   ☕  C O S M I C   B R E W   │ *       .       .
     *         └───────────────────────────────┘            *
  🪐  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗  🌌
     ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
     ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗   ⟨/⟩
     ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝    λ
     ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗  ☄️
{NEBULA}  ══════════════════════════════════════════════════════════════════════
  ✨ UNIVERSAL MULTI-AGENT CATALOG • SKILLS • MCP • PLUGINS • OLLAMA ✨
{PURPLE}  ══════════════════════════════════════════════════════════════════════{RESET}
"""
    print(banner)


def discover_skills() -> dict[str, dict[str, Path]]:
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


def tui_single_select(
    title: str,
    options: list[tuple[str, str, str]],  # (key, label, subtitle)
    default_idx: int = 0,
    allow_back: bool = False,
) -> str:
    """Interactive single-choice menu with cosmic purple aesthetics and Back support."""
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

        buf.append(f"{BOLD}{PURPLE}┌── 🪐 {title} {RESET}\n")
        lines = 1

        for idx, (key, label, sub) in enumerate(options):
            is_active = idx == cursor
            radio = f"{MAGENTA}(•){RESET}" if is_active else f"{DIM}( ){RESET}"
            ptr = f"{MAGENTA}❯{RESET}" if is_active else " "
            sub_text = f" {DIM}— {sub}{RESET}" if sub else ""

            if is_active:
                buf.append(f"  {ptr} {radio} {BOLD}{NEBULA}{label}{RESET}{sub_text}{ESC}K\n")
            else:
                buf.append(f"  {ptr} {radio} {WHITE}{label}{RESET}{sub_text}{ESC}K\n")
            lines += 1

        back_hint = " | b/←: Back" if allow_back else ""
        footer = f"{DIM}└── [↑/↓/j/k: Orbit | Enter: Confirm{back_hint} | Esc/q: Abort]{RESET}"
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
            elif allow_back and key in ("b", "B", "LEFT", "BACKSPACE"):
                print()
                return "__BACK__"
            elif key in ("ESC", "q", "Q", "EOF"):
                cancel_and_exit()
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

    print()
    return options[cursor][0]


def tui_multiselect(
    title: str,
    options: list[tuple[str, str, str]],  # (key, label, subtitle)
    default_selected: list[str] | None = None,
    allow_empty: bool = False,
    allow_back: bool = False,
) -> list[str] | str:
    """Interactive multi-select menu with STRICT selection validation, Back support & purple styling."""
    if not sys.stdin.isatty():
        return [opt[0] for opt in options] if default_selected is None else default_selected

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    selected = set(default_selected if default_selected is not None else [options[0][0]])
    cursor = 0
    num_opts = len(options)
    lines_rendered = 0
    warning_msg = ""

    def render():
        nonlocal lines_rendered
        buf = []
        if lines_rendered > 0:
            buf.append(f"{ESC}{lines_rendered}F")

        buf.append(f"{BOLD}{PURPLE}┌── 🌌 {title} {RESET}\n")
        lines = 1

        for idx, (key, label, sub) in enumerate(options):
            is_active = idx == cursor
            is_checked = key in selected
            box = f"{COSMIC_GREEN}[✔]{RESET}" if is_checked else f"{DIM}[ ]{RESET}"
            ptr = f"{MAGENTA}❯{RESET}" if is_active else " "

            sub_text = f" {DIM}({sub}){RESET}" if sub else ""
            if is_active:
                buf.append(f"  {ptr} {box} {BOLD}{NEBULA}{label}{RESET}{sub_text}{ESC}K\n")
            else:
                buf.append(f"  {ptr} {box} {WHITE}{label}{RESET}{sub_text}{ESC}K\n")
            lines += 1

        if warning_msg:
            buf.append(f"  {GOLD_STAR}⚠️  {warning_msg}{RESET}{ESC}K\n")
            lines += 1

        back_hint = " | b/←: Back" if allow_back else ""
        footer = f"{DIM}└── [↑/↓/j/k: Orbit | Space: Toggle | a: All | Enter: Confirm{back_hint} | Esc/q: Abort]{RESET}"
        buf.append(f"{footer}{ESC}K\n")
        lines += 1

        lines_rendered = lines
        sys.stdout.write("".join(buf))
        sys.stdout.flush()

    try:
        while True:
            render()
            key = getch()
            warning_msg = ""
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
                if not selected and not allow_empty:
                    warning_msg = "Mission Check Required: Please select at least one item using [Space] before launching!"
                elif selected or allow_empty:
                    break
            elif allow_back and key in ("b", "B", "LEFT", "BACKSPACE"):
                print()
                return "__BACK__"
            elif key in ("ESC", "q", "Q", "EOF"):
                cancel_and_exit()
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

    print()
    return [opt[0] for opt in options if opt[0] in selected]


def tui_skill_browser(
    all_skills: list[dict],
    default_selected_names: set[str] | None = None,
    allow_back: bool = True,
) -> list[tuple[str, str, Path]] | str:
    """Interactive Skill-by-Skill browser with viewport scrolling, search, and Back support."""
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

    selected_names = set(default_selected_names if default_selected_names is not None else [])
    cursor = 0
    page_size = 10
    lines_rendered = 0
    warning_msg = ""

    try:
        while True:
            items = get_filtered_skills()
            if not items:
                items = all_skills
                search_query = ""

            num_items = len(items)
            cursor = max(0, min(cursor, num_items - 1))

            start_idx = max(0, min(cursor - page_size // 2, num_items - page_size))
            end_idx = min(start_idx + page_size, num_items)
            visible_items = items[start_idx:end_idx]
            focused = items[cursor]

            buf = []
            if lines_rendered > 0:
                buf.append(f"{ESC}{lines_rendered}F")

            header = f"{BOLD}{PURPLE}┌── 🎯 Cosmic Skill Observatory [Selected: {len(selected_names)}/{len(all_skills)}] {RESET}"
            if search_query:
                header += f" {GOLD_STAR}(Filter: '{search_query}'){RESET}"
            buf.append(f"{header}{ESC}K\n")
            lines = 1

            for rel_i, item in enumerate(visible_items):
                abs_i = start_idx + rel_i
                is_active = abs_i == cursor
                is_checked = item["name"] in selected_names

                box = f"{COSMIC_GREEN}[✔]{RESET}" if is_checked else f"{DIM}[ ]{RESET}"
                ptr = f"{MAGENTA}❯{RESET}" if is_active else " "

                name_fmt = f"{BOLD}{NEBULA}{item['name']:<28}{RESET}" if is_active else f"{WHITE}{item['name']:<28}{RESET}"
                cat_fmt = f"{PURPLE}[{item['category']}]{RESET}"
                author_fmt = f"{DIM}by {item['author'][:18]}{RESET}"

                buf.append(f"  {ptr} {box} {name_fmt} {cat_fmt:<32} {author_fmt}{ESC}K\n")
                lines += 1

            sort_label = f"Sort: {sort_modes[sort_idx].capitalize()}"
            scroll_info = f"Observing {start_idx+1}-{end_idx} of {num_items} skills [{sort_label}]"
            buf.append(f"  {DIM}── {scroll_info} ──{RESET}{ESC}K\n")
            lines += 1

            if warning_msg:
                buf.append(f"  {GOLD_STAR}⚠️  {warning_msg}{RESET}{ESC}K\n")
                lines += 1

            desc_wrapped = focused["desc"][:160] + "..." if len(focused["desc"]) > 160 else focused["desc"]
            buf.append(f"{BOLD}{VIOLET}┌─ 🔭 Skill Astrophysics & Telemetry ────────────────────────────────{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Orbit/Name:{RESET}        {NEBULA}{focused['name']}{RESET} ({CYAN_DEV}{focused['category']}{RESET}){ESC}K\n")
            buf.append(f"│ {BOLD}Astronomer/Author:{RESET} {WHITE}{focused['author']}{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Blueprint/Desc:{RESET}    {DIM}{desc_wrapped}{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Telemetry/URL:{RESET}     {STARLIGHT}{focused['github_url']}{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Constellation:{RESET}     ⭐ {GOLD_STAR}pedroiff0/awesome-skills{RESET} | MIT License{ESC}K\n")
            buf.append(f"{BOLD}{VIOLET}└────────────────────────────────────────────────────────────────────{RESET}{ESC}K\n")
            lines += 7

            back_hint = " | b/←: Back" if allow_back else ""
            footer = f"{DIM}└── [↑/↓/j/k: Orbit | Space: Toggle | a: All | /: Search | s: Sort | Enter: Confirm{back_hint} | Esc: Abort]{RESET}"
            buf.append(f"{footer}{ESC}K\n")
            lines += 1

            lines_rendered = lines
            sys.stdout.write("".join(buf))
            sys.stdout.flush()

            key = getch()
            warning_msg = ""
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
                sys.stdout.write(f"\n{BOLD}{GOLD_STAR}Filter skills by keyword (Enter to clear): {RESET}")
                sys.stdout.flush()
                try:
                    search_query = input().strip()
                except (EOFError, KeyboardInterrupt):
                    search_query = ""
                cursor = 0
                lines_rendered = 0
                sys.stdout.write(HIDE_CURSOR)
            elif key == "ENTER":
                if not selected_names:
                    warning_msg = "Please check at least one skill using [Space] before confirming!"
                else:
                    break
            elif allow_back and key in ("b", "B", "LEFT", "BACKSPACE"):
                print()
                return "__BACK__"
            elif key in ("ESC", "q", "Q", "EOF"):
                cancel_and_exit()
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

    print()
    return [(s["category"], s["name"], s["path"]) for s in all_skills if s["name"] in selected_names]


def run_uninstaller():
    """Interactive uninstaller to safely clean installed skills across agents with Back navigation."""
    ensure_tty()
    print(f"\n{BOLD}{PURPLE}┌── 🗑️  Awesome Skills Uninstaller & De-Orbiter {RESET}")
    print(f"{DIM}Select which agent environments you want to inspect and clean:{RESET}\n")

    step = 1
    target_agents = ["agy", "claude", "hermes", "cursor"]
    scope_choice = "global"

    while True:
        if step == 1:
            agent_opts = [(k, v["name"], v["desc"]) for k, v in AGENTS.items()]
            res = tui_multiselect("Select Agent(s) to Clean", agent_opts, default_selected=target_agents, allow_back=True)
            if res == "__BACK__":
                return
            target_agents = res
            step = 2
            continue

        elif step == 2:
            scope_opts = [
                ("global", "Global User Profile (~)", "Scans ~/.<agent>/skills/ and ~/.cursor/rules/"),
                ("local", "Local Workspace Repository (.)", "Scans .agent/skills/, .cursor/rules/, .claude/skills/"),
            ]
            res = tui_single_select("Choose Uninstallation Scope", scope_opts, default_idx=0 if scope_choice == "global" else 1, allow_back=True)
            if res == "__BACK__":
                step = 1
                continue
            scope_choice = res
            step = 3
            continue

        elif step == 3:
            found_entries = []
            for agent_key in target_agents:
                agent_info = AGENTS[agent_key]
                target_dir = agent_info["global_dir"] if scope_choice == "global" else agent_info["local_dir"]
                if not target_dir.exists():
                    continue

                if agent_info["format"] == "cursor_mdc":
                    for mdc in target_dir.glob("*.mdc"):
                        found_entries.append((f"{agent_key}:{mdc.name}", f"{mdc.name} ({agent_info['name']})", str(mdc), agent_key, mdc))
                elif agent_info["format"] == "categorized_dir":
                    for skill_dir in target_dir.glob("*/*"):
                        if skill_dir.is_dir() or skill_dir.is_symlink():
                            found_entries.append((f"{agent_key}:{skill_dir.name}", f"{skill_dir.name} [{skill_dir.parent.name}] ({agent_info['name']})", str(skill_dir), agent_key, skill_dir))
                else:
                    for skill_dir in target_dir.glob("*"):
                        if skill_dir.is_dir() or skill_dir.is_symlink():
                            found_entries.append((f"{agent_key}:{skill_dir.name}", f"{skill_dir.name} ({agent_info['name']})", str(skill_dir), agent_key, skill_dir))

            if not found_entries:
                print(f"\n{COSMIC_GREEN}✔ Clean orbit! No installed skills or rules found in the selected locations.{RESET}\n")
                return

            entry_opts = [(e[0], e[1], e[2]) for e in found_entries]
            res = tui_multiselect(
                f"Found {len(found_entries)} installed skill(s)/rule(s). Select items to REMOVE:",
                entry_opts,
                default_selected=[],
                allow_back=True,
            )
            if res == "__BACK__":
                step = 2
                continue

            selected_keys = res
            if not selected_keys:
                print(f"{GOLD_STAR}No items selected for removal.{RESET}")
                return

            print(f"\n{BOLD}{GOLD_STAR}⚠️  Removing {len(selected_keys)} item(s)...{RESET}\n")
            removed_count = 0
            for key in selected_keys:
                for entry in found_entries:
                    if entry[0] == key:
                        path_obj: Path = entry[4]
                        try:
                            if path_obj.is_symlink() or path_obj.is_file():
                                path_obj.unlink()
                            elif path_obj.is_dir():
                                shutil.rmtree(path_obj)
                            print(f"  {COSMIC_GREEN}✔ De-orbited:{RESET} {path_obj}")
                            removed_count += 1
                        except Exception as e:
                            print(f"  {GOLD_STAR}Error removing {path_obj}: {e}{RESET}")

            print(f"\n{COSMIC_GREEN}{BOLD}🎉 Uninstallation Complete! Removed {removed_count} skill(s)/rule(s).{RESET}\n")
            return


def run_open_source_cloner():
    """Interactive Open Source Repositories Cloner Hub with Back support."""
    ensure_tty()
    print(f"\n{BOLD}{PURPLE}┌── 🌐 Open Source Repositories Hub (Curated via OpenCurious & GitHub Stars) {RESET}")
    print(f"{DIM}Select repositories to clone locally to your workspace:{RESET}\n")

    repo_opts = [
        (r["repo"], f"{r['repo']:<35} ⭐ {r['stars']:<7} [{r['cat']}]", r["desc"])
        for r in OPEN_SOURCE_REPOS
    ]
    selected_repos = tui_multiselect("Select Open Source Repositories to Clone", repo_opts, default_selected=[repo_opts[0][0]], allow_back=True)

    if selected_repos == "__BACK__" or not selected_repos:
        return

    try:
        dest_dir_input = input(f"{GOLD_STAR}Target destination directory [default: ./open-source] (b to back): {RESET}").strip()
    except (EOFError, KeyboardInterrupt):
        cancel_and_exit()

    if dest_dir_input.lower() in ("b", "back"):
        return run_open_source_cloner()

    dest_base = Path(dest_dir_input if dest_dir_input else "./open-source").resolve()
    dest_base.mkdir(parents=True, exist_ok=True)

    print(f"\n{BOLD}{PURPLE}Cloning {len(selected_repos)} repository(ies) to {dest_base}...{RESET}\n")
    for r in selected_repos:
        repo_name = r.split("/")[1]
        target_path = dest_base / repo_name
        if target_path.exists():
            print(f"  {GOLD_STAR}• {r} already exists at {target_path}. Updating via git pull...{RESET}")
            subprocess.run(["git", "-C", str(target_path), "pull", "--ff-only"], capture_output=True)
        else:
            print(f"  {NEBULA}• Cloning https://github.com/{r}.git...{RESET}")
            subprocess.run(["git", "clone", "--depth", "1", f"https://github.com/{r}.git", str(target_path)])
        print(f"  {COSMIC_GREEN}✔ Ready: {r}{RESET}\n")

    print(f"{COSMIC_GREEN}{BOLD}🎉 Open source repositories cloned successfully!{RESET}\n")


def run_ollama_manager():
    """Interactive Ollama Open Source Models Manager with Back support."""
    ensure_tty()
    print(f"\n{BOLD}{PURPLE}┌── 🦙 Ollama Open Source Models Catalog (Lightweight to Heavyweight) {RESET}")
    print(f"{DIM}High-performance local LLMs for coding, refactoring, and deep reasoning:{RESET}\n")

    model_opts = [
        (m["tag"], f"{m['tag']:<24} {m['tier']:<16} ({m['size']}, VRAM {m['vram']})", m["desc"])
        for m in OLLAMA_MODELS
    ]
    selected_models = tui_multiselect("Select Ollama Models to Download / Pull", model_opts, default_selected=["qwen2.5-coder:7b", "deepseek-r1:1.5b"], allow_back=True)

    if selected_models == "__BACK__" or not selected_models:
        return

    has_ollama = shutil.which("ollama") is not None

    if has_ollama:
        print(f"\n{BOLD}{PURPLE}🚀 Pulling {len(selected_models)} model(s) via Ollama...{RESET}\n")
        for tag in selected_models:
            print(f"  {BOLD}Running:{RESET} {GOLD_STAR}ollama pull {tag}{RESET}")
            subprocess.run(["ollama", "pull", tag])
            print(f"  {COSMIC_GREEN}✔ Model {tag} is ready for local inference!{RESET}\n")
    else:
        print(f"\n{GOLD_STAR}{BOLD}Notice:{RESET} 'ollama' command was not found in your system PATH.")
        print(f"To install Ollama, visit: {NEBULA}https://ollama.com/{RESET}\n")
        print(f"{BOLD}Commands to run once Ollama is installed:{RESET}")
        for tag in selected_models:
            print(f"  {NEBULA}ollama run {tag}{RESET}")
        print()


def run_quick_install_flow(catalog: dict, all_skills_flat: list[dict], agents_dict: dict) -> str | None:
    """Quick Install workflow with full step-by-step verification and Back navigation."""
    step = 1
    selected_agents = ["agy", "claude", "hermes", "cursor"]
    elite_items = [s for s in all_skills_flat if s["name"] in ELITE_SKILLS]
    selected_skill_names = [s["name"] for s in elite_items]

    while True:
        if step == 1:
            agent_opts = [(k, v["name"], v["desc"]) for k, v in agents_dict.items()]
            res = tui_multiselect(
                "Quick Install - Step 1/2: Verify Target Agent(s) to Equip",
                agent_opts,
                default_selected=selected_agents,
                allow_back=True,
            )
            if res == "__BACK__":
                return "__BACK__"
            selected_agents = res
            step = 2
            continue

        elif step == 2:
            elite_opts = [(s["name"], f"{s['name']:<30} [{s['category']}]", f"by {s['author']}") for s in elite_items]
            res = tui_multiselect(
                "Quick Install - Step 2/2: Verify Elite Skills to Install",
                elite_opts,
                default_selected=selected_skill_names,
                allow_back=True,
            )
            if res == "__BACK__":
                step = 1
                continue
            selected_skill_names = res
            break

    skills_to_install = []
    for s in elite_items:
        if s["name"] in selected_skill_names:
            skills_to_install.append((s["category"], s["name"], s["path"]))

    print(f"\n{BOLD}{PURPLE}🚀 Launching Quick Install: {len(skills_to_install)} skill(s) into {len(selected_agents)} agent(s)...{RESET}\n")

    for agent_key in selected_agents:
        if agent_key not in agents_dict:
            continue
        agent_info = agents_dict[agent_key]
        target_dir = agent_info["global_dir"]
        print(f"  {BOLD}Configuring {agent_info['name']}{RESET} -> {DIM}{target_dir}{RESET}")
        installed_count = 0
        for cat, name, path in skills_to_install:
            if install_skill_to_target(path, cat, name, agent_key, target_dir, use_symlink=True):
                installed_count += 1
        print(f"  {COSMIC_GREEN}✔ Installed {installed_count} skill(s) into {agent_info['name']}{RESET}\n")

    print(f"{PURPLE}{BOLD}══════════════════════════════════════════════════════════════════════{RESET}")
    print(f"  {COSMIC_GREEN}{BOLD}🎉 Orbit Achieved! Quick Install Completed Successfully!{RESET}")
    print(f"  {WHITE}Skills are active and ready for prompt triggers in your AI agents.{RESET}")
    print(f"{PURPLE}{BOLD}══════════════════════════════════════════════════════════════════════{RESET}\n")
    return None


def convert_skill_to_cursor_mdc(skill_path: Path, target_dir: Path, skill_name: str):
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
        else:
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
        print(f"{GOLD_STAR}Warning installing {skill_name} to {agent_key}: {e}{RESET}")
        return False


def run_interactive():
    ensure_tty()
    print_banner()

    catalog = discover_skills()
    total_skills = sum(len(s) for s in catalog.values())
    total_cats = len(catalog)

    all_skills_flat = []
    for cat, sks in catalog.items():
        for name, path in sks.items():
            fm = parse_frontmatter(path / "SKILL.md")
            author = fm.get("author") or "Open Source Community"
            desc = fm.get("description") or f"Reusable {name} skill"
            all_skills_flat.append({
                "name": name,
                "category": cat,
                "path": path,
                "author": author,
                "desc": desc,
                "github_url": f"{GITHUB_BASE_URL}/{cat}/{name}",
            })

    print(f"  {BOLD}Active Constellation:{RESET} {COSMIC_GREEN}{total_skills} skills{RESET} in {PURPLE}{total_cats} categories{RESET} • {MAGENTA}2 plugins{RESET} • {GOLD_STAR}4 MCP servers{RESET}.\n")

    # State variables for Back navigation
    step = 0
    step0_idx = 0
    selected_agents = ["agy", "claude", "hermes"]
    selected_scope = "global"
    selected_mode = "skill_by_skill"
    selected_cats = []
    selected_skill_names_set = set()
    selected_method = "symlink"
    skills_to_install: list[tuple[str, str, Path]] = []

    while True:
        # =====================================================================
        # STEP 0: Workflow Selection
        # =====================================================================
        if step == 0:
            step0_opts = [
                ("quick", "🚀 Quick Install (Curated Elite Pack)", "Verify and install top 13 starred essential skills & MCPs for selected agents"),
                ("manual", "⚙️  Custom / Manual Setup (Interactive Wizard)", "Choose agents, scope, skill-by-skill, categories, plugins & packs"),
                ("uninstall", "🗑️  Uninstall / Clean Installed Skills", "Scan and safely remove installed skills/rules across agents"),
                ("open_source", "🌐 Explore & Clone Open-Source Repositories", "Curated top-starred GitHub repos via OpenCurious"),
                ("ollama", "🦙 Open-Source Models for Ollama", "Local models from ultra-lightweight (1.5B) to heavy reasoning (70B+)"),
            ]
            step0_choice = tui_single_select("Step 0: Choose Installation Workflow", step0_opts, default_idx=step0_idx, allow_back=False)
            step0_idx = [opt[0] for opt in step0_opts].index(step0_choice)

            if step0_choice == "uninstall":
                run_uninstaller()
                continue
            elif step0_choice == "open_source":
                run_open_source_cloner()
                continue
            elif step0_choice == "ollama":
                run_ollama_manager()
                continue
            elif step0_choice == "quick":
                res = run_quick_install_flow(catalog, all_skills_flat, AGENTS)
                if res == "__BACK__":
                    continue
                return
            elif step0_choice == "manual":
                step = 1
                continue

        # =====================================================================
        # STEP 1: Target Agents
        # =====================================================================
        elif step == 1:
            agent_opts = [(k, v["name"], v["desc"]) for k, v in AGENTS.items()]
            res = tui_multiselect(
                "Step 1: Select Target Agent(s) to Equip",
                agent_opts,
                default_selected=selected_agents,
                allow_back=True,
            )
            if res == "__BACK__":
                step = 0
                continue
            selected_agents = res
            step = 2
            continue

        # =====================================================================
        # STEP 2: Installation Scope
        # =====================================================================
        elif step == 2:
            scope_opts = [
                ("global", "Global User Profile", "Installed in ~/.<agent> — available across all projects"),
                ("local", "Local Workspace Repository", "Installed in .agent/ or .cursor/ — scoped to current project"),
            ]
            default_scope_idx = 0 if selected_scope == "global" else 1
            res = tui_single_select("Step 2: Choose Installation Scope", scope_opts, default_idx=default_scope_idx, allow_back=True)
            if res == "__BACK__":
                step = 1
                continue
            selected_scope = res
            step = 3
            continue

        # =====================================================================
        # STEP 3: Which Skills
        # =====================================================================
        elif step == 3:
            mode_opts = [
                ("skill_by_skill", "🎯 Browse & Select Skill by Skill (Full Catalog)", "Inspect metadata, author, GitHub link, stars, and pick individually"),
                ("pack_fullstack", PACKS["fullstack"]["title"], PACKS["fullstack"]["description"]),
                ("pack_devops", PACKS["devops"]["title"], PACKS["devops"]["description"]),
                ("pack_ai", PACKS["ai"]["title"], PACKS["ai"]["description"]),
                ("pack_academic", PACKS["academic"]["title"], PACKS["academic"]["description"]),
                ("pack_creative", PACKS["creative"]["title"], PACKS["creative"]["description"]),
                ("pack_all", PACKS["all"]["title"], f"All {total_skills} skills across {total_cats} categories"),
                ("categories", "🗂️  Select by Category", "Choose entire categories from a list"),
            ]
            mode_keys = [m[0] for m in mode_opts]
            default_mode_idx = mode_keys.index(selected_mode) if selected_mode in mode_keys else 0
            res = tui_single_select("Step 3: Which Skills would you like to install?", mode_opts, default_idx=default_mode_idx, allow_back=True)
            if res == "__BACK__":
                step = 2
                continue
            selected_mode = res

            if selected_mode == "skill_by_skill":
                browser_res = tui_skill_browser(all_skills_flat, default_selected_names=selected_skill_names_set, allow_back=True)
                if browser_res == "__BACK__":
                    continue
                skills_to_install = browser_res
                selected_skill_names_set = set(s[1] for s in skills_to_install)

            elif selected_mode.startswith("pack_"):
                pack_key = selected_mode.replace("pack_", "")
                pack_cats = PACKS[pack_key]["categories"]
                skills_to_install = []
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
                chosen_cats = tui_multiselect("Select Desired Categories", cat_opts, default_selected=selected_cats or [cat_opts[0][0]], allow_back=True)
                if chosen_cats == "__BACK__":
                    continue
                selected_cats = chosen_cats
                skills_to_install = []
                for cat in selected_cats:
                    for name, path in catalog[cat].items():
                        skills_to_install.append((cat, name, path))

            step = 4
            continue

        # =====================================================================
        # STEP 4: Method & Execution
        # =====================================================================
        elif step == 4:
            method_opts = [
                ("symlink", "Symlink (Dynamic Link)", "Auto-updates dynamically on git pull"),
                ("copy", "Direct File Copy", "Independent snapshot clone"),
            ]
            default_method_idx = 0 if selected_method == "symlink" else 1
            res = tui_single_select("Step 4: Choose Installation Method", method_opts, default_idx=default_method_idx, allow_back=True)
            if res == "__BACK__":
                step = 3
                continue
            selected_method = res
            use_symlink = selected_method == "symlink"
            break

    if not skills_to_install:
        print(f"\n{GOLD_STAR}No skills selected for installation.{RESET}")
        return

    # Execute
    print(f"\n{BOLD}{PURPLE}🚀 Launching payload: {len(skills_to_install)} skill(s) into {len(selected_agents)} agent(s)...{RESET}\n")

    for agent_key in selected_agents:
        if agent_key not in AGENTS:
            continue
        agent_info = AGENTS[agent_key]
        target_dir = agent_info["global_dir"] if selected_scope == "global" else agent_info["local_dir"]
        print(f"  {BOLD}Configuring {agent_info['name']}{RESET} -> {DIM}{target_dir}{RESET}")
        installed_count = 0
        for cat, name, path in skills_to_install:
            if install_skill_to_target(path, cat, name, agent_key, target_dir, use_symlink=use_symlink):
                installed_count += 1
        print(f"  {COSMIC_GREEN}✔ Installed {installed_count} skill(s) into {agent_info['name']}{RESET}\n")

    print(f"{PURPLE}{BOLD}══════════════════════════════════════════════════════════════════════{RESET}")
    print(f"  {COSMIC_GREEN}{BOLD}🎉 Orbit Achieved! Installation Completed Successfully!{RESET}")
    print(f"  {WHITE}Skills are active and ready for prompt triggers in your AI agents.{RESET}")
    print(f"{PURPLE}{BOLD}══════════════════════════════════════════════════════════════════════{RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        prog="awesome-skills installer",
        description="Universal Multi-Agent Skill Installer for awesome-skills (Cosmic Purple Dev Edition)",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick install elite pack for all detected agents",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Uninstall / clean installed skills across agents",
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
    parser.add_argument(
        "--repos",
        action="store_true",
        help="List curated open source repositories from OpenCurious",
    )
    parser.add_argument(
        "--ollama",
        action="store_true",
        help="List curated Ollama open-source models",
    )

    args = parser.parse_args()
    catalog = discover_skills()

    if args.uninstall:
        run_uninstaller()
        return

    if args.repos:
        print_banner()
        print(f"{BOLD}{PURPLE}=== Featured Open Source Repositories (via OpenCurious & GitHub Stars) ==={RESET}\n")
        for r in OPEN_SOURCE_REPOS:
            print(f"  • {BOLD}{r['repo']:<35}{RESET} ⭐ {r['stars']:<7} [{r['cat']}] — {r['desc']}")
        return

    if args.ollama:
        print_banner()
        print(f"{BOLD}{PURPLE}=== Open Source Ollama Models Catalog (Lightweight to Heavyweight) ==={RESET}\n")
        for m in OLLAMA_MODELS:
            print(f"  • {BOLD}{m['tag']:<24}{RESET} {m['tier']:<16} ({m['size']}, VRAM {m['vram']}) — {m['desc']}")
        return

    if args.list:
        print_banner()
        for cat, sks in sorted(catalog.items()):
            print(f"\n{BOLD}{PURPLE}=== {cat} ({len(sks)} skills) ==={RESET}")
            for name, path in sorted(sks.items()):
                fm = parse_frontmatter(path / "SKILL.md")
                author = fm.get("author", "Open Source Community")
                desc = fm.get("description", "")
                print(f"  • {BOLD}{name}{RESET} (by {author}): {desc[:80]}{'...' if len(desc)>80 else ''}")
        return

    if args.quick:
        skills_to_install = []
        for cat, sks in catalog.items():
            for name, path in sks.items():
                if name in ELITE_SKILLS:
                    skills_to_install.append((cat, name, path))
        target_agents = ["agy", "claude", "hermes", "cursor"]
        for agent_key in target_agents:
            agent_info = AGENTS[agent_key]
            target_dir = agent_info["global_dir"] if args.scope == "global" else agent_info["local_dir"]
            for cat, name, path in skills_to_install:
                install_skill_to_target(path, cat, name, agent_key, target_dir, use_symlink=not args.copy)
            print(f"✔ Quick installed {len(skills_to_install)} skills to {agent_info['name']}")
        return

    if args.agent or args.pack or args.category or args.skills:
        selected_agents = list(AGENTS.keys()) if args.agent == "all" else (args.agent.split(",") if args.agent else ["agy"])
        use_symlink = not args.copy
        skills_to_install = []

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
