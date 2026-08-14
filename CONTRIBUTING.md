# Contributing to awesome-skills

Thanks for helping build a high-quality, multi-tool skill library. This document
sets the bar for contributions and the standard workflow we use on every issue
and pull request.

## Code of conduct

By participating you agree to our [Code of Conduct](CODE_OF_CONDUCT.md) and
[Security policy](SECURITY.md).

## Repository standard (this is a public, community-maintained repo)

Every issue and PR follows the **seven standard assignment fields**:

| Field | Issue | PR |
|---|---|---|
| **Assignee** | ✅ | ✅ |
| **Reviewer** | set on the fix PR | ✅ |
| **Labels** | ✅ | ✅ (inherit + type) |
| **Project** | ✅ (Awesome Skills — Roadmap) | ✅ |
| **Milestone** | ✅ (Backlog or release tag) | ✅ (same as issue) |
| **Development** | n/a | ✅ (branch↔issue link) |
| **Relationship** | parent/child links | `Closes #N` / `Relates #N` |

Templates live in `.github/ISSUE_TEMPLATE/` (bug / feature / task) and
`.github/PULL_REQUEST_TEMPLATE.md`. Use them — they pre-fill assignments.

## Workflow

1. Open or pick an issue. Self-assign; set Labels / Project / Milestone.
2. Branch from `main`: `feat/...`, `fix/...`, `docs/...`, `chore/...`.
3. Build the skill/agent/plugin using `templates/` (multi-tool compatible:
   Hermes, Claude, Cursor, Windsurf, OpenClaw, Roo, Cline, AGY, …).
4. Verify locally (see below). No verification → no merge.
5. Open a PR with all assignments filled; post a review per `docs/CODE_REVIEW.md`.
6. Merge `--rebase` on approval; delete the branch.

## Skill / Agent / Plugin standards

- **One canonical `SKILL.md`** (Hermes format) + thin adaptors (`CLAUDE.md`,
  `manifest.json`) — never duplicate logic across tools.
- **Frontmatter** with `name`, `description`, `version`, `author`, `license`,
  `platforms`, `metadata.hermes.tags`.
- **No secrets** — tokens go in env / secret store, never in the body.
- **Idempotent** scripts; include a verification snippet.
- **Explicit triggers** so the agent knows when to load it.
- **KISS/DRY** — concise instructions, concrete examples, no noise.

## Verification (run before opening a PR)

```bash
# regenerate the index
python3 tools/gen_index.py

# lint a SKILL.md frontmatter
python3 -c "import yaml; yaml.safe_load(open('skills/<cat>/<name>/SKILL.md').read().split('---')[1]); print('SKILL_OK')"

# validate a manifest.json
python3 -c "import json; json.load(open('templates/.../manifest.json')); print('MANIFEST_OK')"
```

## Review model

Follow [`docs/CODE_REVIEW.md`](docs/CODE_REVIEW.md): fixed comment structure,
severity table (🔴 Blocker / 🟠 Maior / 🟡 Menor / 🔵 Nit), and per-category
rubrics (security, multi-tool compat, docs, verification).

## Releases

- Catalog changes are continuous; tag semver (`vMAJOR.MINOR.PATCH`) on curated
  milestones. `Backlog` is the catch-all for unscheduled work.
- Keep `README.md` accurate (run `gen_index.py` — it regenerates from `SKILL.md`).
