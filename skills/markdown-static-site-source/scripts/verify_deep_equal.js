#!/usr/bin/env node
/* Generalized deep-equal verifier for two JS data files that assign a global.
 * Usage: node verify_deep_equal.js ORIG.js GENERATED.js [VARNAME]
 * Exit 0 = semantically equal; Exit 1 = difference.
 * NOTE: a byte `diff` is a FALSE POSITIVE here — only the parsed object matters.
 */
'use strict';
const fs = require('fs');

function load(file, varName) {
  const src = fs.readFileSync(file, 'utf8');
  const vn = varName || (src.match(/window\.([A-Z_]+)\s*=/) || [, 'X'])[1];
  const fn = new Function('window', src + `\nreturn window.${vn};`);
  const win = {};
  fn(win);
  return win[vn];
}

function deepEqual(a, b) {
  if (a === b) return true;
  if (a === null || b === null) return a === b;
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    return a.every((x, i) => deepEqual(x, b[i]));
  }
  if (typeof a === 'object' && typeof b === 'object') {
    const ka = Object.keys(a), kb = Object.keys(b);
    if (ka.length !== kb.length) return false;
    return ka.every(k => Object.prototype.hasOwnProperty.call(b, k) && deepEqual(a[k], b[k]));
  }
  return false;
}

const [, , origPath, genPath, vn] = process.argv;
if (!origPath || !genPath) {
  console.error('uso: node verify_deep_equal.js ORIG.js GENERATED.js [VARNAME]');
  process.exit(2);
}
const a = load(origPath, vn), b = load(genPath, vn);
if (deepEqual(a, b)) {
  console.log('OK: objetos semanticamente iguais.');
  process.exit(0);
} else {
  console.error('DIFERENCA: objetos divergem.');
  process.exit(1);
}
