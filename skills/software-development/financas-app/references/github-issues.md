# Issues no GitHub (repo pedroiff0/financas-app)

Criar em lote com `gh issue create`. `gh` já autenticado (`gh auth status` → logado).
NUNCA usar labels inexistentes — os válidos são:

| Label | Uso |
|---|---|
| `bug` | Defeito de comportamento/código |
| `documentation` | Docs/HANDOFF/README |
| `enhancement` | Nova funcionalidade |
| `modulo:financas` | Contas, lançamentos, orçamentos, metas |
| `modulo:investimentos` | Carteira, corretoras, ativos, operações |
| `modulo:moto` | Oficina, manutenções, abastecimentos, gastos |
| `infra` | Docker, CI, deploy, backup |
| `seguranca` | Auth, CSP, validação, dados sensíveis |
| `testes` | Cobertura/qualidade de teste |
| `ux` | Interface, layout, acessibilidade |
| `good first issue` | Bom para iniciantes |
| `help wanted` | Precisa de atenção extra |

Labels INVÁLIDOS (não usar): `melhoria`, `tech`, `frontend`, `backend`, `urgente`.

Exemplo de criação em lote (script bash):
```bash
REPO=pedroiff0/financas-app
gh issue create --repo "$REPO" --title "Título" --body "$(cat <<'EOF'
Corpo em markdown. Refere-se a: arquivo/rota.
Tarefas:
- item 1
- item 2
EOF
)" --label "modulo:financas","ux"
```

## Versionamento desejado pelo usuário
- SemVer (v0.1.0) + tag anotada no git a cada release.
- `CHANGELOG.md` por PR (seções Breaking/Features/Fixes).
- `app.locals.assetVersion` deveria vir de `package.json#version` (hoje é injetado no shell
  via `ASSET_VERSION`). Issue #12 mapeia isso.
