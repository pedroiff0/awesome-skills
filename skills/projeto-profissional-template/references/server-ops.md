# Operação do servidor — projeto-profissional

Comandos exatos usados e validados neste projeto. O servidor roda localmente
apontando para o Mongo em container Docker.

## 1. Identificar o servidor do projeto (NÃO matar os de outros projetos)

Outros projetos (financas-app etc.) também rodam `node src/server.js`. O do
projeto-profissional usa `MONGO_URI` apontando para `app_db`.

```bash
# lista PIDs e o MONGO_URI de cada um
for p in $(pgrep -f 'node src/server.js'); do
  echo "PID $p: $(tr '\0' ' ' < /proc/$p/environ 2>/dev/null | grep -oE 'MONGO_URI=[^ ]*' | head -1) PORT=$(tr '\0' ' ' < /proc/$p/environ 2>/dev/null | grep -oE 'PORT=[^ ]*' | head -1)"
done
```

O alvo tem `MONGO_URI=mongodb://192.168.112.3:27017/app_db` e `PORT=4450`.
Matar só ele: `kill <pid>`. (Os outros têm `financas_db` etc. — ignorar.)

## 2. Dropar o banco demo (forçar reseed no boot)

```bash
# achar o container mongo do projeto (nome muda; usar o ID do `docker ps`)
docker ps --format '{{.Names}}\t{{.ID}}' | grep -i mongo
CID=3a0622a4098f   # substituir pelo ID atual

# NOTA: `docker exec <nome>` pode dar "No such container"; usar o ID funciona.
docker exec $CID mongosh --quiet --eval "db.getSiblingDB('app_demo_db').dropDatabase()"
```

Bancos: `app_db` (prod), `app_test_db` (teste), `app_demo_db` (demo). O demo é
o que se reseeda.

## 3. Subir o servidor com o env correto

```bash
cd /home/pedro/Repositorios/templates/projeto-profissional/app
export MONGO_URI="mongodb://192.168.112.3:27017/app_db"
export PORT=4450
export NODE_ENV=development
export JWT_SECRET="${JWT_SECRET:-dev-secret-projeto-profissional-local}"
export APP_BASE_URL="http://localhost:4450"
export COOKIE_SECURE="false"
nohup node src/server.js > /tmp/pp-server.log 2>&1 &
sleep 6 && tail -25 /tmp/pp-server.log
```

O boot re-seeda o demo (3000 tarefas etc.) e abre a porta 4450. Verificar:
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4450/demo/start   # esperado 302
```

## 4. Contar dados no demo (via mongosh no container)

```bash
docker exec $CID mongosh --quiet --eval "
const d=db.getSiblingDB('app_demo_db');
print('tarefas:', d.tasks.countDocuments());
print('projetos:', d.projects.countDocuments());
print('profissionais:', d.professionals.countDocuments());
print('usuarios demo:', d.users.countDocuments({email:/@example.com\$/}));
"
```

## 5. Rodar a suíte de testes

```bash
cd app
export NODE_ENV=test
export JWT_SECRET='test-secret-com-mais-de-32-caracteres-ok!!'
node node_modules/.bin/jest --runInBand --forceExit 2>&1 | tail -40
```

Primeira execução baixa o binário do mongodb-memory-server (rede). ~78 testes;
esperado tudo verde após os ajustes de schema/teste.
