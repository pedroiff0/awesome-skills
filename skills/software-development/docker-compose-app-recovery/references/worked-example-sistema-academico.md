# Worked example — sistema-academico (IFF)

## Situation
User asked: "Qual é a senha de admin@admin.com no sistema-academico docker compose logs app".
The admin account existed (`createdAt: 2026-08-02`), so the password was a one-time
random seed printed only at first boot and was UNRECOVERABLE from logs.

## Where the password lived
`app/src/seeds/admin.seed.js`:
- `ADMIN_EMAIL = 'admin@admin.com'`
- `generateStrongPassword()` = `crypto.randomBytes(18).toString('base64url')` (24 chars, ~144 bits)
- `bcrypt.hash(password, SALT_ROUNDS)` with `SALT_ROUNDS = 12`, using `bcryptjs`
- Printed ONCE in `server.js` only when `seedAdminIfEmpty()` returns `created: true`:
  ```
  if (adminSeed.created) {
    console.log('Conta admin criada (unica vez - guarde esta senha agora):');
    console.log(`  Senha:  ${adminSeed.password}`);
  }
  ```
- Collected via `app/src/middleware/auth.js` / `pageAuth.js` (admin = support account).

## Logs confirmed empty
```
docker compose logs app   # only: Conectado ao MongoDB / [seed] 90 disciplina(s) /
                          # Planilha importada / Servidor escutando na porta 5010
journalctl CONTAINER_NAME=sistema-academico-app-1   # no password line retained
```

## Reset (run inside the app container)
Host file `reset-admin-pass.js`, executed via stdin (host not mounted at /app):
```
docker compose exec -T app node - < reset-admin-pass.js
```
Script did: generate pw, `bcrypt.hash(pw, 12)`,
`MongoClient('mongodb://mongo:27017/academico_db')`,
`db.users.updateOne({email:'admin@admin.com', role:'admin'}, {$set:{passwordHash, updatedAt:new Date()}})`.
Result: `matchedCount=1 modifiedCount=1`. New password e.g. `CRL6nvPyT8Mj-rDzlzIRJ0P3`.

## Verify behaviorally (no test suite in repo)
1. Inside container: `bcrypt.compare(pw, hash)` -> `true`.
2. Live login — body shape from `app/src/schemas/auth.schemas.js` `loginSchema`:
   `{ identifier: z.string(), password: z.string() }` (NOT `{email,password}`).
   Route: `POST /api/auth/login` (auth.routes.js).
   ```
   curl -s -c cj.txt -X POST http://localhost:4445/api/auth/login \
     -H 'Content-Type: application/json' \
     -d '{"identifier":"admin@admin.com","password":"CRL6nvPyT8Mj-rDzlzIRJ0P3"}'
   # -> 200, { user:{role:'admin',...}, token:'eyJ...' }
   curl -s -b cj.txt http://localhost:4445/api/auth/me
   # -> 200, same admin identity (proves cookie/session path too)
   ```
3. Cleanup: `rm -f reset-admin-pass.js` and any `/tmp/hermes-verify-*`.

## mongosh pitfall hit
`docker compose exec mongo mongosh academico_db -e '...'` ->
`MongoshUnimplementedError: unrecognized option: -e`. Fix: `mongosh academico_db --quiet --eval '...'`.

## Note
AGENTS.md for this repo claims the admin/professor cluster was "removed in 2026-08-03",
but the admin seed (`admin@admin.com`) still exists and is active in code + DB. The
AGENTS.md statement is stale on this point — don't trust it blindly; verify against the
actual source and DB.
