# Tema "deep space" + glassmorphism (padrão visual REAL do Pedro)

Quando o Pedro pede "padrão profissional", "igual às outras landing pages" ou
"refatoração gigante de DESIGN", o padrão de referência NÃO é o DESIGN.md sóbrio
institucional do template — é o visual dos **outros sites dele**:
`~/portfolio` (GitHub Pages, tema astronomia/glass) e o site Quartz
`phrandrance.com`. Esse é o "developer-grade aesthetic" do perfil dele:

- Fundo **deep space**: `radial-gradient` escuro + **canvas animado** com
  starfield (cai devagar), galáxias espirais e **constelações**.
- **Mouse repulsion**: partículas/orbs que FOGEM do cursor (empurra, não atrai).
  O portfólio original NÃO tinha repulsão (só orbs quicando) — foi construída do
  zero nesta base; veja o snippet abaixo.
- **Glassmorphism**: painéis com `backdrop-filter: blur(10px)`, borda fina
  `rgba(140,160,255,.16)`, fundo `rgba(17,21,46,.72)`. Conteúdo OPAQUE; só o
  véu de fundo é desfocado.
- Gradiente azul→violeta `--grad: linear-gradient(135deg,#6ea8fe,#b692ff)` como
  ÚNICO acento (CTAs, links ativos, ícones). Resto é neutro frio sobre escuro.
- Fontes **Sora** (display/títulos) + **Inter** (corpo) via Google Fonts — a CSP
  precisa liberar `fontSrc: ['self','https://fonts.googleapis.com','https://fonts.gstatic.com']`
  (e o `<link preconnect>` no head).
- **Seletor de idioma por BANDEIRAS SVG** (PT/EN/ES/FR), não `<select>` de texto.
- Sem emoji: SVG inline ou `✕` (U+2715) para fechar.
- Respeitar `prefers-reduced-motion` (parar animações do canvas).

## Arquivos desta base (após a refatoração)

- `public/css/theme-space.css` — tokens, fundo space, glass, navbar/footer/hero/
  cards glass, board/calendário glass. `main.css` virou complemento mínimo.
- `public/js/space-bg.js` — canvas starfield + galáxias + constelações + orbs
  COM repulsão do mouse.
- `views/partials/header.ejs` — navbar glass + canvas de fundo + seletor de
  bandeiras + logo de anel planetário.
- `views/landing.ejs` — hero (eyebrow + título grad + sub + CTAs + badges), sem
  grid de 3 bancos (ver pitfall 72).
- `DESIGN.md` / `AGENTS.md` **atualizados** para o tema space/glass (a versão
  anterior mandava "sem animação, sem framework CSS, landing sempre clara" — isso
  conflita com o padrão real e foi sobrescrito).

## Snippet: repulsão do mouse (orbs fogem do cursor)

Dentro do loop de desenho das orbs, após mover com velocidade base:

```js
if (mouse.active) {
  const dx = o.x - mouse.x, dy = o.y - mouse.y;
  const d = Math.hypot(dx, dy);
  const mr = 160 * gdpr;               // raio de influência
  if (d < mr && d > 0.01) {
    const f = (mr - d) / mr;           // força cresce perto do cursor
    o.x += (dx / d) * f * 6 * gdpr;
    o.y += (dy / d) * f * 6 * gdpr;
  }
}
```

`mouse` vem de `mousemove`/`touchmove` (clientX/Y * dpr). Sem isso o efeito de
"repulsão" simplesmente não existe — é o diferencial que o perfil pede.

## Quando aplicar

Sempre que ele criticar o visual ("css horrível", "não está igual ao padrão
exigido", "verifique as outras landing pages"): copie o padrão acima, NÃO o
sober do DESIGN.md antigo. E atualize o próprio DESIGN.md/AGENTS.md para refletir
o tema escolhido, senão o repo fica em contradição interna (o AGENTS.md exige
seguir o DESIGN.md). Ver pitfall 80.
