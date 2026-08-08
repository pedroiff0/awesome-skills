// Template de verificação ad-hoc de um SERVICE desta base, contra Mongo em
// memória. Use quando o prompt pedir evidência e a suíte Jest ainda não cobre
// o código novo (ex.: domínio recém-migrado, testes antigos ainda no nome
// velho). NÃO substitui `npm test` — rotule o resultado como ad-hoc.
//
// Uso:
//   V=$(mktemp /tmp/hermes-verify-XXXXXX.js)
//   # escreva este conteúdo em $V, ajuste a seção CENÁRIO
//   cd <repo>/app && node $V        # cwd em app/ é obrigatório (pitfall 31)
//   rm -f $V
//
// Armadilhas já embutidas aqui:
//   - `path` absoluto + require() a partir de app/node_modules (pitfall 31).
//   - AppError expõe `statusCode`, NÃO `status` (pitfall 41).
//   - NODE_ENV=test antes de qualquer require (desliga limiters).
//   - acumula PASS numa lista e imprime no fim: falha morre no 1º assert,
//     então o que já passou fica visível e o diagnóstico é imediato.

process.env.NODE_ENV = 'test';

const path = '/home/pedro/Repositorios/pessoal/<PROJETO>/app/';
const mongoose = require(path + 'node_modules/mongoose');
const { MongoMemoryServer } = require(path + 'node_modules/mongodb-memory-server');
const assert = require('assert');

const svc = require(path + 'src/services/<NOME>Service');
const s = require(path + 'src/schemas/<NOME>.schemas');

// Erro esperado do domínio: sempre statusCode, nunca status.
const comStatus = (code) => (e) => e.statusCode === code;

(async () => {
  const mem = await MongoMemoryServer.create();
  await mongoose.connect(mem.getUri());
  const uid = new mongoose.Types.ObjectId();
  const ok = [];

  /* ---------------- CENÁRIO (substitua) ---------------- */

  // 1. Schemas: parse feliz + rejeição explícita do valor inválido.
  const dto = s.criarXSchema.parse({ /* ... */ });
  assert.throws(() => s.criarXSchema.parse({ /* inválido */ }));
  ok.push('schemas: parse ok e valor inválido rejeitado');

  // 2. CRUD + invariantes de unicidade.
  const doc = await svc.criarX(uid, dto);
  await assert.rejects(() => svc.criarX(uid, dto), comStatus(409));
  ok.push('criar: duplicado -> 409');

  // 3. ESCOPO POR USUÁRIO — nunca omita: é a falha de segurança mais cara.
  await assert.rejects(
    () => svc.obterX(new mongoose.Types.ObjectId(), doc._id),
    comStatus(404)
  );
  ok.push('escopo: recurso de outro user -> 404');

  // 4. Valores derivados (regra arquitetural 10: nunca guardados).
  //    Confira o número REFAZENDO a conta a partir das fixtures, à mão.
  // assert.strictEqual(x.totalCents, 10 * 500);
  // ok.push('derivado: totalCents = litros x preco');

  // 5. Agregados: some as fixtures manualmente antes de comparar.
  // const esperado = /* soma explícita */;
  // assert.strictEqual((await svc.resumo(uid)).totalCents, esperado);

  // 6. Delete com/sem histórico, se o domínio tiver esse guard.
  // await assert.rejects(() => svc.removerX(uid, doc._id), comStatus(422));

  /* ---------------- fim do CENÁRIO ---------------- */

  console.log(ok.map((l, i) => `  ${i + 1}. PASS ${l}`).join('\n'));
  console.log(`\n${ok.length}/${ok.length} verificacoes ad-hoc passaram`);

  await mongoose.disconnect();
  await mem.stop();
})().catch((e) => {
  console.error('FALHOU:', e);
  process.exit(1);
});
