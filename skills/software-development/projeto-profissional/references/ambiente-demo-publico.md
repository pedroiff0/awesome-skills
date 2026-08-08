# Terceiro ambiente: demonstração pública (produção / teste / demo)

O template nasce com duas stacks (produção + teste). Quando Pedro pedir "um
botão de demo na landing" ou "três bancos de dados", a resposta é uma **terceira
stack isolada**, não um usuário de demonstração dentro da produção.

## O quadro completo

| | Produção | Teste / carga | **Demo** |
|---|---|---|---|
| Arquivo | `docker-compose.yml` | `docker-compose.test.yml` | `docker-compose.demo.yml` |
| Projeto | `-p fa` | `-p fa-test` | `-p fa-demo` |
| Banco | `financas_db` (volume) | `financas_test_db` (tmpfs) | `financas_demo_db` (**tmpfs**) |
| Porta | 4450 | 4451 | 4452 |
| `NODE_ENV` | `production` | `staging` | `staging` |
| Rate limit | ativo | desligado | **desligado** |
| Credencial | privada | previsível (k6) | **publicada na landing** |
| Semeadura | vazia | admin + demo | `SEED_DEMO=true` no boot |

Por que a demo é `staging` e não `production`: `config/env.js` recusa
`RATE_LIMIT_DISABLED=true` sob `production` (guard existente), e uma demo
apresentada para várias pessoas ao mesmo tempo não pode cair no limiter de
3 tentativas.

Por que **tmpfs**: é a única das três que se assume pública. Derrubou a stack,
os dados somem — não há o que vazar, e não existe backup a proteger. Isso é
argumento de segurança, não economia.

## Semear no boot, com a trava dentro do seed

```js
// src/server.js, depois de seedAdminIfEmpty()
if (process.env.SEED_DEMO === 'true') {
  try {
    await require('./seeds/demo.seed').semearDemo();
  } catch (err) {
    console.error('Falha ao semear a demo:', err.message);
  }
}
```

A lógica vive em `src/seeds/demo.seed.js` (exporta `semearDemo()`); o
`scripts/seed-demo.js` vira um wrapper fino que só conecta e chama. Duplicar os
dados nos dois arquivos garante que um fica desatualizado.

**A trava por nome de banco tem de ser dupla** (pitfall 26 do SKILL.md):

- No módulo: `if (!/test|demo/i.test(process.env.MONGO_URI)) throw new Error('Recusado: ...')`
- No script CLI: a mesma checagem **antes do `mongoose.connect`**.

Motivo: o script conectava primeiro e validava depois, então apontá-lo para
produção falhava com `ECONNREFUSED` em vez da mensagem `Recusado:`. O teste
existente em `tests/config.test.js` casa com `/Recusado/` e passou a reprovar —
o refactor quebrou a evidência de segurança sem quebrar a segurança. Valide
antes de qualquer I/O.

## Escrever o seed: confira os campos reais do model ANTES

Um seed longo escrito "de cabeça" falha um campo por vez, um boot por erro.
Nesta base os nomes que o instinto erra:

| Instinto | Real |
|---|---|
| `Transaction.type: 'despesa'` | **`kind`** |
| `Transaction.fixed: true` | **`nature: 'fixa'`** |
| `Trade.kind: 'compra'` | **`side`** |
| `Asset.kind` / `currentPriceCents` | **`class`** / **`lastPriceCents'** |
| `Account.type: 'outro'` | enum é `corrente\|poupanca\|carteira\|cartao\|investimento` |

Receita para não descobrir de um em um:

```bash
for m in transaction budget goal vehicle asset trade account; do
  echo "=== $m"; grep -oE "^    [a-zA-Z]+:" src/models/$m.model.js | tr -d ' :' | tr '\n' ' '; echo
