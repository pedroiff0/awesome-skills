# How to publish `my-skill` across tools

## Hermes Agent
```bash
cp -r . ~/.hermes/skills/<category>/my-skill
```

## Claude Code / Claude.ai
```bash
mkdir -p .claude/skills/my-skill
cp SKILL.md .claude/skills/my-skill/
# optional project memory:
cp SKILL.md CLAUDE.md
```

## Cursor
Add to `.cursor/rules/my-skill.mdc`:
```
---
description: my-skill
globs: **/*
alwaysApply: false
---
@SKILL.md
```

## Windsurf
Add to `.windsurfrules` (or `.windsurf/skills/my-skill.md`):
```
# my-skill
@SKILL.md
```

## OpenClaw / Roo / Cline / AGY
Drop the folder where the loader expects skills; most read `SKILL.md`
or `manifest.json`. Point `manifest.json` `entry` at `SKILL.md`.

## Verify
```bash
python3 -c "import yaml,sys; yaml.safe_load(open('SKILL.md').read().split('---')[1]); print('SKILL_OK')"
```
