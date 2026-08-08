# Shell da área logada: navbar, largura do layout e página de tutorial

Complemento de `ui-landing-and-footer.md`, que cobre a landing pública. Este
arquivo é a **área autenticada**: a barra de navegação, o container do conteúdo
e a aba de tutorial. Validado em `financas-app`.

Quando Pedro diz *"a navbar precisa ser refatorada por completo"*, *"o layout
precisa se estender ao máximo (respeitando uma borda razoável das laterais)"* ou
*"está super péssimo"*, é este conjunto que ele está olhando.

## O defeito nº 1: `.container` com largura travada

O template nasce com `max-width: 1180px`. Num monitor grande isso deixa duas
faixas enormes vazias e é exatamente o que ele chama de layout ruim.

```css
:root {
  /* Respiro lateral ÚNICO: navbar e conteúdo alinham pela mesma margem. */
  --gutter: clamp(1rem, 3.5vw, 2.75rem);
}

.container {
  width: 100%;
  max-width: 1800px;          /* teto alto, não 1180 */
  margin: 1.75rem auto;
  padding: 0 var(--gutter);
}
```

Duas decisões que importam:

- **`--gutter` é um token compartilhado**, usado tanto no `.container` quanto no
  `.topbar-inner`. Sem isso a marca da navbar não alinha com o título da página
  e o desalinhamento salta aos olhos.
- **Teto de 1800px, não `none`.** "Estender ao máximo" não é linha de texto
  quilométrica em ultrawide — é aproveitar a tela sem espremer.

Os grids internos têm o mesmo vício. Trocar `repeat(4, 1fr)` fixo por `auto-fit`
faz o layout acompanhar a largura sem media query:

```css
.kpi-grid  { grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); }
.form-grid { grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); align-items: end; }
.split     { grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); }
```

## Navbar: menus nativos, zero JS

A CSP proíbe script inline, então dropdown e menu mobile precisam funcionar sem
JS. Duas primitivas HTML resolvem:

**Menu da conta = `<details>`/`<summary>`.** Ganha teclado e Esc de graça.

```css
.menu { position: relative; }
.menu summary { list-style: none; cursor: pointer; }
.menu summary::-webkit-details-marker { display: none; }
.menu-pop { position: absolute; right: 0; top: calc(100% + 6px); }
```

**Menu mobile = checkbox + `~`.** O `<label>` vira o botão hambúrguer:

```html
<input type="checkbox" id="nav-toggle" class="nav-toggle" hidden />
<label for="nav-toggle" class="nav-burger" aria-label="Abrir menu">…</label>
<nav class="nav-main">…</nav>
```
```css
.nav-toggle, .nav-burger { display: none; }         /* desktop */
@media (max-width: 900px) {
  .nav-burger { display: grid; margin-left: auto; }
  .nav-main { display: none; position: absolute; top: 100%; left: 0; right: 0; }
  .nav-toggle:checked ~ .nav-main { display: flex; }
  .nav-user { margin-left: 0; }   /* o burger assumiu o margin-left:auto */
}
```

O `~` exige que o checkbox seja **irmão anterior** da nav — se ele estiver
dentro de outro elemento, o seletor não casa e o menu nunca abre.

### Item ativo sem repetir em cada rota

Injete o path uma vez no `app.js` (mesma lógica de `app.locals.appName`,
pitfall 19) — como é **por request**, vai em `res.locals`, não em `app.locals`:

```js
app.use((req, res, next) => { res.locals.currentPath = req.path; next(); });
```
```ejs
<% const ativo = (p) => (currentPath === p ? ' class="is-active" aria-current="page"' : ''); %>
<a href="/app"<%- ativo('/app') %>>Painel</a>
```

Use `<%- %>` (não `<%= %>`) para emitir o atributo, senão as aspas saem
escapadas como `&quot;`.

### Tokens de estado derivados (funcionam nos dois temas)

Evita manter um par de cores para claro e outro para escuro:

```css
--hover:  color-mix(in srgb, var(--text) 6%, transparent);
--active: color-mix(in srgb, var(--primary) 12%, transparent);
```

### O que vai na nav e o que vai no menu da conta

Módulos e páginas de uso diário ficam na nav horizontal; o resto (Cadastros,
Perfil, Usuários, Sair) vai para o `<details>`. A nav antiga listava tudo em
linha e ficava ilegível a partir de ~6 itens.

