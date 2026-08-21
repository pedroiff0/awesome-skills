<div align="center">

# awesome-skills

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Skills](https://img.shields.io/badge/skills-124-blue.svg)
![Plugins](https://img.shields.io/badge/plugins-2-purple.svg)
![MCP](https://img.shields.io/badge/mcp--servers-4-orange.svg)
![Categories](https://img.shields.io/badge/categories-19-blue.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**The Universal Multi-Agent Catalog of Skills, Plugins & Model Context Protocol (MCP) Servers.**

*Write once in `SKILL.md` — run on Google Antigravity, Claude Code, Hermes Agent, Cursor, Windsurf, Roo & Codex.*

</div>

---

## 🧭 Autonomous Agent Setup (No CLI Required)

If you are an **AI Agent** (or asked an agent to clone this repository), activate the Master Skill:

> 🤖 **[`awesome-skills-master`](skills/autonomous-ai-agents/awesome-skills-master/SKILL.md)** — Fully autonomous procedural guide for agents to auto-detect their host environment (AGY, Claude, Cursor, Hermes, Roo), adapt rules (`.cursor/rules/*.mdc`, `CLAUDE.md`), link skills, configure MCP servers, and preserve strict author attribution without user prompts.

---

## ⚡ Quick Start: Interactive Installer (Caveman-style)

Install skills interactively with a terminal TUI menu, skill-by-skill live browser, author credits, and curated packs:

```bash
# Run directly via curl (Interactive TUI)
curl -fsSL https://raw.githubusercontent.com/pedroiff0/awesome-skills/main/install.sh | bash

# Or clone and run locally
git clone https://github.com/pedroiff0/awesome-skills.git
cd awesome-skills
./install.sh
```

---

## 🤖 Installation by Agent (Direct 1-Liners)

### 🪐 Google Antigravity (AGY)

```bash
# Global User Skills
mkdir -p ~/.gemini/antigravity-cli/skills && cp -r skills/*/* ~/.gemini/antigravity-cli/skills/
# Workspace Local Skills
mkdir -p .agent/skills && cp -r skills/<category>/<skill> .agent/skills/
```

### 🏛️ Hermes Agent (Nous Research)

```bash
mkdir -p ~/.hermes/skills && cp -r skills/* ~/.hermes/skills/
```

### ⚡ Claude Code (Anthropic CLI)

```bash
mkdir -p ~/.claude/skills && cp -r skills/*/* ~/.claude/skills/
```

### 🎯 Cursor IDE (.mdc Rules)

```bash
./install.sh --agent cursor --scope local --pack fullstack
```

### 🌊 Windsurf & Roo Code / Cline

```bash
mkdir -p .windsurf/skills && cp -r skills/*/* .windsurf/skills/
mkdir -p ~/.roo/skills && cp -r skills/*/* ~/.roo/skills/
```

---

## 🔌 Model Context Protocol (MCP) & Plugins

| Component | Description | Config Location |
| :--- | :--- | :--- |
| **[`mcp/context-mode`](mcp/context-mode)** | AST indexed search & token compression server | `mcp/context-mode/mcp.json` |
| **[`mcp/sqlite-explorer`](mcp/sqlite-explorer)** | SQLite schema analysis & SQL executor | `mcp/sqlite-explorer/mcp.json` |
| **[`mcp/puppeteer-browser`](mcp/puppeteer-browser)** | Headless browser rendering & screenshots | `mcp/puppeteer-browser/mcp.json` |
| **[`mcp/filesystem-pro`](mcp/filesystem-pro)** | Granular scoped filesystem permissions | `mcp/filesystem-pro/mcp.json` |
| **[`plugins/auto-git-checkpoint`](plugins/auto-git-checkpoint)** | Pre/post task automatic git atomic commits | `plugins/auto-git-checkpoint/plugin.json` |
| **[`plugins/token-guardian`](plugins/token-guardian)** | Turn-by-turn context burn monitor | `plugins/token-guardian/plugin.json` |

---

## 📦 Curated Packs

| Pack | Focus | Key Categories | Install Command |
| :--- | :--- | :--- | :--- |
| **🚀 Full-Stack Dev** | Web, APIs, Testing, Refactoring | `software-development`, `web`, `github` | `./install.sh --pack fullstack` |
| **⚡ DevOps & Cloud** | Containers, Caddy, Cloudflare, CI/CD | `devops`, `github` | `./install.sh --pack devops` |
| **🧠 Autonomous AI & MLOps** | Multi-Agent topologies, RAG, Token ops | `autonomous-ai-agents`, `mlops` | `./install.sh --pack ai` |
| **📚 Academic & LaTeX** | Paper writing, LaTeX CVs, arXiv, i18n | `latex`, `research`, `content-i18n` | `./install.sh --pack academic` |
| **🎨 Creative & Media** | Architecture diagrams, ASCII, Audio | `creative`, `media`, `desktop` | `./install.sh --pack creative` |
| **📦 Complete Catalog** | All 124+ skills across 19 categories | All categories | `./install.sh --pack all` |

---

## 🗂️ Skills Catalog Index

> **124 skills** organized across **19 categories** with strict attribution.

### apple

| Skill | Description | Author / Credits |
|---|---|---|
| [`apple-notes`](skills/apple/apple-notes/SKILL.md) | Manage Apple Notes via memo CLI: create, search, edit. | Hermes Agent |
| [`apple-reminders`](skills/apple/apple-reminders/SKILL.md) | Apple Reminders via remindctl: add, list, complete. | Hermes Agent |
| [`findmy`](skills/apple/findmy/SKILL.md) | Track Apple devices/AirTags via FindMy.app on macOS. | Hermes Agent |
| [`imessage`](skills/apple/imessage/SKILL.md) | Send and receive iMessages/SMS via the imsg CLI on macOS. | Hermes Agent |

### autonomous-ai-agents

| Skill | Description | Author / Credits |
|---|---|---|
| [`agy-customizations`](skills/autonomous-ai-agents/agy-customizations/SKILL.md) | Comprehensive guide and reference for the Antigravity Customization System. Use to author skills, contextual rules, plugins, hooks, and MCP servers with correct priori... | Pedro Henrique Rocha de Andrade |
| [`antigravity-guide`](skills/autonomous-ai-agents/antigravity-guide/SKILL.md) | Provides a comprehensive guide, architecture reference, and quick-access sitemap for Google Antigravity (AGY), including CLI, Antigravity 2.0, IDE extensions, Python S... | Pedro Henrique Rocha de Andrade |
| [`awesome-skills-master`](skills/autonomous-ai-agents/awesome-skills-master/SKILL.md) | Master catalog orchestrator and autonomous installer for AI agents. Use when exploring, cloning, discovering, or installing skills, plugins, or MCP servers from awesom... | Pedro Henrique Rocha de Andrade |
| [`claude-code`](skills/autonomous-ai-agents/claude-code/SKILL.md) | Delegate coding to Claude Code CLI (features, PRs). | Hermes Agent + Teknium |
| [`codex`](skills/autonomous-ai-agents/codex/SKILL.md) | Delegate coding to OpenAI Codex CLI (features, PRs). | Hermes Agent |
| [`computer-use`](skills/autonomous-ai-agents/computer-use/SKILL.md) | \| | Pedro Henrique Rocha de Andrade |
| [`context-mode`](skills/autonomous-ai-agents/context-mode/SKILL.md) | Context optimization and compression routing rules for AI agents exploring large codebases, reading massive logs, searching symbols, and batching tool executions. | Pedro Henrique Rocha de Andrade |
| [`dogfood`](skills/autonomous-ai-agents/dogfood/SKILL.md) | Exploratory QA of web apps: find bugs, evidence, reports. | Pedro Henrique Rocha de Andrade |
| [`hermes-agent`](skills/autonomous-ai-agents/hermes-agent/SKILL.md) | Configure, extend, or contribute to Hermes Agent. | Hermes Agent + Teknium |
| [`opencode`](skills/autonomous-ai-agents/opencode/SKILL.md) | Delegate coding to OpenCode CLI (features, PR review). | Hermes Agent |
| [`rag-local-lancedb`](skills/autonomous-ai-agents/rag-local-lancedb/SKILL.md) | Build, query, and manage local vector embeddings and semantic search pipelines using LanceDB and HuggingFace/SentenceTransformers embeddings without cloud dependencies. | Pedro Henrique Rocha de Andrade |
| [`skills-sh-registry`](skills/autonomous-ai-agents/skills-sh-registry/SKILL.md) | Discover, query, evaluate, and fetch skills from the open skills.sh ecosystem (Vercel Labs) and global agent skill repositories. | Vercel Labs / skills.sh Community |
| [`watermarks-remover`](skills/autonomous-ai-agents/watermarks-remover/SKILL.md) | Strip multi-vendor AI provenance marks, invisible Unicode characters (ZWSP, ZWNJ, Bidi, variation selectors), statistical text watermarks, and C2PA/EXIF/XMP metadata f... | Guillaume Meyer & Pedro Henrique Rocha de Andrade |
| [`yuanbao`](skills/autonomous-ai-agents/yuanbao/SKILL.md) | Yuanbao (元宝) groups: @mention users, query info/members. | Pedro Henrique Rocha de Andrade |

### content-i18n

| Skill | Description | Author / Credits |
|---|---|---|
| [`libretranslate-markdown-i18n`](skills/content-i18n/libretranslate-markdown-i18n/SKILL.md) | Machine-translate Markdown / Obsidian / Quartz content into other languages using a self-hosted LibreTranslate instance, preserving frontmatter, headings, emojis, bold... | Pedro Henrique Rocha de Andrade |
| [`mt-markup-preserving-translation`](skills/content-i18n/mt-markup-preserving-translation/SKILL.md) | Translate Markdown/Obsidian/Quartz content with LibreTranslate while preserving wikilinks, embeds, URLs, tables, HTML blocks, proper nouns, and canonical section title... | Pedro Henrique Rocha de Andrade |

### creative

| Skill | Description | Author / Credits |
|---|---|---|
| [`architecture-diagram`](skills/creative/architecture-diagram/SKILL.md) | Dark-themed SVG architecture/cloud/infra diagrams as HTML. | Cocoon AI (hello@cocoon-ai.com), ported by Hermes Agent |
| [`ascii-art`](skills/creative/ascii-art/SKILL.md) | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. | 0xbyt4, Hermes Agent |
| [`ascii-video`](skills/creative/ascii-video/SKILL.md) | ASCII video: convert video/audio to colored ASCII MP4/GIF. | Pedro Henrique Rocha de Andrade |
| [`baoyu-infographic`](skills/creative/baoyu-infographic/SKILL.md) | Infographics: 21 layouts x 21 styles (信息图, 可视化). | 宝玉 (JimLiu) |
| [`claude-design`](skills/creative/claude-design/SKILL.md) | Design one-off HTML artifacts (landing, deck, prototype). | BadTechBandit |
| [`comfyui`](skills/creative/comfyui/SKILL.md) | Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter injection. Uses the official comfy-cli for lifecycl... | [kshitijk4poor, alt-glitch, purzbeats] |
| [`design-md`](skills/creative/design-md/SKILL.md) | Author/validate/export Google's DESIGN.md token spec files. | Hermes Agent |
| [`excalidraw`](skills/creative/excalidraw/SKILL.md) | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). | Hermes Agent |
| [`humanizer`](skills/creative/humanizer/SKILL.md) | Humanize text: strip AI-isms and add real voice. | Siqi Chen (@blader, https://github.com/blader/humanizer), ported by Hermes Agent |
| [`manim-video`](skills/creative/manim-video/SKILL.md) | Manim CE animations: 3Blue1Brown math/algo videos. | Pedro Henrique Rocha de Andrade |
| [`p5js`](skills/creative/p5js/SKILL.md) | p5.js sketches: gen art, shaders, interactive, 3D. | Pedro Henrique Rocha de Andrade |
| [`popular-web-designs`](skills/creative/popular-web-designs/SKILL.md) | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. | Hermes Agent + Teknium (design systems sourced from VoltAgent/awesome-design-md) |
| [`portfolio-github-pages`](skills/creative/portfolio-github-pages/SKILL.md) | Build and deploy a personal/academic PORTFOLIO as a single-page STATIC site (no build step) to GitHub Pages via the gh CLI. Use when the user asks for a portfolio, lan... | Pedro Henrique Rocha de Andrade |
| [`pretext`](skills/creative/pretext/SKILL.md) | Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flow around obstacles, text-as-geometry games, kineti... | Hermes Agent |
| [`sketch`](skills/creative/sketch/SKILL.md) | Throwaway HTML mockups: 2-3 design variants to compare. | Hermes Agent (adapted from gsd-build/get-shit-done) |
| [`songwriting-and-ai-music`](skills/creative/songwriting-and-ai-music/SKILL.md) | Songwriting craft and Suno AI music prompts. | Pedro Henrique Rocha de Andrade |
| [`touchdesigner-mcp`](skills/creative/touchdesigner-mcp/SKILL.md) | Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-time visuals. 36 native tools. | kshitijk4poor |

### data-science

| Skill | Description | Author / Credits |
|---|---|---|
| [`jupyter-live-kernel`](skills/data-science/jupyter-live-kernel/SKILL.md) | Iterative Python via live Jupyter kernel (hamelnb). | Hermes Agent |
| [`suap-iff-api`](skills/data-science/suap-iff-api/SKILL.md) | Authenticate to and consume the SUAP IFF (Instituto Federal Fluminense) API v2 from the CLI — obtain the JWT access/refresh token via matricula+senha, then fetch stude... | Pedro Henrique Rocha de Andrade |

### desktop

| Skill | Description | Author / Credits |
|---|---|---|
| [`desktop-theming`](skills/desktop/desktop-theming/SKILL.md) | Make a Linux desktop (XFCE/GNOME/KDE) look like macOS or otherwise "rice" it — WhiteSur GTK/icon/cursor themes, Plank dock, San-Francisco-like fonts, xfconf config. Us... | Pedro Henrique Rocha de Andrade |
| [`hermes-desktop-plugins`](skills/desktop/hermes-desktop-plugins/SKILL.md) | Write desktop app plugins that add UI panes and commands. | Pedro Henrique Rocha de Andrade |

### devops

| Skill | Description | Author / Credits |
|---|---|---|
| [`docker-single-port-multi-instance`](skills/devops/docker-single-port-multi-instance/SKILL.md) | Consolidate multiple Docker Compose app instances (production / test / demo) behind ONE host port using an nginx reverse proxy that routes by URL path prefix (e.g. /de... | Pedro Henrique Rocha de Andrade |
| [`hybrid-desktop-server-ops`](skills/devops/hybrid-desktop-server-ops/SKILL.md) | Comprehensive runbook and operational architecture for running a single Linux machine as both a daily development desktop and a 24/7 home/cloud server (Debian/Ubuntu,... | Pedro Henrique Rocha de Andrade |

### email

| Skill | Description | Author / Credits |
|---|---|---|
| [`himalaya`](skills/email/himalaya/SKILL.md) | Himalaya CLI: IMAP/SMTP email from terminal. | community |

### github

| Skill | Description | Author / Credits |
|---|---|---|
| [`codebase-inspection`](skills/github/codebase-inspection/SKILL.md) | Inspect codebases w/ pygount: LOC, languages, ratios. | Hermes Agent |
| [`git-conventional-commits`](skills/github/git-conventional-commits/SKILL.md) | Author standardized conventional commit messages (feat, fix, docs, refactor, chore), generate automated semver releases, and format pull request descriptions. | Pedro Henrique Rocha de Andrade |
| [`github-auth`](skills/github/github-auth/SKILL.md) | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. | Hermes Agent |
| [`github-code-review`](skills/github/github-code-review/SKILL.md) | Review PRs: diffs, inline comments via gh or REST. | Hermes Agent |
| [`github-issue-pr-attribs`](skills/github/github-issue-pr-attribs/SKILL.md) | Standardize GitHub ISSUE and PR metadata (Assignee, Reviewer, Labels, Project, Milestone, Development, Relationship) and ship a strong, well-structured code-review tem... | Hermes Agent |
| [`github-issues`](skills/github/github-issues/SKILL.md) | Create, triage, label, assign GitHub issues via gh or REST. | Hermes Agent |
| [`github-pr-workflow`](skills/github/github-pr-workflow/SKILL.md) | GitHub PR lifecycle: branch, commit, open, CI, merge. | Hermes Agent |
| [`github-profile-readme`](skills/github/github-profile-readme/SKILL.md) | Build or rewrite a GitHub profile README (the username/username special repo) with a personalized theme — animated SVG banner, stats cards, contribution snake, tech ba... | Pedro Henrique Rocha de Andrade |
| [`github-repo-management`](skills/github/github-repo-management/SKILL.md) | Clone/create/fork repos; manage remotes, releases. | Hermes Agent |
| [`github-starred-kb`](skills/github/github-starred-kb/SKILL.md) | Personal GitHub knowledge base built from the user's starred repos (pedroiff0). Maps all 41 starred repositories into knowledge domains (free APIs, sysadmin/self-hoste... | Hermes Agent |
| [`hermes-installed-catalog`](skills/github/hermes-installed-catalog/SKILL.md) | Live catalog of skills, plugins, and agents actually installed on THIS Hermes server (pedroiff0). Lists the 233 installed skills grouped by domain, the 18 installed pl... | Hermes Agent |
| [`readme-template`](skills/github/readme-template/SKILL.md) | Standard README template for repos — professional structure with badges, overview, table of contents, features/modules, stack, installation, configuration, tests, secu... | pedroiff0 |

### latex

| Skill | Description | Author / Credits |
|---|---|---|
| [`cv-latex-multilingual`](skills/latex/cv-latex-multilingual/SKILL.md) | Manter o CV LaTeX multilíngue do usuário (classe altacv) em ~/Repositorios/pessoal/cv — PT (fonte), EN (espelho), ES/FR (gerados do EN via translate_cv.py). Abrange co... | Pedro Henrique Rocha de Andrade |
| [`latex-cv-maintenance`](skills/latex/latex-cv-maintenance/SKILL.md) | Use when reviewing, updating, or keeping consistent a multi-language LaTeX CV (altacv.cls). Covers treating Portuguese as source of truth and mirroring to other langua... | Hermes Agent |

### media

| Skill | Description | Author / Credits |
|---|---|---|
| [`gif-search`](skills/media/gif-search/SKILL.md) | Search/download GIFs from Tenor via curl + jq. | Hermes Agent |
| [`heartmula`](skills/media/heartmula/SKILL.md) | HeartMuLa: Suno-like song generation from lyrics + tags. | Pedro Henrique Rocha de Andrade |
| [`songsee`](skills/media/songsee/SKILL.md) | Audio spectrograms/features (mel, chroma, MFCC) via CLI. | community |
| [`youtube-content`](skills/media/youtube-content/SKILL.md) | YouTube transcripts to summaries, threads, blogs. | Pedro Henrique Rocha de Andrade |

### mlops

| Skill | Description | Author / Credits |
|---|---|---|
| [`audiocraft-audio-generation`](skills/mlops/audiocraft/SKILL.md) | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. | Orchestra Research |
| [`evaluating-llms-harness`](skills/mlops/lm-evaluation-harness/SKILL.md) | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). | Orchestra Research |
| [`gpu-debian-setup`](skills/mlops/gpu-debian-setup/SKILL.md) | Install and verify NVIDIA proprietary GPU drivers on Debian (including trixie/13) so local LLM tools (Ollama, llama.cpp, vLLM) can use the GPU. Covers nouveau blacklis... | Pedro Henrique Rocha de Andrade |
| [`huggingface-hub`](skills/mlops/huggingface-hub/SKILL.md) | HuggingFace hf CLI: search/download/upload models, datasets. | Hugging Face |
| [`llama-cpp`](skills/mlops/llama-cpp/SKILL.md) | llama.cpp local GGUF inference + HF Hub model discovery. | Orchestra Research |
| [`segment-anything-model`](skills/mlops/segment-anything/SKILL.md) | SAM: zero-shot image segmentation via points, boxes, masks. | Orchestra Research |
| [`serving-llms-vllm`](skills/mlops/vllm/SKILL.md) | vLLM: high-throughput LLM serving, OpenAI API, quantization. | Orchestra Research |
| [`weights-and-biases`](skills/mlops/weights-and-biases/SKILL.md) | W&B: log ML experiments, sweeps, model registry, dashboards. | Orchestra Research |

### note-taking

| Skill | Description | Author / Credits |
|---|---|---|
| [`obsidian`](skills/note-taking/obsidian/SKILL.md) | Read, search, create, and edit notes in the Obsidian vault. | Pedro Henrique Rocha de Andrade |

### productivity

| Skill | Description | Author / Credits |
|---|---|---|
| [`airtable`](skills/productivity/airtable/SKILL.md) | Airtable REST API via curl. Records CRUD, filters, upserts. | community |
| [`google-workspace`](skills/productivity/google-workspace/SKILL.md) | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. | Nous Research |
| [`maps`](skills/productivity/maps/SKILL.md) | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. | Mibayy |
| [`nano-pdf`](skills/productivity/nano-pdf/SKILL.md) | Edit PDF text/typos/titles via nano-pdf CLI (NL prompts). | community |
| [`notion`](skills/productivity/notion/SKILL.md) | Notion API + ntn CLI: pages, databases, markdown, Workers. | community |
| [`ocr-and-documents`](skills/productivity/ocr-and-documents/SKILL.md) | Extract text from PDFs/scans (pymupdf, marker-pdf). | Hermes Agent |
| [`petdex`](skills/productivity/petdex/SKILL.md) | Install and select animated petdex mascots for Hermes. | Hermes Agent |
| [`powerpoint`](skills/productivity/powerpoint/SKILL.md) | Create, read, edit .pptx decks, slides, notes, templates. | Pedro Henrique Rocha de Andrade |
| [`suap-api`](skills/productivity/suap-api/SKILL.md) | Consume the SUAP (Sistema Unificado de Administração Pública) REST API v2 used by Brazilian federal institutes (IFRN, IFF, IFS, etc.) — obtain a JWT via /api/v2/autent... | Pedro Henrique Rocha de Andrade |
| [`teams-meeting-pipeline`](skills/productivity/teams-meeting-pipeline/SKILL.md) | Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs, manage Microsoft Graph subscriptions. | Hermes Agent + Teknium |

### research

| Skill | Description | Author / Credits |
|---|---|---|
| [`arxiv`](skills/research/arxiv/SKILL.md) | Search arXiv papers by keyword, author, category, or ID. | Hermes Agent |
| [`blogwatcher`](skills/research/blogwatcher/SKILL.md) | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. | JulienTant (fork of Hyaxia/blogwatcher) |
| [`grill-me-interview`](skills/research/grill-me-interview/SKILL.md) | Conduct an interactive, rigorous architecture interview. Grills the user with probing questions one at a time to clarify ambiguous requirements, design decisions, edge... | Matt Pocock / skills.sh Community |
| [`lattes-xml-projetos`](skills/research/lattes-xml-projetos/SKILL.md) | Use when gerar, limpar ou inserir itens de bolsa/projetos de pesquisa (PARTICIPACAO-EM-PROJETO / PROJETO-DE-PESQUISA) em XML de importação do Currículo Lattes. Cobre a... | Hermes Agent |
| [`llm-wiki`](skills/research/llm-wiki/SKILL.md) | Karpathy's LLM Wiki: build/query interlinked markdown KB. | Hermes Agent |
| [`nosignups-catalog`](skills/research/nosignups-catalog/SKILL.md) | Catálogo curado de ferramentas open source sem signup (NoSignups.net). 234 tools organizadas por categoria e relevância para DevOps/self-hosted/operations. Use para en... | Pedro (pedroiff0) |
| [`polymarket`](skills/research/polymarket/SKILL.md) | Query Polymarket: markets, prices, orderbooks, history. | Hermes Agent + Teknium |
| [`research-paper-writing`](skills/research/research-paper-writing/SKILL.md) | Write ML papers for NeurIPS/ICML/ICLR: design→submit. | Orchestra Research |

### smart-home

| Skill | Description | Author / Credits |
|---|---|---|
| [`openhue`](skills/smart-home/openhue/SKILL.md) | Control Philips Hue lights, scenes, rooms via OpenHue CLI. | community |

### social-media

| Skill | Description | Author / Credits |
|---|---|---|
| [`xurl`](skills/social-media/xurl/SKILL.md) | X/Twitter via xurl CLI: post, search, DM, media, v2 API. | xdevplatform + openclaw + Hermes Agent |

### software-development

| Skill | Description | Author / Credits |
|---|---|---|
| [`adhoc-verification`](skills/software-development/adhoc-verification/SKILL.md) | Produce fresh, focused, local verification evidence for a code change without relying on the full test suite. Use when a system reminder (or the user) demands ad-hoc v... | Pedro Henrique Rocha de Andrade |
| [`docker-compose-app-recovery`](skills/software-development/docker-compose-app-recovery/SKILL.md) | Recover or reset credentials and directly operate the database of an app running under docker-compose (lost admin password, one-time seed password, locked out, read/wr... | Pedro Henrique Rocha de Andrade |
| [`document-exports`](skills/software-development/document-exports/SKILL.md) | Generate and TEST downloadable document exports (PDF/CSV) from a Node/Express backend — pdfkit streaming, CSV BOM, cents formatting, and the supertest/pdfkit pitfalls... | Pedro Henrique Rocha de Andrade |
| [`docx-analysis-conversion`](skills/software-development/docx-analysis-conversion/SKILL.md) | Extract, analyze, edit, and convert Microsoft Word (.docx) documents to structured Markdown, JSON, or clean text preserving tables, headers, and bullet lists. | Pedro Henrique Rocha de Andrade |
| [`financas-app`](skills/software-development/financas-app/SKILL.md) | Corrigir, estender e validar o app de finanças pessoais (Node/Express + EJS + MongoDB + Docker). Cobre a arquitetura de porta única 4460 com demo via /demo, o fluxo de... | Pedro Henrique Rocha de Andrade |
| [`frontend-design-systems`](skills/software-development/frontend-design-systems/SKILL.md) | Architect and build production-grade web interfaces with modern design systems: Tailwind CSS v4, Shadcn UI primitives, Radix UI, dark mode tokens, and accessible WCAG... | Anthropic / skills.sh Community |
| [`grill-with-docs`](skills/software-development/grill-with-docs/SKILL.md) | Cross-examine codebase architecture against official library documentation and API specs. Identifies deprecations, anti-patterns, and suboptimal library usage. | Matt Pocock / skills.sh Community |
| [`handoff-resume`](skills/software-development/handoff-resume/SKILL.md) | Resume in-progress coding work across sessions from a HANDOFF.md and a dirty git working tree. Use when a task says "continue from HANDOFF.md", "retomar o processament... | Pedro Henrique Rocha de Andrade |
| [`hermes-agent-skill-authoring`](skills/software-development/hermes-agent-skill-authoring/SKILL.md) | Author in-repo SKILL.md: frontmatter, validator, structure, and writing-quality principles. | Hermes Agent |
| [`node-inspect-debugger`](skills/software-development/node-inspect-debugger/SKILL.md) | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. | Hermes Agent |
| [`obscure-tool-install-lookup`](skills/software-development/obscure-tool-install-lookup/SKILL.md) | Use when a user asks how to install or use an obscure CLI tool, agent, or package and search engines are blocked, CAPTCHA-walled, or unhelpful. Resolves canonical inst... | Hermes Agent |
| [`plan`](skills/software-development/plan/SKILL.md) | Plan mode: write an actionable markdown plan to .hermes/plans/, no execution. Bite-sized tasks, exact paths, complete code. | Hermes Agent (writing-craft adapted from obra/superpowers) |
| [`playwright-browser-automation`](skills/software-development/playwright-browser-automation/SKILL.md) | Run automated headless browser testing, scrape dynamic SPAs, capture high-resolution full-page screenshots, and perform visual regression testing with Playwright. | Pedro Henrique Rocha de Andrade |
| [`projeto-profissional`](skills/software-development/projeto-profissional/SKILL.md) | Bootstrap a new professional repo from Pedro's hardened Node/Express+MongoDB+EJS base template (JWT auth, admin/user roles, admin-controlled registration, security def... | Pedro Henrique Rocha de Andrade |
| [`projeto-profissional-template`](skills/software-development/projeto-profissional-template/SKILL.md) | Development & operations workflow for the user's "projeto-professional" template (Node 20 + Express + MongoDB/Mongoose + EJS SSR + JWT). Captures recurring gotchas — r... | Pedro Henrique Rocha de Andrade |
| [`python-debugpy`](skills/software-development/python-debugpy/SKILL.md) | Debug Python: pdb REPL + debugpy remote (DAP). | Hermes Agent |
| [`requesting-code-review`](skills/software-development/requesting-code-review/SKILL.md) | Pre-commit review: security scan, quality gates, auto-fix. | Hermes Agent (adapted from obra/superpowers + MorAlekss) |
| [`security-sast-audit`](skills/software-development/security-sast-audit/SKILL.md) | Perform static application security testing (SAST), secret scanning, dependency vulnerability audits (OWASP Top 10, bandit, semgrep, trivy, pip-audit, npm audit). | Pedro Henrique Rocha de Andrade |
| [`simplify-code`](skills/software-development/simplify-code/SKILL.md) | Parallel 3-agent cleanup of recent code changes. | Hermes Agent (inspired by Claude Code /simplify) |
| [`spike`](skills/software-development/spike/SKILL.md) | Throwaway experiments to validate an idea before build. | Hermes Agent (adapted from gsd-build/get-shit-done) |
| [`systematic-debugging`](skills/software-development/systematic-debugging/SKILL.md) | 4-phase root cause debugging: understand bugs before fixing. | Hermes Agent (adapted from obra/superpowers) |
| [`test-driven-development`](skills/software-development/test-driven-development/SKILL.md) | TDD: enforce RED-GREEN-REFACTOR, tests before code. | Hermes Agent (adapted from obra/superpowers) |
| [`web-fullstack-gotchas`](skills/software-development/web-fullstack-gotchas/SKILL.md) | Armadilhas recorrentes em apps fullstack Node/Express + EJS + CSS + jest + Docker (padrão do projeto financas-app, mas aplicável a qualquer stack similar). USE quando... | Pedro Henrique Rocha de Andrade |
| [`xlsx-data-wrangling`](skills/software-development/xlsx-data-wrangling/SKILL.md) | Query, validate, clean, and manipulate Excel (.xlsx/.xls) spreadsheets programmatically without GUI using pandas, openpyxl, and polars. | Pedro Henrique Rocha de Andrade |

### web

| Skill | Description | Author / Credits |
|---|---|---|
| [`animated-portfolio-sites`](skills/web/animated-portfolio-sites/SKILL.md) | Build a one-page animated personal or portfolio site (canvas starfield, rotating galaxies with mouse parallax, hidden accordion/card content, anchor nav) and publish i... | Hermes Agent |
| [`express-csp-runtime-config`](skills/web/express-csp-runtime-config/SKILL.md) | How to pass server-side runtime config (API prefix, feature flags, user id, CSRF token) from an Express/EJS app to client JS when a strict Content-Security-Policy is i... | Pedro Henrique Rocha de Andrade |
| [`frontend-visual-verification`](skills/web/frontend-visual-verification/SKILL.md) | Confirm a CSS/HTML/template change actually rendered in a running browser — without being fooled by stale browser cache. Use whenever you edited frontend code (CSS, EJ... | Pedro Henrique Rocha de Andrade |
| [`github-pages-portfolio`](skills/web/github-pages-portfolio/SKILL.md) | Build, update, and verify a single-page static portfolio / intro site on GitHub Pages (pure HTML+CSS+JS, no build step). Covers sourcing content read-only from the use... | Pedro Henrique Rocha de Andrade |
| [`markdown-site-source-pipeline`](skills/web/markdown-site-source-pipeline/SKILL.md) | Keep a static HTML/JS site's content in an editable Markdown source file; generate the data artifact (JS/JSON) the site consumes; guarantee identical render via semant... | Pedro Henrique Rocha de Andrade |
| [`markdown-static-site-source`](skills/web/markdown-static-site-source/SKILL.md) | Make a data-driven static site (content lives in a JS/JSON object consumed by a render script) editable from Markdown/Obsidian. Generate the data file from a YAML-fron... | Pedro Henrique Rocha de Andrade |
| [`nextjs-app-router-patterns`](skills/web/nextjs-app-router-patterns/SKILL.md) | Architect and implement modern Next.js App Router applications with Server Components (RSC), Server Actions, Parallel/Intercepting Routes, and Streaming SSR. | Pedro Henrique Rocha de Andrade |
| [`quartz-multilang-site-maintenance`](skills/web/quartz-multilang-site-maintenance/SKILL.md) | Maintain and edit a Quartz static site (Quartz Syncer / quartz-site fork) that publishes to GitHub Pages — especially editing the 4-language home/index pages (pt-br/en... | Hermes Agent |
| [`static-site-md-source`](skills/web/static-site-md-source/SKILL.md) | Turn an EXISTING static site (HTML/CSS/JS) into a Markdown-editable source WITHOUT changing its rendered output. Use when the user likes the current site ("muito bom,... | Pedro Henrique Rocha de Andrade |

---

## 📂 Repository Structure

```
awesome-skills/
  ├── skills/<category>/<name>/   # Canonical SKILL.md + references/ + scripts/
  ├── plugins/<name>/             # Reusable agent plugins & lifecycle hooks
  ├── mcp/<name>/                 # Model Context Protocol (MCP) server definitions
  ├── install.sh                  # Universal interactive installer (Caveman-style)
  ├── tools/
  │   ├── installer.py            # TUI & CLI installation engine
  │   └── gen_index.py            # Regenerates README catalog index
  ├── templates/                  # Starter kits: skill / agent / plugin / mcp
  ├── packages/awesomeskills/     # Python package CLI (`awesomeskills install`)
  ├── docs/CODE_REVIEW.md         # Review standard
  └── .github/                    # Issue & PR templates + CI workflow
```

---

## ⚖️ Author Credits & Attribution Standards

awesome-skills strictly credits all original authors, community projects, and research creators:
- **Anthropic & skills.sh Ecosystem**: Frontend design, tool calling specifications, and Claude skills.
- **Nous Research**: Hermes Agent architecture, agent templates, and core skills.
- **Matt Pocock**: `grill-me`, `grill-with-docs` requirement interview architectures.
- **Vercel Labs**: `skills.sh` registry and discovery patterns.
- **Guillaume Meyer**: `watermarks-remover` AI provenance hygiene tooling.
- **Pedro Henrique Rocha de Andrade**: Architecture, catalog curation, Antigravity ecosystem, multi-agent installer, and DevOps skills.

---

## 📊 RepoActivity

[![Star History Chart](https://api.star-history.com/svg?repos=pedroiff0/awesome-skills&type=Date)](https://www.star-history.com/#pedroiff0/awesome-skills&type=Date)

---

## 👨‍💻 Author & Maintainer

<div align="center">

<img src="https://raw.githubusercontent.com/pedroiff0/pedroiff0/main/assets/pedroiff0.gif" alt="pedroiff0" width="900"/>

</div>

<div align="center">

**2026 Awesome Skills**

Made with ☕, code and ☄️ by **Pedro Henrique Rocha de Andrade**

[![GitHub](https://img.shields.io/badge/GitHub-pedroiff0-181717?logo=github&logoColor=white)](https://github.com/pedroiff0)
[![Site Oficial](https://img.shields.io/badge/Site-Oficial-22c55e?logo=googlechrome&logoColor=white)](https://phrandrade.com/)
[![Portfólio](https://img.shields.io/badge/Portfólio-2563eb?logo=github&logoColor=white)](https://pedroiff0.github.io/webpage/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Pedro_Rocha-0077b5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedro-rocha-de-andrade)

</div>
