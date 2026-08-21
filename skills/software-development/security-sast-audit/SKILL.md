---
name: security-sast-audit
description: "Perform static application security testing (SAST), secret scanning, dependency vulnerability audits (OWASP Top 10, bandit, semgrep, trivy, pip-audit, npm audit)."
version: 1.0.0
author: Pedro Henrique Rocha de Andrade
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, sast, secret-scan, owasp, audit, cve]
    related_skills: [codebase-inspection, devops]
---

# Static Application Security Testing (SAST) & Auditing

Audit codebases for exposed secrets, outdated dependencies with known CVEs, and insecure code patterns.

## When to Use

- Pre-commit security verification or PR review security audits.
- Scanning for hardcoded API keys, JWT tokens, and private certificates.
- Checking npm or pip dependency lockfiles against advisory databases.
