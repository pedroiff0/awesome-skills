---
name: financas-app
description: Corrigir, estender e validar o app de finanças pessoais (Node/Express + EJS + MongoDB + Docker). Cobre a arquitetura de porta única 4460 com demo via /demo, o fluxo de correção de UI (rebuild de AMBOS os containers + ASSET_VERSION), validação por browser headless no IP docker, verificação ad-hoc e o padrão Editar/Excluir via modal. Use quando o usuário pedir ajustes de UI, correção de bugs, edição de registros, ou versionamento/issues no repo pedroiff0/financas-app.
---

# financas-app — correção e extensão

App de controle financeiro (Node 20 + Express, EJS SSR + JS vanilla, MongoDB/Mongoose,
Zod, JWT). Três módulos independentes (financas/investimentos/veiculos) ligados por flags
em `config/env.js`. Arquitetura de camadas rígida: rota → controller → service → model.
Seguir `AGENTS.md` (Zod obrigatório, erros com `AppError`, sem JS inline — todo script em
`/js/`, CSP proíbe `unsafe-inline`).

## Arquitetura de deploy (PORTA ÚNICA 4460)

```
:4460 (nginx, única porta exposta)
   /demo/*  ──► app-demo  (autologin, mongo-demo isolado, JWT_SECRET_DEMO)
   /*       ──► app       (principal; mongo volume fa_mongo_data)
```
- `app-demo` monta rotas TAMBÉM sob `/demo` (páginas `/demo/*` e APIs `/demo/api/*`); o
  frontend prefixa chamadas de API com `data-api-prefix` do `<html>` (lido em `common.js`).
- `demoAutologin` emite JWT de verdade a cada request (só com `DEMO_AUTOLOGIN=true`).

### PITFALL RECORRENTE (já custou horas)
A página `/demo/app` carrega o CSS de **`/css/main.css` (app principal)**, NÃO de
`/demo/css/main.css` (app-demo). Por isso, para validar qualquer correção de CSS, é
obrigatório **rebuildar AMBOS os containers** (`app` e `app-demo`) e subir com a mesma
`ASSET_VERSION`. Se mexer só no app-demo, o CSS novo não aparece no browser.
- Bump `ASSET_VERSION` via env no shell (não editar `.env`): `ASSET_VERSION=N docker compose -p fa build --no-cache app app-demo && docker compose -p fa up -d app app-demo`.
- Se o CSS servido não mudar, o Docker pode ter cacheado a camada de COPY: usar `--no-cache`.
- Checar o CSS servido: `curl -s http://127.0.0.1:4460/css/main.css | grep ...` (app principal)
  e `/demo/css/main.css` (app-demo).

## Validação no browser (headless)
- O browser da ferramenta alcança o docker no host **192.168.80.1:4460** (NÃO 127.0.0.1:4460).
- `browser_navigate` + `browser_snapshot` para inspecionar; `browser_vision` para checagem
  visual (tema claro/escuro). O usuário aprova UI só vendo screenshot real.
- `browser_click` nem sempre dispara handlers JS (overlay/datepicker interceptando); se o
  modal não abrir, disparar via `browser_console`: `document.querySelector('button[data-acao=...]').click()`.
- Evitar cache do browser de validação: ao trocar ASSET_VERSION, navegar primeiro na URL
  exata do CSS (`/css/main.css?v=N` sem /demo) para popular aquele cache, depois na página.

## Verificação ad-hoc (exigida pelo system reminder)
Após editar, criar script temporário em `/tmp/hermes-verify-*.js` que inspeciona artifacts
servidos (CSS/JS/HTML via http) + fontes no repo, e resume explicitamente como verificação
ad-hoc (não suíte jest). Rodar com `node` e remover o script. Não confiar só em "jest verde"
para trabalho de UI. Cuidado: `curl` anônimo de rota autenticada cai em `/login` (falso
negativo) — validar HTML autenticado pelo browser ou checar o arquivo dentro do container
(`docker compose exec app-demo grep ...`).

## Padrão Editar/Excluir (tudo que é registrável)
- `public/js/modal.js` exporta `abrirModal(titulo, campos, onSalvar)` (sem JS inline, CSP ok).
- Ativos, Corretoras e Lançamentos já usam: botão "Editar" na linha/card abre o modal
  pré-preenchido; PATCH no backend já existe (schema Zod + controller + service).
