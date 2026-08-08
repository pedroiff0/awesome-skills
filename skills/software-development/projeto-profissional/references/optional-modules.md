# Módulos opcionais (domínios independentes na mesma app)

Quando Pedro diz que os domínios são **modulares** ("finanças não é obrigatório
para investimentos, são modulares, todos 3 principais"), ele quer que cada um
ligue/desligue sozinho — sem que um vire pré-requisito do outro. Não é só
esconder item de menu: a rota tem que sumir e o painel tem que continuar de pé.

Validado em `financas-app` com 3 módulos (financas, investimentos, veiculos),
provado por `tests/modulos.test.js`.

> O terceiro módulo nasceu como `moto` e foi depois ampliado para `veiculos`
> (carro + moto). Ao renomear/ampliar um módulo existente, siga a seção
> "Renomear ou ampliar um módulo" no fim deste arquivo — a flag é só um dos
> ~8 pontos de edição.

## A decisão central: flags por GETTER, guard por REQUEST

O instinto é montar as rotas condicionalmente no boot:

```js
// ❌ NÃO faça isso
if (env.modules.financas) router.use('/financas', require('./financas.routes'));
```

Funciona em produção, mas trava o teste: para cobrir as combinações você teria
que remontar o app, e `jest.resetModules()` cria um mongoose novo que perde a
conexão do `setupDb` — todo teste morre em timeout de 5s sem mensagem útil
(pitfall 36).

A forma que funciona nos dois mundos:

**1. `config/env.js` — getters, não valores congelados**

```js
modules: {
  get financas()      { return String(process.env.MODULE_FINANCAS      ?? 'true').toLowerCase() !== 'false'; },
  get investimentos() { return String(process.env.MODULE_INVESTIMENTOS ?? 'true').toLowerCase() !== 'false'; },
  get moto()          { return String(process.env.MODULE_MOTO          ?? 'true').toLowerCase() !== 'false'; },
  // sem toJSON, res.json() de um objeto só-getter sai {}
  toJSON() { return { financas: this.financas, investimentos: this.investimentos, moto: this.moto }; },
},
```

O default é **ligado**: `?? 'true'` + `!== 'false'` significa que só a string
literal `"false"` desliga. Env ausente nunca derruba um módulo por acidente.

**2. `routes/index.js` — middleware avaliado a cada request**

```js
const seModulo = (nome) => (req, res, next) => {
  if (!env.modules[nome]) return res.status(404).json({ error: 'Modulo desativado' });
  return next();
};

router.use('/financas',      seModulo('financas'),      require('./financas.routes'));
router.use('/investimentos', seModulo('investimentos'), require('./investimentos.routes'));
router.use('/moto',          seModulo('moto'),          require('./moto.routes'));

router.get('/modules', (req, res) => res.status(200).json({ modules: env.modules }));
```

404 (não 403): módulo desligado não deve nem revelar que a rota existiria.

**3. `pages.routes.js` — mesmo guard, senão sobra view órfã por URL direta**

```js
const paginaDeModulo = (modulo, rota, view) =>
  router.get(rota, pageAuth, requirePasswordChanged, (req, res, next) => {
    if (!env.modules[modulo]) return next();   // cai no notFoundHandler
    return res.render(view, { user: req.user });
  });
```

**4. Nav — `app.locals` uma vez, não por rota** (pitfall 19)

```js
app.locals.modules = env.modules;   // em app.js, junto de appName
```

```ejs
<% if (modules.financas) { %><a href="/lancamentos">Lançamentos</a><% } %>
<% if (modules.moto) { %><a href="/moto">Moto</a><% } %>
```

## Desacoplar o dashboard (a parte que mais dá trabalho)

Um dashboard escrito antes da modularidade quase sempre está acoplado: faz
`Promise.all` de tudo e soma patrimônio assumindo que contas e carteira existem.
Com finanças desligado ele quebra inteiro.

Regras:

- Move a rota para a raiz da API — `GET /api/dashboard` (pitfall 37).
- Cada bloco só é calculado se o módulo estiver ligado; devolva `null`/ausente
  em vez de objeto vazio, para a view distinguir "desligado" de "zerado".
- Agregados somam só o que existe:
  `(out.contas?.totalCents || 0) + (out.investimentos?.totals.totalMarketCents || 0)`.
- Devolva `modules` no payload — a view usa para decidir o que renderizar.
- No `.ejs`, envolva cada bloco em `<% if (modules.X) { %>`; no JS, teste
  `if (d.resumo)` / `if (d.moto)` antes de tocar em `getElementById`. Os dois
  lados: sem o `if` do EJS o HTML fica órfão, sem o `if` do JS dá TypeError.

## Teste que prova a independência

Com getters + guard por request, um único app cobre tudo:

```js
function ligar({ financas = true, investimentos = true, moto = true }) {
  process.env.MODULE_FINANCAS = String(financas);
  process.env.MODULE_INVESTIMENTOS = String(investimentos);
  process.env.MODULE_MOTO = String(moto);
}
afterEach(() => {                     // senão vaza para os outros arquivos
  delete process.env.MODULE_FINANCAS;
  delete process.env.MODULE_INVESTIMENTOS;
  delete process.env.MODULE_MOTO;
});
```

Casos que valem a pena (todos verdes em `financas-app`):

- cada módulo funcionando com os outros **desligados** (prova que não há
  pré-requisito escondido);
- dashboard 200 com finanças off, `resumo` undefined, demais blocos presentes;
- só um módulo ligado ⇒ `patrimonioCents === 0` sem estourar;
- página de módulo desligado ⇒ 404 por URL direta; volta a 200 ao religar;
- `/api/modules` refletindo exatamente as flags;
- tudo desligado ⇒ sobram auth, admin e dashboard.

## Checklist ao adicionar o módulo N+1

1. `MODULE_<NOME>` como getter em `config/env.js` (+ `toJSON`).
2. `seModulo('<nome>')` no `routes/index.js`.
3. `paginaDeModulo('<nome>', ...)` no `pages.routes.js`.
4. `<% if (modules.<nome>) %>` no header e no dashboard.
5. Bloco opcional no `relatorioService.dashboard()`.
6. Linhas novas em `tests/endpoints.test.js` e um caso em `tests/modulos.test.js`.
7. `.env.example` documentando a flag.

## Renomear ou ampliar um módulo (ex.: `moto` → `veiculos`)

Ampliar um domínio específico para o genérico que o contém (Moto → Veículos =
carro + moto) é **renomear em ~8 lugares + generalizar o modelo**, não só
trocar a flag. Sequência que funcionou:

1. **Leia o modelo genérico ANTES de escrever o service.** Nesta base o
   `vehicle.model.js`/`fuelLog.model.js`/`vehicleExpense.model.js` já podem ter
   sido criados por outra etapa (ou outro agente) com o campo já renomeado
   (`motorcycleId` → `vehicleId`) e enums maiores. Escrever o service a partir
   do modelo antigo gera queries que não casam com nada e retornam vazio sem
   erro.
2. **Renomeie a chave estrangeira em todo o service**: `motorcycleId` →
   `vehicleId`, `Motorcycle` → `Vehicle`, `MotoExpense` → `VehicleExpense`.
   Preserve a lógica linha a linha; o objetivo é diff de renomeação, não
   reescrita.
3. **Discriminador `type`** (`['carro','moto']`) no modelo pai. Os registros
   filhos (manutenção, abastecimento, gasto) **não carregam o tipo** — filtrar
   por `?type` exige resolver os ids antes:

   ```js
   async function idsPorTipo(userId, type) {
     const docs = await Vehicle.find({ userId, type }).select('_id').lean();
     return docs.map((d) => d._id);
   }
   // no filtro: else if (type) filtro.vehicleId = { $in: await idsPorTipo(userId, type) };
   ```
   Extraia isso num `filtroBase(userId, {vehicleId, type, from, to})` único em
   vez de repetir o mesmo bloco em três listagens (era duplicado no original).
4. **Enums crescem, não bifurcam.** Um enum comum com valores que só fazem
   sentido em um tipo (`corrente`/`relacao` só em moto; `arcondicionado`/
   `embreagem` só em carro; `flex`/`diesel` só em carro) é melhor que dois
   caminhos de validação. Comente no schema qual valor pertence a quê.
5. **A diferença que realmente importa é o combustível.** Carro flex alterna
   gasolina/etanol entre abastecimentos; somar litros dos dois produz um km/l
   que não descreve nenhum. Registre `fuel` **no abastecimento** (nunca
   `'flex'` — o tanque recebe um combustível por vez) e calcule
   `consumoPorCombustivel()` **por trecho** (pares consecutivos do mesmo
   veículo, só `fullTank`), agrupando pelo `fuel` do abastecimento que fechou o
   trecho. Mantenha `consumoMedio` geral para compatibilidade.
6. **Resumo de garagem mista precisa de quebra.** Um `totalCents` único para
   carro + moto é número sem dono: acrescente `porVeiculo`
   (`_id/nickname/type/totalCents`) e `porTipo` (`{carro, moto}`) via
   `$group: {_id: '$vehicleId'}` nas três coleções.

   **⚠️ O bug que essa quebra esconde: amplitude de odômetro só existe DENTRO
   de um veículo.** Um `$group: {_id: null, minOd: {$min}, maxOd: {$max}}` sobre
   a garagem inteira subtrai o hodômetro da moto (18.500) do hodômetro do carro
   (52.000) e devolve **34.410 km rodados e 237 km/l** — números inventados que
   passam despercebidos porque nenhum teste de módulo único os pega. Agrupe por
   veículo e some as amplitudes:

   ```js
   const distPorVeic = await FuelLog.aggregate([
     { $match: base },
     { $group: { _id: '$vehicleId', minOd: {$min:'$odometer'}, maxOd: {$max:'$odometer'}, qtd: {$sum:1} } },
   ]);
   const kmRodados = distPorVeic.filter((v) => v.qtd > 1)
     .reduce((s, v) => s + (v.maxOd - v.minOd), 0);
   ```

   O `qtd > 1` importa: com um único abastecimento a amplitude é 0 e não há
   distância medida.

   **O mesmo vício no consumo médio:** `kmRodados / litrosTotais` erra porque o
   **primeiro abastecimento de cada veículo entra no volume sem ter coberto
   distância medida**. Não recalcule — reaproveite o que `consumoPorCombustivel()`
   já somou por trecho, devolvendo `{ porCombustivel, geral }`. Devolva `geral`
   **fora** do mapa de combustíveis, senão a UI que faz `Object.entries()` para
   listar combustíveis renderiza uma linha `geral: 12.4` fingindo ser gasolina.

   Regra geral: **todo agregado derivado sobre uma coleção heterogênea precisa
   de um teste com DOIS registros de tipos/donos diferentes.** Um teste com um
   veículo só passa com a fórmula errada. O caso mínimo que trava a regressão:
   carro 52.000→52.400 (400 km) + moto 18.500→18.700 (200 km) ⇒
   `kmRodados === 600`, e `consumoMedio < 40`.
7. **Pontos de edição fora do trio service/controller/rotas** — todos já
   mordidos: `routes/index.js` (mount + `seModulo`), `config/env.js` (getter
   **e** `toJSON`), `pages.routes.js`, `relatorioService.dashboard()` (a chave
   do bloco no payload muda — a view/JS que lia `d.moto` quebra),
   `.env.example`, e a doc (`README`, `AGENTS.md`, `docs/operacao.md`).
8. **`git rm` os arquivos antigos** (service, controller, rotas, schemas,
   models) e faça um grep final por `motoService|motorcycleId|MODULE_MOTO`
   esperando zero hits em `src/`. Depois `node -e "require('./src/app').createApp()"`
   — o boot pega import órfão que o grep não pega.
9. **Os testes antigos vão falhar, e isso é o resultado esperado, não uma
   regressão.** `tests/modulos.test.js` seta `MODULE_MOTO` e espera
   `{...moto:true}`; `tests/moto.test.js` bate nas rotas velhas. Renomeie-os na
   mesma leva ou avise explicitamente quais falham e por quê — não relate
   "suíte quebrada" sem essa distinção.

### Trabalho concorrente com outro agente

Numa migração dessas outro agente pode estar mexendo nos mesmos arquivos. O
`patch` avisa (*"modified by sibling subagent … after this agent's last read"*)
e **rejeita o hunk inteiro do arquivo**, mas aplica os demais se você separar.
Reaja relendo só o arquivo tocado e reenviando o patch sem aquele hunk — foi
o caso do `pages.routes.js`, que o sibling já havia migrado corretamente.
