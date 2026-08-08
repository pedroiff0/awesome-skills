# Passo a passo — correção de UI (financas-app)

1. **Localizar**: `read_file`/`search_files` em `app/views/*.ejs`, `app/public/js/*.js`,
   `app/public/css/main.css`. Não chutar — ler o seletor real antes de editar.
2. **Editar** CSS/JS/EJS respeitando AGENTS.md (sem JS inline; todo script em `/js/`;
   `escapeHtml()` em saída user-facing; Zod em POST/PUT/PATCH).
3. **Rebuild AMBOS os containers** (pitfall do CSS do /demo):
   ```bash
   ASSET_VERSION=N docker compose -p fa build --no-cache app app-demo
   ASSET_VERSION=N docker compose -p fa up -d app app-demo
   ```
   Se o CSS servido não mudar, o Docker cacheou a camada de COPY → `--no-cache` resolve.
4. **Validar no browser** (host docker `192.168.80.1:4460`, NÃO 127.0.0.1):
   - `browser_navigate http://192.168.80.1:4460/demo/<pagina>`
   - `browser_snapshot` / `browser_console` para medir margens (ex.:
     `[...document.querySelectorAll('main > section.card')].map(c=>({h2:c.querySelector('h2')?.textContent, top:Math.round(c.getBoundingClientRect().top), marginTop:getComputedStyle(c).marginTop}))`).
   - `browser_vision` para checagem visual (tema claro e escuro).
   - Se modal não abrir com `browser_click`, disparar via console:
     `document.querySelector('button[data-acao="editar"]').click()`.
5. **Verificação ad-hoc**: script `/tmp/hermes-verify-*.js` inspecionando CSS/JS/HTML
   servidos + fontes; rodar com `node` e remover. Resumir como ad-hoc (não jest).
6. **Testes**: `cd app && npx jest --forceExit` (alvo 230+ verde) ANTES do commit.
7. **Commit + push** (usuário quer empurrar após corrigir):
   `git commit -q -m "fix(escopo): ..." && git push origin feat/porta-unica-demo-rota`.

## Casos comuns já resolvidos (não reintroduzir)
- `.card + .card { margin-top }` global desalinhava segundo card de `.grid-2`/`.split` →
  anulado com `.grid-2 > .card + .card { margin-top: 0 }` etc.
- `.container > .card { margin-top: 1.5rem }` para espaçar módulos do painel.
- `.card > .card { margin-top: 1.25rem }` para cards aninhados.
- `.row-tight` (lista de metas): `gap` + inputs que não encolhem.
- Filtros do extrato: `.filtros.row { flex-wrap: wrap }` + `min-width` nos `input[type=date]`.
- `.dataTables_wrapper .row` herda `display:flex` do `.row` global → restaurar flex com
  espaçamento (length/busca/paginação).
- Gráficos de rosca: sem texto de % fixo no centro; info no hover (`<title>` SVG).

## Logout travado (causa raiz já corrigida)
`user.model.js`: `tokenValidAfter` default era `new Date()` → todo usuário novo nascia com
token inválido. Agora `default: null`. Logout/reset usam `authOptional` (não barram token
inválido). Se reaparecer "token inválido ao sair", revisar esses dois pontos.
