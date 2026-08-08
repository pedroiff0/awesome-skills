# Domínio financeiro e gráficos sob CSP

Notas destiladas ao construir `financas-app` (derivado do template). Valem para
qualquer app do Pedro que lide com dinheiro, séries mensais ou dashboards —
não só para aquele projeto.

## Regra número um: dinheiro em CENTAVOS inteiros

Todo campo monetário é `Number` inteiro em centavos, no banco, no Zod, no
service e na API. Float só existe na apresentação.

- Zod: `z.coerce.number().int()`, nunca `z.number()` solto.
- Conversão de entrada: `Math.round(Number(txt.replace(',', '.')) * 100)` —
  sem o `Math.round`, `19.99 * 100 === 1998.9999999999998`.
- Saída: `Intl.NumberFormat('pt-BR', {style:'currency',currency:moeda})
  .format(cents / 100)`.
- Quantidade de ativo é a única exceção: cripto/ETF fracionário exigem
  `Number` real. O dinheiro ao lado continua inteiro.

## Nunca persista o que dá para derivar

Saldo de conta e posição de carteira são **calculados**, não colunas mutáveis:

- Saldo = `openingBalanceCents` + receitas + transferências recebidas −
  (despesas + transferências enviadas), filtrando `paid: true`.
- Posição = redução da sequência de trades ordenada por data.

Por quê: um lançamento corrigido recalcula tudo sozinho, sem migração e sem
divergência entre extrato e total. O custo é uma agregação; resolva o N+1 com
UM `$facet` que traz entradas, saídas e transferências de todas as contas de
uma vez.

## Preço médio ponderado (regra da Receita, e a que Ghostfolio/Maybe usam)

- **Compra** dilui o médio; taxas entram no custo.
- **Venda** realiza lucro contra o médio corrente e **não altera** o médio das
  cotas restantes. Baixa o custo proporcionalmente.
- Posição zerada ⇒ zere `costCents` também, senão o próximo aporte herda lixo.
- **Ordene por data antes de reduzir.** Um trade inserido fora de ordem
  (backfill) distorce o médio silenciosamente. Há teste para isso — mantenha.
- Custódia é **por corretora**: a mesma ação em duas corretoras são duas
  posições. Venda a descoberto é bloqueada comparando com a posição *daquela*
  corretora, não com a global.
- Provento não mexe em quantidade; acumula num campo próprio.

## Competência mensal: `YYYY-MM` em UTC

`month` como string `YYYY-MM` é comparável, indexável e imune a fuso. Toda a
aritmética de mês em `Date.UTC`: usar horário local faz o dia 1 cair no mês
anterior em UTC-3.

- Intervalo **semiaberto** `[início, fim)` — com `$lte` você perde ou duplica
  lançamentos de 23:59.
- O `$dateToString` da agregação precisa de `timezone: 'UTC'` para o rótulo
  bater com o intervalo do resumo; sem isso um mês some do gráfico.
- Dia 31 em fevereiro: `Math.min(dia, ultimoDiaDoMes)`, senão o `Date` rola
  para março e a recorrência pula uma competência.
- Formatar data vinda da API: fatie a string (`iso.slice(0,10).split('-')`),
  não construa `Date` — senão o dia 1 aparece como dia 30.

## Recorrências: guarde o molde, materialize sob demanda

Não gere 120 lançamentos futuros. Guarde a recorrência e crie o lançamento do
mês quando pedirem, com `paid:false` (conta a pagar). Idempotência vem de um
índice único parcial `(recurrenceId, date)` — a geração engole `E11000` de
propósito, então rodar duas vezes no mesmo mês não duplica.

## Isolamento por usuário é responsabilidade do service

O `userId` vem SEMPRE de `req.user`, nunca do corpo. E não basta filtrar a
query principal: valide que `accountId`/`categoryId`/`brokerId` recebidos
**pertencem ao usuário**, senão um ObjectId válido de outro usuário passa pelo
Zod e vaza dado. Teste isso explicitamente (crie dois usuários na suíte).

## Gráficos: SVG à mão, porque a CSP proíbe CDN e inline

Nada de Chart.js via CDN (`script-src 'self'`) e nada de `<script>` inline.
Um `financas-lib.js` com ~150 linhas cobre barras agrupadas, rosca e barra de
progresso. Detalhes que custaram tempo:

- SVG montado por string ⇒ **todo texto passa por `escapeHtml`**, inclusive
  dentro de `<title>` e de atributos `fill`.
- Rosca com **um único item de 100%** não renderiza: o arco `A` de 360° tem
  ponto inicial igual ao final. Trate esse caso com `<circle>` + `stroke`.
- `<title>` dentro do `<path>` dá tooltip nativo, sem JS.
- Divisão por zero vira `NaN` na view: `limite > 0 ? ... : 0`.
- Carregue a lib compartilhada no `footer.ejs`, antes do `pageScript`.

## Um endpoint de dashboard, não seis

`GET /api/<dominio>/dashboard?month=&months=` devolve resumo, série, saldos,
orçamentos, metas e carteira num `Promise.all`. Uma request, um estado
consistente, e a página não pisca em cascata.
