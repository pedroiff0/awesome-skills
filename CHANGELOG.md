# Changelog

All notable changes to this project are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- `CODEOWNERS` documenting ownership per area.
- `.editorconfig` for consistent formatting.
- `awesomeskills` package (`packages/awesomeskills`): CLI with `index` and
  `catalog` commands, installable via `pip install ./packages/awesomeskills`.
- Standard issue/PR governance (`.github/ISSUE_TEMPLATE`, `PULL_REQUEST_TEMPLATE`).
- `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`.
- `docs/CODE_REVIEW.md` review standard.
- Discussions, Wiki (tab), Projects (V2), GitHub Pages enabled.
- Security: secret scanning, push protection, Dependabot enabled.
- `templates/` starter kits (skill / agent / plugin) for multi-tool use.

### Changed
- README rewritten as an enterprise-grade, multi-tool catalog landing page.
- Branch protection on `main`: direct pushes blocked (PR required).

## [1.0.0] - 2026-08-14

### Added
- Initial public release: **105 skills** across **23 categories**.
- Multi-tool compatible (`SKILL.md` canonical; `CLAUDE.md` / `manifest.json`
  adaptors for Hermes, Claude, Cursor, Windsurf, OpenClaw, Roo, Cline, AGY).
- `tools/gen_index.py` to regenerate the README index.
- 14 repository topics + professional description.

[Unreleased]: https://github.com/pedroiff0/awesome-skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/pedroiff0/awesome-skills/releases/tag/v1.0.0
