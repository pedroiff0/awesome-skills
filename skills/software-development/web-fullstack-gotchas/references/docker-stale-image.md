# Docker: código editado no disco NÃO aparece após `restart` (imagem bakeada)

Receita exata e o erro que confunde, capturados na sessão do projeto-profissional.

## Sintoma
Você editou `app/views/*`, `app/public/css/*`, `app/src/*` no disco. Rodou
`docker compose restart` (ou o usuário reiniciou o app). A página continua com
o layout/código ANTIGO. "Não surtiu efeito nenhum."

## Causa raiz
O `docker-compose.yml` deste template (e de financas-app/sistema-academico)
faz `build:` com `dockerfile: app/Dockerfile`, e o Dockerfile faz
`COPY app/ ./` em tempo de BUILD. **Não há bind mount do código.** O container
roda o que foi copiado para a imagem quando ela foi buildada. `restart` só
religa o mesmo container/imagem — não re-copia o disco.

```
# Dockerfile (app/Dockerfile) — sem bind mount:
COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --chown=node:node app/ ./
```

Portanto: **editar código no disco nunca entra no container até a imagem ser
rebuildada.** Isso é independente de `NODE_ENV`, de cache de browser ou de
`restart: unless-stopped`.

## Correção (a única que funciona)
```bash
cd /caminho/do/projeto
docker compose build --no-cache app      # re-copia o app/ atual para a imagem
docker compose up -d --force-recreate app # recria o container a partir da imagem nova
```
`--no-cache` garante que o `COPY app/` rode de novo mesmo que o Docker ache o
layer "inalterado". `--force-recreate` destrói o container velho e sobe o novo
(imagens diferentes têm digests diferentes, então `up -d` sozinho pode não
recriar se o compose achar que "já está rodando").

## Como confirmar que o NOVO código está no ar (não confie no print)
1. Espere o health: `docker inspect -f '{{.State.Health.Status}}' <container>`
   deve virar `healthy` (o app semeia 3 bancos no boot, leva alguns segundos).
2. Descubra onde o container realmente escuta — NÃO assuma loopback:
   ```bash
   docker port <container>          # ex.: 5000/tcp => 100.120.54.126:4450
   ```
   O `BIND_ADDR` do `.env` costuma ser um IP não-loopback (ex.:
   `100.120.54.126`), então `curl 127.0.0.1:4450` dá **exit 7 (failed to
   connect)** mesmo com o app saudável. Use o HostIp:Porta do `docker port`.
3. Busque a página e grep por assinaturas do NOVO design vs o antigo:
   ```bash
   curl -s http://<HostIp>:<Port>/ -o /tmp/live.html -w 'HTTP %{http_code}\n'
   grep -c 'lp-hero-inner'        /tmp/live.html   # novo: >0
   grep -c 'class="lang-btn"'     /tmp/live.html   # novo: >0
   grep -c 'space-bg\|glass-card' /tmp/live.html   # antigo: 0
   ```
   Só declare "funciona" depois desse grep bater. Um `docker compose restart`
   (sem build) vai continuar mostrando as assinaturas antigas — é o teste
   definitivo de que o rebuild foi necessário.

## Armadilha do curl em loop (hardline blocklist)
Evite `for s in ...; do grep ...; done` com curl aninhado — o parser de comando
pode bloquear o comando inteiro (blocklist de "loop+url"). Prefira um único
`curl` seguido de `grep` separados, ou salve o HTML e grepe o arquivo.

## Ordem correta de trabalho quando o app roda em Docker
1. Edite o código no disco (views/CSS/JS/src).
2. Valide estaticamente se puder (render EJS sem Mongo, lint DESIGN.md).
3. **`docker compose build --no-cache app`** + **`up -d --force-recreate app`**.
4. Aguarde health; `curl` no HostIp:Porta real; grep assinaturas.
5. Só então tire screenshot / declare pronto.

Não pule o passo 3 por "já rodei restart". Restart não rebuilda imagem.
