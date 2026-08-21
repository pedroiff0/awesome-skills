---
name: agy-customizations
description: "Comprehensive guide and reference for the Antigravity Customization System. Use to author skills, contextual rules, plugins, hooks, and MCP servers with correct priority loading."
version: 1.0.0
author: Pedro Henrique Rocha de Andrade
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [antigravity, customizations, plugins, mcp, rules, skills]
    related_skills: [antigravity-guide, context-mode]
---

# Antigravity Customization System

This skill explains how customizations work within Antigravity (AGY), their discovery mechanisms, loading priorities, and best practices for creating skills, rules, plugins, and MCP servers.

## When to Use

- Writing new custom skills for Antigravity workspaces.
- Adding repository rules (`.agent/rules/*.md` or `AGENTS.md`).
- Configuring Model Context Protocol (MCP) servers (`~/.gemini/antigravity-cli/mcp/`).
- Building lifecycle hooks and terminal integration extensions.

## Discovery & Loading Priority

Customizations are discovered and merged in the following order of precedence (highest to lowest):

1. **Workspace Local**: `<workspace_root>/.agent/skills/`
2. **Global User**: `~/.gemini/antigravity-cli/skills/`
3. **Built-in System**: `antigravity-cli/builtin/skills/`

## Authoring Canonical SKILL.md

Every skill must have a root `SKILL.md` with standard YAML frontmatter with `name` and `description`.
