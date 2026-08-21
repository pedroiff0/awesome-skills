---
name: docker-compose-app-recovery
description: Recover or reset credentials and directly operate the database of an app running under docker-compose (lost admin password, one-time seed password, locked out, read/write app DB). Covers running one-off scripts inside the app container, mongosh pitfalls, and verifying via the live API.
author: DevOps Community
---

# docker-compose-app-recovery

Use this when a user is locked out of a docker-compose app, can't find a password,
needs to reset an admin, or must read/write the app's database directly. The core
insight: **recover by writing to the DB from inside the app container**, reusing the
app's own dependencies (bcrypt + mongodb driver + connection string), then verify
through the live API — not by grepping logs.

## When this fires
- "Qual a senha de admin@example.com?" and the password came from a seed.
- "Perdi a senha do admin / não consigo logar."
- "Preciso resetar a senha / criar um usuário admin."
- "Quero ler/alterar dados no banco do app no docker."

## Steps

1. **Locate the compose project.**
   ```
   find ~ -maxdepth 4 -iname 'docker-compose*.y*ml'
   cd <project>; docker compose ps
   ```
   Confirm which service is the app (`app`, `web`, ...) and the DB (`mongo`, `postgres`, ...).

2. **Map the auth model.** Grep the source for how passwords are set:
   ```
   grep -rniE "seed|admin|password|bcrypt" app/src
   ```
   Read the seed file. Learn: (a) where the password is generated, (b) whether it is
   random and printed ONLY on first creation, (c) the hash lib + rounds (bcryptjs@12,
   argon2, etc.), (d) the user collection name and the discriminator field
   (`role`, `email`, `isAdmin`).

3. **Recoverability check — usually UNRECOVERABLE.** If the account already exists
   (`createdAt` in the past) and the password was a one-time random seed printed only
   at first boot, it is gone:
   - `docker compose logs app` won't have it (it's only printed when `created` is true).
   - `journalctl CONTAINER_NAME=...` usually doesn't retain boot logs across recreations.
   - bcrypt/argon2 are one-way — the stored hash can't be reversed.
   Don't burn time grepping logs. Go straight to reset (step 4).

4. **Reset by writing the DB from INSIDE the app container** (not the host). The app
   container already has the exact bcrypt + mongodb driver and the same `MONGO_URI` —
   reuse them so the hash is 100% compatible with the login path.
   - Write a temp script on the host (see `scripts/reset-password-in-container.js`).
   - Run it via **stdin**, because the host file is NOT mounted at the container's
     `/app` cwd:
     ```
     docker compose exec -T app node - < reset.js
     ```
   - The script: generate a strong password (`crypto.randomBytes(18).toString('base64url')`),
     hash with the SAME lib+rounds the app uses, connect via the app's `MONGO_URI`,
     `updateOne` the user's `passwordHash`, print the new password ONCE.

5. **Verify behaviorally** (most of these repos have no test suite):
   - Inside container: `bcrypt.compare(pw, hash)` → `true`.
   - Live API: `curl -s -X POST http://localhost:<port>/api/auth/login -H 'Content-Type: application/json' -d '{"identifier":"<email>","password":"<pw>"}'` → `200` + JWT.
   - Then `curl -s -b cookie.jar http://localhost:<port>/api/auth/me` → `200` (proves the
     session/cookie path works too).

6. **Cleanup.** Delete the temp script on the host and any `/tmp/hermes-verify-*` files.
   The new password exists only in the chat output and the DB hash — tell the user to
   store it in a password manager; it will NOT appear in `docker compose logs`.

## Pitfalls
- **mongosh has no `-e` flag.** The legacy `mongo` shell did (`mongo db -e '...'`).
  mongosh uses `mongosh <db> --quiet --eval '...'`. Using `-e` throws
  `unrecognized option: -e`.
- **Don't `docker compose exec app node /host/path.js`.** cwd is `/app`; the host file
  isn't there → `MODULE_NOT_FOUND`. Pipe via stdin: `node - < file`.
- **Match the app's exact hash lib + rounds.** If the app uses `bcryptjs@12`, reuse
  `bcryptjs` at 12 rounds — don't swap to node `bcrypt` or `argon2`. The login path
  compares with the app's lib; deviating is fragile even if it "verifies". Running
  inside the app container guarantees you use the app's deps.
- **The seed won't reprint the password on restart.** It only logs on first creation
  (`if (adminSeed.created)`). Telling the user "restart the container to see it" is wrong.
- **Read the login schema before curling.** Zod bodies vary: this app expects
  `{identifier, password}`, not `{email, password}`. Inspect `loginSchema` in
  `app/src/schemas/*` first, or you'll get 400s.
- **Two app containers / wrong DB.** `docker compose exec mongo mongosh` vs `app` — pick
  the right service. Confirm the DB name from `MONGO_URI` (e.g. `academico_db`).

## References
- `references/worked-example-sistema-academico.md` — full real session: one-time seed
  password, where it lived, the reset script, the login body shape, and the end-to-end
  verification. Use as a concrete template.
- `scripts/reset-password-in-container.js` — parameterized reset script. Copy, set
  `URI`, `COLLECTION`, the match filter (`email`/`role`), and run via stdin into the
  app container.
