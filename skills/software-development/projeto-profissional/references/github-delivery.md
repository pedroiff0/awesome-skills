# Entrega no GitHub: app privado com CI, issues, PR e Project

A seção "Publishing to GitHub as a template repository" do SKILL.md cobre o
caso do *template público*. Este arquivo cobre o outro caso: **projeto derivado,
repositório privado**, que é o que o Pedro pede quando diz "publique-o no
github com a CI, ISSUES, PR, crie um PROJECT associado. Repo Privado."

Ele lista os artefatos em uma frase só. Trate cada um como item de checklist —
entregar 4 de 5 e resumir como pronto custa um turno.

## Ordem que funciona

```bash
# 1. Auditar antes do primeiro push (privado hoje pode virar público amanhã)
git add -A && git check-ignore -v .env backups app/node_modules   # os 3 têm de casar
git diff --cached --name-only | grep -E '^\.env$|node_modules|backups/'  # vazio

# 2. Commit + repo privado em um passo
gh repo create <nome> --private --source=. --remote=origin \
  --description "..." --push

# 3. Conferir que a CI do template rodou VERDE no GitHub, não só local
gh run list --limit 3
gh run view <id> --log | grep -E 'Tests:|Suites:'

# 4. Labels antes das issues (senão --label falha silenciosamente)
gh label create "modulo:<nome>" --color 1d76db --description "..." --force

# 5. Issues de roadmap
gh issue create --title "..." --body "..." --label "modulo:x,enhancement"

# 6. Project (v2) — precisa de escopo OAuth extra, ver abaixo
gh project create --owner <user> --title "..." --format json   # anote id e number
gh project item-add <number> --owner <user> --url <url-da-issue>
gh project link <number> --owner <user> --repo <user>/<repo>
```

## O escopo `project` não vem no login padrão do gh

`gh project create` falha com
`your authentication token is missing required scopes [project read:project]`.
Isso **não** é bug nem limitação do ambiente — é escopo que o Pedro precisa
autorizar uma vez:

```bash
gh auth refresh -h github.com -s project,read:project
```

Três detalhes que travam esse comando:

1. **`-h github.com` é obrigatório** fora de terminal interativo, senão sai
   `--hostname required when not running interactively`.
2. **É device-code**: rode com `background=true, pty=true`, leia o código no
   `process(action='poll')` e **mostre o código ao Pedro** junto com
   <https://github.com/login/device>. O comando fica bloqueado esperando.
3. **Ele pede um Enter** ("Press Enter to open ... in your browser") e depois
   tenta `xdg-open`, que falha em máquina sem navegador
   (`www-browser: not found`). Isso é ruído, não erro: mande o Enter com
   `process(action='submit')` e o fluxo segue esperando a autorização. Confirme
   com `gh auth status | grep -i scopes` antes de tentar o `project create` de
   novo.

## Mexer em campo do Project v2 exige IDs, não nomes

`gh project item-edit` não aceita "Status=Todo". Colete os IDs primeiro:

```bash
gh project field-list <number> --owner <user> --format json   # id do campo + das opções
gh project item-list <number> --owner <user> --format json    # id de cada item
gh project item-edit --id <item> --project-id <PVT_...> \
  --field-id <PVTSSF_...> --single-select-option-id <opt>
```

O `--project-id` é o `PVT_...` devolvido pelo `create` (não o número).

## O PR é para demonstrar o fluxo, então feche o ciclo

Branch → commit → push → `gh pr create` → **esperar a CI** (`gh pr checks <n>`,
leva ~2 min) → `gh pr merge --squash --delete-branch` → `git checkout main &&
git pull`. Abrir o PR e parar aí deixa a árvore local numa branch órfã.

Escolha para o PR um trabalho real — de preferência fechando parte de uma das
issues que você acabou de abrir. Um PR de "atualiza README" desperdiça a
demonstração; um que corrige um defeito medido mostra o padrão de evidência.

## Corpo de issue/PR: escreva o porquê, com números

O padrão que o Pedro valoriza: tabela antes/depois com valores medidos, o
critério objetivo (ex.: mínimo AA da WCAG), e uma frase dizendo como você sabe
que funciona. Deixe explícito o que ficou de fora — checkbox desmarcada é mais
honesta que escopo silenciosamente ampliado.

Cuidado com heredoc: `gh pr create --body "$(cat <<'EOF' ... EOF)"` preserva
markdown e crases sem o shell interpretar.

## Quando o `gh` não ajuda: PAT + GraphQL API direto

Nesta sessão o `gh auth login --with-token` com um PAT classic **travou** em
`missing required scope 'read:org'` — e `read:org` **não aparece** na lista de
escopos do PAT classic (só existe em OAuth do próprio gh). O `gh auth refresh`
também trava em prompt device-code que o agente não consegue completar sozinho.
Saída que funcionou de fato:

1. Crie um PAT classic com os escopos `repo`, `project`, `read:project`,
   `workflow` (e quaisquer outros que já usava). **Não** precisa de `read:org`.
2. Não use `gh auth login`. Passe o token direto a um script Python que chama a
   GitHub GraphQL API — ela não exige `read:org`:

```python
import os, json, urllib.request
TOKEN = os.environ["GH_PAT"]  # export GH_PAT=ghp_xxx  (não cole no comando)
def gql(q, v=None):
    body = json.dumps({"query": q, "variables": v or {}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json",
                  "User-Agent": "hermes"})
    with urllib.request.urlopen(req) as r:
        d = json.load(r)
    if "errors" in d: raise SystemExit(d["errors"])
    return d["data"]
# criar Project V2 (user-level): ownerId = viewer.id
vid = gql("query { viewer { id login } }")["viewer"]
proj = gql("mutation($o:ID!,$t:String!){createProjectV2(input:{ownerId:$o,title:$t}){projectV2{id number url}}}",
           {"o": vid["id"], "t": "Roadmap"})["createProjectV2"]["projectV2"]
```

3. Adicionar issues já existentes ao Project:

```python
# pegar node id da issue
iid = gql("query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){id}}}",
          {"o":"pedroiff0","r":"<repo>","n":1})["repository"]["issue"]["id"]
item = gql("mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}",
           {"p": proj["id"], "c": iid})["addProjectV2ItemById"]["item"]["id"]
# mover coluna (Status é single-select): pegue field/options e use updateProjectV2ItemFieldValue
```

Pitfalls reais desta sessão:
- `updateProjectV2Field` (redefinir opções do Status) exige `color` e
  `description` em cada opção — se omitir, erro de validação. Melhor: **não
  redefina** as opções; use as defaults (`Todo`, `In Progress`, `Done`) que o
  Project já cria.
- `fieldValues` de um item inclui nós que não são single-select (ex.: título) e
  vêm sem `name` → filtre com `n.get("name")` ao ler a coluna.
- `gh api rest /users/<user>/projects/<n>` retorna 404 para Projects V2 (a rota
  REST não existe); confirme sempre via GraphQL `user(login){projectsV2{...}}`.
- O token aparece em texto puro no chat/history do shell. Recomende ao dono
  revogar após o uso; o Project e os vínculos ficam persistidos no GitHub, não
  dependem mais do token.
