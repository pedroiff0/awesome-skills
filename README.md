<div align="center">

# awesome-skills

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Skills](https://img.shields.io/badge/skills-119-blue.svg)
![Categories](https://img.shields.io/badge/categories-19-blue.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Multi-Agent](https://img.shields.io/badge/Multi--Agent-AGY%20|%20Claude%20|%20Hermes%20|%20Cursor-8a2be2.svg)

**Universal multi-agent library of reusable Skills, Agents & Rules.**

*Write once in `SKILL.md` — run on Google Antigravity, Claude Code, Hermes Agent, Cursor, Windsurf & Cline.*

</div>

---

## ⚡ Quick Start: Interactive Installer (Caveman-style)

Install skills interactively with a TUI menu, fuzzy search, agent selector, and curated packs:

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

Select your AI agent or IDE below for ready-to-run setup commands:

### 🪐 Google Antigravity (AGY)

```bash
# Global User Skills (available in all workspaces)
mkdir -p ~/.gemini/antigravity-cli/skills
cp -r skills/*/* ~/.gemini/antigravity-cli/skills/

# Or install into current workspace
mkdir -p .agent/skills
cp -r skills/<category>/<skill> .agent/skills/
```

### 🏛️ Hermes Agent (Nous Research)

```bash
# Global installation into Hermes catalog
mkdir -p ~/.hermes/skills
cp -r skills/* ~/.hermes/skills/

# Install single category
cp -r skills/devops ~/.hermes/skills/
```

### ⚡ Claude Code (Anthropic CLI)

```bash
# Global installation for Claude Code CLI
mkdir -p ~/.claude/skills
cp -r skills/*/* ~/.claude/skills/

# Workspace installation
mkdir -p .claude/skills
cp -r skills/<category>/<skill> .claude/skills/
```

### 🎯 Cursor IDE (.mdc Rules)

```bash
# Automatically convert & install skills as Cursor rules (.cursor/rules/*.mdc)
./install.sh --agent cursor --scope local --pack fullstack
```

### 🌊 Windsurf & Roo Code / Cline

```bash
# Windsurf Workspace Skills
mkdir -p .windsurf/skills && cp -r skills/*/* .windsurf/skills/

# Roo Code / Cline Skills
mkdir -p ~/.roo/skills && cp -r skills/*/* ~/.roo/skills/
```

---

## 📦 Curated Packs

| Pack | Focus | Key Categories | Install Command |
| :--- | :--- | :--- | :--- |
| **🚀 Full-Stack Dev** | Web, APIs, Testing, Refactoring | `software-development`, `web`, `github` | `./install.sh --pack fullstack` |
| **⚡ DevOps & Cloud** | Containers, Caddy, Cloudflare, CI/CD | `devops`, `github` | `./install.sh --pack devops` |
| **🧠 Autonomous AI & MLOps** | Multi-Agent topologies, RAG, Token ops | `autonomous-ai-agents`, `mlops` | `./install.sh --pack ai` |
| **📚 Academic & LaTeX** | Paper writing, LaTeX CVs, arXiv, i18n | `latex`, `research`, `content-i18n` | `./install.sh --pack academic` |
| **🎨 Creative & Media** | Architecture diagrams, ASCII, Audio | `creative`, `media`, `desktop` | `./install.sh --pack creative` |
| **📦 Complete Catalog** | All 118+ skills across 19 categories | All categories | `./install.sh --pack all` |

---

## 🌐 Multi-Agent Architecture

Every entry is a self-contained, versioned unit consumed — with thin adaptors — by the major agent runtimes:

| Runtime | Loads From | Format |
| :--- | :--- | :--- |
| **Google Antigravity (AGY)** | `~/.gemini/antigravity-cli/skills/` or `.agent/skills/` | `SKILL.md` (native) |
| **Hermes Agent** | `~/.hermes/skills/<cat>/<skill>/` | `SKILL.md` (native) |
| **Claude Code** | `~/.claude/skills/<skill>/` | `SKILL.md` / `CLAUDE.md` |
| **Cursor** | `.cursor/rules/<skill>.mdc` | MDC Rule with frontmatter |
| **Windsurf** | `.windsurfrules` or `.windsurf/skills/` | Markdown Context |
| **Roo Code / Cline** | `~/.roomodes` / `~/.roo/skills/` | `SKILL.md` (native) |
| **OpenCode / Codex** | `~/.config/opencode/skills/` | Markdown Rule |

> See [`templates/`](templates/) for starter kits (skill / agent / plugin).

---

## 🗂️ Skills Catalog Index

> **119 skills** organized across **19 categories**.

### apple

| Skill | Description |
|---|---|
| [`apple-notes`](skills/apple/apple-notes/SKILL.md) | Manage Apple Notes via memo CLI: create, search, edit. |
| [`apple-reminders`](skills/apple/apple-reminders/SKILL.md) | Apple Reminders via remindctl: add, list, complete. |
| [`findmy`](skills/apple/findmy/SKILL.md) | Track Apple devices/AirTags via FindMy.app on macOS. |
| [`imessage`](skills/apple/imessage/SKILL.md) | Send and receive iMessages/SMS via the imsg CLI on macOS. |

### autonomous-ai-agents

| Skill | Description |
|---|---|
| [`agy-customizations`](skills/autonomous-ai-agents/agy-customizations/SKILL.md) | Comprehensive guide and reference for the Antigravity Customization System. Use to author skills, contextual rules, plugins, hooks, and MCP servers with correct priority loading. |
| [`antigravity-guide`](skills/autonomous-ai-agents/antigravity-guide/SKILL.md) | Provides a comprehensive guide, architecture reference, and quick-access sitemap for Google Antigravity (AGY), including CLI, Antigravity 2.0, IDE extensions, Python SDK, slash... |
| [`claude-code`](skills/autonomous-ai-agents/claude-code/SKILL.md) | Delegate coding to Claude Code CLI (features, PRs). |
| [`codex`](skills/autonomous-ai-agents/codex/SKILL.md) | Delegate coding to OpenAI Codex CLI (features, PRs). |
| [`computer-use`](skills/autonomous-ai-agents/computer-use/SKILL.md) | \| |
| [`context-mode`](skills/autonomous-ai-agents/context-mode/SKILL.md) | Context optimization and compression routing rules for AI agents exploring large codebases, reading massive logs, searching symbols, and batching tool executions. |
| [`dogfood`](skills/autonomous-ai-agents/dogfood/SKILL.md) | Exploratory QA of web apps: find bugs, evidence, reports. |
| [`hermes-agent`](skills/autonomous-ai-agents/hermes-agent/SKILL.md) | Configure, extend, or contribute to Hermes Agent. |
| [`opencode`](skills/autonomous-ai-agents/opencode/SKILL.md) | Delegate coding to OpenCode CLI (features, PR review). |
| [`rag-local-lancedb`](skills/autonomous-ai-agents/rag-local-lancedb/SKILL.md) | Build, query, and manage local vector embeddings and semantic search pipelines using LanceDB and HuggingFace/SentenceTransformers embeddings without cloud dependencies. |
| [`watermarks-remover`](skills/autonomous-ai-agents/watermarks-remover/SKILL.md) | Strip multi-vendor AI provenance marks, invisible Unicode characters (ZWSP, ZWNJ, Bidi, variation selectors), statistical text watermarks, and C2PA/EXIF/XMP metadata from files... |
| [`yuanbao`](skills/autonomous-ai-agents/yuanbao/SKILL.md) | Yuanbao (元宝) groups: @mention users, query info/members. |

### content-i18n

| Skill | Description |
|---|---|
| [`libretranslate-markdown-i18n`](skills/content-i18n/libretranslate-markdown-i18n/SKILL.md) | Machine-translate Markdown / Obsidian / Quartz content into other languages using a self-hosted LibreTranslate instance, preserving frontmatter, headings, emojis, bold/italic, w... |
| [`mt-markup-preserving-translation`](skills/content-i18n/mt-markup-preserving-translation/SKILL.md) | Translate Markdown/Obsidian/Quartz content with LibreTranslate while preserving wikilinks, embeds, URLs, tables, HTML blocks, proper nouns, and canonical section titles. Use for... |

### creative

| Skill | Description |
|---|---|
| [`architecture-diagram`](skills/creative/architecture-diagram/SKILL.md) | Dark-themed SVG architecture/cloud/infra diagrams as HTML. |
| [`ascii-art`](skills/creative/ascii-art/SKILL.md) | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. |
| [`ascii-video`](skills/creative/ascii-video/SKILL.md) | ASCII video: convert video/audio to colored ASCII MP4/GIF. |
| [`baoyu-infographic`](skills/creative/baoyu-infographic/SKILL.md) | Infographics: 21 layouts x 21 styles (信息图, 可视化). |
| [`claude-design`](skills/creative/claude-design/SKILL.md) | Design one-off HTML artifacts (landing, deck, prototype). |
| [`comfyui`](skills/creative/comfyui/SKILL.md) | Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter injection. Uses the official comfy-cli for lifecycle and dire... |
| [`design-md`](skills/creative/design-md/SKILL.md) | Author/validate/export Google's DESIGN.md token spec files. |
| [`excalidraw`](skills/creative/excalidraw/SKILL.md) | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). |
| [`humanizer`](skills/creative/humanizer/SKILL.md) | Humanize text: strip AI-isms and add real voice. |
| [`manim-video`](skills/creative/manim-video/SKILL.md) | Manim CE animations: 3Blue1Brown math/algo videos. |
| [`p5js`](skills/creative/p5js/SKILL.md) | p5.js sketches: gen art, shaders, interactive, 3D. |
| [`popular-web-designs`](skills/creative/popular-web-designs/SKILL.md) | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. |
| [`portfolio-github-pages`](skills/creative/portfolio-github-pages/SKILL.md) | Build and deploy a personal/academic PORTFOLIO as a single-page STATIC site (no build step) to GitHub Pages via the gh CLI. Use when the user asks for a portfolio, landing page,... |
| [`pretext`](skills/creative/pretext/SKILL.md) | Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flow around obstacles, text-as-geometry games, kinetic typograp... |
| [`sketch`](skills/creative/sketch/SKILL.md) | Throwaway HTML mockups: 2-3 design variants to compare. |
| [`songwriting-and-ai-music`](skills/creative/songwriting-and-ai-music/SKILL.md) | Songwriting craft and Suno AI music prompts. |
| [`touchdesigner-mcp`](skills/creative/touchdesigner-mcp/SKILL.md) | Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-time visuals. 36 native tools. |

### data-science

| Skill | Description |
|---|---|
| [`jupyter-live-kernel`](skills/data-science/jupyter-live-kernel/SKILL.md) | Iterative Python via live Jupyter kernel (hamelnb). |
| [`suap-iff-api`](skills/data-science/suap-iff-api/SKILL.md) | Authenticate to and consume the SUAP IFF (Instituto Federal Fluminense) API v2 from the CLI — obtain the JWT access/refresh token via matricula+senha, then fetch student data (p... |

### desktop

| Skill | Description |
|---|---|
| [`desktop-theming`](skills/desktop/desktop-theming/SKILL.md) | Make a Linux desktop (XFCE/GNOME/KDE) look like macOS or otherwise "rice" it — WhiteSur GTK/icon/cursor themes, Plank dock, San-Francisco-like fonts, xfconf config. Use when a u... |
| [`hermes-desktop-plugins`](skills/desktop/hermes-desktop-plugins/SKILL.md) | Write desktop app plugins that add UI panes and commands. |

### devops

| Skill | Description |
|---|---|
| [`docker-single-port-multi-instance`](skills/devops/docker-single-port-multi-instance/SKILL.md) | Consolidate multiple Docker Compose app instances (production / test / demo) behind ONE host port using an nginx reverse proxy that routes by URL path prefix (e.g. /demo). Use w... |
| [`hybrid-desktop-server-ops`](skills/devops/hybrid-desktop-server-ops/SKILL.md) | Comprehensive runbook and operational architecture for running a single Linux machine as both a daily development desktop and a 24/7 home/cloud server (Debian/Ubuntu, GNOME, Doc... |

### email

| Skill | Description |
|---|---|
| [`himalaya`](skills/email/himalaya/SKILL.md) | Himalaya CLI: IMAP/SMTP email from terminal. |

### github

| Skill | Description |
|---|---|
| [`codebase-inspection`](skills/github/codebase-inspection/SKILL.md) | Inspect codebases w/ pygount: LOC, languages, ratios. |
| [`git-conventional-commits`](skills/github/git-conventional-commits/SKILL.md) | Author standardized conventional commit messages (feat, fix, docs, refactor, chore), generate automated semver releases, and format pull request descriptions. |
| [`github-auth`](skills/github/github-auth/SKILL.md) | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. |
| [`github-code-review`](skills/github/github-code-review/SKILL.md) | Review PRs: diffs, inline comments via gh or REST. |
| [`github-issue-pr-attribs`](skills/github/github-issue-pr-attribs/SKILL.md) | Standardize GitHub ISSUE and PR metadata (Assignee, Reviewer, Labels, Project, Milestone, Development, Relationship) and ship a strong, well-structured code-review template. Inc... |
| [`github-issues`](skills/github/github-issues/SKILL.md) | Create, triage, label, assign GitHub issues via gh or REST. |
| [`github-pr-workflow`](skills/github/github-pr-workflow/SKILL.md) | GitHub PR lifecycle: branch, commit, open, CI, merge. |
| [`github-profile-readme`](skills/github/github-profile-readme/SKILL.md) | Build or rewrite a GitHub profile README (the username/username special repo) with a personalized theme — animated SVG banner, stats cards, contribution snake, tech badges, proj... |
| [`github-repo-management`](skills/github/github-repo-management/SKILL.md) | Clone/create/fork repos; manage remotes, releases. |
| [`github-starred-kb`](skills/github/github-starred-kb/SKILL.md) | Personal GitHub knowledge base built from the user's starred repos (pedroiff0). Maps all 41 starred repositories into knowledge domains (free APIs, sysadmin/self-hosted, Python,... |
| [`hermes-installed-catalog`](skills/github/hermes-installed-catalog/SKILL.md) | Live catalog of skills, plugins, and agents actually installed on THIS Hermes server (pedroiff0). Lists the 233 installed skills grouped by domain, the 18 installed plugins, and... |
| [`readme-template`](skills/github/readme-template/SKILL.md) | Standard README template for repos — professional structure with badges, overview, table of contents, features/modules, stack, installation, configuration, tests, security, stru... |

### latex

| Skill | Description |
|---|---|
| [`cv-latex-multilingual`](skills/latex/cv-latex-multilingual/SKILL.md) | Manter o CV LaTeX multilíngue do usuário (classe altacv) em ~/Repositorios/pessoal/cv — PT (fonte), EN (espelho), ES/FR (gerados do EN via translate_cv.py). Abrange correções de... |
| [`latex-cv-maintenance`](skills/latex/latex-cv-maintenance/SKILL.md) | Use when reviewing, updating, or keeping consistent a multi-language LaTeX CV (altacv.cls). Covers treating Portuguese as source of truth and mirroring to other languages, cross... |

### media

| Skill | Description |
|---|---|
| [`gif-search`](skills/media/gif-search/SKILL.md) | Search/download GIFs from Tenor via curl + jq. |
| [`heartmula`](skills/media/heartmula/SKILL.md) | HeartMuLa: Suno-like song generation from lyrics + tags. |
| [`songsee`](skills/media/songsee/SKILL.md) | Audio spectrograms/features (mel, chroma, MFCC) via CLI. |
| [`youtube-content`](skills/media/youtube-content/SKILL.md) | YouTube transcripts to summaries, threads, blogs. |

### mlops

| Skill | Description |
|---|---|
| [`audiocraft-audio-generation`](skills/mlops/audiocraft/SKILL.md) | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. |
| [`evaluating-llms-harness`](skills/mlops/lm-evaluation-harness/SKILL.md) | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). |
| [`gpu-debian-setup`](skills/mlops/gpu-debian-setup/SKILL.md) | Install and verify NVIDIA proprietary GPU drivers on Debian (including trixie/13) so local LLM tools (Ollama, llama.cpp, vLLM) can use the GPU. Covers nouveau blacklist, initram... |
| [`huggingface-hub`](skills/mlops/huggingface-hub/SKILL.md) | HuggingFace hf CLI: search/download/upload models, datasets. |
| [`llama-cpp`](skills/mlops/llama-cpp/SKILL.md) | llama.cpp local GGUF inference + HF Hub model discovery. |
| [`segment-anything-model`](skills/mlops/segment-anything/SKILL.md) | SAM: zero-shot image segmentation via points, boxes, masks. |
| [`serving-llms-vllm`](skills/mlops/vllm/SKILL.md) | vLLM: high-throughput LLM serving, OpenAI API, quantization. |
| [`weights-and-biases`](skills/mlops/weights-and-biases/SKILL.md) | W&B: log ML experiments, sweeps, model registry, dashboards. |

### note-taking

| Skill | Description |
|---|---|
| [`obsidian`](skills/note-taking/obsidian/SKILL.md) | Read, search, create, and edit notes in the Obsidian vault. |

### productivity

| Skill | Description |
|---|---|
| [`airtable`](skills/productivity/airtable/SKILL.md) | Airtable REST API via curl. Records CRUD, filters, upserts. |
| [`google-workspace`](skills/productivity/google-workspace/SKILL.md) | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. |
| [`maps`](skills/productivity/maps/SKILL.md) | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. |
| [`nano-pdf`](skills/productivity/nano-pdf/SKILL.md) | Edit PDF text/typos/titles via nano-pdf CLI (NL prompts). |
| [`notion`](skills/productivity/notion/SKILL.md) | Notion API + ntn CLI: pages, databases, markdown, Workers. |
| [`ocr-and-documents`](skills/productivity/ocr-and-documents/SKILL.md) | Extract text from PDFs/scans (pymupdf, marker-pdf). |
| [`petdex`](skills/productivity/petdex/SKILL.md) | Install and select animated petdex mascots for Hermes. |
| [`powerpoint`](skills/productivity/powerpoint/SKILL.md) | Create, read, edit .pptx decks, slides, notes, templates. |
| [`suap-api`](skills/productivity/suap-api/SKILL.md) | Consume the SUAP (Sistema Unificado de Administração Pública) REST API v2 used by Brazilian federal institutes (IFRN, IFF, IFS, etc.) — obtain a JWT via /api/v2/autenticacao/tok... |
| [`teams-meeting-pipeline`](skills/productivity/teams-meeting-pipeline/SKILL.md) | Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs, manage Microsoft Graph subscriptions. |

### research

| Skill | Description |
|---|---|
| [`arxiv`](skills/research/arxiv/SKILL.md) | Search arXiv papers by keyword, author, category, or ID. |
| [`blogwatcher`](skills/research/blogwatcher/SKILL.md) | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. |
| [`lattes-xml-projetos`](skills/research/lattes-xml-projetos/SKILL.md) | Use when gerar, limpar ou inserir itens de bolsa/projetos de pesquisa (PARTICIPACAO-EM-PROJETO / PROJETO-DE-PESQUISA) em XML de importação do Currículo Lattes. Cobre a estrutura... |
| [`llm-wiki`](skills/research/llm-wiki/SKILL.md) | Karpathy's LLM Wiki: build/query interlinked markdown KB. |
| [`nosignups-catalog`](skills/research/nosignups-catalog/SKILL.md) | Catálogo curado de ferramentas open source sem signup (NoSignups.net). 234 tools organizadas por categoria e relevância para DevOps/self-hosted/operations. Use para encontrar al... |
| [`polymarket`](skills/research/polymarket/SKILL.md) | Query Polymarket: markets, prices, orderbooks, history. |
| [`research-paper-writing`](skills/research/research-paper-writing/SKILL.md) | Write ML papers for NeurIPS/ICML/ICLR: design→submit. |

### smart-home

| Skill | Description |
|---|---|
| [`openhue`](skills/smart-home/openhue/SKILL.md) | Control Philips Hue lights, scenes, rooms via OpenHue CLI. |

### social-media

| Skill | Description |
|---|---|
| [`xurl`](skills/social-media/xurl/SKILL.md) | X/Twitter via xurl CLI: post, search, DM, media, v2 API. |

### software-development

| Skill | Description |
|---|---|
| [`adhoc-verification`](skills/software-development/adhoc-verification/SKILL.md) | Produce fresh, focused, local verification evidence for a code change without relying on the full test suite. Use when a system reminder (or the user) demands ad-hoc verificatio... |
| [`docker-compose-app-recovery`](skills/software-development/docker-compose-app-recovery/SKILL.md) | Recover or reset credentials and directly operate the database of an app running under docker-compose (lost admin password, one-time seed password, locked out, read/write app DB... |
| [`document-exports`](skills/software-development/document-exports/SKILL.md) | Generate and TEST downloadable document exports (PDF/CSV) from a Node/Express backend — pdfkit streaming, CSV BOM, cents formatting, and the supertest/pdfkit pitfalls that silen... |
| [`docx-analysis-conversion`](skills/software-development/docx-analysis-conversion/SKILL.md) | Extract, analyze, edit, and convert Microsoft Word (.docx) documents to structured Markdown, JSON, or clean text preserving tables, headers, and bullet lists. |
| [`financas-app`](skills/software-development/financas-app/SKILL.md) | Corrigir, estender e validar o app de finanças pessoais (Node/Express + EJS + MongoDB + Docker). Cobre a arquitetura de porta única 4460 com demo via /demo, o fluxo de correção... |
| [`handoff-resume`](skills/software-development/handoff-resume/SKILL.md) | Resume in-progress coding work across sessions from a HANDOFF.md and a dirty git working tree. Use when a task says "continue from HANDOFF.md", "retomar o processamento", or whe... |
| [`hermes-agent-skill-authoring`](skills/software-development/hermes-agent-skill-authoring/SKILL.md) | Author in-repo SKILL.md: frontmatter, validator, structure, and writing-quality principles. |
| [`node-inspect-debugger`](skills/software-development/node-inspect-debugger/SKILL.md) | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. |
| [`obscure-tool-install-lookup`](skills/software-development/obscure-tool-install-lookup/SKILL.md) | Use when a user asks how to install or use an obscure CLI tool, agent, or package and search engines are blocked, CAPTCHA-walled, or unhelpful. Resolves canonical install comman... |
| [`plan`](skills/software-development/plan/SKILL.md) | Plan mode: write an actionable markdown plan to .hermes/plans/, no execution. Bite-sized tasks, exact paths, complete code. |
| [`playwright-browser-automation`](skills/software-development/playwright-browser-automation/SKILL.md) | Run automated headless browser testing, scrape dynamic SPAs, capture high-resolution full-page screenshots, and perform visual regression testing with Playwright. |
| [`projeto-profissional`](skills/software-development/projeto-profissional/SKILL.md) | Bootstrap a new professional repo from Pedro's hardened Node/Express+MongoDB+EJS base template (JWT auth, admin/user roles, admin-controlled registration, security defaults, ful... |
| [`projeto-profissional-template`](skills/software-development/projeto-profissional-template/SKILL.md) | Development & operations workflow for the user's "projeto-professional" template (Node 20 + Express + MongoDB/Mongoose + EJS SSR + JWT). Captures recurring gotchas — require-cac... |
| [`python-debugpy`](skills/software-development/python-debugpy/SKILL.md) | Debug Python: pdb REPL + debugpy remote (DAP). |
| [`requesting-code-review`](skills/software-development/requesting-code-review/SKILL.md) | Pre-commit review: security scan, quality gates, auto-fix. |
| [`security-sast-audit`](skills/software-development/security-sast-audit/SKILL.md) | Perform static application security testing (SAST), secret scanning, dependency vulnerability audits (OWASP Top 10, bandit, semgrep, trivy, pip-audit, npm audit). |
| [`simplify-code`](skills/software-development/simplify-code/SKILL.md) | Parallel 3-agent cleanup of recent code changes. |
| [`spike`](skills/software-development/spike/SKILL.md) | Throwaway experiments to validate an idea before build. |
| [`systematic-debugging`](skills/software-development/systematic-debugging/SKILL.md) | 4-phase root cause debugging: understand bugs before fixing. |
| [`test-driven-development`](skills/software-development/test-driven-development/SKILL.md) | TDD: enforce RED-GREEN-REFACTOR, tests before code. |
| [`web-fullstack-gotchas`](skills/software-development/web-fullstack-gotchas/SKILL.md) | Armadilhas recorrentes em apps fullstack Node/Express + EJS + CSS + jest + Docker (padrão do projeto financas-app, mas aplicável a qualquer stack similar). USE quando esbarrar e... |
| [`xlsx-data-wrangling`](skills/software-development/xlsx-data-wrangling/SKILL.md) | Query, validate, clean, and manipulate Excel (.xlsx/.xls) spreadsheets programmatically without GUI using pandas, openpyxl, and polars. |

### web

| Skill | Description |
|---|---|
| [`animated-portfolio-sites`](skills/web/animated-portfolio-sites/SKILL.md) | Build a one-page animated personal or portfolio site (canvas starfield, rotating galaxies with mouse parallax, hidden accordion/card content, anchor nav) and publish it free on... |
| [`express-csp-runtime-config`](skills/web/express-csp-runtime-config/SKILL.md) | How to pass server-side runtime config (API prefix, feature flags, user id, CSRF token) from an Express/EJS app to client JS when a strict Content-Security-Policy is in force (h... |
| [`frontend-visual-verification`](skills/web/frontend-visual-verification/SKILL.md) | Confirm a CSS/HTML/template change actually rendered in a running browser — without being fooled by stale browser cache. Use whenever you edited frontend code (CSS, EJS/HTML, co... |
| [`github-pages-portfolio`](skills/web/github-pages-portfolio/SKILL.md) | Build, update, and verify a single-page static portfolio / intro site on GitHub Pages (pure HTML+CSS+JS, no build step). Covers sourcing content read-only from the user's existi... |
| [`markdown-site-source-pipeline`](skills/web/markdown-site-source-pipeline/SKILL.md) | Keep a static HTML/JS site's content in an editable Markdown source file; generate the data artifact (JS/JSON) the site consumes; guarantee identical render via semantic deep-eq... |
| [`markdown-static-site-source`](skills/web/markdown-static-site-source/SKILL.md) | Make a data-driven static site (content lives in a JS/JSON object consumed by a render script) editable from Markdown/Obsidian. Generate the data file from a YAML-frontmatter MD... |
| [`nextjs-app-router-patterns`](skills/web/nextjs-app-router-patterns/SKILL.md) | Architect and implement modern Next.js App Router applications with Server Components (RSC), Server Actions, Parallel/Intercepting Routes, and Streaming SSR. |
| [`quartz-multilang-site-maintenance`](skills/web/quartz-multilang-site-maintenance/SKILL.md) | Maintain and edit a Quartz static site (Quartz Syncer / quartz-site fork) that publishes to GitHub Pages — especially editing the 4-language home/index pages (pt-br/en/es/fr), c... |
| [`static-site-md-source`](skills/web/static-site-md-source/SKILL.md) | Turn an EXISTING static site (HTML/CSS/JS) into a Markdown-editable source WITHOUT changing its rendered output. Use when the user likes the current site ("muito bom, não mexa n... |

---

## 📂 Repository Structure

```
awesome-skills/
  ├── skills/<category>/<name>/   # Canonical SKILL.md + references/ + scripts/
  ├── install.sh                  # Universal interactive installer (Caveman-style)
  ├── tools/
  │   ├── installer.py            # TUI & CLI installation engine
  │   └── gen_index.py            # Regenerates README catalog index
  ├── templates/                  # Starter kits: skill / agent / plugin
  ├── packages/awesomeskills/     # Python package CLI (`awesomeskills install`)
  ├── docs/CODE_REVIEW.md         # Review standard
  └── .github/                    # Issue & PR templates + CI workflow
```

---

## 📊 RepoActivity

[![Star History Chart](https://api.star-history.com/svg?repos=pedroiff0/awesome-skills&type=Date)](https://www.star-history.com/#pedroiff0/awesome-skills&type=Date)

---

## 👨‍💻 Author

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
