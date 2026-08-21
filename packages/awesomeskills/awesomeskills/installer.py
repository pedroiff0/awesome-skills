#!/usr/bin/env python3
"""Universal Multi-Agent Skills Installer for awesome-skills (Cosmic Purple Dev Edition).

Features:
- Standardized Checkbox Selection Pattern [✔] across ALL steps.
- Arrow Key Step Navigation: '←' (Left Arrow / b) to GO BACK, '→' (Right Arrow / Enter) to ADVANCE.
- 4-Tier Local AI Models Registry (Leve, Intermediário, Pesado, DataCenter) with direct ollama.com links.
- 6-Category Open-Source Repositories Hub curated via OpenCurious (17,000+ repos directory).
- Clickable Terminal Hyperlinks (OSC 8 + explicit URLs) for Skills, Repositories, and Ollama Models.
- Aesthetic Purple, Astronomy & Developer Theme with Cosmic Coffee intro ☕ 🪐 🌌.
- Step 0: Quick Install, Custom Manual Setup, Uninstall, Open-Source Hub, and Ollama Hub.
- Strict selection validation: Users CANNOT proceed with 0 items selected.
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

# Categorized Open Source Repositories Hub (Curated via OpenCurious)
REPO_CATEGORIES = {
    "AI & Autonomous Agents": [
        {"repo": "openclaw/openclaw", "url": "https://github.com/openclaw/openclaw", "stars": "100k+", "desc": "Personal AI assistant for any OS & platform (The lobster way 🦞)"},
        {"repo": "ollama/ollama", "url": "https://github.com/ollama/ollama", "stars": "110k+", "desc": "Run Llama 3, DeepSeek, Qwen 2.5 locally on CPU & GPU"},
        {"repo": "Significant-Gravitas/AutoGPT", "url": "https://github.com/Significant-Gravitas/AutoGPT", "stars": "170k+", "desc": "Vision of accessible autonomous AI agents for everyone"},
        {"repo": "huggingface/transformers", "url": "https://github.com/huggingface/transformers", "stars": "135k+", "desc": "State-of-the-art ML framework for PyTorch, JAX & TensorFlow"},
        {"repo": "NousResearch/hermes-agent", "url": "https://github.com/NousResearch/hermes-agent", "stars": "25k+", "desc": "The open agent that grows with you & runs canonical skills"},
        {"repo": "anthropics/claude-code", "url": "https://github.com/anthropics/claude-code", "stars": "45k+", "desc": "Agentic coding CLI tool living in your terminal"},
        {"repo": "anomalyco/opencode", "url": "https://github.com/anomalyco/opencode", "stars": "20k+", "desc": "Terminal-native open-source coding agent"},
        {"repo": "obra/superpowers", "url": "https://github.com/obra/superpowers", "stars": "30k+", "desc": "Agentic skills framework & software development methodology"},
        {"repo": "langflow-ai/langflow", "url": "https://github.com/langflow-ai/langflow", "stars": "55k+", "desc": "Visual IDE for building & orchestrating AI workflows"},
        {"repo": "langgenius/dify", "url": "https://github.com/langgenius/dify", "stars": "65k+", "desc": "Production-ready LLM application & agent platform"},
        {"repo": "open-webui/open-webui", "url": "https://github.com/open-webui/open-webui", "stars": "75k+", "desc": "User-friendly AI web UI supporting Ollama and OpenAI APIs"},
        {"repo": "firecrawl/firecrawl", "url": "https://github.com/firecrawl/firecrawl", "stars": "25k+", "desc": "Turn websites into clean LLM-ready markdown for RAG"},
        {"repo": "langchain-ai/langchain", "url": "https://github.com/langchain-ai/langchain", "stars": "95k+", "desc": "The agent engineering and context orchestration platform"},
        {"repo": "ggml-org/llama.cpp", "url": "https://github.com/ggml-org/llama.cpp", "stars": "70k+", "desc": "Port of LLMs in pure C/C++ with GPU acceleration"},
        {"repo": "AUTOMATIC1111/stable-diffusion-webui", "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui", "stars": "140k+", "desc": "Browser interface for Stable Diffusion image generation"},
        {"repo": "Comfy-Org/ComfyUI", "url": "https://github.com/Comfy-Org/ComfyUI", "stars": "60k+", "desc": "Modular node graph UI for Stable Diffusion and Flux"},
    ],
    "Developer Tools & Architecture": [
        {"repo": "codecrafters-io/build-your-own-x", "url": "https://github.com/codecrafters-io/build-your-own-x", "stars": "320k+", "desc": "Master programming by recreating tech from scratch"},
        {"repo": "donnemartin/system-design-primer", "url": "https://github.com/donnemartin/system-design-primer", "stars": "280k+", "desc": "Design large-scale systems & tech interview prep"},
        {"repo": "trimstray/the-book-of-secret-knowledge", "url": "https://github.com/trimstray/the-book-of-secret-knowledge", "stars": "150k+", "desc": "CLI tools, one-liners, security cheatsheets and hacks"},
        {"repo": "microsoft/vscode", "url": "https://github.com/microsoft/vscode", "stars": "165k+", "desc": "Visual Studio Code editor engine"},
        {"repo": "ohmyzsh/ohmyzsh", "url": "https://github.com/ohmyzsh/ohmyzsh", "stars": "175k+", "desc": "Community-driven framework for managing Zsh configs"},
        {"repo": "n8n-io/n8n", "url": "https://github.com/n8n-io/n8n", "stars": "55k+", "desc": "Workflow automation platform with native AI integrations"},
        {"repo": "excalidraw/excalidraw", "url": "https://github.com/excalidraw/excalidraw", "stars": "85k+", "desc": "Virtual collaborative whiteboard for sketching hand-drawn diagrams"},
        {"repo": "microsoft/markitdown", "url": "https://github.com/microsoft/markitdown", "stars": "35k+", "desc": "Python tool for converting office documents & PDFs to Markdown"},
    ],
    "Web Frontend & UI Systems": [
        {"repo": "shadcn-ui/ui", "url": "https://github.com/shadcn-ui/ui", "stars": "75k+", "desc": "Accessible React & Tailwind CSS component primitives"},
        {"repo": "vercel/next.js", "url": "https://github.com/vercel/next.js", "stars": "125k+", "desc": "The React Framework for the Web with App Router & SSR"},
        {"repo": "facebook/react", "url": "https://github.com/facebook/react", "stars": "230k+", "desc": "The library for web and native user interfaces"},
        {"repo": "vuejs/vue", "url": "https://github.com/vuejs/vue", "stars": "207k+", "desc": "Progressive JavaScript framework for building UIs"},
        {"repo": "mrdoob/three.js", "url": "https://github.com/mrdoob/three.js", "stars": "102k+", "desc": "JavaScript 3D WebGL library"},
        {"repo": "electron/electron", "url": "https://github.com/electron/electron", "stars": "115k+", "desc": "Build cross-platform desktop apps with JS, HTML, and CSS"},
    ],
    "Backend, Cloud & DevOps": [
        {"repo": "kubernetes/kubernetes", "url": "https://github.com/kubernetes/kubernetes", "stars": "110k+", "desc": "Production-grade container scheduling & management"},
        {"repo": "torvalds/linux", "url": "https://github.com/torvalds/linux", "stars": "180k+", "desc": "Linux kernel source tree"},
        {"repo": "rustdesk/rustdesk", "url": "https://github.com/rustdesk/rustdesk", "stars": "78k+", "desc": "Open-source self-hosted remote desktop software"},
        {"repo": "tauri-apps/tauri", "url": "https://github.com/tauri-apps/tauri", "stars": "85k+", "desc": "Build smaller, faster desktop & mobile apps with Rust"},
        {"repo": "denoland/deno", "url": "https://github.com/denoland/deno", "stars": "95k+", "desc": "Modern JavaScript and TypeScript runtime"},
        {"repo": "public-apis/public-apis", "url": "https://github.com/public-apis/public-apis", "stars": "310k+", "desc": "Collective list of free APIs for software development"},
    ],
    "Learning, Roadmaps & CS": [
        {"repo": "sindresorhus/awesome", "url": "https://github.com/sindresorhus/awesome", "stars": "340k+", "desc": "Curated awesome lists about all kinds of interesting topics"},
        {"repo": "nilbuild/developer-roadmap", "url": "https://github.com/nilbuild/developer-roadmap", "stars": "290k+", "desc": "Interactive roadmaps & career guides for developers"},
        {"repo": "jwasham/coding-interview-university", "url": "https://github.com/jwasham/coding-interview-university", "stars": "300k+", "desc": "Complete computer science study plan to become a software engineer"},
        {"repo": "EbookFoundation/free-programming-books", "url": "https://github.com/EbookFoundation/free-programming-books", "stars": "330k+", "desc": "Freely available programming books in all languages"},
        {"repo": "freeCodeCamp/freeCodeCamp", "url": "https://github.com/freeCodeCamp/freeCodeCamp", "stars": "400k+", "desc": "Learn to code for free with interactive curriculum"},
    ],
    "Mobile & Low-Level Systems": [
        {"repo": "flutter/flutter", "url": "https://github.com/flutter/flutter", "stars": "165k+", "desc": "Build multi-platform applications from a single codebase"},
        {"repo": "facebook/react-native", "url": "https://github.com/facebook/react-native", "stars": "120k+", "desc": "Framework for building native mobile apps using React"},
        {"repo": "Genymobile/scrcpy", "url": "https://github.com/Genymobile/scrcpy", "stars": "115k+", "desc": "Display and control Android devices over USB/TCP"},
    ],
}

# Flattened list of all repos
ALL_OPEN_SOURCE_REPOS = []
for cat_name, repos in REPO_CATEGORIES.items():
    for r in repos:
        ALL_OPEN_SOURCE_REPOS.append({**r, "cat": cat_name})

# 4-Tier Categorized Local Ollama Models Registry
OLLAMA_TIERS = {
    "🪶 Leve (0.5B - 3.8B)": [
        {"tag": "qwen2.5:0.5b", "url": "https://ollama.com/library/qwen2.5", "size": "0.5B", "vram": "~0.8 GB", "desc": "Microscopic footprint, instant text classification & stubs"},
        {"tag": "qwen2.5:1.5b", "url": "https://ollama.com/library/qwen2.5", "size": "1.5B", "vram": "~1.5 GB", "desc": "Ultra-fast JSON parsing, fast routing, and background tasks"},
        {"tag": "deepseek-r1:1.5b", "url": "https://ollama.com/library/deepseek-r1", "size": "1.5B", "vram": "~1.8 GB", "desc": "Step-by-step mathematical reasoning and logic on pure CPU"},
        {"tag": "llama3.2:1b", "url": "https://ollama.com/library/llama3.2", "size": "1.2B", "vram": "~1.3 GB", "desc": "Instant text classification and lightweight instruction filtering"},
        {"tag": "llama3.2:3b", "url": "https://ollama.com/library/llama3.2", "size": "3.2B", "vram": "~2.8 GB", "desc": "Best lightweight balance for daily conversational chat"},
        {"tag": "phi3.5:3.8b", "url": "https://ollama.com/library/phi3.5", "size": "3.8B", "vram": "~3.2 GB", "desc": "Microsoft Phi-3.5 Mini - high instruction accuracy & reasoning"},
        {"tag": "smollm2:135m", "url": "https://ollama.com/library/smollm2", "size": "135M", "vram": "~0.3 GB", "desc": "Ultra-compact edge intelligence for micro-controllers"},
        {"tag": "smollm2:1.7b", "url": "https://ollama.com/library/smollm2", "size": "1.7B", "vram": "~1.6 GB", "desc": "Top quality on consumer laptops without discrete GPU"},
        {"tag": "tinyllama:1.1b", "url": "https://ollama.com/library/tinyllama", "size": "1.1B", "vram": "~1.1 GB", "desc": "Classic lightweight pre-trained model"},
        {"tag": "granite3-dense:2b", "url": "https://ollama.com/library/granite3-dense", "size": "2.0B", "vram": "~1.9 GB", "desc": "IBM enterprise-grade small model for code & tabular data"},
        {"tag": "moondream:1.8b", "url": "https://ollama.com/library/moondream", "size": "1.8B", "vram": "~2.0 GB", "desc": "Lightweight multimodal vision model for image inspection"},
    ],
    "⚡ Intermediário (7B - 9B)": [
        {"tag": "qwen2.5-coder:7b", "url": "https://ollama.com/library/qwen2.5-coder", "size": "7.6B", "vram": "~5.5 GB", "desc": "🏆 Gold standard for local code generation, refactoring & AST fixes"},
        {"tag": "deepseek-r1:7b", "url": "https://ollama.com/library/deepseek-r1", "size": "7.6B", "vram": "~6.0 GB", "desc": "Step-by-step reasoning with transparent <think> traces"},
        {"tag": "llama3.1:8b", "url": "https://ollama.com/library/llama3.1", "size": "8.0B", "vram": "~6.2 GB", "desc": "Meta flagship 8B general instruction & tool-calling model"},
        {"tag": "gemma2:9b", "url": "https://ollama.com/library/gemma2", "size": "9.2B", "vram": "~7.5 GB", "desc": "Google Gemma 2 - highest synthesis quality & docstrings"},
        {"tag": "mistral:7b", "url": "https://ollama.com/library/mistral", "size": "7.2B", "vram": "~5.8 GB", "desc": "Fast, deterministic JSON outputs and structured task parsing"},
        {"tag": "hermes3:8b", "url": "https://ollama.com/library/hermes3", "size": "8.0B", "vram": "~6.2 GB", "desc": "Nous Research uncensored model optimized for agent skills"},
        {"tag": "codellama:7b", "url": "https://ollama.com/library/codellama", "size": "7.0B", "vram": "~5.5 GB", "desc": "Specialized code completion and infilling"},
        {"tag": "starcoder2:7b", "url": "https://ollama.com/library/starcoder2", "size": "7.0B", "vram": "~5.5 GB", "desc": "Multi-language code completion trained on 600+ languages"},
        {"tag": "deepseek-coder-v2:16b", "url": "https://ollama.com/library/deepseek-coder-v2", "size": "16B", "vram": "~9.0 GB", "desc": "Efficient MoE (2.4B active) coding model"},
        {"tag": "granite3-dense:8b", "url": "https://ollama.com/library/granite3-dense", "size": "8.0B", "vram": "~6.2 GB", "desc": "IBM enterprise tabular, code and RAG workflows"},
        {"tag": "llava:7b", "url": "https://ollama.com/library/llava", "size": "7.0B", "vram": "~6.5 GB", "desc": "Visual question answering, chart reading, and UI analysis"},
        {"tag": "nomic-embed-text", "url": "https://ollama.com/library/nomic-embed-text", "size": "137M", "vram": "~0.5 GB", "desc": "8192 context text embeddings for vector RAG"},
        {"tag": "bge-m3", "url": "https://ollama.com/library/bge-m3", "size": "567M", "vram": "~1.2 GB", "desc": "Multilingual multi-granularity dense/sparse embedding"},
    ],
    "🚀 Pesado (14B - 35B)": [
        {"tag": "qwen2.5-coder:14b", "url": "https://ollama.com/library/qwen2.5-coder", "size": "14.7B", "vram": "~10.5 GB", "desc": "Enterprise-grade coding matching proprietary model quality"},
        {"tag": "deepseek-r1:14b", "url": "https://ollama.com/library/deepseek-r1", "size": "14.7B", "vram": "~11.0 GB", "desc": "Deep mathematical, algorithmic, and concurrency reasoning"},
        {"tag": "qwen2.5-coder:32b", "url": "https://ollama.com/library/qwen2.5-coder", "size": "32.5B", "vram": "~20.0 GB", "desc": "👑 State-of-the-art open-source software engineer (Top coding eval)"},
        {"tag": "deepseek-r1:32b", "url": "https://ollama.com/library/deepseek-r1", "size": "32.5B", "vram": "~21.0 GB", "desc": "Extreme logical reasoning for complex architectural bugs"},
        {"tag": "qwen2.5:14b", "url": "https://ollama.com/library/qwen2.5", "size": "14.7B", "vram": "~10.5 GB", "desc": "Balanced 14B general model with 128k context support"},
        {"tag": "qwen2.5:32b", "url": "https://ollama.com/library/qwen2.5", "size": "32.5B", "vram": "~20.0 GB", "desc": "High-capacity reasoning without requiring a 70B setup"},
        {"tag": "command-r:35b", "url": "https://ollama.com/library/command-r", "size": "35.0B", "vram": "~22.0 GB", "desc": "Cohere Command-R - specialized for Tool Use and massive RAG"},
        {"tag": "gemma2:27b", "url": "https://ollama.com/library/gemma2", "size": "27.2B", "vram": "~17.5 GB", "desc": "High-throughput 27B model rivaling previous 70B class models"},
        {"tag": "codellama:34b", "url": "https://ollama.com/library/codellama", "size": "34.0B", "vram": "~22.0 GB", "desc": "High-precision Python/C++/Rust code synthesis"},
        {"tag": "starcoder2:15b", "url": "https://ollama.com/library/starcoder2", "size": "15.0B", "vram": "~11.5 GB", "desc": "Multi-language code repository comprehension"},
        {"tag": "mixtral:8x7b", "url": "https://ollama.com/library/mixtral", "size": "47B", "vram": "~26.0 GB", "desc": "Sparse MoE with 13B active parameters per token"},
        {"tag": "deepseek-coder:33b", "url": "https://ollama.com/library/deepseek-coder", "size": "33.0B", "vram": "~21.5 GB", "desc": "Established high-performance code completion engine"},
    ],
    "🏢 DataCenter (70B - 405B)": [
        {"tag": "deepseek-r1:70b", "url": "https://ollama.com/library/deepseek-r1", "size": "70B", "vram": "~42.0 GB", "desc": "🧠 Absolute pinnacle in open mathematical and coding reasoning"},
        {"tag": "llama3.3:70b", "url": "https://ollama.com/library/llama3.3", "size": "70B", "vram": "~42.0 GB", "desc": "Meta flagship 70B with full tool calling & 128k context fidelity"},
        {"tag": "qwen2.5:72b", "url": "https://ollama.com/library/qwen2.5", "size": "72.7B", "vram": "~44.0 GB", "desc": "Benchmark champion across MMLU, GSM8k, HumanEval"},
        {"tag": "mixtral:8x22b", "url": "https://ollama.com/library/mixtral", "size": "141B", "vram": "~80.0 GB", "desc": "Massive MoE (39B active) with high math & multilingual prowess"},
        {"tag": "command-r-plus:104b", "url": "https://ollama.com/library/command-r-plus", "size": "104B", "vram": "~65.0 GB", "desc": "Enterprise RAG, multilingual routing and business intelligence"},
        {"tag": "llama3.1:70b", "url": "https://ollama.com/library/llama3.1", "size": "70B", "vram": "~42.0 GB", "desc": "Proven flagship open weights foundation model"},
    ],
}

# Flattened list of all Ollama models
ALL_OLLAMA_MODELS = []
for tier_name, models in OLLAMA_TIERS.items():
    for m in models:
        ALL_OLLAMA_MODELS.append({**m, "tier": tier_name})

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


def hyperlink(url: str, text: str | None = None) -> str:
    """Create terminal clickable hyperlink (OSC 8 standard) with fallback text."""
    display = text if text is not None else url
    return f"\033]8;;{url}\033\\{display}\033]8;;\033\\"


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
    brew_link = hyperlink("https://github.com/pedroiff0/awesome-skills", "☕ COSMIC BREW")
    catalog_link = hyperlink("https://www.opencurious.com/explore-open-source", "OPENCURIOUS")
    banner = f"""{PURPLE}{BOLD}
          .      *       .     (  )   (   )  )       *       .      .
    *        .       .          ) (   )  (  (     .       .      *
       .         *       .     ( )  (    ) )        .        .
   .       *   ┌───────────────────────────────┐     *      .       *
             * │      {brew_link}      │ *       .       .
     *         └───────────────────────────────┘            *
  🪐  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗  🌌
     ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
     ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗   ⟨/⟩
     ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝    λ
     ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗  ☄️
{NEBULA}  ══════════════════════════════════════════════════════════════════════
  ✨ UNIVERSAL MULTI-AGENT CATALOG • SKILLS • MCP • PLUGINS • OLLAMA ✨
  🌌 Powered by {catalog_link} & Open-Source Community
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


def tui_multiselect(
    title: str,
    options: list[tuple[str, str, str]],  # (key, label, subtitle)
    default_selected: list[str] | None = None,
    allow_empty: bool = False,
    allow_back: bool = False,
    single_choice: bool = False,
) -> list[str] | str:
    """Standardized Checkbox Selection Interface [✔] across ALL steps with Left/Right arrow navigation."""
    if not sys.stdin.isatty():
        return [opt[0] for opt in options] if default_selected is None else default_selected

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    selected = set(default_selected if default_selected is not None else ([options[0][0]] if not allow_empty else []))
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

        back_hint = " | ←/b: Back" if allow_back else ""
        all_hint = " | a: All" if not single_choice else ""
        footer = f"{DIM}└── [↑/↓: Move | Space: Toggle{all_hint} | →/Enter: Next{back_hint} | Esc: Abort]{RESET}"
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
                if single_choice:
                    selected.clear()
                    selected.add(cur_key)
                else:
                    if cur_key in selected:
                        selected.remove(cur_key)
                    else:
                        selected.add(cur_key)
            elif key in ("a", "A") and not single_choice:
                if len(selected) == num_opts:
                    selected.clear()
                else:
                    selected = set(opt[0] for opt in options)
            elif key in ("ENTER", "RIGHT"):
                if not selected and not allow_empty:
                    warning_msg = "Please check at least one item using [Space] before advancing!"
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
    """Interactive Skill-by-Skill browser with viewport scrolling, search, hyperlinks, and Left/Right arrow navigation."""
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
            github_clickable = hyperlink(focused["github_url"], f"🔗 {focused['github_url']}")
            repo_clickable = hyperlink("https://github.com/pedroiff0/awesome-skills", "⭐ pedroiff0/awesome-skills")

            buf.append(f"{BOLD}{VIOLET}┌─ 🔭 Skill Astrophysics & Telemetry ────────────────────────────────{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Orbit/Name:{RESET}        {NEBULA}{focused['name']}{RESET} ({CYAN_DEV}{focused['category']}{RESET}){ESC}K\n")
            buf.append(f"│ {BOLD}Astronomer/Author:{RESET} {WHITE}{focused['author']}{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Blueprint/Desc:{RESET}    {DIM}{desc_wrapped}{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Telemetry/URL:{RESET}     {STARLIGHT}{github_clickable}{RESET}{ESC}K\n")
            buf.append(f"│ {BOLD}Constellation:{RESET}     {GOLD_STAR}{repo_clickable}{RESET} | MIT License{ESC}K\n")
            buf.append(f"{BOLD}{VIOLET}└────────────────────────────────────────────────────────────────────{RESET}{ESC}K\n")
            lines += 7

            back_hint = " | ←/b: Back" if allow_back else ""
            footer = f"{DIM}└── [↑/↓: Move | Space: Toggle | a: All | /: Search | s: Sort | →/Enter: Next{back_hint} | Esc: Abort]{RESET}"
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
            elif key in ("ENTER", "RIGHT"):
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
            res = tui_multiselect("Choose Uninstallation Scope", scope_opts, default_selected=[scope_choice], allow_back=True, single_choice=True)
            if res == "__BACK__":
                step = 1
                continue
            scope_choice = res[0]
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
    """Interactive Open Source Repositories Cloner Hub with Subcategories & Clickable Links."""
    ensure_tty()
    step = 1
    selected_subcat = "ALL"
    selected_repos = []

    while True:
        if step == 1:
            cat_opts = [("ALL", "🌐 All Open Source Repositories", f"{len(ALL_OPEN_SOURCE_REPOS)} projects")]
            for cat_name, repos in REPO_CATEGORIES.items():
                cat_opts.append((cat_name, f"📁 {cat_name}", f"{len(repos)} repositories"))

            res = tui_multiselect("Open Source Hub - Step 1/2: Choose Repository Subcategory", cat_opts, default_selected=[selected_subcat], allow_back=True, single_choice=True)
            if res == "__BACK__":
                return
            selected_subcat = res[0]
            step = 2
            continue

        elif step == 2:
            repos_pool = ALL_OPEN_SOURCE_REPOS if selected_subcat == "ALL" else [r for r in ALL_OPEN_SOURCE_REPOS if r["cat"] == selected_subcat]
            repo_opts = [
                (r["repo"], f"{r['repo']:<35} ⭐ {r['stars']:<7} [{r['cat']}]", f"Link: {r['url']} — {r['desc']}")
                for r in repos_pool
            ]
            res = tui_multiselect(
                f"Open Source Hub - Step 2/2: Select Repositories to Clone [{selected_subcat}]",
                repo_opts,
                default_selected=[repo_opts[0][0]],
                allow_back=True,
            )
            if res == "__BACK__":
                step = 1
                continue
            selected_repos = res
            break

    try:
        dest_dir_input = input(f"{GOLD_STAR}Target destination directory [default: ./open-source] (b to back): {RESET}").strip()
    except (EOFError, KeyboardInterrupt):
        cancel_and_exit()

    if dest_dir_input.lower() in ("b", "back"):
        return run_open_source_cloner()

    dest_base = Path(dest_dir_input if dest_dir_input else "./open-source").resolve()
    dest_base.mkdir(parents=True, exist_ok=True)

    print(f"\n{BOLD}{PURPLE}Cloning {len(selected_repos)} repository(ies) to {dest_base}...{RESET}\n")
    for r_name in selected_repos:
        r_info = next(item for item in ALL_OPEN_SOURCE_REPOS if item["repo"] == r_name)
        repo_short = r_name.split("/")[1]
        target_path = dest_base / repo_short
        repo_link = hyperlink(r_info["url"], r_name)

        if target_path.exists():
            print(f"  {GOLD_STAR}• {repo_link} already exists at {target_path}. Updating via git pull...{RESET}")
            subprocess.run(["git", "-C", str(target_path), "pull", "--ff-only"], capture_output=True)
        else:
            print(f"  {NEBULA}• Cloning {repo_link} ({r_info['url']})...{RESET}")
            subprocess.run(["git", "clone", "--depth", "1", f"https://github.com/{r_name}.git", str(target_path)])
        print(f"  {COSMIC_GREEN}✔ Ready: {repo_link} -> {target_path}{RESET}\n")

    print(f"{COSMIC_GREEN}{BOLD}🎉 Open source repositories cloned successfully!{RESET}\n")


def run_ollama_manager():
    """Interactive Ollama Open Source Models Hub with Hardware Tiers (Leve, Intermediário, Pesado, DataCenter)."""
    ensure_tty()
    step = 1
    selected_tier = "ALL"
    selected_models = []

    while True:
        if step == 1:
            tier_opts = [("ALL", "🦙 All Local Ollama Models", f"{len(ALL_OLLAMA_MODELS)} models across 4 tiers")]
            for tier_name, models in OLLAMA_TIERS.items():
                tier_opts.append((tier_name, f"⚡ {tier_name}", f"{len(models)} local models"))

            res = tui_multiselect("Ollama Hub - Step 1/2: Choose Hardware / Capacity Tier", tier_opts, default_selected=[selected_tier], allow_back=True, single_choice=True)
            if res == "__BACK__":
                return
            selected_tier = res[0]
            step = 2
            continue

        elif step == 2:
            models_pool = ALL_OLLAMA_MODELS if selected_tier == "ALL" else [m for m in ALL_OLLAMA_MODELS if m["tier"] == selected_tier]
            model_opts = [
                (m["tag"], f"{m['tag']:<24} {m['tier']:<22} ({m['size']}, VRAM {m['vram']})", f"Library: {m['url']} — {m['desc']}")
                for m in models_pool
            ]
            res = tui_multiselect(
                f"Ollama Hub - Step 2/2: Select Models to Download / Pull [{selected_tier}]",
                model_opts,
                default_selected=[model_opts[0][0]],
                allow_back=True,
            )
            if res == "__BACK__":
                step = 1
                continue
            selected_models = res
            break

    has_ollama = shutil.which("ollama") is not None

    if has_ollama:
        print(f"\n{BOLD}{PURPLE}🚀 Pulling {len(selected_models)} model(s) via Ollama...{RESET}\n")
        for tag in selected_models:
            m_info = next(item for item in ALL_OLLAMA_MODELS if item["tag"] == tag)
            model_link = hyperlink(m_info["url"], tag)
            print(f"  {BOLD}Running:{RESET} {GOLD_STAR}ollama pull {tag}{RESET} ({model_link})")
            subprocess.run(["ollama", "pull", tag])
            print(f"  {COSMIC_GREEN}✔ Model {model_link} is ready for local inference!{RESET}\n")
    else:
        print(f"\n{GOLD_STAR}{BOLD}Notice:{RESET} 'ollama' command was not found in your system PATH.")
        install_link = hyperlink("https://ollama.com/", "https://ollama.com/")
        print(f"To install Ollama, visit: {NEBULA}{install_link}{RESET}\n")
        print(f"{BOLD}Commands to run once Ollama is installed:{RESET}")
        for tag in selected_models:
            m_info = next(item for item in ALL_OLLAMA_MODELS if item["tag"] == tag)
            model_link = hyperlink(m_info["url"], tag)
            print(f"  {NEBULA}ollama run {tag}{RESET}  (Details: {model_link})")
        print()


def run_quick_install_flow(catalog: dict, all_skills_flat: list[dict], agents_dict: dict) -> str | None:
    """Quick Install workflow with full step-by-step verification, clickable links and Back navigation."""
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
            skills_to_install.append((s["category"], s["name"], s["path"], s["github_url"]))

    print(f"\n{BOLD}{PURPLE}🚀 Launching Quick Install: {len(skills_to_install)} skill(s) into {len(selected_agents)} agent(s)...{RESET}\n")

    for agent_key in selected_agents:
        if agent_key not in agents_dict:
            continue
        agent_info = agents_dict[agent_key]
        target_dir = agent_info["global_dir"]
        print(f"  {BOLD}Configuring {agent_info['name']}{RESET} -> {DIM}{target_dir}{RESET}")
        installed_count = 0
        for cat, name, path, gh_url in skills_to_install:
            if install_skill_to_target(path, cat, name, agent_key, target_dir, use_symlink=True):
                installed_count += 1
                skill_link = hyperlink(gh_url, name)
                print(f"    {COSMIC_GREEN}✔{RESET} {skill_link} {DIM}({gh_url}){RESET}")
        print(f"  {COSMIC_GREEN}✔ Total {installed_count} skill(s) equipped into {agent_info['name']}{RESET}\n")

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
    step0_choice = "quick"
    selected_agents = ["agy", "claude", "hermes"]
    selected_scope = "global"
    selected_mode = "skill_by_skill"
    selected_cats = []
    selected_skill_names_set = set()
    selected_method = "symlink"
    skills_to_install: list[tuple[str, str, Path]] = []

    while True:
        # =====================================================================
        # STEP 0: Workflow Selection (Consistent Checkbox Pattern)
        # =====================================================================
        if step == 0:
            step0_opts = [
                ("quick", "🚀 Quick Install (Curated Elite Pack)", "Verify and install top 13 starred essential skills & MCPs for selected agents"),
                ("manual", "⚙️  Custom / Manual Setup (Interactive Wizard)", "Choose agents, scope, skill-by-skill, categories, plugins & packs"),
                ("uninstall", "🗑️  Uninstall / Clean Installed Skills", "Scan and safely remove installed skills/rules across agents"),
                ("open_source", "🌐 Explore & Clone Open-Source Repositories", f"Curated {len(ALL_OPEN_SOURCE_REPOS)} top-starred GitHub repos across 6 categories"),
                ("ollama", "🦙 Open-Source Models for Ollama", f"Local models from {len(ALL_OLLAMA_MODELS)} registry items across 4 tiers"),
            ]
            res = tui_multiselect("Step 0: Choose Installation Workflow", step0_opts, default_selected=[step0_choice], allow_back=False, single_choice=True)
            step0_choice = res[0]

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
                quick_res = run_quick_install_flow(catalog, all_skills_flat, AGENTS)
                if quick_res == "__BACK__":
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
            res = tui_multiselect("Step 2: Choose Installation Scope", scope_opts, default_selected=[selected_scope], allow_back=True, single_choice=True)
            if res == "__BACK__":
                step = 1
                continue
            selected_scope = res[0]
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
            res = tui_multiselect("Step 3: Which Skills would you like to install?", mode_opts, default_selected=[selected_mode], allow_back=True, single_choice=True)
            if res == "__BACK__":
                step = 2
                continue
            selected_mode = res[0]

            if selected_mode == "skill_by_skill":
                browser_res = tui_skill_browser(all_skills_flat, default_selected_names=selected_skill_names_set, allow_back=True)
                if browser_res == "__BACK__":
                    continue
                skills_to_install = [(s[0], s[1], s[2]) for s in browser_res]
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
            res = tui_multiselect("Step 4: Choose Installation Method", method_opts, default_selected=[selected_method], allow_back=True, single_choice=True)
            if res == "__BACK__":
                step = 3
                continue
            selected_method = res[0]
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
            gh_url = f"{GITHUB_BASE_URL}/{cat}/{name}"
            skill_link = hyperlink(gh_url, name)
            if install_skill_to_target(path, cat, name, agent_key, target_dir, use_symlink=use_symlink):
                installed_count += 1
                print(f"    {COSMIC_GREEN}✔{RESET} {skill_link} {DIM}({gh_url}){RESET}")
        print(f"  {COSMIC_GREEN}✔ Total {installed_count} skill(s) equipped into {agent_info['name']}{RESET}\n")

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
        help="List curated Ollama open-source models across 4 tiers",
    )

    args = parser.parse_args()
    catalog = discover_skills()

    if args.uninstall:
        run_uninstaller()
        return

    if args.repos:
        print_banner()
        for cat_name, repos in REPO_CATEGORIES.items():
            print(f"\n{BOLD}{PURPLE}=== {cat_name} ({len(repos)} repositories) ==={RESET}")
            for r in repos:
                r_link = hyperlink(r["url"], r["repo"])
                print(f"  • {BOLD}{r_link:<35}{RESET} ⭐ {r['stars']:<7} — {r['desc']}\n    {DIM}URL:{RESET} {STARLIGHT}{r['url']}{RESET}")
        return

    if args.ollama:
        print_banner()
        for tier_name, models in OLLAMA_TIERS.items():
            print(f"\n{BOLD}{PURPLE}=== {tier_name} ({len(models)} models) ==={RESET}")
            for m in models:
                m_link = hyperlink(m["url"], m["tag"])
                print(f"  • {BOLD}{m_link:<24}{RESET} ({m['size']}, VRAM {m['vram']}) — {m['desc']}\n    {DIM}Library:{RESET} {STARLIGHT}{m['url']}{RESET}")
        return

    if args.list:
        print_banner()
        for cat, sks in sorted(catalog.items()):
            print(f"\n{BOLD}{PURPLE}=== {cat} ({len(sks)} skills) ==={RESET}")
            for name, path in sorted(sks.items()):
                fm = parse_frontmatter(path / "SKILL.md")
                author = fm.get("author", "Open Source Community")
                desc = fm.get("description", "")
                gh_url = f"{GITHUB_BASE_URL}/{cat}/{name}"
                s_link = hyperlink(gh_url, name)
                print(f"  • {BOLD}{s_link}{RESET} (by {author}): {desc[:70]}{'...' if len(desc)>70 else ''}\n    {DIM}Link:{RESET} {STARLIGHT}{gh_url}{RESET}")
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
