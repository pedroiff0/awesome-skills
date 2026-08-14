# Agent Definition Template (multi-tool)

Use this to define a **reusable agent** (a focused worker with a system prompt,
allowed tools, and constraints) that multiple agent runtimes can load.

## Canonical shape

```
my-agent/
  AGENT.md           # system prompt + role + constraints (canonical)
  SKILL.md           # optional: skills the agent auto-loads
  manifest.json      # metadata for loaders that need JSON (AGY, etc.)
  README.md          # install per tool
```

## AGENT.md (canonical)

```markdown
# Role
You are <name>, a <specialty> agent.

# Objective
<one sentence: what you deliver>

# Operating rules
- <rule 1: never do X>
- <rule 2: always verify Y before Z>
- <rule 3: escalate to human on ambiguity>

# Tools (allow-list)
- read, write, bash, web, <…>

# Workflow
1. <step>
2. <step>
3. produce <artifact> and stop.

# Output format
<exact shape of the result you return>
```

## manifest.json

```json
{
  "name": "my-agent",
  "version": "0.1.0",
  "type": "agent",
  "entry": "AGENT.md",
  "compat": ["hermes", "claude", "cursor", "openclaw", "agy"],
  "tools": ["read", "write", "bash", "web"],
  "escalate_on": ["ambiguity", "missing credentials"]
}
```

## Install per tool
- **Hermes**: reference via `delegate_task` role or drop `AGENT.md` in an agent dir.
- **Claude Code**: `CLAUDE.md` at repo root or `.claude/agents/my-agent.md`.
- **Cursor/Windsurf**: include `AGENT.md` in rules.
- **AGY / OpenClaw**: point loader at `manifest.json`.
