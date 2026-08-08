# i18n (PT/EN/ES/FR) + tema claro/escuro — padrão do projeto-profissional

Requisito do Pedro: botão de idioma (PT/EN/ES/FR) e botão de trocar tema
(claro/escuro) no topbar, landing por instância com storytelling, e demo
autologada direto. Implementado sem quebrar a CSP (`script-src 'self'`, sem
`unsafe-inline`).

## 1. Middleware i18n (`src/middleware/i18n.js`)

Lê `?lang=xx` > cookie `lang` > `'pt'`. Valida contra a lista; grava cookie
(1 ano) quando veio da query; define `res.locals.lang` e `res.locals.t`.

```js
const { LANGS, translate } = require('../config/i18n');
function i18n(req, res, next) {
  const fromQuery = typeof req.query.lang === 'string' ? req.query.lang.toLowerCase() : '';
  const fromCookie = req.cookies && req.cookies.lang;
  const raw = fromQuery || fromCookie || 'pt';
  const lang = LANGS.includes(raw) ? raw : 'pt';
  if (fromQuery && fromQuery !== fromCookie) {
    res.cookie('lang', lang, { maxAge: 365*24*60*60*1000, sameSite: 'lax', path: '/' });
  }
  res.locals.lang = lang;
  res.locals.t = (key) => translate(lang, key);
  next();
}
module.exports = i18n;
```

Registrar em `app.js` DEPOIS de `cookieParser()` e ANTES de `express.static`
e das rotas. Assim `t()` existe em toda view (inclusive no `header`/`footer`
parciais e na `error.ejs` — ver pitfall 69).

## 2. Dicionário (`src/config/i18n.js`)

`DICT = { pt:{...}, en:{...}, es:{...}, fr:{...} }` com chaves planas
(`nav.enter`, `login.title`, `theme.toDark`, `landing.what`, ...). `translate`
cai no `pt` quando a chave não existe no idioma pedido. Manter as 4 línguas em
sincronia — chave nova em `pt` vai para as outras três (mesmo que seja um
placeholder), senão o seletor "funciona" mas some texto.

## 3. Helper nas views

`res.locals.t` está disponível em qualquer `.ejs`: `<%= t('nav.enter') %>`.
Para texto longo/específico por instância (storytelling da landing), use um
segundo dicionário indexado por modo+idioma — ver `src/config/landingContent.js`
(`CONTENT[modo][lang] = { eyebrow, title, lede, cta, points[], demoNote }`, com
fallback `byMode[lang] || byMode.pt`). A landing lê `modeFromEnv()` e
`res.locals.lang` e passa `landingFor(mode, lang)` + `ctaHref` para a view.

## 4. Tema (claro/escuro)

CSS: além de `@media (prefers-color-scheme: dark)`, adicionar
`:root[data-theme='dark']` e `:root[data-theme='light']` que SOBREPÕEM as
variáveis (`--bg`, `--surface`, `--text`, `--muted`, `--border`, `--primary`).
Toggle forçado ganha de `prefers-color-scheme`.

JS (`public/js/common.js`, no `DOMContentLoaded`):
- Botão `#theme-toggle` com dois SVGs (sol/lua), `aria-pressed`, `aria-label`.
- Lê cookie `theme` (`'auto'|'light'|'dark'`); aplica `data-theme` no
  `<html>` (ou remove para "auto"). Persiste em cookie no clique.
- `applyTheme(theme)` liga `aria-pressed`/label e mostra/esconde os SVGs.

## 5. Seletor de idioma

No topbar: `<select id="lang-switcher">` com 4 `<option value="pt|en|es|fr">`.
No `change`: `params.set('lang', value); window.location.search = params` —
o middleware grava o cookie e re-renderiza no idioma. NÃO usar `onclick` inline.
Pré-selecionar com o cookie atual ao carregar.

## 6. Gotchas de verificação (desta sessão)

- **Env antes do require (pitfall 67):** `env.js` faz `dotenv.config()` e lê
  `NODE_ENV`/`JWT_SECRET` no require. Setar depois de `require('./src/app')`
  não adianta — em produção o `requiredInProd` mata o boot. Defina a env ANTES
  dos requires ou rode o filho com a env no shell.
- **Um NODE_ENV por processo (pitfall 68):** não cacheie `config/env` entre
  modos no mesmo processo. Para testar produção+teste+demo, spawn de 1
  processo por modo.
- **Fallback de `t` no errorHandler (pitfall 69):** `error.ejs` inclui o
  `header` que usa `t()`; garanta `res.locals.t` em todo caminho de erro (ou
  passe `t: res.locals.t || ((k)=>k)` no `res.render` do errorHandler).
- **Regressão em aberto (pitfall 66):** instância `NODE_ENV=demo` renderizou a
  landing de PRODUÇÃO num teste ad-hoc. Ao retomar, confirmar `modeFromEnv()`
  DENTRO do handler da landing e que `res.locals.lang` está definido; não
  declarar pronto sem um `curl` real em cada porta.
