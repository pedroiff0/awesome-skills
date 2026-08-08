---
name: handoff-resume
description: Resume in-progress coding work across sessions from a HANDOFF.md and a dirty git working tree. Use when a task says "continue from HANDOFF.md", "retomar o processamento", or when picking up a repo mid-change with uncommitted edits and an open PR. Covers reading continuity docs, reconciling the real tree, decoding repo jargon, verifying rendered UI without a trusted screenshot, and committing to the existing branch to update the PR.
---

# Handoff Resume

Resume multi-session coding work without losing context. The repo carries a
HANDOFF.md (continuity doc) and/or a dirty working tree with in-progress edits
on a branch that tracks an open PR.

## When to use
- User says "retomar de HANDOFF.md", "continue from <file>", "voltar ao trabalho em <repo>".
- `git status` shows modified/untracked files and a branch tracking a remote PR.
- You need to know what's done vs in-progress vs pending before touching anything.

## Steps
1. **Read HANDOFF.md (or the named file) fully.** It records branch, last
   commit, PR number, committed vs uncommitted files, decisions/why, and
   pending tasks. This is the map, not the ground truth.
2. **Reconcile with reality.** Run `git status` + `git diff --stat` (and
   `git diff` on suspect files). HANDOFF can be stale — the tree is the truth.
   A "clean" HANDOFF often hides many already-modified files.
3. **Read the repo's rule files**: AGENTS.md, CLAUDE.md, DESIGN.md. These carry
   architectural rules and design-system gates you must not violate.
4. **Find the gap.** What the user now wants vs what's already in the tree.
   Disambiguate repo jargon from the code, not from the word alone — e.g. a
   "módulo de velocidade" in a finance app with only Finanças/Investimentos/
   Veículos means the **Veículos** module (km, odômetro). Read the code to
   confirm before acting.
5. **Make the change.** Reuse existing helpers/patterns instead of inventing:
   if the frontend already has SVG chart helpers (`barrasAgrupadas`, `rosca`,
   `legenda`), call them for the new graph rather than pulling in a chart lib.
6. **Verify** (see Verification path below). Keep any design-system lint at
   0 errors.
7. **Update HANDOFF.md** with the new state, then commit on the EXISTING branch
   and push (updates the open PR automatically). Do NOT open a new branch or a
   new PR unless explicitly told.

## Verification path (when you can't trust a visual screenshot)
This environment's `browser_vision` often returns a **blank viewport** for
server-rendered pages, while the accessibility tree is reliable. Don't block
on the blank screenshot — verify with:
- `browser_snapshot` (full) — confirms rendered elements, heading levels, and
  `<image>` roles carrying native `<title>` tooltips (proof the SVG chart drew).
- `browser_console` — must show 0 JS errors after navigation.
- **Live server check**: for Dockerized apps, rebuild and hit the real endpoint
  with curl, grepping for the new element ids / markup:
  `docker compose -p fa build app app-demo && docker compose -p fa up -d app app-demo`
  (optionally reseed: `docker compose -p fa exec -T app-demo node scripts/seed-demo.js`)
  then `curl -s -b cookies <url> | grep 'id="chart-..."'`.
- Treat `browser_vision` as a bonus only. A blank return is a tooling quirk,
  not evidence the page is broken.

## Pitfalls
- **HANDOFF staleness**: always cross-check with `git diff`. The doc may claim
  a clean tree while 11 files are modified.
- **Scope creep on commit**: a dirty tree holds half-finished, unrelated edits.
  `git add -A` sweeps them into the push and pollutes the PR. Add specific
  files, or confirm with the user before lumping in-progress work.
- **Design-system gate**: repos with DESIGN.md gate on
  `npx -y @google/design.md lint DESIGN.md` (0 errors). Custom components that
  aren't valid schema sub-tokens produce warnings — keep them as YAML comments,
  not `components:` entries, to stay at 0 warnings.
- **Pedro (pedroiff0) design approval**: he approves UI changes ONLY after
  seeing the rendered result. Get visual sign-off (screenshot) before
  commit/merge; never impose a heavy theme he didn't ask for.

## References
- `references/worked-example-financas.md` — concrete financas-app resumption:
  branch/PR, the "velocidade→Veículos" decoding, Docker rebuild + demo reseed,
  browser verification, and the design.md lint/comment trick.
