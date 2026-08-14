# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| `main` | ✅ |
| latest semver tag | ✅ |
| older tags | ❌ |

## Reporting a vulnerability

**Do not open a public issue for security vulnerabilities.**

Report privately via one of:
- GitHub Security Advisories (repo → Security → Advisories → "Report a vulnerability")
- Email the maintainer (see profile) with subject `[awesome-skills SECURITY]`

Include:
- Affected skill/agent/plugin or file path
- Steps to reproduce
- Impact and suggested mitigation

We aim to acknowledge within **72 hours** and provide a fix plan within
**14 days** for confirmed issues.

## Scope

In scope:
- Malicious or unsafe instructions in a skill that could exfiltrate data,
  run destructive commands, or bypass safety.
- Supply-chain risk in `scripts/` (unpinned fetches, obfuscated code).
- Leaked secrets committed to the repo.

Out of scope:
- General how-to questions (use Discussions / issues).
- Bugs that are not security-relevant (open a normal issue).

## Our commitments

- No secrets are stored in the repo; all examples use placeholders.
- Skills that call external tools must fail closed (non-zero exit) on error.
- We review every PR for secrets and unsafe instructions before merge.
