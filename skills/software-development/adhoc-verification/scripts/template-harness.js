'use strict';
// TEMPLATE for a focused ad-hoc verification harness.
// Copy to ./hermes-verify-<topic>.js next to your package, edit, run, delete.
// NO Jest globals here — plain node. Call setup/teardown helpers yourself.
process.env.NODE_ENV = 'test';
process.env.JWT_SECRET = 'test-secret-com-mais-de-32-caracteres-ok!!';

const request = require('supertest');
const jwt = require('jsonwebtoken');
// Adjust paths to your project layout:
const { setupDb, teardownDb, clearDb } = require('./tests/helpers/db');
const { createApp } = require('./src/app');

// Build an instance with a given env, then restore env so later instances
// aren't polluted.
function appCom(flags = {}) {
  const before = {};
  for (const k of Object.keys(flags)) before[k] = process.env[k];
  Object.assign(process.env, flags);
  const app = createApp();
  Object.assign(process.env, before);
  return app;
}

// Mint a cookie signed with a DIFFERENT secret (simulates a foreign instance).
function foreignCookie(secret = 'segredo-estranho-diferente-32+') {
  const t = jwt.sign({ id: '000000000000000000000000', role: 'user' }, secret,
    { expiresIn: '2h', algorithm: 'HS256' });
  return `token=${t}`;
}

let failures = 0;
const ok = (cond, msg) => {
  console.log((cond ? 'PASS' : 'FAIL') + ': ' + msg);
  if (!cond) failures++;
};

(async () => {
  await setupDb();
  try {
    // --- your checks here ---
    // const app = appCom({ SOME_FLAG: 'true' });
    // const r = await request(app).get('/some/path');
    // ok(r.status === 200, 'GET /some/path => 200');
  } catch (e) {
    console.error('ERROR IN HARNESS:', e);
    failures++;
  } finally {
    await teardownDb();
    console.log(failures === 0
      ? '\nAD-HOC: ALL CHECKS PASSED'
      : `\nAD-HOC: ${failures} FAILURE(S)`);
    process.exit(failures === 0 ? 0 : 1);
  }
})();
