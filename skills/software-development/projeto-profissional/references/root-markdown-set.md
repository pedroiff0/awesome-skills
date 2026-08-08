# Root markdown set — what goes in each file

Every Pedro repo ships this set. The value is in the split: each file answers a
different reader's question. Duplicating content across them is the main
failure mode — cross-link instead.

| File | Reader | Answers |
|------|--------|---------|
| `README.md` | anyone landing on the repo | what it is, how to run it, endpoint table, data model, adapt-for-new-project steps |
| `AGENTS.md` | coding agents | architecture rules, **what NEVER to do**, common flows, PR checklist |
| `CLAUDE.md` | Claude Code specifically | commands, decisions already made, known traps — links to AGENTS.md instead of repeating it |
| `SECURITY.md` | auditor / reporter | reporting process, full security architecture, per-release checklist |
| `CONTRIBUTING.md` | human contributor | env setup, branch/commit conventions, code standards, test expectations |
| `CODE_OF_CONDUCT.md` | community | Contributor Covenant 2.1 adaptation |
| `CHANGELOG.md` | upgrader | Keep a Changelog + SemVer; a `### Segurança` subsection for security fixes |
| `LICENSE` | legal | MIT, copyright Pedro |
| `docs/architecture.md` | new dev | layer table, middleware order, auth flow, account lifecycle, error handling |
| `docs/deployment.md` | operator | required env vars, compose, reverse proxy, systemd unit, health checks, backup, secret rotation |

## AGENTS.md vs CLAUDE.md

Do NOT duplicate. `AGENTS.md` is the normative one — architecture rules,
prohibitions, checklists. `CLAUDE.md` opens with a pointer to it and then
carries only:

- exact commands to run,
- decisions already settled ("no self-registration is the premise, not a gap";
  "no bundler on purpose"), so a future agent doesn't 'fix' them,
- the concrete traps with symptoms.

## Writing conventions

- Portuguese prose, since Pedro reads them.
- `AGENTS.md` "O que NUNCA fazer" section uses ❌ bullets with the *reason*
  attached — a prohibition without a reason gets overridden by the next agent.
- Record real bugs in the traps section with the symptom, not just the fix:
  "login responds 200 and the session still doesn't stick" is what someone
  actually greps for.
- Endpoint tables in README list method, route and required access level.
- `.env.example` documents every variable with a comment, all values empty,
  and shows the generation command for secrets
  (`openssl rand -base64 48`).
