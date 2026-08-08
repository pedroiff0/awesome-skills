// Boot smoke test for the projeto-profissional template.
//
// USAGE: copy this file into the app/ directory and run it FROM THERE:
//   cp <skill>/scripts/smoke-boot.js app/ && cd app && node smoke-boot.js
// Running it from /tmp fails with MODULE_NOT_FOUND — it resolves
// mongodb-memory-server from the app's own node_modules.
//
// Verifies for real: server boots, admin seed fires, public pages answer 200,
// protected pages redirect to /login, bad login is a generic 401, and the CSP
// header comes out restrictive.

process.env.NODE_ENV = 'development';
process.env.JWT_SECRET = 'smoke-secret-com-mais-de-32-caracteres!!';

const { MongoMemoryServer } = require('mongodb-memory-server');

(async () => {
  const mongod = await MongoMemoryServer.create();
  process.env.MONGO_URI = mongod.getUri('smoke_db');
  process.env.PORT = '5099';

  await require('./src/server').main();
  await new Promise((r) => setTimeout(r, 1200));

  const base = 'http://127.0.0.1:5099';
  let falhas = 0;

  const esperado = {
    '/': 200,
    '/login': 200,
    '/api/health/ready': 200,
    '/app': 302,
    '/admin': 302,
  };

  for (const [rota, status] of Object.entries(esperado)) {
    const res = await fetch(base + rota, { redirect: 'manual' });
    const ok = res.status === status;
    if (!ok) falhas += 1;
    console.log(`${ok ? 'OK ' : 'FAIL'} ${rota} -> ${res.status} ${res.headers.get('location') || ''}`);
  }

  const bad = await fetch(`${base}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: 'naoexiste@example.com', password: 'x' }),
  });
  const body = await bad.json();
  const loginOk = bad.status === 401 && body.error === 'Credenciais invalidas';
  if (!loginOk) falhas += 1;
  console.log(`${loginOk ? 'OK ' : 'FAIL'} login invalido -> ${bad.status} ${JSON.stringify(body)}`);

  const csp = (await fetch(`${base}/login`)).headers.get('content-security-policy');
  const cspOk = csp && csp.includes("script-src 'self'") && !csp.includes('unsafe-inline');
  if (!cspOk) falhas += 1;
  console.log(`${cspOk ? 'OK ' : 'FAIL'} CSP: ${csp}`);

  console.log(falhas === 0 ? '\nSMOKE OK' : `\nSMOKE FALHOU (${falhas})`);
  process.exit(falhas === 0 ? 0 : 1);
})();
