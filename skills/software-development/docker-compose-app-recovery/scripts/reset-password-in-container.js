// Reset an app user's password by writing the DB from INSIDE the app container.
// Run with:  docker compose exec -T app node - < this-file.js
// (host file is NOT mounted at /app; stdin is how the container's node reads it)
//
// Prereqs (already present in the app container): bcryptjs + mongodb driver,
// and the same MONGO_URI the app uses. Reuse the app's deps so the hash matches
// the login path exactly.
//
// ADJUST THESE to the target app:
const URI = 'mongodb://mongo:27017/academico_db'; // from docker-compose MONGO_URI
const COLLECTION = 'users';
const MATCH = { email: 'admin@admin.com', role: 'admin' }; // discriminator field(s)
const SALT_ROUNDS = 12; // MUST match the app's seed (e.g. bcryptjs @ 12)

const crypto = require('crypto');
const bcrypt = require('bcryptjs');
const { MongoClient } = require('mongodb');

(async () => {
  const password = crypto.randomBytes(18).toString('base64url'); // 24 chars, ~144 bits
  const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
  const client = new MongoClient(URI);
  await client.connect();
  const res = await client.db().collection(COLLECTION).updateOne(
    MATCH,
    { $set: { passwordHash, updatedAt: new Date() } }
  );
  await client.close();
  if (res.matchedCount === 0) {
    console.error('USUARIO_NAO_ENCONTRADO');
    process.exit(2);
  }
  console.log('=== SENHA NOVA GERADA ===');
  console.log('match:', JSON.stringify(MATCH));
  console.log('Senha:', password);
  console.log('matched=' + res.matchedCount + ' modified=' + res.modifiedCount);
})().catch(e => { console.error('ERRO:', e.message); process.exit(1); });
