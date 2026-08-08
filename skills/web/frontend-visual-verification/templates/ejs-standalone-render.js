#!/usr/bin/env node
// Renderiza uma view EJS do projeto DE FORMA ISOLADA (sem MongoDB/servidor) para
// verificação visual via browser (file:///tmp/lp_pub/out.html).
// Uso: node ejs-standalone-render.js <pagina.ejs> [modo]
//   - APP deve apontar para a pasta 'app' do projeto (ajuste abaixo).
//   - localsFor(page, mode) retorna os locals que a rota normalmente injeta.
const fs = require('fs');
const path = require('path');

// >>> ajuste para o seu projeto <<<
const APP = '/home/pedro/Repositorios/templates/projeto-profissional/app';
// <<<

const ejs = require(path.join(APP, 'node_modules/ejs'));
const VIEWS = path.join(APP, 'views');

function localsFor(page, mode) {
  // Exemplo para uma landing que injeta bancos por ambiente + i18n.
  // Adapte ao seu caso (leia os módulos de config reais do projeto).
  const { landingFor } = require(path.join(APP, 'src/config/landingContent'));
  const { DICT } = require(path.join(APP, 'src/config/i18n'));
  const lang = (mode && DICT[mode] ? mode : 'pt');
  const t = (k) => (DICT[lang][k] !== undefined ? DICT[lang][k]
    : (DICT.pt[k] !== undefined ? DICT.pt[k] : k));
  const bancos = ['production', 'test', 'demo'].map((m) => {
    const c = landingFor(m, lang);
    return { id: m, titulo: c.title, desc: c.lede, points: c.points || [],
      badge: c.badge, href: m === 'demo' ? '/demo/start' : `/${m}/login`,
      cta: c.cta, classe: `env-${m.slice(0, 4)}` };
  });
  return { bancos, lang, lp: true, t };
}

function render(page, mode) {
  return ejs.render(fs.readFileSync(path.join(VIEWS, page), 'utf8'), localsFor(page, mode),
    { views: [VIEWS], filename: path.join(VIEWS, page) });
}

const page = process.argv[2] || 'landing.ejs';
const mode = process.argv[3];
const html = render(page, mode);
const outDir = '/tmp/lp_pub';
fs.mkdirSync(path.join(outDir, 'css'), { recursive: true });
fs.mkdirSync(path.join(outDir, 'js'), { recursive: true });
fs.copyFileSync(path.join(APP, 'public/css/main.css'), path.join(outDir, 'css/main.css'));
fs.copyFileSync(path.join(APP, 'public/js/common.js'), path.join(outDir, 'js/common.js'));
fs.writeFileSync(path.join(outDir, 'out.html'),
  html.replace('/css/', 'css/').replace('/js/', 'js/'));
console.log('open file://' + path.join(outDir, 'out.html'));
