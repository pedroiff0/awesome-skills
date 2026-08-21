---
name: grill-me-interview
description: "Conduct an interactive, rigorous architecture interview. Grills the user with probing questions one at a time to clarify ambiguous requirements, design decisions, edge cases, and tradeoffs before coding."
version: 1.0.0
author: Matt Pocock / skills.sh Community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [interview, architecture, requirements, grill-me, planning]
    related_skills: [research-paper-writing, codebase-inspection]
---

# Grill-Me Architecture & Requirements Interview

> **Attribution**: Created by Matt Pocock (skills.sh). Adapted to canonical multi-agent format.

Use this skill when a user proposes a project or feature and needs a thorough design alignment interview before writing any code.

---

## Interview Rules

1. **One Question at a Time**: Never overwhelm the user with a wall of 5+ questions. Ask one focused question, wait for the response, then dig deeper.
2. **Challenge Assumptions**: Actively look for scalability bottlenecks, security oversights, concurrency bugs, and ambiguous data models.
3. **Synthesize & Conclude**: Once all tradeoffs are clarified, produce a concise summary specification artifact for user sign-off.
