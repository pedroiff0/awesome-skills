#!/usr/bin/env node
// verify-quartz-scripts.mjs
// Downloads the LIVE Quartz `postscript.js`, then `node --check`s every
// `static/scripts/script-N-<hash>.js` it imports. Catches the esbuild
// minifier regex corruption (`\/` -> `/` making `/^\//` -> `/^//`, which
// breaks the whole Promise.all and kills every site button) — a bug that
// `npm run check` and the deploy's permissive transpile BOTH miss.
//
// Usage: node scripts/verify-quartz-scripts.mjs [baseUrl]
//   baseUrl defaults to https://pedroiff0.github.io/page
import { execSync } from "node:child_process";
import { writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const base = process.argv[2] || "https://pedroiff0.github.io/page";

async function get(url) {
  const res = await fetch(url, { redirect: "follow" });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.text();
}

function check(src, label) {
  const f = join(tmpdir(), label.replace(/[^a-z0-9.-]/gi, "_"));
  writeFileSync(f, src);
  try {
    execSync(`node --check ${f}`, { stdio: "pipe" });
    return true;
  } catch {
    return false;
  }
}

(async () => {
  let home;
  try {
    home = await get(`${base}/pt-br/`);
  } catch (e) {
    console.error("Falha ao baixar home:", e.message);
    process.exit(2);
  }
  const post = (home.match(/src="([^"]*postscript[^"]*\.js)"/) || [])[1];
  if (!post) {
    console.error("postscript.js não encontrado no HTML da home");
    process.exit(2);
  }
  const postUrl = post.startsWith("http") ? post : `${base}/${post.replace(/^\.\.\//, "")}`;
  const postSrc = await get(postUrl);
  const scripts = [
    ...new Set(
      [...postSrc.matchAll(/static\/scripts\/script-\d+-[a-f0-9]*\.js/g)].map((m) => m[0]),
    ),
  ];
  if (!scripts.length) {
    console.error("Nenhum static/scripts/script-N encontrado no postscript");
    process.exit(2);
  }
  let bad = 0;
  for (const s of scripts) {
    const url = s.startsWith("http") ? s : `${base}/${s}`;
    let src;
    try {
      src = await get(url);
    } catch (e) {
      console.log(`${s}: FETCH FAIL (${e.message})`);
      bad++;
      continue;
    }
    if (/^\s*<!doctype|<html/i.test(src)) {
      console.log(`${s}: retornou HTML (404?) — provavelmente caminho errado`);
      bad++;
      continue;
    }
    const ok = check(src, s);
    console.log(`${s}: ${ok ? "OK" : "ERRO DE SINTAXE"}`);
    if (!ok) bad++;
  }
  if (bad) {
    console.error(
      `\n${bad} script(s) com problema. O site provavelmente tem botões quebrados (Promise.all do postscript rejeita).`,
    );
    process.exit(1);
  }
  console.log("\nTodos os scripts OK. postscript.js vai importar sem rejeitar Promise.all.");
})();
