---
name: express-csp-runtime-config
description: "How to pass server-side runtime config (API prefix, feature flags, user id, CSRF token) from an Express/EJS app to client JS when a strict Content-Security-Policy is in force (helmet default scriptSrc self, with no unsafe-inline). Use this whenever you need to inject a value the browser JS must read at runtime, but adding a script tag triggers a silent CSP block."
---

# Express + strict CSP: injecting runtime config to the client

## When this applies
- Express app rendering EJS (or any server template) with helmet CSP.
- scriptSrc includes only 'self' (the template default) — there is NO
  'unsafe-inline'. This is the secure default and must NOT be relaxed to
  "fix" a script.
- You need a value computed server-side (API path prefix, feature flag,
  locale, CSRF token, demo vs prod marker) available to a .js file served
  from /js/.

## The trap (what happened in a real session)
Injecting the value via an inline script in the EJS head:
```ejs
<script>window.__API_PREFIX__ = '<%= apiPrefix %>';</script>
```
looks correct and even appears in the served HTML — but the browser silently
drops the inline script because the CSP forbids unsafe-inline. Result:
window.__API_PREFIX__ is undefined, the client JS never applies the prefix,
and you get cryptic failures elsewhere (e.g. every API call hits the wrong
backend → 401 Token invalido, with no console error pointing at the cause).
The HTML source (curl) shows the script; the live DOM shows undefined. That
gap IS the fingerprint of a CSP-blocked inline script.

## The pattern that works
Put the value in a data-* attribute on <html> (or <body>), and read it
from the served JS via getAttribute. No inline script, so CSP is happy.

In the EJS layout (views/partials/header.ejs or equivalent):
```ejs
<html lang="pt-BR" data-api-prefix="<%= typeof apiPrefix !== 'undefined' ? apiPrefix : '' %>">
```

In the served JS (public/js/common.js):
```js
async function apiRequest(url, options = {}) {
  const prefix = document.documentElement.getAttribute('data-api-prefix') || '';
  const finalUrl = url.startsWith('/api/') ? prefix + url : url;
  // ... fetch(finalUrl, ...)
}
```

## Diagnosis checklist when "it works via curl but the browser shows undefined"
1. curl the page and grep for the injected value — if present in HTML but
   typeof window.X is undefined in the browser console, the value was in an
   inline script blocked by CSP.
2. Open DevTools → Network/Console: a blocked inline script logs
   "Refused to execute inline script because it violates CSP" (sometimes only
   in the browser console, not surfaced as a JS error).
3. Fix: move the data to a data-* attribute; read it with getAttribute.

## Rules
- NEVER add 'unsafe-inline' to scriptSrc to make an inline script work.
  Move the data to an attribute instead. This is also an explicit project rule
  in many AGENTS.md files ("no inline scripts — CSP has no unsafe-inline").
- Keep the default maxAge for static assets in production (e.g. 1h), but set
  it to 0 in staging/demo so a rebuild does not leave stale JS in the browser
  during verification.

## Reference
See references/financas-app-example.md for the exact before/after from the
financas-app project (demo served under /demo with API prefix injected via
data-api-prefix.