- Ao adicionar edição a outro recurso, seguir o mesmo padrão (não criar novo modal).

## Segurança — NUNCA expor token da demo
O `demoAutologin` emite um JWT real do usuário demo. NÃO extrair, logar nem reutilizar esse
cookie/token. Se um comando de verificação capturá-lo por engano, descartar com `rm`
imediatamente e não reusá-lo. Validar logout/reset via browser autenticado ou checando
artifacts servidos, nunca copiando o token.

## BUG root-cause recorrente: tokenValidAfter invalida JWT
- `user.model.js` tinha `tokenValidAfter: { type: Date, default: () => new Date() }`.
  Todo usuário novo NASCE com sessão inválida: o `iat` (segundos TRUNCADOS) do JWT emitido
  logo após fica MENOR que `validAfterSec` → `resolveUser` retorna null → "Token invalido
  ou expirado" em logout (`/api/auth/logout`) e reset (`/api/reset-demo`).
- Sintoma reportado pelo usuário: "não consigo fazer logout, token inválido".
- Fix aplicado: `default: null` (resolveUser pula a checagem quando null). As ações de
  invalidação reais (troca/reset de senha, desativação em userService) continuam setando
  `new Date()` explicitamente — isso é correto e deve continuar.
- Middleware `authOptional` (não barra token inválido, só popula `req.user` se válido)
  aplicado em `/api/auth/logout` e `/api/reset-demo` para o logout/reset SEMPRE concluírem
  (limpam cookie / resetam banco) mesmo com token vencido.
- Ao mexer em auth, lembre: logout é a operação que INVALIDA a sessão — não pode exigir
  token válido no middleware `auth`.

## UI: remover > reestilizar (preferência do usuário)
- O usuário rejeitou a paginação "Primeiro/Anterior/1/Próximo/Último" MESMO após
  reestilização cuidadosa (bordas, hover, página ativa azul). Aceitou a REMOÇÃO:
  `paging: false` no DataTable (busca client-side + rolagem natural da página continuam).
- Lição: quando o usuário chamar um elemento de UI de "horrível", REMOVA-o (ou simplifique
  radicalmente), não apenas estilize. Valide por screenshot antes de commitar.
- Atenção após remover paginação: a tabela fica larga em mobile → precisa de
  `.table-responsive` (overflow-x:auto). Issue #21 do repo cobre isso.

## Gateway Telegram (Planck bot) — já existe, use
- Não é necessário configurar: o Hermes já tem `hermes-gateway.service` (systemd, ativo)
  com o Telegram pareado no canal "Pedro Rocha" (DM, id 8869378956) — esse é o "Planck bot"
  (hostname da máquina = `planck.local`).
- `channel_directory.json` em `~/.hermes` lista o canal. `hermes gateway status` mostra o
  service ativo.
- Para continuar a conversa por lá, o USUÁRIO abre o DM do bot e manda msg; o agente CLI não
  migra o chat em andamento sozinho. Pode haver instabilidade de rede ao `api.telegram.org`
  no ambiente — mas o canal existe.

## Versionamento / Issues (quando o usuário pedir "levantamento")
- Quer SemVer + CHANGELOG + tag de release; `app.locals.assetVersion` deveria vir de
  `package.json#version`.
- Criar issues em lote com `gh issue create` usando os LABELS VÁLIDOS do repo
  (ver references/github-issues.md): `bug`, `documentation`, `enhancement`, `modulo:financas`,
  `modulo:investimentos`, `modulo:moto`, `infra`, `seguranca`, `testes`, `ux`,
  `good first issue`, `help wanted`. NÃO usar labels inventados (ex.: `melhoria` não existe).
- Ao pedir levantamento, o usuário quer que eu CRIE as issues E COMECE a implementar uma —
  não apenas planeje.

## Testes
- `cd app && npx jest --forceExit` (Mongo em memória). Alvo: 230+ verde.
- REGRA DO AGENTS.md: não rodar linters/testes em trabalho criativo de UI até o usuário
  gostar ou antes de commitar — MAS rodar jest antes do commit para garantir verde.

## Referências
- `references/demo-architecture.md` — detalhes de rotas /demo, autologin, reset-demo.
- `references/ui-fix-workflow.md` — passo a passo de correção de UI + validação.
- `references/github-issues.md` — labels válidos e script de criar issues em lote.
