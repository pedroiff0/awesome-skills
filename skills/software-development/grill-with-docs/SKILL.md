---
name: grill-with-docs
description: "Cross-examine codebase architecture against official library documentation and API specs. Identifies deprecations, anti-patterns, and suboptimal library usage."
version: 1.0.0
author: Matt Pocock / skills.sh Community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [code-review, docs, best-practices, grill-me, refactoring]
    related_skills: [grill-me-interview, codebase-inspection]
---

# Grill With Documentation & Official Specs

> **Attribution**: Created by Matt Pocock (skills.sh). Adapted to canonical multi-agent format.

Verifies code implementations against the authoritative documentation of underlying libraries and frameworks.

---

## Operational Steps

1. Inspect imported third-party packages in `package.json`, `pyproject.toml`, or `Cargo.toml`.
2. Compare code usage against current official API specifications (e.g. Next.js 15 breaking changes, Pydantic v2 migrations).
3. Point out deprecated methods, sub-optimal query patterns, or missing error boundaries.
