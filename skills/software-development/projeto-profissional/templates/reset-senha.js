/* Redefine a senha de um usuario pela linha de comando.
 *
 * Serve para o caso classico de perder o acesso ao admin: o seed nao recria
 * usuario que ja existe, entao sem isto a unica saida seria mexer no banco na
 * mao — e hash de senha escrito a mao e como se acerta o pe na porta.
 *
 *   docker compose -p <proj> exec -T app node scripts/reset-senha.js <email> [senha]
 *
 * Sem a senha no argumento, gera uma forte e imprime uma unica vez. A senha
 * nunca aparece em log da aplicacao, so no stdout deste comando.
 *
 * ATENCAO ao copiar para um projeto derivado: o container roda com rootfs
 * read-only, entao `docker compose cp` falha com "container rootfs is marked
 * read-only". O script precisa entrar na IMAGEM — commite o arquivo e rode
 * `docker compose -p <proj> up -d --build app`.
 */
const crypto = require('crypto');
const mongoose = require('mongoose');
const env = require('../src/config/env');
const User = require('../src/models/user.model');
const authService = require('../src/services/authService');

const [email, senhaArg] = process.argv.slice(2);

if (!email) {
  console.error('uso: node scripts/reset-senha.js <email> [senha]');
  process.exit(1);
}

// Senha gerada: 24 chars base64url, sem caractere que atrapalhe copiar/colar.
const senha = senhaArg || crypto.randomBytes(18).toString('base64url');

(async () => {
  await mongoose.connect(env.mongoUri);

  const user = await User.findOne({ email: email.toLowerCase().trim() });
  if (!user) {
    console.error(`usuario '${email}' nao encontrado em ${env.mongoUri.split('/').pop()}`);
    await mongoose.disconnect();
    process.exit(1);
  }

  user.passwordHash = await authService.hashPassword(senha);
  // Reabilita quem tenha sido bloqueado por tentativas e limpa reset pendente.
  user.mustChangePassword = false;
  user.failedLoginAttempts = 0;
  user.lockUntil = undefined;
  user.passwordResetToken = undefined;
  user.passwordResetExpires = undefined;
  await user.save();

  console.log(`\nsenha redefinida para ${user.email} (${user.role})`);
  if (!senhaArg) console.log(`nova senha: ${senha}\n`);

  await mongoose.disconnect();
})().catch(async (err) => {
  console.error('falhou:', err.message);
  await mongoose.disconnect().catch(() => {});
  process.exit(1);
});
