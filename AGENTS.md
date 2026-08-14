# AGENTS.md — awesome-skills

Guidance for AI agents (Hermes, Claude, Cursor, Windsurf, OpenClaw, AGY, …) that
work in this repository. Read this before editing.

## Purpose

awesome-skills is a **public, community-maintained catalog** of reusable
Skills, Agents, and Plugins for AI agents. Every entry is procedural memory
that must work across multiple runtimes from a single canonical `SKILL.md`.

## Hard rules

1. **One canonical `SKILL.md`** per skill (Hermes format). Adaptors
   (`CLAUDE.md`, `manifest.json`) must only *reference or translate* — never
   duplicate logic.
2. **No secrets** — tokens, keys, passwords never in body or scripts. Use env /
   secret store. Fail closed (non-zero exit) on error.
3. **API purity** — anything touching `*API*` (specs, wrappers, clients) must be
   **pure**: no leaked credentials (keys/tokens/secrets) and no proprietary or
   closed-source code. Use only public specs, fictional examples, and stubs.
   Never embed a real token, signed request, or internal endpoint.
4. **Multi-tool compatible** — if it only works in one runtime, it does not
   belong here.
5. **Idempotent scripts** — safe to run more than once.
6. **Verifiable** — ship a check, or state the blocker explicitly.
7. **KISS/DRY** — concise instructions, concrete examples, no noise.

## Structure

```
skills/<category>/<name>/   # SKILL.md + references/ + scripts/ + templates/
templates/                  # starter kits: skill / agent / plugin
docs/CODE_REVIEW.md         # review standard
tools/gen_index.py          # regenerates README.md from SKILL.md
.github/                    # ISSUE_TEMPLATE + PULL_REQUEST_TEMPLATE
```

## Workflow (every change)

1. Branch from `main`: `feat/...`, `fix/...`, `docs/...`, `chore/...`.
2. Follow `templates/` for new skills/agents/plugins.
3. **Never hand-edit the README above the Index/Contributing sections** —
   run `python3 tools/gen_index.py` instead.
4. Verify locally (below). No verification → no merge.
5. Open a PR with the **seven standard assignment fields** (see
   `CONTRIBUTING.md`): Assignee, Reviewer, Labels, Project, Milestone,
   Development, Relationship.
6. Review per `docs/CODE_REVIEW.md` (severity table + rubrics).
7. Merge `--rebase`; delete the branch.

## Verification (run before committing)

```bash
python3 tools/gen_index.py
python3 -c "import yaml; yaml.safe_load(open('skills/<cat>/<name>/SKILL.md').read().split('---')[1]); print('SKILL_OK')"
python3 -c "import json; json.load(open('templates/.../manifest.json')); print('MANIFEST_OK')"
```

The CI workflow (`.github/workflows/ci.yml`) runs the same checks on every PR.

## Conventions

- Frontmatter: `name`, `description`, `version`, `author`, `license`,
  `platforms`, `metadata.hermes.tags` — all present.
- `description` is imperative and states when to use the skill.
- Tags drive discoverability; pick 3–6 accurate ones.
- Releases are semver tags (`vMAJOR.MINOR.PATCH`); `Backlog` is the default
  milestone for unscheduled work.
