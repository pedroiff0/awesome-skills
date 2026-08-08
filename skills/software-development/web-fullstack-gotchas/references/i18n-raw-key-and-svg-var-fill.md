# i18n raw-key + SVG var() fill — diagnóstico e receita

Condensado da sessão projeto-profissional (Node/Express + EJS + Docker, 3 modos
na mesma porta /app /test /demo). Complementa SKILL.md §20-§23.

## A. Chave i18n crua (`proj.list` na tela)

Causa quase certa: a chave falta no idioma ATIVO (PT costuma ser editado por
ultimo e ficar com bloco incompleto). `nav.*`/`landing.*` funcionam; `proj.*`/
`pro.*` saem crus porque en/es/fr tem o bloco e o PT nao.

Diagnostico isolado (nao precisa subir container):
```js
const { translate } = require('./src/config/i18n');
console.log(translate('pt','proj.list')); // 'proj.list'  => falta no PT
console.log(translate('pt','nav.tasks')); // 'Tarefas'     => OK
```
Confirma no arquivo:
```bash
grep -n "'proj.list':" src/config/i18n.js
# se so aparece em linhas de en/es/fr (ex.: 197/299/401), o PT (linhas ~90) nao tem
```
Correcao: adicione o bloco PT faltante. Verificacao ao vivo:
```bash
curl -s -b /tmp/demo.cookies /demo/projetos | grep -c 'proj.list'  # 0
curl -s -b /tmp/demo.cookies /demo/projetos | grep -c 'Projetos registrados'  # >0
```

## B. SVG fill="var(--brand)" fica preto

`var()` NAO resolve em atributo de apresentacao SVG. Remova do atributo, use
classe + CSS:
```html
<rect class="bar" x=".." y=".." width=".." height=".." rx="1.5"></rect>
```
```css
.bars svg .bar { fill: var(--brand); }
.bars-labels { display:flex; gap:.4rem; flex-wrap:wrap; margin-top:.5rem; }
.bars-labels span { flex:1; text-align:center; }
```
Verificacao no browser:
```js
getComputedStyle(document.querySelector('.bar')).fill // rgb(37,99,235), NAO rgb(0,0,0)
```

## C. Barras sobrepostas (bloco solido) em viewBox 0..100 + preserveAspectRatio=none

`x="6%" width="88%"` => cada barra ocupa 88% da largura => sobrepoem. Use
user-space:
```js
const slot = 100 / entries.length;
const bw = Math.min(slot * 0.6, 14);
const x = i * slot + (slot - bw) / 2;
const y = 100 - h;            // h = Math.max(3, round(total/max*94))
// rótulos em HTML (.bars-labels) ABAIXO do svg, nao <text> no svg
```

## D. EJS escapa aspas de atributo (falso FAIL em verificacao)

`data-theme="<%= lpDark ? 'dark':'light' %>"` => servido como
`data-theme=&#34;dark&#34;`. Browser decodifica certo; mas
`html.includes('data-theme="dark"')` falha. No harness confira:
`html.includes('data-theme=&#34;dark&#34;')` ou `curl | grep -o '<html[^>]*>'`.

## E. Arbitro de deploy stale

```bash
docker exec projeto-profissional-app-1 grep -c "proj.list" /app/src/config/i18n.js
docker exec projeto-profissional-app-1 grep -c "renderizarCards" /app/public/js/board.js
```
Container tem + browser nao => cache cliente ou browser abriu antes do rebuild.
Container NAO tem => rebuild nao incluiu patch:
`docker compose build --no-cache app && docker compose up -d --force-recreate app`.
