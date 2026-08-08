# Cache-bust recipe — verify a frontend change actually rendered

Scenario: you edited CSS/HTML/template; the browser screenshot still shows the
old layout. Don't trust the screenshot — run the triple-check.

## 1. Triple-check (terminal + browser)

Server is serving new code?
```bash
curl -s http://127.0.0.1:4452/css/main.css | grep -c 'tut-layout'   # new token => >0
curl -s http://127.0.0.1:4452/css/main.css | wc -c                    # compare byte size to local
```

DOM has the new structure? → `browser_snapshot()` and look for your new class.

Computed style matches the new code? → `browser_console`:
```js
(() => {
  const el = document.querySelector('.tut-layout');
  if (!el) return 'SELECTOR NOT IN DOM';
  const cs = getComputedStyle(el);
  return { display: cs.display, grid: cs.gridTemplateColumns,
           position: getComputedStyle(document.querySelector('.tut-side')).position };
})()
```
If `display` is `block` but your CSS says `grid` → it's stale cache.

## 2. Force a fresh stylesheet (no hard-reload in toolset)

`browser_console`:
```js
(() => {
  const l = document.querySelector('link[rel="stylesheet"]');
  l.href = l.href.split('?')[0] + '?cb=' + Date.now();
  return 'busted: ' + l.href;
})()
```
Wait ~600ms, then `browser_vision` again.

## 3. Container didn't pick up the edit?

Readonly filesystem ⇒ rebuild:
```bash
export BIND_ADDR=0.0.0.0
docker compose -f docker-compose.demo.yml -p fa-demo up -d --build
```

## 4. Protected page bounces you to /login?

Get a session cookie via curl, then reuse it:
```bash
curl -s -c /tmp/cj.txt -d "email=demo@financas.app&password=Demo123456" \
     http://127.0.0.1:4452/api/auth/login >/dev/null
curl -s -b /tmp/cj.txt http://127.0.0.1:4452/tutorial | grep -o 'tut-layout'
```
Or in the browser: fill the login form with demo creds, then navigate.
