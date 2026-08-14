# awesome-skills

Coleção pessoal de **skills** (memória procedural) usadas pelo agente [Hermes](https://hermes-agent.nousresearch.com/docs).
Cada skill é um diretório com `SKILL.md` (frontmatter YAML + instruções) e,
opcionalmente, `references/`, `scripts/`, `templates/`, `assets/`.

**105 skills** em 23 categorias.

## Instalação

```bash
git clone https://github.com/pedroiff0/awesome-skills.git
cp -r awesome-skills/skills/* ~/.hermes/skills/
```

Ou apenas uma categoria/skill: copie o diretório desejado para `~/.hermes/skills/`.

## Índice

### apple

| Skill | Descrição |
|---|---|
| [`apple-notes`](skills/apple/apple-notes/SKILL.md) | Manage Apple Notes via memo CLI: create, search, edit. |
| [`apple-reminders`](skills/apple/apple-reminders/SKILL.md) | Apple Reminders via remindctl: add, list, complete. |
| [`findmy`](skills/apple/findmy/SKILL.md) | Track Apple devices/AirTags via FindMy.app on macOS. |
| [`imessage`](skills/apple/imessage/SKILL.md) | Send and receive iMessages/SMS via the imsg CLI on macOS. |

### autonomous-ai-agents

| Skill | Descrição |
|---|---|
| [`claude-code`](skills/autonomous-ai-agents/claude-code/SKILL.md) | Delegate coding to Claude Code CLI (features, PRs). |
| [`codex`](skills/autonomous-ai-agents/codex/SKILL.md) | Delegate coding to OpenAI Codex CLI (features, PRs). |
| [`hermes-agent`](skills/autonomous-ai-agents/hermes-agent/SKILL.md) | Configure, extend, or contribute to Hermes Agent. |
| [`opencode`](skills/autonomous-ai-agents/opencode/SKILL.md) | Delegate coding to OpenCode CLI (features, PR review). |

### content-i18n

| Skill | Descrição |
|---|---|
| [`libretranslate-markdown-i18n`](skills/content-i18n/libretranslate-markdown-i18n/SKILL.md) | Machine-translate Markdown / Obsidian / Quartz content into other languages using a self-hosted LibreTranslate instance, preserving frontmatter, headings, emojis, bold/italic, wikilinks (![[...]]/[[...]]) and internal... |

### creative

| Skill | Descrição |
|---|---|
| [`architecture-diagram`](skills/creative/architecture-diagram/SKILL.md) | Dark-themed SVG architecture/cloud/infra diagrams as HTML. |
| [`ascii-art`](skills/creative/ascii-art/SKILL.md) | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. |
| [`ascii-video`](skills/creative/ascii-video/SKILL.md) | ASCII video: convert video/audio to colored ASCII MP4/GIF. |
| [`baoyu-infographic`](skills/creative/baoyu-infographic/SKILL.md) | Infographics: 21 layouts x 21 styles (信息图, 可视化). |
| [`claude-design`](skills/creative/claude-design/SKILL.md) | Design one-off HTML artifacts (landing, deck, prototype). |
| [`comfyui`](skills/creative/comfyui/SKILL.md) | Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter injection. Uses the official comfy-cli for lifecycle and direct REST/WebSocket API for execution. |
| [`design-md`](skills/creative/design-md/SKILL.md) | Author/validate/export Google's DESIGN.md token spec files. |
| [`excalidraw`](skills/creative/excalidraw/SKILL.md) | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). |
| [`humanizer`](skills/creative/humanizer/SKILL.md) | Humanize text: strip AI-isms and add real voice. |
| [`manim-video`](skills/creative/manim-video/SKILL.md) | Manim CE animations: 3Blue1Brown math/algo videos. |
| [`p5js`](skills/creative/p5js/SKILL.md) | p5.js sketches: gen art, shaders, interactive, 3D. |
| [`popular-web-designs`](skills/creative/popular-web-designs/SKILL.md) | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. |
| [`portfolio-github-pages`](skills/creative/portfolio-github-pages/SKILL.md) | Build and deploy a personal/academic PORTFOLIO as a single-page STATIC site (no build step) to GitHub Pages via the gh CLI. Use when the user asks for a portfolio, landing page, "pagina de portfólio", professional sit... |
| [`pretext`](skills/creative/pretext/SKILL.md) | Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flow around obstacles, text-as-geometry games, kinetic typography, and text-powered generative art. Pro... |
| [`sketch`](skills/creative/sketch/SKILL.md) | Throwaway HTML mockups: 2-3 design variants to compare. |
| [`songwriting-and-ai-music`](skills/creative/songwriting-and-ai-music/SKILL.md) | Songwriting craft and Suno AI music prompts. |
| [`touchdesigner-mcp`](skills/creative/touchdesigner-mcp/SKILL.md) | Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-time visuals. 36 native tools. |

