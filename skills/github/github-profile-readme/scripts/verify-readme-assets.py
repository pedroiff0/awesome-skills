#!/usr/bin/env python3
"""Ad-hoc verification for a GitHub profile README repo.

Usage: python3 verify-readme-assets.py <repo_root>
Checks:
  - .github/workflows/snake.yml parses; has name/on/permissions/jobs/snk step.
  - assets/starfield.svg (if present) is well-formed XML.
  - (optional) prints raw URLs to curl-check manually.

NOTE: PyYAML parses YAML `on:` as boolean True (YAML 1.1). We test
`(True in data) or ('on' in data)` — never just `'on' in data`.
This is AD-HOC verification, not a canonical suite.
"""
import sys, os, yaml
try:
    import xml.dom.minidom as minidom
except Exception:
    minidom = None

root = sys.argv[1] if len(sys.argv) > 1 else "."
checks = []

wf = os.path.join(root, ".github/workflows/snake.yml")
if os.path.exists(wf):
    with open(wf) as f:
        d = yaml.safe_load(f)
    checks.append(("workflow.name", "name" in d))
    checks.append(("workflow.on", (True in d) or ("on" in d)))
    checks.append(("permissions.contents=write", d.get("permissions", {}).get("contents") == "write"))
    checks.append(("jobs.generate", "jobs" in d and "generate" in d["jobs"]))
    uses = [s.get("uses") for s in d["jobs"]["generate"]["steps"]]
    checks.append(("snk step", any("snk" in u for u in uses)))
    checks.append(("publish step", any("ghaction-github-pages" in u for u in uses)))
else:
    checks.append(("snake.yml present", False))

svg = os.path.join(root, "assets/starfield.svg")
if os.path.exists(svg) and minidom:
    try:
        minidom.parse(svg)
        checks.append(("starfield.svg XML", True))
    except Exception:
        checks.append(("starfield.svg XML", False))
elif os.path.exists(svg):
    checks.append(("starfield.svg XML (minidom missing)", True))  # skip parse, file exists

ok = all(v for _, v in checks)
for n, v in checks:
    print(f"[{'OK' if v else 'FAIL'}] {n}")
print("\nAD-HOC VERIFICATION:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
