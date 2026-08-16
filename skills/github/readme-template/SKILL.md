---
name: readme-template
description: Standard README template for repos — professional structure with badges, overview, table of contents, features/modules, stack, installation, configuration, tests, security, structure, docs, roadmap, contribute, license, author + RepoActivity sections (Star History, repo stats) + profile GIF footer. Use when creating or rewriting a README for any repo.
version: 1.0.0
author: pedroiff0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [github, readme, template, documentation, repo, professional]
---

# README Template — professional repo standard

Build a professional, rich README for any repository. Combines the
financas-app structure with RepoActivity sections (Star History, badges) and
the pedroiff0 profile GIF footer.

## Trigger
User asks to "create a README", "write a README for repo X", "rewrite my README",
"make a professional README", or any task that produces a README.md for a repo.

## Source examples
- **financas-app README** (`financas-app/README.md`): hero logo, screenshots
  grid, index, modules table, stack table, features list, demo, install, config,
  docker, tests, security, structure, docs, roadmap, contribute, license, author.
- **Awesome Credential-Verification-Platform** (`ishandutta2007/...`): centered
  banner + shields badges, overview, table of contents, comparative tables,
  how-to-contribute, star history chart, disclaimer — the "RepoActivity" sections.
- **Profile GIF**: `https://raw.githubusercontent.com/pedroiff0/pedroiff0/main/assets/pedroiff0.gif`

## Anatomy of the README

### 1. Header (centered)
```markdown
<div align="center">

<img src="PATH_TO_LOGO" alt="Project Logo" width="120" height="120"/>

> One-line tagline describing the project.

</div>
```

### 2. Badges (shields.io — centered, right after header)
Row of flat-square or for-the-badge shields:
- License
- Stars / Forks
- PRs welcome
- Version / Release
- Build status (if CI on)
- Follow / social

```markdown
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License"/></a>
<a href="stargazers"><img src="https://img.shields.io/github/stars/OWNER/REPO?style=flat-square&color=gold" alt="Stars"/></a>
```

### 3. Screenshots / Demo GIF
```markdown
<div align="center">

**Tour / Demo**

<img src="docs/assets/demo-tour.gif" alt="Demo" width="900"/>

</div>
```

### 4. Table of Contents
- O que é / About
- Módulos / Features
- Stack Técnica
- Funcionalidades
- Demo
- Instalação / Quick Start
- Configuração
- Docker (if applicable)
- Testes
- Segurança / Security
- Estrutura do Projeto
- Documentação
- Roadmap
- Contribuição
- Licença
- Autor

### 5. About / O que é
One paragraph explaining what the project is, its purpose, and key differentiator.

### 6. Modules / Features table
If multi-module, a table with module name, flag/env, routes, coverage.
Otherwise a bullet list of features grouped by category.

### 7. Stack Técnica
Table: Runtime, Server, Database, Views, Validation, Auth, Security, Tests, Deploy.

### 8. Installation + Config + Docker + Tests
Code blocks with exact commands. Env var table. Makefile targets if applicable.

### 9. Security
Bullet list of security measures. Link to SECURITY.md if exists.

### 10. Estrutura do Projeto
Tree of directories with one-line descriptions per folder.

### 11. Documentação
Table linking to AGENTS.md, SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, CHANGELOG.md.

### 12. Roadmap
Link to GitHub Project + phase table with status (✅/🔄/🚧/📋).

### 13. Contribuição
Link to CONTRIBUTING.md + bullet list of conventions (conventional commits, branch naming, PR checklist).

### 14. Licença
License name + link to LICENSE file.

### 15. Author + RepoActivity (footer)
```markdown
---

## 📊 RepoActivity

[![Star History Chart](https://star-history.dera.page/svg?repos=OWNER/REPO&type=date&legend=top-left)](https://star-history.dera.page/#OWNER/REPO&type=date&legend=top-left)

---

## 👨‍💻 Autor

<div align="center">

<img src="https://raw.githubusercontent.com/pedroiff0/pedroiff0/main/assets/pedroiff0.gif" alt="pedroiff0" width="900"/>

</div>

<div align="center">

**YYYY Project Name**

Feito com ☕, código e ☄️ por **Author Name**

[![GitHub](https://img.shields.io/badge/GitHub-pedroiff0-181717?logo=github&logoColor=white)](https://github.com/pedroiff0)
[![Site Oficial](https://img.shields.io/badge/Site-Oficial-22c55e?logo=googlechrome&logoColor=white)](https://phrandrade.com/)
[![Portfólio](https://img.shields.io/badge/Portfólio-2563eb?logo=github&logoColor=white)](https://pedroiff0.github.io/webpage/)

</div>
```

