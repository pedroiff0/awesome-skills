# Acesso e operação das duas stacks

Pedro pergunta isto sempre que um projeto derivado sobe: **"como faço o acesso
ao app de testes e produção?"**. Responder bem exige checar o estado real, não
recitar o `.env.example` — as duas stacks têm bancos e admins independentes.

Todo projeto derivado deve ganhar um `docs/operacao.md` cobrindo: as duas
stacks, criação de usuário, reset de senha, módulos, backup e exposição na
rede. Não deixe isso só no README.

## Antes de responder, confirme o que está no ar

O erro clássico é informar credenciais do banco errado. Um stack pode ter
subido com override de demo e continuar assim horas depois:

```bash
docker inspect <proj>-app-1 --format '{{range .Config.Env}}{{println .}}{{end}}' \
  | grep -E 'MONGO_URI|NODE_ENV|ADMIN_EMAIL'
docker compose -p <proj> exec -T mongo mongosh --quiet \
  --eval 'db.adminCommand("listDatabases").databases.forEach(d=>print(d.name))'
```

Aconteceu de verdade: a porta de produção estava servindo `financas_demo`
(sobra do override do pitfall 23) enquanto o `financas_db` real estava vazio.
Voltar para produção é subir **sem** o `-f /tmp/*-demo.override.yml`:
`docker compose -p <proj> up -d --force-recreate app`.

Depois confirme os usuários que existem de fato:

```bash
docker compose -p <proj> exec -T mongo mongosh <db> --quiet \
  --eval 'db.users.find({},{email:1,role:1,isActive:1,mustChangePassword:1,failedLoginAttempts:1,_id:0}).forEach(u=>printjson(u))'
```

## `ADMIN_PASSWORD` vazio ⇒ nenhum admin utilizável

O compose traz `ADMIN_PASSWORD: ${ADMIN_PASSWORD:-}`. Com `.env` sem essa
chave, o seed não deixa uma senha que você conheça — e como **o seed não
recria usuário existente**, trocar a variável depois não adianta nada. Ou você
define antes do primeiro boot, ou usa o reset abaixo.

## Reset de senha (a ferramenta que faltava)

`templates/reset-senha.js` → copie para `<repo>/app/scripts/reset-senha.js`.

```bash
docker compose -p <proj> exec -T app node scripts/reset-senha.js admin@example.com
```

Redefine a senha, limpa `failedLoginAttempts`/`lockUntil`/token de reset, e
imprime a senha gerada uma única vez.

**Pitfall:** o container tem rootfs read-only (`no-new-privileges`, read-only
container do baseline), então `docker compose cp` falha com *"container rootfs
is marked read-only"*. O script tem que entrar na **imagem**:
`docker compose -p <proj> up -d --build app`.

## Criar usuário por API

O caminho é `/api/admin/users` (**não** `/usuarios`). A resposta traz
`senhaTemporaria` uma única vez e o usuário nasce com `mustChangePassword`.

```bash
TOKEN=$(curl -s -X POST http://localhost:<porta>/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@example.com","password":"..."}' | jq -r .token)

curl -s -X POST http://localhost:<porta>/api/admin/users \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name":"Fulano","email":"fulano@exemplo.com","role":"user"}'
```

## O 429 ao final de uma sessão de verificação é esperado

Depois de testar login várias vezes, produção passa a responder **429** — são
os `RATE_LIMIT_AUTH_MAX=3 / 30 min` do baseline, não senha errada. Distinga
antes de alarmar o Pedro (ou de "consertar" o que não está quebrado):

- `failedLoginAttempts: 0` no Mongo ⇒ nenhuma senha errada chegou; é só a
  janela do limiter por IP.
- Para destravar: aguardar a janela ou `docker compose -p <proj> restart app`
  (o contador do express-rate-limit vive em memória).
- Martele login na stack de **teste**, onde `RATE_LIMIT_DISABLED=true` — é
  exatamente para isso que ela existe.

## Verificação ad-hoc de script operacional

Script que mexe em credencial merece prova, e ela **não cabe no Jest** (precisa
de container + banco reais). Rode contra a stack de teste, nunca produção, e
rotule como ad-hoc. O que fez diferença:

- provar os **dois lados**: a senha nova loga (200) **e** a antiga passa a
  falhar (401). Só checar o 200 não prova que trocou.
- casos de erro: usuário inexistente e uso sem argumento ⇒ exit 1.
- **restaurar o estado** no fim (voltar a senha original da stack de teste).
- `trap`/limpeza e remover o script de `/tmp` ao terminar.
