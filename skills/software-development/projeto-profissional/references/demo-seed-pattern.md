# Padrão de seed de demonstração ("banco super preenchido")

Quando o Pedro pede "botão de demo que carrega um usuário em banco seed demo"
ou "banco deve estar super preenchido para explorar os recursos", a intenção é
**exercitar todas as telas do template com dados plausíveis**, não só o admin.

## Formato que funcionou (PR #8, derivado da conversa)

Domínios enxutos de demonstração, criados em camadas:

- `src/services/demoService.js` → `carregarDemo({ usuarios, projetos, itens, force })`
  - idempotente: se já há dados (`CatalogItem.countDocuments() > 0`) retorna
    `{ carregado: false, motivo: 'ja_existe' }` — evita duplicar a cada clique.
  - `force: true` apaga as coleções de demo e repopula.
  - usuários `@example.com` com papéis variados; senha = a do `SEED_PASSWORD_FILE`
    (compartilhada, mesma do admin) para o dono conseguir logar em qualquer um.
  - projetos com `status`/`tags`/`ownerId` (exercita escopo por usuário); catálogo
    com `sku`/`category`/`price`/`stock` (exercita busca `$text`, filtro, paginação).
- Botão no dashboard (`/app`), **só fora de produção** (`process.env.NODE_ENV
  !== 'production'`). Backend duplamente bloqueado: a view só renderiza o botão
  fora de produção **e** o controller `demo.controller.js` retorna 403 se
  `req.app.get('env') === 'production'`.
- Telas de exploração: `/projetos` (filtro status/tag + paginação) e `/catalogo`
  (busca + filtro de categoria), cada uma com `pageScript` próprio em `public/js/`
  que consome `/api/projects` e `/api/catalog`.

## Pitfalls de seed/teste que esta sessão bateu (e custaram voltas)

1. **`mustChangePassword` bloqueia o render de página autenticada.** O admin
   criado por `seedAdminIfEmpty` com senha vinda de arquivo nasce com
   `mustChangePassword: true`; o `requirePasswordChanged` redireciona `/projetos`
   → `/primeiro-acesso` (302), não 200. Em testes de render autenticado, zere o
   flag **antes** de logar: `User.updateOne({email:'admin@admin.com'},{$set:{mustChangePassword:false}})`.

2. **Seed de teste não pode depender do HD do dono.** O `SEED_PASSWORD_FILE`
   aponta para `~/Documentos/comum/...`, que não existe no CI. Crie um **fixture
   temporário** em `os.tmpdir()` dentro do próprio `tests/seed.test.js` e aponte
   `process.env.SEED_PASSWORD_FILE` para ele — assim o teste passa em qualquer
   runner. Nunca aponte o teste para o caminho real do HD.

3. **`afterEach(clearDb)` apaga o admin entre testes.** Não use `beforeAll` para
   semear e espere que o login funcione em testes seguintes — o `clearDb` mata o
   admin. Garanta o usuário alvo **dentro de cada `it`** (helper `login(email)`
   que chama `seedAdminIfEmpty`/`carregarDemo` antes de logar).

4. **Ordem importa no `login` helper.** Se o `carregarDemo({force:false})`
   retornar `ja_existe` cedo (já há itens de um teste anterior), ele não recria
   nada — mas os usuários demo do teste anterior ainda existem, então o login de
   admin continua ok. O 401 vem de **outra** causa (senha do fixture vs
   `AdminComum123!!`): garanta que o `SEED_PASSWORD_FILE` do teste contenha a
   senha que o helper usa no `send({password: ...})`.

5. **`demoN@example.com` pode ser admin.** `carregarDemo` marca `i % 7 === 0`
   como admin, então `demo1` (i=0) é admin e enxerga todos os projetos — um teste
   de "usuário comum só vê os próprios" deve usar `demo2` (não-admin).

6. **Endpoint de demo exige auth.** `POST /api/demo/load` usa o middleware
   `auth`; chamadas de teste sem `Bearer` caem em 401, não 403. O bloqueio de
   produção (403) só dispara **depois** do auth — teste-o com token válido.
