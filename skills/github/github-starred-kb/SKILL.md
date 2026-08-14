---
name: github-starred-kb
description: "Personal GitHub knowledge base built from the user's starred repos (pedroiff0). Maps all 41 starred repositories into knowledge domains (free APIs, sysadmin/self-hosted, Python, AI/agents/RAG, algorithms, math/edu, astronomy/science, web/Node, Hermes ecosystem, news) and provides on-demand retrieval of the relevant repo content via raw README / GitHub API. Use as a base of knowledge when the user asks for libraries, APIs, self-hosted tools, agent patterns, or references."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Knowledge-Base, Starred, APIs, Sysadmin, Self-Hosted, Python, AI-Agents, RAG, Reference, Research]
    related_skills: [github-issue-pr-attribs, github-pr-workflow, github-code-review]
---

# GitHub Starred Knowledge Base (pedroiff0)

This skill turns the user's **41 starred GitHub repositories** into a reusable
knowledge base. Instead of cloning 41 repos (huge, stale fast), it keeps a
**mapped index** and fetches the specific repo's content **on demand** via the
GitHub raw API / `gh api` when a query matches a domain.

Use it whenever the user asks for: a free API, a self-hosted tool, a Python
library, an AI agent/RAG pattern, an algorithm, a math/edu resource, an
astronomy reference, a Node/web example, or anything their starred repos cover.

## The 41 starred repos, by domain

Full table (with stars + raw URL) lives in `references/starred-index.md`.
Quick domain map:

| Domain | Starred repos |
|---|---|
| **Free APIs** | `public-apis/public-apis` |
| **Sysadmin** | `awesome-foss/awesome-sysadmin` |
| **Self-hosted** | `awesome-selfhosted/awesome-selfhosted` |
| **Python** | `vinta/awesome-python`, `TheAlgorithms/Python`, `langflow-ai/langflow`, `D4Vinci/Scrapling`, `guillaumemeyer/watermarks-remover`, `shubhomoydas/ad_examples`, `pedroiff0/planilhador`, `pedroiff0/levantamento-estoque`, `pedroiff0/controle-estoque`, `pedroiff0/academicoWeb`, `pedroiff0/spectraviewer`, `pedroiff0/anomaly_detection`, `pedroiff0/CalculoNumerico`, `pedroiff0/verdementa`, `pedroiff0/caixas` |
| **AI / Agents / RAG / MCP** | `Shubhamsaboo/awesome-llm-apps`, `Arindam200/awesome-ai-apps`, `punkpeye/awesome-mcp-servers`, `ZeroPointRepo/awesome-hermes-skills`, `langflow-ai/langflow`, `Anil-matcha/ai-creator-academy`, `athola/claude-night-market`, `outsourc-e/hermes-workspace` |
| **Algorithms / CS** | `TheAlgorithms/Python`, `TheAlgorithms/Java` |
| **Math / Edu / Video** | `3b1b/manim`, `ranieremenezes/easyspec`, `pedroiff0/CalculoNumerico`, `pedroiff0/formularios`, `pedroiff0/sistema-academico`, `pedroiff0/academicoWeb`, `pedroiff0/guia-github` |
| **Astronomy / Science** | `pedroiff0/spectraviewer`, `pedroiff0/anomaly_detection`, `ranieremenezes/easyspec`, `TrackersSun/NASA-SPACE-APPS-CHALLENGE-2022`, `pedroiff0/quartz-site` |
| **Web / Node / EJS** | `pedroiff0/financas-app`, `pedroiff0/projeto-profissional`, `pedroiff0/portfolio`, `pedroiff0/sistema-academico`, `HafizulHaque/node-js-mongoose-jwt-auth-mvc-app`, `outsourc-e/hermes-workspace` |
| **Hermes ecosystem** | `ZeroPointRepo/awesome-hermes-skills`, `outsourc-e/hermes-workspace`, `athola/claude-night-market` |
| **Profile / Docs** | `pedroiff0/pedroiff0`, `pedroiff0/cv`, `pedroiff0/guia-github` |
| **News / Misc** | `kornha/parliament` |
| **Meta awesome** | `sindresorhus/awesome` (index of all awesome lists) |

## How to use (on-demand retrieval)

When a query falls in a domain, fetch the relevant repo's README or specific
file via raw GitHub, then synthesize. Do NOT clone the whole star list.

### 1. Resolve which starred repo(s) match
```bash
# list domains for a keyword
python3 skills/github/github-starred-kb/scripts/fetch_kb.py --match "api clima"
# -> public-apis/public-apis
```

### 2. Fetch the raw README (or a path)
```bash
# via helper (prints raw URL or content)
python3 skills/github/github-starred-kb/scripts/fetch_kb.py --repo public-apis/public-apis --readme
# manual equivalent:
curl -sL https://raw.githubusercontent.com/public-apis/public-apis/master/README.md
```

### 3. For "awesome" lists, grep the section you need
```bash
curl -sL https://raw.githubusercontent.com/public-apis/public-apis/master/README.md \
  | grep -iA3 "weather\|climate"
```

### 4. For the user's own repos, prefer the local clone when present
```bash
# e.g. financas-app lives at /home/pedro/Repositorios/pessoal/financas-app
# awesome-skills at /home/pedro/Repositorios/pessoal/awesome-skills
```

## Refreshing the index

The star list changes over time. To rebuild `references/starred-index.md`:
```bash
python3 skills/github/github-starred-kb/scripts/fetch_kb.py --rebuild
```
This calls `gh api users/pedroiff0/starred` and rewrites the index with current
stars + categories (categories are heuristics; review the diff).

## Pitfalls

- **Don't clone all 41.** They're large and go stale; fetch on demand.
- **Raw default branch** differs (`master` vs `main`). The helper tries both;
  if a manual curl 404s, swap the branch.
- **awesome lists are huge** — grep the specific section, don't paste the whole file.
- **Categories are a heuristic map**, not gospel; a repo can serve multiple domains.
- Prefer the **local clone** for the user's own repos (fresher + offline).