## RepoActivity sections (always include)
1. **Star History chart** — `star-history.dera.page` SVG with repo param.
2. **Profile GIF** — `pedroiff0.gif` from the profile repo, centered, width 900.
3. **Author badges** — GitHub, Site, Portfólio shields.

## Rules
- **Centered header** with logo + tagline.
- **Badges row** right after header (license, stars, forks, PRs).
- **Screenshots/GIF** centered with caption.
- **Tables** for stack, modules, env vars, docs, roadmap.
- **Code blocks** for install/config/test commands.
- **Tree** for project structure.
- **RepoActivity** at the bottom: Star History + profile GIF + author badges.
- **No plain/flat README** — always rich, structured, professional.
- **Language**: match the repo's existing language (PT-BR for Pedro's repos, EN for international).
- **License badge** must match the actual LICENSE file.
- **Star History URL** must use the correct OWNER/REPO.

## Pitfalls
- `star-history.dera.page` é o serviço confiável de Star History (o antigo `star-history.com` foi descontinuado). Sempre use o domínio `.dera.page`.
- Profile GIF URL é fixa: `https://raw.githubusercontent.com/pedroiff0/pedroiff0/main/assets/pedroiff0.gif`
- Shields.io badges: use `style=flat-square` para consistência.
- Se CI está off, NÃO adicione badge de build (aparecerá "failing").
- `raw.githubusercontent.com` NÃO funciona em repos privados sem token de autenticação — use paths relativos para imagens em repos privados.

## README em repo privado
Repos privados NÃO podem usar `raw.githubusercontent.com` para imagens (retorna 404 sem token). Para que o README funcione em repo privado:

### Imagens locais (logo, screenshots, GIFs)
SEMPRE use paths relativos ao invés de URLs absolutas:

```markdown
<!-- ❌ NÃO funciona em repo privado -->
<img src="https://raw.githubusercontent.com/OWNER/REPO/main/docs/assets/logo.png"/>

<!-- ✅ Funciona em repo privado -->
<img src="docs/assets/logo.png"/>
```

O GitHub resolve paths relativos automaticamente no render do README.

### GIF do perfil (footer)
Para repos privados, o GIF do perfil NÃO aparece (URL raw é do repo público `pedroiff0/pedroiff0`). Opções:
1. **Remover o GIF** do footer em repos privados.
2. **Usar path relativo** se o GIF for copiado para o repo privado:
   ```markdown
   <img src="assets/pedroiff0.gif" alt="pedroiff0" width="900"/>
   ```
3. **Manter o GIF apenas em repos públicos** — a skill detecta pelo contexto.

### Star History
`star-history.dera.page` depende da API pública do GitHub. Para repo privado:
- O chart NÃO funciona (repo não é público, sem dados na API).
- **Solução**: omitir a seção Star History em repos privados.
- Alternativa: badge estático "Private repo" no lugar.

### Badges shields.io
Badges que dependem de dados públicos (stars, forks, license) NÃO funcionam em repo privado:
- `img.shields.io/github/stars/OWNER/REPO` → 404 ou "not found"
- `img.shields.io/github/forks/OWNER/REPO` → 404 ou "not found"
- `img.shields.io/github/license/OWNER/REPO` → 404 ou "not found"

**Solução para repos privosos:**
- Badges estáticos manuais:
  ```markdown
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Status-active-success.svg?style=flat-square" alt="Status"/>
  ```
- Ou omitir badges dinâmicos e manter apenas os estáticos (license, status, tech stack).

### Resumo: o que muda em repo privado
| Seção | Repo público | Repo privado |
|-------|-------------|--------------|
| Logo/screenshots | URL raw ou path relativo | **Path relativo obrigatório** |
| GIF do perfil | URL raw funciona | **Omitir ou path relativo** |
| Star History | Funciona | **Omitir** |
| Badges stars/forks | Funciona | **Omitir ou estático** |
| Badge license | Funciona | **Estático manual** |
| Tech badges | Funciona | Funciona (são estáticos) |

### Template para repo privado
Quando o usuário pedir README para repo privado, a skill DEVE:
1. Usar paths relativos para TODAS as imagens.
2. Omitir Star History.
3. Substituir badges dinâmicos por estáticos.
4. Omitir ou usar path relativo para o GIF do perfil.
5. Adicionar nota no README: "Repo privado — badges indisponíveis."

## Verification
After writing the README:
1. `curl -s -o /dev/null -w "%{http_code}\n" <star-history-url>` → expect 200.
2. `curl -s -o /dev/null -w "%{http_code}\n" <profile-gif-url>` → expect 200.
3. `curl -s -o /dev/null -w "%{http_code}\n" <each-shield-url>` → expect 200.
4. Verify LICENSE file exists and matches badge.
5. Verify all linked docs (AGENTS.md, SECURITY.md, etc.) exist.
