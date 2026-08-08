# Cobertura de TODOS os endpoints (teste de inventário)

Quando Pedro pede "testes automatizados para cada endpoint", ele não quer só
mais testes de regra de negócio — quer garantia de que **nenhuma rota ficou
registrada sem cobertura**. O padrão barato e eficaz é um arquivo de inventário
usando `it.each`.

Validado em `financas-app`: `tests/endpoints.test.js`, 82 verificações sobre
~44 rotas, verde junto com os testes de domínio (177 no total).

## Por que inventário e não só testes de domínio

Teste de domínio prova que a rota que você lembrou funciona. Inventário prova
que a rota que você **esqueceu** existe — pega rota não registrada em
`routes/index.js`, guard de auth faltando e método errado (PUT vs POST). É o
teste que denuncia o endpoint novo sem cobertura.

## Estrutura

```js
/* Cada entrada: método, caminho, statuses aceitáveis numa chamada
   AUTENTICADA com corpo vazio. O ponto não é validar a regra de negócio —
   é provar que a rota está montada (nada de 404) e que o guard responde. */
const ENDPOINTS = [
  ['get',  '/api/health',              [200]],
  ['get',  '/api/modules',             [200]],
  ['get',  '/api/dashboard',           [200]],
  ['post', '/api/auth/login',          [401, 422, 429]],
  ['get',  '/api/admin/users',         [403]],   // user comum: 403 prova rota + guard
  ['get',  '/api/financas/contas',     [200]],
  ['post', '/api/financas/contas',     [422]],   // corpo vazio ⇒ Zod
  ['put',  '/api/financas/orcamentos', [422]],   // upsert é PUT, não POST
  // ...
];

describe('inventario de endpoints — todos respondem (nenhum 404 de rota)', () => {
  it.each(ENDPOINTS)('%s %s', async (metodo, caminho, esperados) => {
    const res = await request(app)[metodo](caminho).set(auth()).send({});
    expect(res.status).not.toBe(404);
    expect(esperados).toContain(res.status);
  });
});

describe('toda rota /api (exceto publicas) exige autenticacao', () => {
  const PUBLICAS = new Set([
    '/api/health', '/api/modules',
    '/api/auth/login', '/api/auth/logout',
    '/api/auth/forgot-password', '/api/auth/reset-password',
  ]);
  it.each(ENDPOINTS.filter(([, c]) => !PUBLICAS.has(c)))(
    '%s %s sem token',
    async (metodo, caminho) => {
      expect((await request(app)[metodo](caminho).send({})).status).toBe(401);
    }
  );
});
```

## Regras que fazem o inventário valer alguma coisa

- **`expect(res.status).not.toBe(404)` é a asserção principal.** Rota
  inexistente é o defeito que se quer pegar; a lista de statuses aceitáveis é o
  complemento.
- **Aceite uma LISTA de statuses, não um só.** Rotas de auth variam com rate
  limit (401/422/429). Fixar um valor gera teste intermitente.
- **Statuses são deste template: 422 para validação Zod, não 400** (pitfall 33).
  Confirme com uma chamada real antes de escrever a bateria inteira.
- **403 em rota de admin é sucesso**, não falha: prova que a rota existe E que o
  `requireRole` funciona. Não precisa de token de admin no inventário.
- **CUIDADO: em rota de admin o inventário fica CEGO para caminho errado.** O
  `requireRole` responde 403 **antes** de o Express decidir que a rota não
  existe, então `/api/admin/usuarios` (que não existe; o certo é `/users`)
  devolve 403 e passa nos dois asserts — o `not.toBe(404)` e o
  `toContain(403)`. O teste fica verde testando um caminho inexistente. Isso
  passou despercebido até um `curl` real na criação de usuário devolver 404.
  Para as rotas de admin, **copie o caminho do `admin.routes.js`** em vez de
  digitar de memória, e confirme com uma chamada autenticada como admin
  (deve dar 2xx/422, nunca 404). Vale para qualquer prefixo cujo guard
  responda antes do roteamento.
- **Derive a lista das rotas de verdade** (leia os `*.routes.js`), não da
  memória. Foi assim que apareceu o `PUT /orcamentos` (pitfall 38).
- **Rode com `--forceExit`** (pitfall 35).

## Cobertura por módulo de domínio (o complemento)

O inventário é raso de propósito. Cada módulo ainda precisa do seu arquivo com
os casos que importam — no `moto.test.js` (38 testes) o conjunto que valeu foi:

- CRUD completo de cada entidade, incluindo o 404 pós-DELETE;
- **isolamento entre usuários**: com token de outro usuário, todo GET/PATCH/
  DELETE por id deve dar 404 (não 403 — não revelar existência);
- **valores derivados calculados no servidor**: mandar `totalCents: 1` num
  abastecimento e provar que o servidor recomputa `litros × preço`;
- **regra de negócio nas bordas**: primeiro registro sem consumo (não há
  anterior), tanque parcial não gera km/l, custo/km exige 2+ abastecimentos;
- **guard de integridade**: excluir entidade-pai com histórico ⇒ 422 "arquive
  em vez de excluir";
- enum inválido e campo curto ⇒ 422.

Padrão de fixture que evita o pitfall 34: dois usuários no `beforeEach`
(`dono@` e `intruso@`), helpers que devolvem `res.body.<entidade>`, e strings
com 2+ caracteres em todo campo `.min(2)`.
