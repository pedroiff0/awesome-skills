# 🪐 awesome-skills

<div align="center">

![Awesome Skills Banner](assets/banner.svg)

**The Universal, Community-Maintained Catalog of Procedural AI Agent Skills, MCP Servers & Plugins.**

*Write once in canonical `SKILL.md` — Equip instantly across Google Antigravity, Hermes Agent, Claude Code, Cursor, Windsurf, Roo/Cline & OpenCode.*

[![CI](https://github.com/pedroiff0/awesome-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/pedroiff0/awesome-skills/actions/workflows/ci.yml)
![Skills Count](https://img.shields.io/badge/Skills-124-blueviolet?style=flat-square&logo=speedtest&logoColor=white)
![Plugins Count](https://img.shields.io/badge/Plugins-2-purple?style=flat-square&logo=puzzle&logoColor=white)
![MCP Servers](https://img.shields.io/badge/MCP_Servers-4-indigo?style=flat-square&logo=server&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-blue?style=flat-square&logo=linux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
[![Sponsor](https://img.shields.io/badge/Sponsor-Open_for_Sponsors-ea4aaa?style=flat-square&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/pedroiff0)

</div>

---

## ☕ Quick Cosmic Install (One-Liner)

Equip your AI agents instantly using our interactive TUI installer:

```bash
curl -fsSL https://raw.githubusercontent.com/pedroiff0/awesome-skills/main/install.sh | bash
```

Or install and manage via the dedicated Python CLI:

```bash
pip install awesomeskills
awesomeskills install
```

---

## 🖥️ Operating System Support & Auto-Detection

The installer automatically detects your operating system and dynamically configures agent target directories, symlinks, and file copy strategies:

| Operating System | Tier / Support Status | Auto-Detection Mechanism | Target Paths Adapted |
| :--- | :--- | :--- | :--- |
| 🐧 **Linux (Ubuntu, Debian, Arch, Fedora, etc.)** | 🟢 **Tier 1 (Primary & Fully Verified)** | Native POSIX & Linux syscalls | `~/.gemini`, `~/.claude`, `~/.hermes`, `~/.cursor` |
| 🍎 **macOS (Darwin / Apple Silicon & Intel)** | 🟡 **Supported (Paths Adapted)** | `platform.system() == 'Darwin'` | `~/Library/Application Support/...` + dotfiles |
| 🪟 **Windows (WSL / Native / PowerShell)** | 🟡 **Supported (Paths Adapted / WSL Recommended)** | Detects Windows/NT + `%APPDATA%` | `%USERPROFILE%\...`, `%APPDATA%\...` (copy fallback) |

> **Note**: Linux is our primary verified development and testing platform. On macOS and Windows, paths and symlink fallbacks are auto-configured. For Windows users, running inside **WSL (Windows Subsystem for Linux)** is highly recommended.

---

## 🌐 Ecosystem Highlights

- 🎯 **[Explore Open-Source Repositories](references/open-source-repos.md)**: Curated top-starred GitHub projects (100k+ ⭐) enriched via [OpenCurious](https://www.opencurious.com/explore-open-source).
- 🦙 **[Local Ollama Models Catalog](references/ollama-models.md)**: 4 hardware tiers from lightweight (0.5B) to datacenter flagships (70B+) with direct library links.
- 🧩 **[Plugins Directory](plugins/)**: Reusable lifecycle hooks and agent extensions.
- 🔌 **[MCP Servers](mcp/)**: Model Context Protocol servers for enhanced database, filesystem, and context capabilities.

---

## 📚 Skills Catalog Index

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
| [`agy-customizations`](skills/autonomous-ai-agents/agy-customizations/SKILL.md) | Comprehensive guide and reference for the Antigravity Customization System. Use to author skills, contextual rules, plugins, hooks, and MCP servers with correct priori... | Google Antigravity / AGY Community |
| [`antigravity-guide`](skills/autonomous-ai-agents/antigravity-guide/SKILL.md) | Provides a comprehensive guide, architecture reference, and quick-access sitemap for Google Antigravity (AGY), including CLI, Antigravity 2.0, IDE extensions, Python S... | Google Antigravity / AGY Community |
| [`awesome-skills-master`](skills/autonomous-ai-agents/awesome-skills-master/SKILL.md) | Master catalog orchestrator and autonomous installer for AI agents. Use when exploring, cloning, discovering, or installing skills, plugins, or MCP servers from awesom... | awesome-skills Community |
| [`claude-code`](skills/autonomous-ai-agents/claude-code/SKILL.md) | Delegate coding to Claude Code CLI (features, PRs). | Hermes Agent + Teknium |
| [`codex`](skills/autonomous-ai-agents/codex/SKILL.md) | Delegate coding to OpenAI Codex CLI (features, PRs). | Hermes Agent |
| [`computer-use`](skills/autonomous-ai-agents/computer-use/SKILL.md) | | | Anthropic / Open Source Community |
| [`context-mode`](skills/autonomous-ai-agents/context-mode/SKILL.md) | Context optimization and compression routing rules for AI agents exploring large codebases, reading massive logs, searching symbols, and batching tool executions. | Context-Mode Team |
| [`dogfood`](skills/autonomous-ai-agents/dogfood/SKILL.md) | Exploratory QA of web apps: find bugs, evidence, reports. | Hermes Agent Community |
| [`hermes-agent`](skills/autonomous-ai-agents/hermes-agent/SKILL.md) | Configure, extend, or contribute to Hermes Agent. | Hermes Agent + Teknium |
| [`opencode`](skills/autonomous-ai-agents/opencode/SKILL.md) | Delegate coding to OpenCode CLI (features, PR review). | Hermes Agent |
| [`rag-local-lancedb`](skills/autonomous-ai-agents/rag-local-lancedb/SKILL.md) | Build, query, and manage local vector embeddings and semantic search pipelines using LanceDB and HuggingFace/SentenceTransformers embeddings without cloud dependencies. | LanceDB / OSS Community |
| [`skills-sh-registry`](skills/autonomous-ai-agents/skills-sh-registry/SKILL.md) | Discover, query, evaluate, and fetch skills from the open skills.sh ecosystem (Vercel Labs) and global agent skill repositories. | Vercel Labs / skills.sh Community |
| [`watermarks-remover`](skills/autonomous-ai-agents/watermarks-remover/SKILL.md) | Strip multi-vendor AI provenance marks, invisible Unicode characters (ZWSP, ZWNJ, Bidi, variation selectors), statistical text watermarks, and C2PA/EXIF/XMP metadata f... | Guillaume Meyer |
| [`yuanbao`](skills/autonomous-ai-agents/yuanbao/SKILL.md) | Yuanbao (元宝) groups: @mention users, query info/members. | Tencent / Community |

### content-i18n

| Skill | Description | Author / Credits |
|---|---|---|
| [`libretranslate-markdown-i18n`](skills/content-i18n/libretranslate-markdown-i18n/SKILL.md) | Machine-translate Markdown / Obsidian / Quartz content into other languages using a self-hosted LibreTranslate instance, preserving frontmatter, headings, emojis, bold... | LibreTranslate / Community |
| [`mt-markup-preserving-translation`](skills/content-i18n/mt-markup-preserving-translation/SKILL.md) | Translate Markdown/Obsidian/Quartz content with LibreTranslate while preserving wikilinks, embeds, URLs, tables, HTML blocks, proper nouns, and canonical section title... | Open Source Translation Community |

### creative

| Skill | Description | Author / Credits |
|---|---|---|
| [`architecture-diagram`](skills/creative/architecture-diagram/SKILL.md) | Dark-themed SVG architecture/cloud/infra diagrams as HTML. | Cocoon AI (hello@cocoon-ai.com), ported by Hermes Agent |
| [`ascii-art`](skills/creative/ascii-art/SKILL.md) | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. | 0xbyt4, Hermes Agent |
| [`ascii-video`](skills/creative/ascii-video/SKILL.md) | ASCII video: convert video/audio to colored ASCII MP4/GIF. | Open Source Community |
| [`baoyu-infographic`](skills/creative/baoyu-infographic/SKILL.md) | Infographics: 21 layouts x 21 styles (信息图, 可视化). | 宝玉 (JimLiu) |
| [`claude-design`](skills/creative/claude-design/SKILL.md) | Design one-off HTML artifacts (landing, deck, prototype). | BadTechBandit |
| [`comfyui`](skills/creative/comfyui/SKILL.md) | Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter injection. Uses the official comfy-cli for lifecycl... | [kshitijk4poor, alt-glitch, purzbeats] |
| [`design-md`](skills/creative/design-md/SKILL.md) | Author/validate/export Google's DESIGN.md token spec files. | Hermes Agent |
| [`excalidraw`](skills/creative/excalidraw/SKILL.md) | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). | Hermes Agent |
| [`humanizer`](skills/creative/humanizer/SKILL.md) | Humanize text: strip AI-isms and add real voice. | Siqi Chen (@blader, https://github.com/blader/humanizer), ported by Hermes Agent |
| [`manim-video`](skills/creative/manim-video/SKILL.md) | Manim CE animations: 3Blue1Brown math/algo videos. | Manim Community |
| [`p5js`](skills/creative/p5js/SKILL.md) | p5.js sketches: gen art, shaders, interactive, 3D. | Processing Foundation / p5.js Community |
| [`popular-web-designs`](skills/creative/popular-web-designs/SKILL.md) | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. | Hermes Agent + Teknium (design systems sourced from VoltAgent/awesome-design-md) |
| [`portfolio-github-pages`](skills/creative/portfolio-github-pages/SKILL.md) | Build and deploy a personal/academic PORTFOLIO as a single-page STATIC site (no build step) to GitHub Pages via the gh CLI. Use when the user asks for a portfolio, lan... | Open Source Community |
| [`pretext`](skills/creative/pretext/SKILL.md) | Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flow around obstacles, text-as-geometry games, kineti... | Hermes Agent |
| [`sketch`](skills/creative/sketch/SKILL.md) | Throwaway HTML mockups: 2-3 design variants to compare. | Hermes Agent (adapted from gsd-build/get-shit-done) |
| [`songwriting-and-ai-music`](skills/creative/songwriting-and-ai-music/SKILL.md) | Songwriting craft and Suno AI music prompts. | MusicAI / Community |
| [`touchdesigner-mcp`](skills/creative/touchdesigner-mcp/SKILL.md) | Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-time visuals. 36 native tools. | kshitijk4poor |

### data-science

| Skill | Description | Author / Credits |
|---|---|---|
| [`jupyter-live-kernel`](skills/data-science/jupyter-live-kernel/SKILL.md) | Iterative Python via live Jupyter kernel (hamelnb). | Hermes Agent |
| [`suap-iff-api`](skills/data-science/suap-iff-api/SKILL.md) | Authenticate to and consume the SUAP IFF (Instituto Federal Fluminense) API v2 from the CLI — obtain the JWT access/refresh token via matricula+senha, then fetch stude... | IFF Community |

### desktop

| Skill | Description | Author / Credits |
|---|---|---|
| [`desktop-theming`](skills/desktop/desktop-theming/SKILL.md) | Make a Linux desktop (XFCE/GNOME/KDE) look like macOS or otherwise "rice" it — WhiteSur GTK/icon/cursor themes, Plank dock, San-Francisco-like fonts, xfconf config. Us... | Linux / Desktop Theming Community |
| [`hermes-desktop-plugins`](skills/desktop/hermes-desktop-plugins/SKILL.md) | Write desktop app plugins that add UI panes and commands. | Hermes Agent Community |

### devops

| Skill | Description | Author / Credits |
|---|---|---|
| [`docker-single-port-multi-instance`](skills/devops/docker-single-port-multi-instance/SKILL.md) | Consolidate multiple Docker Compose app instances (production / test / demo) behind ONE host port using an nginx reverse proxy that routes by URL path prefix (e.g. /de... | Docker / DevOps Community |
| [`hybrid-desktop-server-ops`](skills/devops/hybrid-desktop-server-ops/SKILL.md) | Comprehensive runbook and operational architecture for running a single Linux machine as both a daily development desktop and a 24/7 home/cloud server (Debian/Ubuntu, ... | DevOps / Linux Community |

### email

| Skill | Description | Author / Credits |
|---|---|---|
| [`himalaya`](skills/email/himalaya/SKILL.md) | Himalaya CLI: IMAP/SMTP email from terminal. | community |

### github

| Skill | Description | Author / Credits |
|---|---|---|
| [`codebase-inspection`](skills/github/codebase-inspection/SKILL.md) | Inspect codebases w/ pygount: LOC, languages, ratios. | Hermes Agent |
| [`git-conventional-commits`](skills/github/git-conventional-commits/SKILL.md) | Author standardized conventional commit messages (feat, fix, docs, refactor, chore), generate automated semver releases, and format pull request descriptions. | Conventional Commits Community |
| [`github-auth`](skills/github/github-auth/SKILL.md) | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. | Hermes Agent |
| [`github-code-review`](skills/github/github-code-review/SKILL.md) | Review PRs: diffs, inline comments via gh or REST. | Hermes Agent |
| [`github-issue-pr-attribs`](skills/github/github-issue-pr-attribs/SKILL.md) | Standardize GitHub ISSUE and PR metadata (Assignee, Reviewer, Labels, Project, Milestone, Development, Relationship) and ship a strong, well-structured code-review tem... | Hermes Agent |
| [`github-issues`](skills/github/github-issues/SKILL.md) | Create, triage, label, assign GitHub issues via gh or REST. | Hermes Agent |
| [`github-pr-workflow`](skills/github/github-pr-workflow/SKILL.md) | GitHub PR lifecycle: branch, commit, open, CI, merge. | Hermes Agent |
| [`github-profile-readme`](skills/github/github-profile-readme/SKILL.md) | Build or rewrite a GitHub profile README (the username/username special repo) with a personalized theme — animated SVG banner, stats cards, contribution snake, tech ba... | GitHub Community |
| [`github-repo-management`](skills/github/github-repo-management/SKILL.md) | Clone/create/fork repos; manage remotes, releases. | Hermes Agent |
| [`github-starred-kb`](skills/github/github-starred-kb/SKILL.md) | Personal GitHub knowledge base built from the user's starred repos (pedroiff0). Maps all 41 starred repositories into knowledge domains (free APIs, sysadmin/self-hoste... | Hermes Agent |
| [`hermes-installed-catalog`](skills/github/hermes-installed-catalog/SKILL.md) | Live catalog of skills, plugins, and agents actually installed on THIS Hermes server (pedroiff0). Lists the 233 installed skills grouped by domain, the 18 installed pl... | Hermes Agent |
| [`readme-template`](skills/github/readme-template/SKILL.md) | Standard README template for repos — professional structure with badges, overview, table of contents, features/modules, stack, installation, configuration, tests, secu... | pedroiff0 |

### latex

| Skill | Description | Author / Credits |
|---|---|---|
| [`cv-latex-multilingual`](skills/latex/cv-latex-multilingual/SKILL.md) | Manter o CV LaTeX multilíngue do usuário (classe altacv) em ~/Repositorios/pessoal/cv — PT (fonte), EN (espelho), ES/FR (gerados do EN via translate_cv.py). Abrange co... | LaTeX Community |
| [`latex-cv-maintenance`](skills/latex/latex-cv-maintenance/SKILL.md) | Use when reviewing, updating, or keeping consistent a multi-language LaTeX CV (altacv.cls). Covers treating Portuguese as source of truth and mirroring to other langua... | Hermes Agent |

### media

| Skill | Description | Author / Credits |
|---|---|---|
| [`gif-search`](skills/media/gif-search/SKILL.md) | Search/download GIFs from Tenor via curl + jq. | Hermes Agent |
| [`heartmula`](skills/media/heartmula/SKILL.md) | HeartMuLa: Suno-like song generation from lyrics + tags. | Heartmula Community |
| [`songsee`](skills/media/songsee/SKILL.md) | Audio spectrograms/features (mel, chroma, MFCC) via CLI. | community |
| [`youtube-content`](skills/media/youtube-content/SKILL.md) | YouTube transcripts to summaries, threads, blogs. | YouTube Tools Community |

### mlops

| Skill | Description | Author / Credits |
|---|---|---|
| [`audiocraft`](skills/mlops/audiocraft/SKILL.md) | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. | Orchestra Research |
| [`gpu-debian-setup`](skills/mlops/gpu-debian-setup/SKILL.md) | Install and verify NVIDIA proprietary GPU drivers on Debian (including trixie/13) so local LLM tools (Ollama, llama.cpp, vLLM) can use the GPU. Covers nouveau blacklis... | Debian / NVIDIA Community |
| [`huggingface-hub`](skills/mlops/huggingface-hub/SKILL.md) | HuggingFace hf CLI: search/download/upload models, datasets. | Hugging Face |
| [`llama-cpp`](skills/mlops/llama-cpp/SKILL.md) | llama.cpp local GGUF inference + HF Hub model discovery. | Orchestra Research |
| [`lm-evaluation-harness`](skills/mlops/lm-evaluation-harness/SKILL.md) | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). | Orchestra Research |
| [`segment-anything`](skills/mlops/segment-anything/SKILL.md) | SAM: zero-shot image segmentation via points, boxes, masks. | Orchestra Research |
| [`vllm`](skills/mlops/vllm/SKILL.md) | vLLM: high-throughput LLM serving, OpenAI API, quantization. | Orchestra Research |
| [`weights-and-biases`](skills/mlops/weights-and-biases/SKILL.md) | W&B: log ML experiments, sweeps, model registry, dashboards. | Orchestra Research |

### note-taking

| Skill | Description | Author / Credits |
|---|---|---|
| [`obsidian`](skills/note-taking/obsidian/SKILL.md) | Read, search, create, and edit notes in the Obsidian vault. | Obsidian Community |

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
| [`powerpoint`](skills/productivity/powerpoint/SKILL.md) | Create, read, edit .pptx decks, slides, notes, templates. | Microsoft / python-pptx Community |
| [`suap-api`](skills/productivity/suap-api/SKILL.md) | Consume the SUAP (Sistema Unificado de Administração Pública) REST API v2 used by Brazilian federal institutes (IFRN, IFF, IFS, etc.) — obtain a JWT via /api/v2/autent... | SUAP Community |
| [`teams-meeting-pipeline`](skills/productivity/teams-meeting-pipeline/SKILL.md) | Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs, manage Microsoft Graph subscriptions. | Hermes Agent + Teknium |

### research

| Skill | Description | Author / Credits |
|---|---|---|
| [`arxiv`](skills/research/arxiv/SKILL.md) | Search arXiv papers by keyword, author, category, or ID. | Hermes Agent |
| [`blogwatcher`](skills/research/blogwatcher/SKILL.md) | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. | JulienTant (fork of Hyaxia/blogwatcher) |
| [`grill-me-interview`](skills/research/grill-me-interview/SKILL.md) | Conduct an interactive, rigorous architecture interview. Grills the user with probing questions one at a time to clarify ambiguous requirements, design decisions, edge... | Matt Pocock / skills.sh Community |
| [`lattes-xml-projetos`](skills/research/lattes-xml-projetos/SKILL.md) | Use when gerar, limpar ou inserir itens de bolsa/projetos de pesquisa (PARTICIPACAO-EM-PROJETO / PROJETO-DE-PESQUISA) em XML de importação do Currículo Lattes. Cobre a... | Hermes Agent |
| [`llm-wiki`](skills/research/llm-wiki/SKILL.md) | Karpathy's LLM Wiki: build/query interlinked markdown KB. | Hermes Agent |
| [`nosignups-catalog`](skills/research/nosignups-catalog/SKILL.md) | Catálogo curado de ferramentas open source sem signup (NoSignups.net). 234 tools organizadas por categoria e relevância para DevOps/self-hosted/operations. Use para en... | NoSignups Community |
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
| [`adhoc-verification`](skills/software-development/adhoc-verification/SKILL.md) | Produce fresh, focused, local verification evidence for a code change without relying on the full test suite. Use when a system reminder (or the user) demands ad-hoc v... | Hermes Agent Community |
| [`docker-compose-app-recovery`](skills/software-development/docker-compose-app-recovery/SKILL.md) | Recover or reset credentials and directly operate the database of an app running under docker-compose (lost admin password, one-time seed password, locked out, read/wr... | DevOps Community |
| [`document-exports`](skills/software-development/document-exports/SKILL.md) | Generate and TEST downloadable document exports (PDF/CSV) from a Node/Express backend — pdfkit streaming, CSV BOM, cents formatting, and the supertest/pdfkit pitfalls ... | Pandoc / Document Tools Community |
| [`docx-analysis-conversion`](skills/software-development/docx-analysis-conversion/SKILL.md) | Extract, analyze, edit, and convert Microsoft Word (.docx) documents to structured Markdown, JSON, or clean text preserving tables, headers, and bullet lists. | Open Source Python Community |
| [`financas-app`](skills/software-development/financas-app/SKILL.md) | Corrigir, estender e validar o app de finanças pessoais (Node/Express + EJS + MongoDB + Docker). Cobre a arquitetura de porta única 4460 com demo via /demo, o fluxo de... | Fullstack Community |
| [`frontend-design-systems`](skills/software-development/frontend-design-systems/SKILL.md) | Architect and build production-grade web interfaces with modern design systems: Tailwind CSS v4, Shadcn UI primitives, Radix UI, dark mode tokens, and accessible WCAG ... | Anthropic / skills.sh Community |
| [`grill-with-docs`](skills/software-development/grill-with-docs/SKILL.md) | Cross-examine codebase architecture against official library documentation and API specs. Identifies deprecations, anti-patterns, and suboptimal library usage. | Matt Pocock / skills.sh Community |
| [`handoff-resume`](skills/software-development/handoff-resume/SKILL.md) | Resume in-progress coding work across sessions from a HANDOFF.md and a dirty git working tree. Use when a task says "continue from HANDOFF.md", "retomar o processament... | Hermes Agent Community |
| [`hermes-agent-skill-authoring`](skills/software-development/hermes-agent-skill-authoring/SKILL.md) | Author in-repo SKILL.md: frontmatter, validator, structure, and writing-quality principles. | Hermes Agent |
| [`node-inspect-debugger`](skills/software-development/node-inspect-debugger/SKILL.md) | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. | Hermes Agent |
| [`obscure-tool-install-lookup`](skills/software-development/obscure-tool-install-lookup/SKILL.md) | Use when a user asks how to install or use an obscure CLI tool, agent, or package and search engines are blocked, CAPTCHA-walled, or unhelpful. Resolves canonical inst... | Hermes Agent |
| [`plan`](skills/software-development/plan/SKILL.md) | Plan mode: write an actionable markdown plan to .hermes/plans/, no execution. Bite-sized tasks, exact paths, complete code. | Hermes Agent (writing-craft adapted from obra/superpowers) |
| [`playwright-browser-automation`](skills/software-development/playwright-browser-automation/SKILL.md) | Run automated headless browser testing, scrape dynamic SPAs, capture high-resolution full-page screenshots, and perform visual regression testing with Playwright. | Microsoft Playwright / OSS Community |
| [`projeto-profissional`](skills/software-development/projeto-profissional/SKILL.md) | Bootstrap a new professional repo from Pedro's hardened Node/Express+MongoDB+EJS base template (JWT auth, admin/user roles, admin-controlled registration, security def... | Fullstack Boilerplate Community |
| [`projeto-profissional-template`](skills/software-development/projeto-profissional-template/SKILL.md) | Development & operations workflow for the user's "projeto-professional" template (Node 20 + Express + MongoDB/Mongoose + EJS SSR + JWT). Captures recurring gotchas — r... | Fullstack Boilerplate Community |
| [`python-debugpy`](skills/software-development/python-debugpy/SKILL.md) | Debug Python: pdb REPL + debugpy remote (DAP). | Hermes Agent |
| [`requesting-code-review`](skills/software-development/requesting-code-review/SKILL.md) | Pre-commit review: security scan, quality gates, auto-fix. | Hermes Agent (adapted from obra/superpowers + MorAlekss) |
| [`security-sast-audit`](skills/software-development/security-sast-audit/SKILL.md) | Perform static application security testing (SAST), secret scanning, dependency vulnerability audits (OWASP Top 10, bandit, semgrep, trivy, pip-audit, npm audit). | OWASP / Security Community |
| [`simplify-code`](skills/software-development/simplify-code/SKILL.md) | Parallel 3-agent cleanup of recent code changes. | Hermes Agent (inspired by Claude Code /simplify) |
| [`spike`](skills/software-development/spike/SKILL.md) | Throwaway experiments to validate an idea before build. | Hermes Agent (adapted from gsd-build/get-shit-done) |
| [`systematic-debugging`](skills/software-development/systematic-debugging/SKILL.md) | 4-phase root cause debugging: understand bugs before fixing. | Hermes Agent (adapted from obra/superpowers) |
| [`test-driven-development`](skills/software-development/test-driven-development/SKILL.md) | TDD: enforce RED-GREEN-REFACTOR, tests before code. | Hermes Agent (adapted from obra/superpowers) |
| [`web-fullstack-gotchas`](skills/software-development/web-fullstack-gotchas/SKILL.md) | Armadilhas recorrentes em apps fullstack Node/Express + EJS + CSS + jest + Docker (padrão do projeto financas-app, mas aplicável a qualquer stack similar). USE quando ... | Fullstack Community |
| [`xlsx-data-wrangling`](skills/software-development/xlsx-data-wrangling/SKILL.md) | Query, validate, clean, and manipulate Excel (.xlsx/.xls) spreadsheets programmatically without GUI using pandas, openpyxl, and polars. | Open Source Python Community |

### web

| Skill | Description | Author / Credits |
|---|---|---|
| [`animated-portfolio-sites`](skills/web/animated-portfolio-sites/SKILL.md) | Build a one-page animated personal or portfolio site (canvas starfield, rotating galaxies with mouse parallax, hidden accordion/card content, anchor nav) and publish i... | Hermes Agent |
| [`express-csp-runtime-config`](skills/web/express-csp-runtime-config/SKILL.md) | How to pass server-side runtime config (API prefix, feature flags, user id, CSRF token) from an Express/EJS app to client JS when a strict Content-Security-Policy is i... | Express.js Community |
| [`frontend-visual-verification`](skills/web/frontend-visual-verification/SKILL.md) | Confirm a CSS/HTML/template change actually rendered in a running browser — without being fooled by stale browser cache. Use whenever you edited frontend code (CSS, EJ... | Web Dev Community |
| [`github-pages-portfolio`](skills/web/github-pages-portfolio/SKILL.md) | Build, update, and verify a single-page static portfolio / intro site on GitHub Pages (pure HTML+CSS+JS, no build step). Covers sourcing content read-only from the use... | GitHub Pages Community |
| [`markdown-site-source-pipeline`](skills/web/markdown-site-source-pipeline/SKILL.md) | Keep a static HTML/JS site's content in an editable Markdown source file; generate the data artifact (JS/JSON) the site consumes; guarantee identical render via semant... | Static Site Community |
| [`markdown-static-site-source`](skills/web/markdown-static-site-source/SKILL.md) | Make a data-driven static site (content lives in a JS/JSON object consumed by a render script) editable from Markdown/Obsidian. Generate the data file from a YAML-fron... | Static Site Community |
| [`nextjs-app-router-patterns`](skills/web/nextjs-app-router-patterns/SKILL.md) | Architect and implement modern Next.js App Router applications with Server Components (RSC), Server Actions, Parallel/Intercepting Routes, and Streaming SSR. | Vercel / Next.js Community |
| [`quartz-multilang-site-maintenance`](skills/web/quartz-multilang-site-maintenance/SKILL.md) | Maintain and edit a Quartz static site (Quartz Syncer / quartz-site fork) that publishes to GitHub Pages — especially editing the 4-language home/index pages (pt-br/en... | Hermes Agent |
| [`static-site-md-source`](skills/web/static-site-md-source/SKILL.md) | Turn an EXISTING static site (HTML/CSS/JS) into a Markdown-editable source WITHOUT changing its rendered output. Use when the user likes the current site ("muito bom, ... | Static Site Community |

---

## 📂 Repository Structure

```
awesome-skills/
  ├── skills/<category>/<name>/   # Canonical SKILL.md + references/ + scripts/
  ├── plugins/<name>/             # Reusable agent plugins & lifecycle hooks
  ├── mcp/<name>/                 # Model Context Protocol (MCP) server definitions
  ├── install.sh                  # Universal interactive installer with OS detection
  ├── tools/
  │   ├── installer.py            # TUI & CLI installation engine (with OS detector)
  │   └── gen_index.py            # Regenerates README catalog index
  ├── references/                 # Open-Source repositories & Ollama models registries
  ├── templates/                  # Starter kits: skill / agent / plugin / mcp
  ├── packages/awesomeskills/     # Python package CLI (`awesomeskills install`)
  ├── docs/CODE_REVIEW.md         # Review standard
  └── .github/                    # Issue & PR templates + CI workflow
```

---

## 💖 Sponsor & Support

Maintaining and expanding the largest universal multi-agent skills catalog requires continuous testing across model APIs, local hardware benchmarks, and community curation.

If **awesome-skills** helps accelerate your AI coding workflows, consider sponsoring the project:

<div align="center">

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor_on-GitHub_Sponsors-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/pedroiff0)

*Your sponsorship helps fund open-weight model testing, server infrastructure, and daily catalog expansion.*

</div>

---

## 🤝 Contributing & Submissions

Contributions are warmly welcomed from the entire open-source community!

- 💡 **Add New Skills**: Submit a PR following `templates/skill/SKILL.md`.
- 🔌 **Add Plugins / MCP**: Provide structured definitions in `plugins/` or `mcp/`.
- 🌐 **Translations & Fixes**: Enhance documentation, multi-OS support, and model catalogs.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/CODE_REVIEW.md](docs/CODE_REVIEW.md) before submitting.

---

## ⚖️ Author Credits & Attribution Standards

awesome-skills strictly credits all original authors, community projects, and research creators:
- **Anthropic & skills.sh Ecosystem**: Frontend design, tool calling specifications, and Claude skills.
- **Nous Research**: Hermes Agent architecture, agent templates, and core skills.
- **Matt Pocock**: `grill-me`, `grill-with-docs` requirement interview architectures.
- **Vercel Labs**: `skills.sh` registry and discovery patterns.
- **Guillaume Meyer**: `watermarks-remover` AI provenance hygiene tooling.
- **Open Source Community**: Open-source tools, Playwright, Pandas, Next.js, Docker, LaTeX, and Linux ecosystem skills.
- **Pedro Henrique Rocha de Andrade**: Repository architecture, catalog curation, and universal multi-agent installer.

---

## 📊 RepoActivity

[![Star History Chart](https://api.star-history.com/svg?repos=pedroiff0/awesome-skills&type=Date)](https://www.star-history.com/#pedroiff0/awesome-skills&type=Date)

---

## 👨‍💻 Maintainer & Curator

<div align="center">

<img src="https://raw.githubusercontent.com/pedroiff0/pedroiff0/main/assets/pedroiff0.gif" alt="pedroiff0" width="900"/>

</div>

<div align="center">

**2026 Awesome Skills**

Curated with ☕, code and ☄️ by **Pedro Henrique Rocha de Andrade**

[![GitHub](https://img.shields.io/badge/GitHub-pedroiff0-181717?logo=github&logoColor=white)](https://github.com/pedroiff0)
[![Site Oficial](https://img.shields.io/badge/Site-Oficial-22c55e?logo=googlechrome&logoColor=white)](https://phrandrade.com/)
[![Portfólio](https://img.shields.io/badge/Portfólio-2563eb?logo=github&logoColor=white)](https://pedroiff0.github.io/webpage/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Pedro_Rocha-0077b5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedro-rocha-de-andrade)

</div>