### data-science

| Skill | Descrição |
|---|---|
| [`jupyter-live-kernel`](skills/data-science/jupyter-live-kernel/SKILL.md) | Iterative Python via live Jupyter kernel (hamelnb). |
| [`suap-iff-api`](skills/data-science/suap-iff-api/SKILL.md) | Authenticate to and consume the SUAP IFF (Instituto Federal Fluminense) API v2 from the CLI — obtain the JWT access/refresh token via matricula+senha, then fetch student data (periodos letivos, dados do aluno, boletim... |

### desktop

| Skill | Descrição |
|---|---|
| [`desktop-theming`](skills/desktop/desktop-theming/SKILL.md) | Make a Linux desktop (XFCE/GNOME/KDE) look like macOS or otherwise "rice" it — WhiteSur GTK/icon/cursor themes, Plank dock, San-Francisco-like fonts, xfconf config. Use when a user asks for a macOS-style / Windows-sty... |

### devops

| Skill | Descrição |
|---|---|
| [`docker-single-port-multi-instance`](skills/devops/docker-single-port-multi-instance/SKILL.md) | Consolidate multiple Docker Compose app instances (production / test / demo) behind ONE host port using an nginx reverse proxy that routes by URL path prefix (e.g. /demo). Use when a user wants 'one port, several apps... |

### email

| Skill | Descrição |
|---|---|
| [`himalaya`](skills/email/himalaya/SKILL.md) | Himalaya CLI: IMAP/SMTP email from terminal. |

### geral

| Skill | Descrição |
|---|---|
| [`animated-portfolio-sites`](skills/animated-portfolio-sites/SKILL.md) | Build a one-page animated personal or portfolio site (canvas starfield, rotating galaxies with mouse parallax, hidden accordion/card content, anchor nav) and publish it free on GitHub Pages. Covers the canvas techniqu... |
| [`computer-use`](skills/computer-use/SKILL.md) | \| |
| [`dogfood`](skills/dogfood/SKILL.md) | Exploratory QA of web apps: find bugs, evidence, reports. |
| [`hermes-desktop-plugins`](skills/hermes-desktop-plugins/SKILL.md) | Write desktop app plugins that add UI panes and commands. |
| [`latex-cv-maintenance`](skills/latex-cv-maintenance/SKILL.md) | Use when reviewing, updating, or keeping consistent a multi-language LaTeX CV (altacv.cls). Covers treating Portuguese as source of truth and mirroring to other languages, cross-checking project/date/role data against... |
| [`lattes-xml-projetos`](skills/lattes-xml-projetos/SKILL.md) | Use when gerar, limpar ou inserir itens de bolsa/projetos de pesquisa (PARTICIPACAO-EM-PROJETO / PROJETO-DE-PESQUISA) em XML de importação do Currículo Lattes. Cobre a estrutura de ATUACOES-PROFISSIONAIS, a limpeza de... |
| [`markdown-site-source-pipeline`](skills/markdown-site-source-pipeline/SKILL.md) | Keep a static HTML/JS site's content in an editable Markdown source file; generate the data artifact (JS/JSON) the site consumes; guarantee identical render via semantic deep-equal verification. Use when a user wants... |
| [`markdown-static-site-source`](skills/markdown-static-site-source/SKILL.md) | Make a data-driven static site (content lives in a JS/JSON object consumed by a render script) editable from Markdown/Obsidian. Generate the data file from a YAML-frontmatter MD source and verify fidelity with SEMANTI... |
| [`mt-markup-preserving-translation`](skills/mt-markup-preserving-translation/SKILL.md) | Translate Markdown/Obsidian/Quartz content with LibreTranslate while preserving wikilinks, embeds, URLs, tables, HTML blocks, proper nouns, and canonical section titles. Use for any "translate this vault/site" task. |
| [`projeto-profissional-template`](skills/projeto-profissional-template/SKILL.md) | Development & operations workflow for the user's "projeto-professional" template (Node 20 + Express + MongoDB/Mongoose + EJS SSR + JWT). Captures recurring gotchas — require-cache restart, demo-DB reseed, Zod field-st... |
| [`quartz-multilang-site-maintenance`](skills/quartz-multilang-site-maintenance/SKILL.md) | Maintain and edit a Quartz static site (Quartz Syncer / quartz-site fork) that publishes to GitHub Pages — especially editing the 4-language home/index pages (pt-br/en/es/fr), cross-referencing sections, removing item... |
| [`static-site-md-source`](skills/static-site-md-source/SKILL.md) | Turn an EXISTING static site (HTML/CSS/JS) into a Markdown-editable source WITHOUT changing its rendered output. Use when the user likes the current site ("muito bom, não mexa no HTML") but wants to edit content in Ob... |
| [`yuanbao`](skills/yuanbao/SKILL.md) | Yuanbao (元宝) groups: @mention users, query info/members. |

### github

| Skill | Descrição |
|---|---|
| [`codebase-inspection`](skills/github/codebase-inspection/SKILL.md) | Inspect codebases w/ pygount: LOC, languages, ratios. |
| [`github-auth`](skills/github/github-auth/SKILL.md) | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. |
| [`github-code-review`](skills/github/github-code-review/SKILL.md) | Review PRs: diffs, inline comments via gh or REST. |
| [`github-issue-pr-attribs`](skills/github/github-issue-pr-attribs/SKILL.md) | Standardize GitHub ISSUE and PR metadata (Assignee, Reviewer, Labels, Project, Milestone, Development, Relationship) and ship a strong, well-structured code-review template. Includes ready-to-use issue forms, PR templ... |
| [`github-issues`](skills/github/github-issues/SKILL.md) | Create, triage, label, assign GitHub issues via gh or REST. |
| [`github-pr-workflow`](skills/github/github-pr-workflow/SKILL.md) | GitHub PR lifecycle: branch, commit, open, CI, merge. |
| [`github-profile-readme`](skills/github/github-profile-readme/SKILL.md) | Build or rewrite a GitHub profile README (the username/username special repo) with a personalized theme — animated SVG banner, stats cards, contribution snake, tech badges, project/research tables. Includes the git co... |
| [`github-repo-management`](skills/github/github-repo-management/SKILL.md) | Clone/create/fork repos; manage remotes, releases. |
| [`github-starred-kb`](skills/github/github-starred-kb/SKILL.md) | Personal GitHub knowledge base built from the user's starred repos (pedroiff0). Maps all 41 starred repositories into knowledge domains (free APIs, sysadmin/self-hosted, Python, AI/agents/RAG, algorithms, math/edu, as... |
| [`hermes-installed-catalog`](skills/github/hermes-installed-catalog/SKILL.md) | Live catalog of skills, plugins, and agents actually installed on THIS Hermes server (pedroiff0). Lists the 233 installed skills grouped by domain, the 18 installed plugins, and confirms there are no custom agent defi... |

### latex

| Skill | Descrição |
|---|---|
| [`cv-latex-multilingual`](skills/latex/cv-latex-multilingual/SKILL.md) | Manter o CV LaTeX multilíngue do usuário (classe altacv) em ~/Repositorios/pessoal/cv — PT (fonte), EN (espelho), ES/FR (gerados do EN via translate_cv.py). Abrange correções de conteúdo, build via Makefile, bugs do g... |

### media

| Skill | Descrição |
|---|---|
| [`gif-search`](skills/media/gif-search/SKILL.md) | Search/download GIFs from Tenor via curl + jq. |
| [`heartmula`](skills/media/heartmula/SKILL.md) | HeartMuLa: Suno-like song generation from lyrics + tags. |
| [`songsee`](skills/media/songsee/SKILL.md) | Audio spectrograms/features (mel, chroma, MFCC) via CLI. |
| [`youtube-content`](skills/media/youtube-content/SKILL.md) | YouTube transcripts to summaries, threads, blogs. |

### mlops

| Skill | Descrição |
|---|---|
| [`gpu-debian-setup`](skills/mlops/gpu-debian-setup/SKILL.md) | Install and verify NVIDIA proprietary GPU drivers on Debian (including trixie/13) so local LLM tools (Ollama, llama.cpp, vLLM) can use the GPU. Covers nouveau blacklist, initramfs, the trixie nvidia-smi transitional-d... |
| [`huggingface-hub`](skills/mlops/huggingface-hub/SKILL.md) | HuggingFace hf CLI: search/download/upload models, datasets. |

### mlops/evaluation

| Skill | Descrição |
|---|---|
| [`evaluating-llms-harness`](skills/mlops/evaluation/lm-evaluation-harness/SKILL.md) | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). |
| [`weights-and-biases`](skills/mlops/evaluation/weights-and-biases/SKILL.md) | W&B: log ML experiments, sweeps, model registry, dashboards. |

