# Reset do banco demo — projeto-profissional

Recipe validado para forçar reseed limpo do `app_demo_db` quando se muda model/
schema/seed (ex: adicionar `dificuldade`, `minutosFoco`, `responsavelId`,
`email`). O seed demo NÃO é idempotente: `insertMany` falha em `E11000
duplicate key` se já houver `users` com `demoN@example.com`.

## Sintoma de zumbi (lê antes de dropar)
Boot crasha com:
`MongoBulkWriteError: E11000 duplicate key error collection: app_demo_db.users
index: email_1 dup key: { email: "demo1@example.com" }`
Causa: um **node server de sessão anterior ainda vivo** (preso num
`containerd-shim-runc-v2` = DENTRO de um container Docker) reinserindo users no
mesmo banco. Dropar o banco sozinho não adianta — o zumbi reinsere.

## Passo a passo (reset limpo)
```bash
cd /home/pedro/Repositorios/templates/projeto-profissional

# 1) achar TODOS os node servers vivos
pgrep -af 'node src/server.js'

# 2) inspecionar o pai de um PID teimoso; se ppid = containerd-shim-runc-v2,
#    está dentro de um container (zumbi de outra sessão)
ps -o pid,ppid,cmd -p <PID>

# 3) matar SÓ o zumbi (kill -9 se necessário). NÃO mate servers de outros
#    projetos (financas-app, fa-app, sistema-academico) — estes usam outros
#    MONGO_URI (financas_db etc.). O alvo usa MONGO_URI=.../app_db e PORT=4450.
kill -9 <PID_zumbi>

# 4) confirmar que 4450 está livre
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:4450/   # esperado 000

# 5) dropar o banco demo (usar ID do container mongo, NUNCA o nome)
CID=3a0622a4098f
docker exec $CID mongosh --quiet --eval "db.getSiblingDB('app_demo_db').dropDatabase()"
# confirmar: docker exec $CID mongosh --quiet --eval "db.getSiblingDB('app_demo_db').users.countDocuments()" => 0

# 6) subir UM servidor (background) com o env correto
cd app
export MONGO_URI="mongodb://192.168.112.3:27017/app_db"
export PORT=4450
export NODE_ENV=development
export JWT_SECRET="dev-secret-projeto-profissional-local"
export SEED_PASSWORD="AdminDemo123!"
node src/server.js > /tmp/pp-server.log 2>&1 &
sleep 14
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:4450/demo/start   # 302 = ok
tail -3 /tmp/pp-server.log
```

## Verificar o seed
```bash
CID=3a0622a4098f
docker exec $CID mongosh --quiet --eval "
const d=db.getSiblingDB('app_demo_db');
print('users:', d.users.countDocuments());
print('tarefas:', d.tasks.countDocuments());
print('com dificuldade:', d.tasks.countDocuments({dificuldade:{\$exists:true,\$ne:null}}));
print('com minutosFoco>0:', d.tasks.countDocuments({minutosFoco:{\$gt:0}}));
print('metas:', d.metas.countDocuments());
"
```

## Gotchas de seed que quebraram o boot nesta sessão (e como evitar)
- **`ReferenceError: projIndice is not defined`** em `demoService.js`: o loop de
  tarefas usa `i`, não `projIndice`. Use `fib[(i + (i % fib.length)) % fib.length]`.
- **`Meta.insertMany is not a function`**: use `models.Meta ||
  require('mongoose').model('Meta')`, NUNCA `require('../models/meta.model')`
  (isso retorna o schema, não o model).
- **Campo `required` novo no model quebra o seed** (ver armadilha 7 da SKILL.md):
  defina o campo em `projDocs`/`profDocs`/`taskDocs` no `demoService.js`.
- **`escapeAttr is not defined`** nos `public/js/*.js`: só existe `escapeHtml`;
  nunca use `escapeAttr`.
