---
name: github-issue-pr-attribs
description: "Standardize GitHub ISSUE and PR metadata (Assignee, Reviewer, Labels, Project, Milestone, Development, Relationship) and ship a strong, well-structured code-review template. Includes ready-to-use issue forms, PR template, and a severity/rubric review model."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Issues, Pull-Requests, Templates, Code-Review, Workflow, Metadata, Labels, Milestones, Projects]
    related_skills: [github-pr-workflow, github-code-review, github-issues]
---

# Standardize GitHub Issue/PR Metadata + Strong Code Review

Turn ad-hoc issues/PRs into a coherent, repeatable workflow. This skill covers
the **seven standard assignment fields** for both issues and PRs, ships
copy-paste **issue forms** and a **PR template**, and provides a **strong,
organized code-review model** (fixed comment structure, severity table,
per-category rubrics).

Use it when a repo has no templates, reviews are inconsistent, or the user asks
to "padronizar issue/PR", "atribuições em issue e PR", "melhorar o code review",
or "criar template de issue/PR".

## When to Use

- Repo lacks `.github/ISSUE_TEMPLATE/*.yml` or `PULL_REQUEST_TEMPLATE.md`.
- Issues/PRs opened with missing assignee, labels, project, or milestone.
- Code review is unstructured / freeform and hard to scan.
- User wants a reusable standard other agents can apply.

## The Seven Standard Assignment Fields

Apply all seven to every issue and PR. API limits noted below.

| Field | Issue | PR |
|---|---|---|
| **Assignee** | ✅ (who owns it) | ✅ |
| **Reviewer** | n/a on issue (set on PR) | ✅ |
| **Labels** | ✅ | ✅ (inherit issue + type) |
| **Project** | ✅ (Projects V2) | ✅ |
| **Milestone** | ✅ (Backlog or semver) | ✅ (same as issue) |
| **Development** | n/a on issue | ✅ (branch↔issue link) |
| **Relationship** | parent/child links | `Fecha #` / `Relaciona #` |

### API reality check (gh / REST)
- `gh issue create` sets: `--assignee`, `--label`, `--milestone`, `--project`, `--body`, `--title`. **No reviewer on issues.**
- `gh pr create` sets: `--assignee`, `--label`, `--milestone`, `--project`, `--head`, `--base`, `--title`, `--body`, `--reviewer` (or `gh pr edit --add-reviewer`).
- **Projects V2** are NOT settable via REST `gh issue/pr create --project` reliably when the project is V2 (REST targets legacy Projects v1 and 404s). Use the GraphQL mutation `addProjectV2ItemById` to attach a V2 project item after creation. See `references/projects-v2.md`.
- **Self-review request**: a single-owner private repo can't formally request review from the same account; document the reviewer in the PR template/body instead.
- **Development link**: opening a PR from a branch whose name references the issue (or `Fecha #N` in body) auto-links; the GitHub UI shows it under "Development" on the issue.

## Workflow (apply to a real repo)

1. **Branch** from `main`: `feat/workflow-standard`.
2. **Create issue forms** in `.github/ISSUE_TEMPLATE/` — copy `templates/bug.yml`, `templates/feature.yml`, `templates/task.yml`. Each pre-sets `assignees: [pedroiff0]` (change to the real default owner) and documents the standard fields in a `markdown` block.
3. **Create PR template** `.github/PULL_REQUEST_TEMPLATE.md` — copy `templates/PULL_REQUEST_TEMPLATE.md`. It has the 7-field assignment checklist + self-review.
4. **Create the review model** `docs/CODE_REVIEW.md` — copy `references/code-review-model.md`.
5. **Update CONTRIBUTING.md** with an "Atribuições padronizadas" section (see `references/contributing-section.md`).
6. **(Optional) Milestone**: create a `Backlog` catch-all if none exists:
   `gh api repos/<owner>/<repo>/milestones -f title=Backlog -f state=open -f description="..."`
7. **Commit only the new files** (preserve any existing working tree):
   `git add .github/... docs/CODE_REVIEW.md CONTRIBUTING.md && git commit -m "docs(workflow): ..."`
8. **Open PR** with all assignments, post a review comment using the model, merge `--rebase`, delete branches.

## Strong Code-Review Model (summary)

Full version in `references/code-review-model.md`. Key pieces:

- **Fixed comment structure**: Resumo · Verificação automática (table) · Achados por severidade (table) · Itens obrigatórios (checklist) · Decisão.
- **Severity table**: 🔴 Blocker (no merge) · 🟠 Maior (must fix this PR or follow-up) · 🟡 Menor (style/naming) · 🔵 Nit (optional).
- **Decision rule**: any 🔴 → ⛔ Blocked; only 🟠/🟡/🔵 → 🔁 Changes requested; nits-only → ✅ Approved.
- **Rubrics by category**: Security (top priority), Architecture (layers), Data (cents/derived), Tests, UI/UX.

## Conventions

- **Milestone/Release**: releases are semver tags; milestone = target tag. `Backlog` = catch-all for unscheduled work. Don't open a milestone per issue.
- **Project**: point V2 project at the repo's roadmap board.
- **Labels**: at least one category (`bug`/`enhancement`/`documentation`/`testes`/`ux`/`seguranca`/`infra`/`backlog`) + module (`modulo:financas` etc.) when applicable.

## Verification

After writing the YAML forms, validate structure (not just parse) before committing:

```bash
python3 - <<'PY'
import glob, yaml, sys
VALID={"markdown","textarea","input","dropdown","checkboxes","radio","code","yaml_metadata"}
errs=[]
for f in sorted(glob.glob(".github/ISSUE_TEMPLATE/*.yml")):
    d=yaml.safe_load(open(f))
    for k in ("name","description","body","assignees","labels"):
        if k not in d: errs.append(f"{f}: falta {k}")
    for i,b in enumerate(d.get("body",[])):
        t=b.get("type")
        if t not in VALID: errs.append(f"{f}[{i}] type {t!r} invalido")
        a=b.get("attributes",{})
        if t in ("textarea","input","dropdown","radio","checkboxes") and "label" not in a:
            errs.append(f"{f}[{i}] {t} sem label")
sys.exit(1 if errs else 0) if errs else print("SCHEMA_OK")
PY
```

Also confirm assignments landed via API after opening, e.g.:
`gh pr view <N> --json assignees,labels,milestone,reviewRequests,projectCards`
(Note: `projectCards` is null on REST for V2 — verify V2 membership via GraphQL, see `references/projects-v2.md`.)

## Pitfalls

- Don't rely on `gh ... --project` for **Projects V2** (REST 404s) — use the GraphQL mutation.
- Single-owner private repo: can't self-request review; put reviewer in template/body.
- Issue forms support labels/assignees via YAML, but NOT milestone/project reviewer — set those at create time or post-hoc.
- Preserve any pre-existing working tree; commit only the new workflow files.