### mlops/inference

| Skill | Descrição |
|---|---|
| [`llama-cpp`](skills/mlops/inference/llama-cpp/SKILL.md) | llama.cpp local GGUF inference + HF Hub model discovery. |
| [`serving-llms-vllm`](skills/mlops/inference/vllm/SKILL.md) | vLLM: high-throughput LLM serving, OpenAI API, quantization. |

### mlops/models

| Skill | Descrição |
|---|---|
| [`audiocraft-audio-generation`](skills/mlops/models/audiocraft/SKILL.md) | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. |
| [`segment-anything-model`](skills/mlops/models/segment-anything/SKILL.md) | SAM: zero-shot image segmentation via points, boxes, masks. |

### note-taking

| Skill | Descrição |
|---|---|
| [`obsidian`](skills/note-taking/obsidian/SKILL.md) | Read, search, create, and edit notes in the Obsidian vault. |

### productivity

| Skill | Descrição |
|---|---|
| [`airtable`](skills/productivity/airtable/SKILL.md) | Airtable REST API via curl. Records CRUD, filters, upserts. |
| [`google-workspace`](skills/productivity/google-workspace/SKILL.md) | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. |
| [`maps`](skills/productivity/maps/SKILL.md) | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. |
| [`nano-pdf`](skills/productivity/nano-pdf/SKILL.md) | Edit PDF text/typos/titles via nano-pdf CLI (NL prompts). |
| [`notion`](skills/productivity/notion/SKILL.md) | Notion API + ntn CLI: pages, databases, markdown, Workers. |
| [`ocr-and-documents`](skills/productivity/ocr-and-documents/SKILL.md) | Extract text from PDFs/scans (pymupdf, marker-pdf). |
| [`petdex`](skills/productivity/petdex/SKILL.md) | Install and select animated petdex mascots for Hermes. |
| [`powerpoint`](skills/productivity/powerpoint/SKILL.md) | Create, read, edit .pptx decks, slides, notes, templates. |
| [`suap-api`](skills/productivity/suap-api/SKILL.md) | Consume the SUAP (Sistema Unificado de Administração Pública) REST API v2 used by Brazilian federal institutes (IFRN, IFF, IFS, etc.) — obtain a JWT via /api/v2/autenticacao/token/, discover real endpoints via /api/op... |
| [`teams-meeting-pipeline`](skills/productivity/teams-meeting-pipeline/SKILL.md) | Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs, manage Microsoft Graph subscriptions. |

