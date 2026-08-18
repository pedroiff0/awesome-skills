---
name: nosignups-catalog
description: "Catálogo curado de ferramentas open source sem signup (NoSignups.net). 234 tools organizadas por categoria e relevância para DevOps/self-hosted/operations. Use para encontrar alternativas open source a ferramentas SaaS, especialmente focado em self-hosted, privacidade e automação."
version: 1.0.0
author: Pedro (pedroiff0)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [open-source, self-hosted, devops, no-signup, tools, catalog, privacy, research]
    related_skills: [github-starred-kb, research-synthesizer, obscure-tool-install-lookup]
---

# NoSignups Catalog

Catálogo curado de **234 ferramentas open source** que funcionam sem signup,
organizadas por categoria e relevância para o perfil DevOps/Operations.

## Fonte

- Site: https://nosignups.net
- Repositório: https://github.com/BraveOPotato/FckSignups
- JSON: https://raw.githubusercontent.com/BraveOPotato/FckSignups/refs/heads/main/tools.json

## Estrutura

```
skills/research/nosignups-catalog/
  SKILL.md                    # Este arquivo
  references/
    full-catalog.md           # Todas as 234 tools organizadas por categoria
    curated-list.md           # Lista curada por relevância DevOps/self-hosted
    tools-data.json           # Dados crus do tools.json (para queries)
  scripts/
    generate_catalog.py       # Atualiza os catálogos a partir do JSON
```

## Quando Usar

- Encontrar alternativas open source a ferramentas SaaS
- Buscar ferramentas self-hosted para substituir serviços pagos
- Encontrar ferramentas de privacidade e segurança
- Encontrar ferramentas de desenvolvimento sem dependências externas
- Descobrir projetos open source relevantes para o ecossistema DevOps

## Como Usar

### 1. Buscar por categoria
Leia `references/full-catalog.md` para a lista completa por categoria
(Development, Utilities, Design, Productivity, Writing, Media, Privacy, Data).

### 2. Buscar por relevância DevOps
Leia `references/curated-list.md` para ferramentas pré-filtradas por relevância
para DevOps, self-hosted, segurança e operações.

### 3. Query programática (Python)
```python
import json

with open('skills/research/nosignups-catalog/references/tools-data.json') as f:
    tools = json.load(f)

# Buscar tools de uma categoria
devops_tools = [t for t in tools if t['category'] == 'development']

# Buscar por keyword
pdf_tools = [t for t in tools if 'pdf' in t['description'].lower()]

# Top stars
top = sorted(tools, key=lambda x: x.get('stars', 0), reverse=True)[:20]
```

### 4. Atualizar o catálogo
```bash
python3 skills/research/nosignups-catalog/scripts/generate_catalog.py
```

## Categorias (10)

| Categoria | Count | Descrição |
|-----------|-------|-----------|
| Development | 63 | IDEs online, formatadores, APIs, diagramas, ícones |
| Utilities | 42 | File transfer, conversores, QR, terminal themes |
| Design & Graphics | 42 | Editores SVG/pixel art, diagramas, ícones |
| Productivity | 22 | PDF, spreadsheets, notas, pomodoro, escritório |
| Writing & Docs | 18 | Markdown editors, ebooks, CV builders |
| Media | 21 | Video, áudio, imagem, compressão |
| Privacy & Security | 8 | Encrypt, encoding, metadata removal |
| Data & Analytics | 10 | Visualização, SQL, CSV, OSINT |
| Education | 5 | Roadmaps, cursos, algoritmos |
| Lists | 3 | Agregadores (free-for.dev, OSINT Framework) |

## Top 20 por Stars (geral)

1. **Roadmaps.sh** (361k) — Roadmaps interativos de carreira dev
2. **VS Code Web** (188k) — Visual Studio Code no navegador
3. **free-for.dev** (129k) — Lista de SaaS com tiers gratuitos
4. **Excalidraw** (128k) — Whiteboard colaborativo
5. **Godot Web** (115k) — Engine de jogos no navegador
6. **Stirling-PDF** (87k) — Editor PDF #1 do GitHub
7. **hoppscotch** (80k) — Alternativa open source ao Postman
8. **OpenCut** (72k) — Alternativa open source ao CapCut
9. **AFFiNE** (70k) — Base de conhecimento next-gen
10. **World Monitor** (62k) — Dashboard de inteligência global
11. **tldraw** (49k) — Ferramenta de desenho
12. **Algorithm Visualizer** (49k) — Visualização de algoritmos
13. **JSON Crack** (44k) — Visualizador JSON → grafos
14. **Logseq** (44k) — Base de conhecimento privacy-first
15. **Cobalt** (42k) — Downloader de mídia
16. **IT-Tools** (40k) — Coleção de ferramentas dev
17. **Croc** (39k) — Transferência segura P2P
18. **drawDB** (38k) — Editor de diagramas DB/SQL
19. **carbon** (36k) — Screenshots bonitas de código
20. **CyberChef** (35k) — "Cyber workbench" (encode/decode/encrypt)

## Destaques DevOps/Self-Hosted

| Tool | Descrição | Stars |
|------|-----------|-------|
| Stirling-PDF | Editor PDF completo | 87k |
| hoppscotch | API client (alt. Postman) | 80k |
| IT-Tools | 50+ ferramentas dev online | 40k |
| drawDB | Diagrama ER + SQL | 38k |
| CyberChef | Encode/decode/encrypt | 35k |
| Grist | Spreadsheet + database | 11k |
| Croc | Transferência segura | 39k |
| PairDrop | AirDrop alternativo | 11k |
| VERT | Conversor de arquivos | 15k |
| CryptPad | Escritório E2E encrypted | 8k |
| privacy.sexy | Hardening scripts | 6k |

## Pitfalls

- **Stars ≠ utilidade**: Ferramentas pequenas (1-50 stars) podem ser extremamente úteis
- **License varia**: Nem tudo é MIT/Apache; verificar antes de usar em produção
- **Manutenção**: Ferramentas pequenas podem estar abandonadas; verificar last commit
- **Self-hosted vs Web-only**: Nem todas podem ser self-hosted; checar campo `github`