## Detalhes de tabela que ele nota

```css
.table-wrap { overflow-x: auto; }          /* rola em vez de estourar o card */
.table .num, .num {
  text-align: right;
  font-variant-numeric: tabular-nums;      /* casas decimais alinhadas */
}
.table th { font-size: .78rem; text-transform: uppercase; color: var(--muted); }
```

`tabular-nums` é o que permite comparar valores batendo o olho numa coluna de
dinheiro — sem isso os dígitos dançam.

## Aba de tutorial

Ele pede *"uma aba de tutorial de como utilizar a aplicação"*. O que funciona:

- Rota simples em `pages.routes.js` (`pageAuth` + `requirePasswordChanged`),
  **fora** de `paginaDeModulo` — o tutorial existe mesmo com módulos desligados.
- TOC sticky no topo com âncoras para cada seção.
- **`scroll-margin-top` nas seções** (~130px): com a topbar sticky, pular por
  âncora esconde o título atrás da barra. É o defeito clássico dessa página.
- Uma seção por módulo, mais uma final **"Como as contas são feitas"**
  explicando cada valor derivado (saldo, patrimônio, km/l, custo/km). É o que
  transforma o tutorial em documento útil em vez de tour de botões.
- Explique o *porquê* das regras de negócio, não só onde clicar: por que marcar
  "tanque cheio" (senão não há km/l), por que informar o combustível em carro
  flex (senão a média mistura etanol com gasolina), o que é preço médio por
  corretora. Prosa curta, sem emoji, `.tut-tip` com barra lateral colorida para
  destaque.
- Largura de leitura: `max-width: 78ch` nas seções de texto, mesmo com o
  container largo. Layout largo é para tabela e KPI, não para parágrafo.

## Revisão visual assistida: o que aceitar e o que descartar

Pedir a um modelo de visão que critique o screenshot acha defeito real, mas
**mede o viewport, não o CSS**. Filtre antes de agir:

Descartou-se com razão (falso positivo):
- *"espaço morto nas laterais, container ~1200px"* — o `.container` já estava em
  1800px; o browser é que renderiza em 1280px. **Cheque `grep max-width` no CSS
  antes de "corrigir" largura.**
- *"grid de KPI desbalanceado, 5 na primeira linha e 3 na segunda"* — é
  `auto-fit` funcionando; a assimetria é consequência do número de cards, não
  defeito.
- *"contraste baixo no rodapé"* — o token já passava 4.5:1 medido. O que
  incomodava era **tamanho de fonte**, não contraste. Meça antes de trocar cor.

Aceitou-se (defeito real, vale corrigir sempre):
- **Ação destrutiva na cor primária.** "Excluir" em azul compete com
  "Cadastrar" e convida ao clique errado. Cinza em repouso, vermelho no hover,
  regra genérica por contexto em vez de listar cada `data-*`:
  ```css
  .table .btn-link          { color: var(--muted); }
  .table .btn-link:hover    { color: var(--error); text-decoration: underline; }
  ```
- **`value="0"` num campo numérico** parece dado preenchido; use `placeholder`.
- **Dois valores monetários na mesma linha do KPI** — empilhe com rótulo
  pequeno (`R$ 4.570,91 / carro` acima de `R$ 381,78 / moto`).

O snapshot de acessibilidade **colapsa texto aninhado**: `<li><strong>x</strong>
<p>y</p></li>` aparece como item vazio. Antes de "consertar" conteúdo sumido,
confirme com `document.querySelectorAll(...).map(e => e.innerHTML)` — na prática
o texto estava todo lá.



Layout é trabalho visual: **renderize e olhe** antes de dar por pronto (ele
aprova só depois de ver). Popule dados de demonstração primeiro — tela vazia
não revela nada sobre espaçamento, alinhamento de coluna numérica ou quebra de
grid. Depois rode o `tests/design.test.js` de contraste (ver SKILL.md) e
confira o resultado no celular via `@media (pointer: coarse)`.

Lembre dos pitfalls 10 e 25: depois de mexer em CSS, `up -d --build` (o
container serve a imagem) **e** `fetch(url, {cache:'reload'})` no browser — os
dois juntos, senão "meu ajuste não fez nada".