### research

| Skill | Descrição |
|---|---|
| [`arxiv`](skills/research/arxiv/SKILL.md) | Search arXiv papers by keyword, author, category, or ID. |
| [`blogwatcher`](skills/research/blogwatcher/SKILL.md) | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. |
| [`llm-wiki`](skills/research/llm-wiki/SKILL.md) | Karpathy's LLM Wiki: build/query interlinked markdown KB. |
| [`polymarket`](skills/research/polymarket/SKILL.md) | Query Polymarket: markets, prices, orderbooks, history. |
| [`research-paper-writing`](skills/research/research-paper-writing/SKILL.md) | Write ML papers for NeurIPS/ICML/ICLR: design→submit. |

### smart-home

| Skill | Descrição |
|---|---|
| [`openhue`](skills/smart-home/openhue/SKILL.md) | Control Philips Hue lights, scenes, rooms via OpenHue CLI. |

### social-media

| Skill | Descrição |
|---|---|
| [`xurl`](skills/social-media/xurl/SKILL.md) | X/Twitter via xurl CLI: post, search, DM, media, v2 API. |

### software-development

| Skill | Descrição |
|---|---|
| [`adhoc-verification`](skills/software-development/adhoc-verification/SKILL.md) | Produce fresh, focused, local verification evidence for a code change without relying on the full test suite. Use when a system reminder (or the user) demands ad-hoc verification after an edit, or when you want to pro... |
| [`docker-compose-app-recovery`](skills/software-development/docker-compose-app-recovery/SKILL.md) | Recover or reset credentials and directly operate the database of an app running under docker-compose (lost admin password, one-time seed password, locked out, read/write app DB). Covers running one-off scripts inside... |
| [`document-exports`](skills/software-development/document-exports/SKILL.md) | Generate and TEST downloadable document exports (PDF/CSV) from a Node/Express backend — pdfkit streaming, CSV BOM, cents formatting, and the supertest/pdfkit pitfalls that silently break tests. |
| [`financas-app`](skills/software-development/financas-app/SKILL.md) | Corrigir, estender e validar o app de finanças pessoais (Node/Express + EJS + MongoDB + Docker). Cobre a arquitetura de porta única 4460 com demo via /demo, o fluxo de correção de UI (rebuild de AMBOS os containers +... |
| [`handoff-resume`](skills/software-development/handoff-resume/SKILL.md) | Resume in-progress coding work across sessions from a HANDOFF.md and a dirty git working tree. Use when a task says "continue from HANDOFF.md", "retomar o processamento", or when picking up a repo mid-change with unco... |
| [`hermes-agent-skill-authoring`](skills/software-development/hermes-agent-skill-authoring/SKILL.md) | Author in-repo SKILL.md: frontmatter, validator, structure, and writing-quality principles. |
| [`node-inspect-debugger`](skills/software-development/node-inspect-debugger/SKILL.md) | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. |
| [`obscure-tool-install-lookup`](skills/software-development/obscure-tool-install-lookup/SKILL.md) | Use when a user asks how to install or use an obscure CLI tool, agent, or package and search engines are blocked, CAPTCHA-walled, or unhelpful. Resolves canonical install commands via GitHub repo search, raw README fe... |
| [`plan`](skills/software-development/plan/SKILL.md) | Plan mode: write an actionable markdown plan to .hermes/plans/, no execution. Bite-sized tasks, exact paths, complete code. |
| [`projeto-profissional`](skills/software-development/projeto-profissional/SKILL.md) | Bootstrap a new professional repo from Pedro's hardened Node/Express+MongoDB+EJS base template (JWT auth, admin/user roles, admin-controlled registration, security defaults, full root markdown set), and maintain it —... |
| [`python-debugpy`](skills/software-development/python-debugpy/SKILL.md) | Debug Python: pdb REPL + debugpy remote (DAP). |
| [`requesting-code-review`](skills/software-development/requesting-code-review/SKILL.md) | Pre-commit review: security scan, quality gates, auto-fix. |
| [`simplify-code`](skills/software-development/simplify-code/SKILL.md) | Parallel 3-agent cleanup of recent code changes. |
| [`spike`](skills/software-development/spike/SKILL.md) | Throwaway experiments to validate an idea before build. |
| [`systematic-debugging`](skills/software-development/systematic-debugging/SKILL.md) | 4-phase root cause debugging: understand bugs before fixing. |
| [`test-driven-development`](skills/software-development/test-driven-development/SKILL.md) | TDD: enforce RED-GREEN-REFACTOR, tests before code. |
| [`web-fullstack-gotchas`](skills/software-development/web-fullstack-gotchas/SKILL.md) | Armadilhas recorrentes em apps fullstack Node/Express + EJS + CSS + jest + Docker (padrão do projeto financas-app, mas aplicável a qualquer stack similar). USE quando esbarrar em HTML escapado na view, testes jest fla... |

### web

| Skill | Descrição |
|---|---|
| [`express-csp-runtime-config`](skills/web/express-csp-runtime-config/SKILL.md) | How to pass server-side runtime config (API prefix, feature flags, user id, CSRF token) from an Express/EJS app to client JS when a strict Content-Security-Policy is in force (helmet default scriptSrc self, with no un... |
| [`frontend-visual-verification`](skills/web/frontend-visual-verification/SKILL.md) | Confirm a CSS/HTML/template change actually rendered in a running browser — without being fooled by stale browser cache. Use whenever you edited frontend code (CSS, EJS/HTML, components) and must verify the visual res... |
| [`github-pages-portfolio`](skills/web/github-pages-portfolio/SKILL.md) | Build, update, and verify a single-page static portfolio / intro site on GitHub Pages (pure HTML+CSS+JS, no build step). Covers sourcing content read-only from the user's existing GitHub repos (public AND private), th... |

## Contribuindo / adicionando skills

1. Crie `skills/<categoria>/<nome-da-skill>/SKILL.md` com frontmatter:

```yaml
---
name: minha-skill
description: "Uma linha, imperativa, dizendo quando usar."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
```

2. Rode `python3 tools/gen_index.py` para regenerar este README.
3. Commit e push.

> README gerado automaticamente — não edite à mão acima da seção Contribuindo.
