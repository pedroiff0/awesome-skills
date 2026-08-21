# Changelog

All notable changes to this project are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [2.1.0] - 2026-08-21

### Added
- **Awesome Skills Master Skill** (`skills/autonomous-ai-agents/awesome-skills-master/SKILL.md`): Autonomous procedural manual for AI agents to auto-detect environments, adapt rules (`.cursor/rules/*.mdc`, `CLAUDE.md`), link skills, configure MCP servers, and preserve author attribution without user prompts.
- **Model Context Protocol (MCP) Server Catalog** (`mcp/`): Ready-to-configure MCP servers (`context-mode`, `sqlite-explorer`, `puppeteer-browser`, `filesystem-pro`).
- **Agent Plugins Catalog** (`plugins/`): Reusable agent hooks & lifecycle plugins (`auto-git-checkpoint`, `token-guardian`).
- **Skills.sh & Community Ingestions**: `frontend-design-systems` (Anthropic), `grill-me-interview` & `grill-with-docs` (Matt Pocock), `skills-sh-registry` (Vercel Labs), `watermarks-remover` (Guillaume Meyer).
- **Comprehensive Author Attribution Matrix** honoring all original authors and upstream ecosystems.

### Changed
- Total catalog expanded to **124 skills**, **2 plugins**, and **4 MCP servers** across 19 categories.
- Updated `tools/gen_index.py` and `README.md` with MCP and Plugin badges and catalog sections.

## [2.0.0] - 2026-08-21

### Added
- **Universal Multi-Agent Interactive Installer** (`install.sh` + `tools/installer.py` + `awesomeskills install`) inspired by Caveman/modern CLI package managers.
- **Dedicated Agent 1-Liners** in README for Google Antigravity (AGY), Hermes Agent, Claude Code, Cursor IDE, Windsurf, and Roo Code / Cline.
- **10 New High-Value Skills** from major AI agent ecosystems.
- **Multi-Agent Documentation Guide** (`docs/MULTI_AGENT_INSTALLER_GUIDE.md`).
- **Curated Skill Packs**: Full-Stack Dev, DevOps & Cloud, Autonomous AI & MLOps, Academic & LaTeX, Creative & Design, and All Catalog.

### Changed
- **Reorganized & Standardized Catalog Hierarchy**: Reorganized 13 orphaned skills to canonical 2-level directory structure (`skills/<category>/<name>/SKILL.md`) across 19 standard categories.
- Updated `tools/gen_index.py` to support multi-agent badges, per-agent installation tables, and dynamic category indexing.

## [1.1.0] - 2026-08-16

### Added
- **RepoActivity** section with Star History chart + Author (GIF + badges) in README.
- **Sponsor** button (`.github/FUNDING.yml` with GitHub Sponsors).
- **Wiki** content (`docs/Wiki-Home.md`).
- **Discussions** with labels: announcement, idea, qa, showcase, general.
- **Issue templates** (bug, feature, task) with 7 standard assignments.
- **PR template** with self-review checklist.
- **Project V2**: "Awesome Skills — Roadmap" created.

### Changed
- README footer translated to English ("Made with ☕, code and ☄️").
- Star History URL corrected.

## [1.0.0] - 2026-08-14

### Added
- Initial public release: **105 skills** across **23 categories**.
- Multi-tool compatible (`SKILL.md` canonical; `CLAUDE.md` / `manifest.json` adaptors for Hermes, Claude, Cursor, Windsurf, OpenClaw, Roo, Cline, AGY).

[2.1.0]: https://github.com/pedroiff0/awesome-skills/releases/tag/v2.1.0
[2.0.0]: https://github.com/pedroiff0/awesome-skills/releases/tag/v2.0.0
[1.1.0]: https://github.com/pedroiff0/awesome-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/pedroiff0/awesome-skills/releases/tag/v1.0.0
