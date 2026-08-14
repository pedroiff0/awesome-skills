# Plugin Template — install guide

## Hermes Agent
```bash
hermes plugins add ./my-plugin
# or drop in: ~/.hermes/hermes-agent/plugins/my-plugin/
```

## Claude Code
- Commands → `.claude/commands/do-thing.md`
- Hooks → `.claude/settings.json` (`PostToolUse` etc.)

## Cursor / Windsurf
Wire `commands/` via rules (`.cursor/rules`, `.windsurfrules`).

## OpenClaw / Roo / Cline / AGY
Load `manifest.json`; most read `commands/` + `hooks/`.

## Verify
```bash
python3 -c "import json; json.load(open('manifest.json')); print('PLUGIN_OK')"
```
