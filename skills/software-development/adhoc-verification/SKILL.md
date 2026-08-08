---
name: adhoc-verification
description: Produce fresh, focused, local verification evidence for a code change without relying on the full test suite. Use when a system reminder (or the user) demands ad-hoc verification after an edit, or when you want to prove one behavior in isolation. Covers the correct way to write a throwaway supertest/harness script against a Jest-coupled app, and the pitfalls that silently give false passes.
---

# Ad-hoc local verification harness

Use this when you need to *prove* a specific change works, the full suite is
slow/irrelevant, or a post-edit system reminder demands "fresh passing
verification evidence." This is NOT a substitute for `npm test` when the suite
is fast — prefer the canonical suite. But a focused harness is the right tool
for one targeted behavior, or to satisfy a reminder cheaply.

## When to reach for this
- A `system` reminder asks for ad-hoc verification of changed paths.
- You changed one middleware/route and want a 10-second check instead of the
  full 30s suite.
- You need to demonstrate a *negative* property (e.g. "instance B rejects a
  cookie minted by instance A") that the suite doesn't isolate.

## Steps
1. **Write the script INSIDE the package directory** (e.g. `app/`), never in
   `/tmp`. A script in `/tmp` cannot resolve the project's `node_modules/`
   (`require('supertest')` → `MODULE_NOT_FOUND`). Name it `./hermes-verify-*.js`
   so it's obviously throwaway and matches the reminder's prefix suggestion.
2. **No Jest globals.** `describe`/`it`/`beforeAll`/`afterAll` are undefined in
   a plain `node` run — they crash with `ReferenceError`. Instead wrap everything
   in an async IIFE and call the project's own DB setup/teardown helpers
   manually (e.g. `setupDb()`, `teardownDb()`, `clearDb()` from the test
   helpers), inside `try/finally`.
3. **Require the app factory, set env first.** Set `process.env.*` (NODE_ENV,
   JWT_SECRET, feature flags) BEFORE `require('./src/app')`, because the app
   reads flags at construction time. If you re-instantiate with different env,
   restore the prior env after, or build each instance in its own closure.
4. **Drive with supertest**: `await request(app).get('/path').set('Cookie', ...)`.
   Assert on `res.status` and `res.text`/body. Print `PASS:`/`FAIL:` lines and
   `process.exit(nonZeroOnFailure)`.
5. **Run, then delete**: `node ./hermes-verify-x.js` then `rm ./hermes-verify-x.js`.

## Critical pitfall: single-instance masking of isolation bugs
A SINGLE app instance with a feature flag on will apply that middleware to ALL
matching paths — so "isolation" between two security contexts cannot be shown
with one instance. To verify that instance A ignores/rejects a token from
instance B (different secret/cookie), you MUST build TWO separate `createApp()`
instances, each with its own env, and:
- mint a "foreign" cookie by signing a JWT with a *different* secret than the
  instance under test (`jwt.sign(payload, 'other-secret-32+', ...)`);
- assert the instance UNDER TEST ignores/overwrites it (e.g. demo autologin
  returns 200 despite a foreign cookie) AND that the instance WITHOUT autologin
  rejects it (redirects / 401).

If you test "isolation" with one instance you'll get a false PASS.

## Skeleton (see references/express-supertest-recipe.md)
A copyable starter lives in `references/express-supertest-recipe.md`; a template
file is in `scripts/template-harness.js`.

## Relation to other skills
- Distinct from `test-driven-development` (RED-GREEN-REFACTOR workflow) and
  `systematic-debugging` (root-cause finding). This is about *proving a fix*
  after the fact. If the three overlap for the curator, consolidation is fine —
  but keep the /tmp-resolution, no-Jest-globals, and two-instance pitfalls.
- For visual/CSS changes use `frontend-visual-verification` (browser) instead.
