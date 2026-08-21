---
name: antigravity-guide
description: "Provides a comprehensive guide, architecture reference, and quick-access sitemap for Google Antigravity (AGY), including CLI, Antigravity 2.0, IDE extensions, Python SDK, slash commands, keybindings, and customization hooks."
version: 1.0.0
author: Pedro Henrique Rocha de Andrade
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [antigravity, agy, autonomous-agents, developer-tools, ide]
    related_skills: [agy-customizations, context-mode, hermes-agent]
---

# Antigravity (AGY) Guide & Architecture Reference

> **Purity rules**: Pure open documentation; no API keys, internal tokens, or closed endpoints.

This skill provides an authoritative operational reference for working with the **Google Antigravity (AGY)** ecosystem, covering the CLI, modern agent capabilities, slash command workflows, sidecars, and IDE features.

## When to Use

- Configuring or diagnosing Antigravity CLI (`agy`) or Antigravity IDE workspaces.
- Authoring custom slash commands, agent modes, or persistent background tasks.
- Integrating MCP (Model Context Protocol) servers and subagent topologies.
- Troubleshooting terminal persistence, persistent runtimes, or task managers.

## Key Architecture & Core Commands

```bash
# Start an interactive pair-programming session
agy

# Run directly against a specific repository or task
agy --dir /path/to/project --goal "Implement feature X with full test coverage"

# List and manage active background tasks and sidecars
agy task list
agy mcp list
```

## Standard Workspace Hierarchy

```
<project_root>/
  ├── .agent/
  │   ├── skills/              # Workspace-scoped skills (SKILL.md)
  │   ├── rules/               # Contextual agent rules (*.md)
  │   └── mcp/                 # Local MCP configuration
  └── AGENTS.md                # Agent instructions & hard rules
```

## Built-in Slash Command System

| Command | Purpose |
| :--- | :--- |
| `/goal` | Autonomous long-running execution mode; continues until goal is verified. |
| `/plan` | Generates a structured multi-step execution plan artifact before coding. |
| `/grill-me` | Interactive design alignment and architecture interview. |
| `/schedule` | Configures cron schedules or one-shot notification timers. |
| `/learn` | Persists user preferences and codebase corrections across conversations. |
