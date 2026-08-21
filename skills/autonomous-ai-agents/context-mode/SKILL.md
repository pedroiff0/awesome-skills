---
name: context-mode
description: "Context optimization and compression routing rules for AI agents exploring large codebases, reading massive logs, searching symbols, and batching tool executions."
version: 1.0.0
author: Context-Mode Team
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [context-compression, token-optimization, code-search, mcp, context-mode]
    related_skills: [antigravity-guide, codebase-inspection]
---

# Context Mode & Token Optimization

This skill provides operational patterns for navigating massive repositories while conserving context tokens using indexed searches, AST filters, and structured outputs.

## When to Use

- Reading large log files (>500 lines) or analyzing multi-megabyte code repositories.
- Performing symbol lookups across hundreds of files without flooding context.
- Running high-volume batch executions or lint sweeps.

## Operational Guidelines

1. **Targeted Line Range Views**: Avoid dumping entire files; view slices using line offsets (`view_file` with `StartLine` and `EndLine`).
2. **Grep Before View**: Use ripgrep (`grep_search`) to locate exact function definitions or usages before loading the containing file.
3. **Subagent Offloading**: For deep exploratory research, invoke an isolated research subagent (`invoke_subagent`) to read docs and summarize findings back to parent context.
