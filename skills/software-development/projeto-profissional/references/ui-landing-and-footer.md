# Landing page + rodapé: o padrão visual do Pedro

Referência do padrão "empresarial" que o Pedro considera aprovado. A origem é
`sistema-academico` (`app/views/landing.ejs` + bloco `.lp-*` em
`app/public/css/main.css`, ~130 linhas). O template `projeto-profissional`
carrega a versão **generalizada** desse mesmo padrão.

Quando ele pedir "landing profissional", "padrão empresarial" ou "igual ao
sistema-academico": porte esse layout, não invente um novo.

## Assinatura de rodapé (literal — não parafraseie)

```
© <ano> Pedro Henrique Rocha de Andrade — feito com café, código e um céu estrelado.
Voltar ao topo ↑
```

- Nome linka para `https://phrandrade.com` (`target="_blank" rel="noopener"`).
- "Voltar ao topo ↑" é **âncora interna** (`href="#topo"`), nunca JS — a CSP do
  template proíbe script inline. Exige `id="topo"` no `<body>` do
  `partials/header.ejs`, senão o link não vai a lugar nenhum.
- Vale para a landing **e** para a área logada (`partials/footer.ejs`).
  Ele pediu explicitamente "internamente isso".
- `scroll-behavior: smooth` no `html`, com `@media (prefers-reduced-motion)`
  desligando.

## Estrutura da landing (ordem que ele aprovou)

1. **Hero** 2 colunas (`1.12fr / 0.88fr`): brand-row (marca + nome + badge),
   `h1` com `<strong>` colorido na segunda linha, lead, dois CTAs
   (primary + outline), nota discreta · card de status à direita com
   mini-stats, barra de progresso e legenda.
2. **Faixa de números** (`.lp-stats`, 4 colunas, fundo branco com bordas).
3. **Recursos** — grid 3×2 de `.lp-feature` com hover `translateY(-3px)`.
4. **Seção alternada** (`.lp-alt`, fundo `#eef3f9`, cantos 26px) em 2 colunas:
   texto + `.lp-list` com `✓` · card de especificações à direita.
5. **Passo a passo** numerado (`.lp-step-n`, círculos).
6. **CTA** em gradiente, cantos 26px, botão invertido (branco sobre a cor).
7. **Rodapé escuro** `#0f172a`: brand + 3 colunas de links, divisor, barra
   inferior com a assinatura acima.

Responsivo em `@media (max-width: 860px)`: tudo vira 1 coluna, stats 2 colunas,
`h1` 2.3rem, rodapé empilhado.

## Regras de estilo que ele cobra

- **SVG inline, nunca emoji.** O original do sistema-academico usa emoji nos
  ícones de recurso; ao portar, troque por SVG 24×24 com
  `stroke="currentColor"` (herda a cor da marca). Emoji que não renderiza ele
  chama de quebrado.
- **Uma única elevação** para todos os cards. Três sombras diferentes foi o
  defeito nº 1 apontado na revisão visual:
  `box-shadow: 0 10px 30px rgba(15,23,42,0.07)`; hover `0 18px 44px …0.12`.
- **Contraste**: `#94a3b8` sobre branco reprova em WCAG AA para texto pequeno.
  Use `#64748b`. No rodapé escuro, `#64748b` some — use `#b6c2d1`.
- Copyright/rodapé nunca abaixo de `0.9rem`.
- Paleta da landing é **variável própria** (`--lp-accent`), separada do app
  autenticado; escopar em `.lp-page` para vencer a `.btn-primary` genérica por
  especificidade.

## Ao generalizar de um projeto real para o template

Grep obrigatório antes de dar por pronto — nenhum resíduo de domínio:
`IFF|boletim|matricula|Engenharia de Computação|CR`.

Números exibidos (testes, req/s, sessões) são reais **daquele** repositório.
Ao clonar o template para um projeto novo, atualize ou remova — senão viram
métrica inventada, que ele já pegou uma vez.

## Pitfall de EJS que quase quebrou

`res.render('landing')` sem passar variável + `<%= appName %>` na view = erro
500. Resolva uma vez em `app.js` com `app.locals.appName = env.appName`
(vale para todas as views), não repetindo no render de cada rota.
