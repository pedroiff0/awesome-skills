# Deploy da demo + banco (financas-app)

## Comandos de rebuild (OBRIGATÓRIO --no-cache)
```bash
cd /home/pedro/Repositorios/pessoal/financas-app
ASSET_VERSION=N docker compose -p fa build --no-cache app app-demo \
  && ASSET_VERSION=N docker compose -p fa up -d app app-demo
```
Sem `--no-cache` a camada COPY do CSS/JS fica em cache e a mudança não aparece.
Bump de ASSET_VERSION evita cache do navegador.

## Inspecionar o banco da demo
O app-demo usa `MONGO_URI=mongodb://mongo-demo:27017/financas_demo_db`.
ATENÇÃO ao sufixo `_db`: consultar `financas_demo` (sem _db) retorna vazio e
engana ("usuário não existe"). Use o nome correto:
```bash
docker compose -p fa exec mongo-demo mongosh --quiet financas_demo_db \
  --eval 'db.users.find({email:"demo@financas.app"},{email:1,tokenValidAfter:1}).toArray()'
```
O usuário demo deve ter `tokenValidAfter: null` (correção da causa raiz de
token inválido ao nascer).

## Reset da demo
`POST /api/reset-demo` (só na instância demo, DEMO_AUTOLOGIN=true). Usa
`authOptional` (não barra token inválido). Recria o usuário demo + 428
lançamentos/18 meses/etc. Se o endpoint 404 em `/demo/api/reset-demo`, chamar
`/api/reset-demo` (o app principal também o monta, mas semeará o banco
PRINCIPAL, não o demo — confira o alvo). O seed também roda no boot
(server.js chama semearDemo() quando DEMO_AUTOLOGIN=true).

## Bug #34 (em aberto)
`/demo/*` redireciona para `/app` (app principal) com "Token inválido".
Pré-existente, ligado a `demoAutologin`/`pageAuth`. Suspeita: o `pageAuth`
valida o token do cookie (que pode ser do app principal) e falha, embora o
`demoAutologin` gere token fresco a cada request. Investigar se `pageAuth`
precisa aceitar o token do demoAutologin como o `authOptional` já aplicado em
logout/reset-demo. Enquanto isso, a validação visual por browser fica bloqueada
neste bug — valide por artifacts servidos + jest.

## Gateway Telegram (Planck bot)
Já pareado: `channel_directory.json` lista "Pedro Rocha" (DM, id 8869378956).
`hermes-gateway.service` (systemd) roda (`hermes gateway status` mostra active).
O agente CLI NÃO inicia conversa no Telegram: para seguir para lá, o USUÁRIO
abra o DM do bot e mande a 1ª mensagem. Log pode mostrar falhas de rede a
`api.telegram.org` (ambiente bloqueia Telegram direto) — não significa que o
canal sumiu.
