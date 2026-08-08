# financas-app: runtime config injection under strict CSP

Context: Express + EJS + helmet. CSP = `scriptSrc: ["'self'"]` (no `unsafe-inline`).
The app is served both as the principal instance and as a demo instance
mounted under `/demo`. The client JS needed to know the API prefix (`''` for
principal, `'/demo'` for demo) so fetches hit the right backend.

## Wrong (silent failure)
`views/partials/header.ejs`:
```ejs
<script>window.__API_PREFIX__ = '<%= typeof apiPrefix !== 'undefined' ? apiPrefix : '' %>';</script>
```
Present in HTML (curl), but `typeof window.__API_PREFIX__ === 'undefined'` in
the browser. helmet CSP blocks the inline script. Symptom surfaced far away:
every `apiRequest('/api/dashboard')` hit the principal instance (no demo user)
→ `401 Token invalido ou expirado` on the demo dashboard.

## Right
`views/partials/header.ejs` — value on the `<html>` element, no inline script:
```ejs
<!DOCTYPE html>
<html lang="pt-BR" data-api-prefix="<%= typeof apiPrefix !== 'undefined' ? apiPrefix : '' %>">
```

`app/src/app.js` sets `res.locals.apiPrefix`:
- default `''` in the currentPath middleware;
- `'/demo'` set by the demo autologin middleware (runs only when
  `DEMO_AUTOLOGIN=true`).

`public/js/common.js` — read from the attribute inside the shared wrapper:
```js
async function apiRequest(url, options = {}) {
  const prefix = document.documentElement.getAttribute('data-api-prefix') || '';
  const finalUrl = url.startsWith('/api/') ? prefix + url : url;
  const res = await fetch(finalUrl, { credentials: 'same-origin', /* ... */ });
  // ...
}
```

## Lesson
A variable that is `undefined` in the browser console but present in the
served HTML is the signature of a CSP-blocked inline script. Move the value to
a `data-*` attribute and read it with `getAttribute`. Never add `unsafe-inline`.
