# Verificação ad-hoc de artifacts servidos (financas-app)

O `curl` anônimo de rota autenticada cai em `/login` e devolve HTML de /login
(sem os scripts da página) -> falso negativo. Para verificar o que o container
serve de verdade, inspecione os artifacts HTTP.

## CSS/JS servido pelo app-demo (host localhost via nginx :4460)
```bash
curl -s "http://127.0.0.1:4460/demo/css/main.css" | grep -c "min-width: 2.1rem"
curl -s "http://127.0.0.1:4460/demo/js/lancamentos.js" | grep -E "paging:|pageLength|pagingType"
curl -s "http://127.0.0.1:4460/demo/lancamentos" | grep -o "main.css?v=[0-9]*"
```

## Script node em /tmp (padrão do reminder de verificação)
Escreva em `/tmp/hermes-verify-<curto>.js`, inspecione artifacts HTTP + fonte,
imprima JSON e `process.exit(ok?0:1)`, depois `rm`.
```js
const http=require('http');
const get=p=>new Promise(r=>http.get({host:'127.0.0.1',port:4460,path:p},
  x=>{let d='';x.on('data',c=>d+=c);x.on('end',()=>r({status:x.statusCode,body:d}))}));
(async()=>{
  const css=(await get('/demo/css/main.css')).body;
  const ok=/\.table-responsive\s*\{[^}]*overflow-x:\s*auto/.test(css)
         && /paging:\s*true/.test((await get('/demo/js/lancamentos.js')).body);
  console.log(ok?'VERIFICACAO AD-HOC: OK':'VERIFICACAO AD-HOC: FALHOU');
  process.exit(ok?0:1);
})().catch(e=>{console.error(e.message);process.exit(2)});
```
Rode: `node /tmp/hermes-verify-x.js; echo exit=$?; rm -f /tmp/hermes-verify-x.js`

## Browser vs curl
- `browser_navigate` usa `192.168.80.1:4460` (host docker); `127.0.0.1:4460`
  funciona para `curl` mas o browser headless nao alcança.
- Se o app-demo tiver o bug #34 (redirect /demo/* -> /app "Token inválido"),
  o browser nao carrega a página: valide por artifacts servidos + jest e
  reporte o blocker.