done
grep -n "enum" src/models/*.model.js
```

Rode isso **uma vez** antes de escrever o seed e ajuste tudo de uma vez.

## Dados que valem a pena semear

Painel vazio é a pior primeira impressão, e 6 meses ainda parecem teste. Mire em
**12 meses fechados**:

- Lançamentos mensais recorrentes (aluguel, salário, assinaturas) com
  `nature: 'fixa'`, mais variáveis que oscilam.
- **Variação determinística**, não aleatória:
  `const oscila = (base, mes, amp) => Math.round(base * (1 + amp * Math.sin(mes * 1.7)))`.
  Com `Math.random()` a landing anuncia um número diferente a cada reinício.
- Eventos esporádicos (`if (m === 6)` dentista, `if (m === 9)` viagem) — sem
  eles todo mês fica idêntico e o gráfico vira uma reta.
- Orçamentos no mês corrente, metas com progresso parcial, operações de compra
  **e** venda **e** provento, carro + moto com odômetro coerente.

## A landing anuncia números lidos do banco

Nunca digite a contagem no HTML: ela envelhece no primeiro `seed` alterado.

`src/services/landingService.js` → `statsDaDemo()`:

- Conta `Transaction`/`Account`/`Category`/`Budget`/`Goal`/`Trade`/`Vehicle` do
  usuário de demo, mais `$min`/`$max` de `date` para derivar os meses cobertos.
- **Cache de 5 minutos** — a landing é a página mais visitada e esses números
  mudam uma vez por deploy.
- **Nunca deixa a página cair**: se `mongoose.connection.readyState !== 1`, se o
  usuário de demo não existir, ou se a query estourar, devolve `null` e a view
  usa um bloco de fallback. A landing é pública; ela não pode dar 500 porque uma
  contagem falhou.

Na view: `<% if (stats) { %> ... <% } else { %> ...fallback... <% } %>`.

O botão aponta para a própria instância quando ela **é** a demo, e para a URL
externa quando não é:

```ejs
<a href="<%= demo.local ? '/login' : (demo.url || '/login') %>">Ver demonstração</a>
```

com `demo.local = process.env.SEED_DEMO === 'true'`.

Testes que valem (`tests/landing.test.js`): fala de finanças e **não** fala do
template genérico; mostra a credencial; não quebra com base vazia; anuncia os
números reais quando semeada; o seed recusa banco de produção.

## O visitante é usuário COMUM, e entra sozinho

Dois erros que andam juntos numa demo recém-criada: fazer o visitante `admin`
(porque o seed padrão do template cria admin) e pedir que ele digite uma senha
que está impressa na landing logo acima do botão.

**Papel.** `role: 'user'` no seed. Os guards já existem
(`requirePageRole('admin')` na página, `requireRole` na API), então o papel é a
única coisa que precisa mudar — não escreva guard novo. O admin da instância de
demo vira uma conta separada e **não divulgada** (`dono-da-demo@...`), só para a
base não nascer sem dono:

```yaml
ADMIN_EMAIL: dono-da-demo@financas.local        # nao divulgado
ADMIN_PASSWORD: ${DEMO_ADMIN_PASSWORD:-...}
DEMO_EMAIL: ${DEMO_EMAIL:-demo@financas.app}    # publicado, role user
DEMO_AUTOLOGIN: "true"
```

**Autologin.** `src/middleware/demoAutologin.js` emite um JWT de verdade pelo
mesmo caminho do login normal — não é bypass, é login programático para uma
conta de dados fictícios. Duas travas no registro:

```js
// app.js, DEPOIS de app.use('/api', apiRoutes)
if (process.env.DEMO_AUTOLOGIN === 'true' && env.nodeEnv !== 'production') {
  const { demoAutologin } = require('./middleware/demoAutologin');
  app.use(/^(?!\/$).*/, demoAutologin);   // tudo MENOS a raiz
}
```

Em qualquer outra instalação o middleware **nem entra na cadeia** — não existe
caminho de código que autentique sem senha. O teste que mais importa é o
negativo: sem a flag, `GET /app` não pode devolver 200 nem `set-cookie`.

### A armadilha: autologin na raiz mata a landing

Aplicado também em `/`, o middleware autentica o visitante **antes** de a rota
da landing rodar. Ela vê `req.user` e redireciona para `/app` — a página que
explica o produto fica inalcançável justamente na instância de demonstração.
Sintoma: `curl /` devolve 302 para `/app` e nenhum teste unitário acusa, porque
cada rota isolada passa. Daí o `/^(?!\/$).*/` acima, com teste de regressão
fixando `GET /` → 200.

### Extraia as opções do cookie antes de ter dois emissores

O autologin precisa emitir **o mesmo** cookie do login. Copiar
`httpOnly/sameSite/secure/maxAge` na mão é como se perde o `httpOnly` num dos
dois — e aí o token vira leitura de XSS. Mova para `src/utils/authCookie.js`
(`COOKIE_NAME`, `COOKIE_OPTIONS`, `setAuthCookie`, `clearAuthCookie`) e faça o
`auth.controller.js` importar de lá.

### Texto da landing muda quando há autologin

Com autologin ligado, anunciar "e-mail / senha" é burocracia inútil. A view
condiciona: `demo.autologin ? '/app' : '/login'` no botão, e a nota vira
"Entra direto, sem senha". Passe `autologin: process.env.DEMO_AUTOLOGIN === 'true'`
junto de `demo.local` na rota.

### Verificando: 401 e 403 não são intercambiáveis

Um script ad-hoc que faz `curl /api/admin/users` **sem cookie** recebe **401**
(não autenticado), não 403. Para provar que o visitante é *autenticado porém
barrado* — que é a afirmação que interessa — capture a sessão do autologin
primeiro:

```bash
curl -s -c /tmp/demo.jar -o /dev/null http://host:4452/app   # autologin grava o cookie
curl -s -b /tmp/demo.jar -o /dev/null -w '%{http_code}\n' http://host:4452/api/admin/users  # 403
```

E `GET /login` devolvendo **302** na instância de demo é o comportamento certo
(já logado ⇒ vai para `/app`), não uma falha. Expectativa errada no script de
verificação, não bug — o padrão de sempre nesta base.

## Reordenar portas entre ambientes

Pedro pode pedir uma numeração diferente da que existe (ele pediu
4450=produção quando 4450 era o teste). Antes de mexer:

1. **Backup primeiro** (`./scripts/backup.sh`) — a troca envolve `down` da stack
   que tem os dados reais.
2. Avise a inversão e ofereça as opções; se ele não responder, siga o que ele
   escreveu explicitamente (foi o pedido literal) e diga no relatório.
3. `down` das duas stacks antes de subir na numeração nova — senão a porta
   ainda está tomada pela stack antiga.
4. Pitfall 13 continua valendo: porta aparece em compose, `.env.example`,
   `config/env.js`, k6, docs e README.

## Reescrever a landing herdada para o domínio real

A landing do template vende o **template** ("a base sólida que todo projeto
deveria ter", "214 requisições por segundo"). Num projeto derivado isso é texto
errado e, pior, métrica não medida naquele app (pitfall: nunca publique número
que você não mediu).

Troque por blocos verdadeiros do domínio. No app de finanças, a seção de
desempenho virou **"As contas"** — valores em centavos inteiros, saldo e preço
médio derivados, média por combustível, exportação PDF/CSV. É verificável e é o
diferencial real.

**Ao renomear uma seção, o `id` muda e as âncoras do rodapé quebram.** Varra:

```js
const ancoras = new Set([...html.matchAll(/href="#([\w-]+)"/g)].map(m => m[1]));
const ids     = new Set([...html.matchAll(/id="([\w-]+)"/g)].map(m => m[1]));
console.log('quebradas:', [...ancoras].filter(a => !ids.has(a)));
```

Deve sair vazio antes do commit.
