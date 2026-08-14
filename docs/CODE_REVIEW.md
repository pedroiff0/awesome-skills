# Code Review — Standard (awesome-skills)

This is the review model we apply to **every PR** in awesome-skills. Copy the
comment template into your PR review. Coherent reviews scale the catalog.

## Principles

1. Review the **instruction**, not the author.
2. **Multi-tool compatibility first** — a skill must work in Hermes *and* be
   trivially adaptable to Claude/Cursor/Windsurf/OpenClaw/AGY via thin adaptors.
3. **No secrets** — tokens, keys, passwords never in body or scripts.
4. **API purity** — anything touching `*API*` stays **pure**: no leaked
   credentials, no proprietary/closed-source code; public specs + fictional
   examples only.
5. **Verifiable** — every change ships with a check or clearly states the blocker.
6. **KISS/DRY** — concise, concrete, no duplicated logic across tools.

## Comment template (copy into the PR)

```markdown
## Code Review — PR #<N>

**Reviewer:** @<login> · **Date:** YYYY-MM-DD · **Decision:** ✅ Approved / 🔁 Changes requested / ⛔ Blocked

### Summary
<1–3 lines: what the PR does and whether it meets the issue #<N>.>

### Automated checks
| Check | Status |
|---|---|
| `python3 tools/gen_index.py` | ✅ / ❌ |
| `SKILL.md` / `manifest.json` lint | ✅ / ❌ |
| No secrets committed | ✅ / ❌ |

### Findings by severity
| # | Severity | File:line | Category | Comment |
|---|---|---|---|---|
| 1 | 🔴 Blocker | … | Security | … |
| 2 | 🟠 Major | … | Multi-tool | … |
| 3 | 🟡 Minor | … | Style | … |
| 4 | 🔵 Nit | … | Convention | … |

### Required items
- [ ] Follows `templates/` (single canonical `SKILL.md` + adaptors)
- [ ] `version` bumped; `metadata.hermes.tags` present
- [ ] No secrets; scripts idempotent
- [ ] API-pure: no leaked credentials, no proprietary code in `*API*` content
- [ ] `gen_index.py` regenerates README without error
- [ ] Docs updated (CONTRIBUTING / README if behavior changed)

### Decision & next steps
<If 🔁/⛔: list must-fix items before re-review.>
```

## Severity table

| Icon | Severity | Action |
|---|---|---|
| 🔴 Blocker | Secret leak, unsafe instruction, broken schema, non-idempotent destructive script | PR cannot merge |
| 🟠 Major | Not multi-tool compatible, missing verification, missing required metadata | Fix this PR or file follow-up |
| 🟡 Minor | Inconsistent style, weak example, missing trigger | Fix if quick |
| 🔵 Nit | Cosmetic preference | Optional |

**Decision rule:** any 🔴 → ⛔; only 🟠/🟡/🔵 → 🔁; nits-only → ✅.

## Rubrics

- **Multi-tool:** canonical `SKILL.md`; `CLAUDE.md`/`manifest.json` only adapt.
- **Security:** no secrets, fail-closed scripts, no unpinned remote fetches,
  and **API-pure** content (`*API*` specs/clients must not leak credentials or
  embed proprietary code).
- **Metadata:** `name`, `description`, `version`, `author`, `license`,
  `platforms`, `metadata.hermes.tags` all present and accurate.
- **Verification:** a runnable check or an explicit blocker statement.
- **Docs:** README/INDEX stay consistent with `gen_index.py`.
