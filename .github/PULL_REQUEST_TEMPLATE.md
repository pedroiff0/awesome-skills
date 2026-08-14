<!--
awesome-skills PR template — standard assignments + self-review.
See docs/CODE_REVIEW.md for the review model.
-->

## 📌 Summary

<!-- What and why. Link the issue: "Closes #N" or "Relates #N". -->

Closes #

## 🧭 Assignments (fill before review)

- [ ] **Assignee:** @pedroiff0
- [ ] **Reviewer:** @pedroiff0
- [ ] **Labels:** (bug / enhancement / documentation / …)
- [ ] **Project:** Awesome Skills — Roadmap
- [ ] **Milestone:** (Backlog / release tag)
- [ ] **Development:** branch linked to issue
- [ ] **Relationship:** Closes/Relates #N

## 🔍 Self-Review

- [ ] New skill/agent/plugin follows `templates/` (multi-tool compatible)
- [ ] `SKILL.md` / `AGENT.md` / `manifest.json` valid (run the verify snippet)
- [ ] `python3 tools/gen_index.py` regenerates README without errors
- [ ] No secrets, no hardcoded tokens
- [ ] Docs updated (CONTRIBUTING / README if behavior changed)

## 🧩 Type

- [ ] 🐞 Bug fix
- [ ] 🚀 Feature / new skill
- [ ] 📋 Task / Docs / Chore
- [ ] 🔒 Security

## 🧪 How to verify

```bash
python3 tools/gen_index.py
# lint a SKILL.md frontmatter:
python3 -c "import yaml; yaml.safe_load(open('skills/<cat>/<name>/SKILL.md').read().split('---')[1]); print('OK')"
```

## 📎 Reviewer notes

<!-- Trade-offs, sensitive areas, open questions. -->
