# pdfkit + supertest: concrete reproduction notes

Captured while building a monthly financial statement export (PDF + CSV) in a
Node/Express app tested with jest + supertest. These are the minimal repro
snippets that prove each gotcha.

## 1. supertest: text body is in res.text, not res.body

Real failure: `Buffer.isBuffer(res.body)` was `false` for a `text/csv` response
and `res.body` was `{}`. `Buffer.from(res.body)` threw
"first argument must be of type string or Buffer... Received an instance of Object".

Fix: read CSV from `res.text` (string). For binary, chain `.buffer(true)`.

```js
const res = await request(app).get('/api/exportacao/extrato.csv?month=2026-03')
  .set(auth(token)).buffer(true);
console.log('isBuf', Buffer.isBuffer(res.body), 'bodyType', typeof res.body,
            'textLen', res.text && res.text.length);
// isBuf false bodyType object textLen 43   <- CSV text is in res.text
```

## 2. pdfkit text is hex-encoded in the content stream

`pdfBuffer.toString('latin1').includes('Nenhum lancamento')` -> false, even for a
real PDF. The content stream looks like:
`1 0 0 1 171.6 484.1 Tm /F1 11 Tf [<4e656e68756d206c616e63616d656e746f206e6f20706572> -15 <696f646f> 0] TJ`

Hex-decode `<...>` blocks to recover the text:
```js
function extrairTextoPDF(buffer) {
  const s = buffer.toString('latin1');
  const re = /<([0-9a-fA-F]+)>/g;
  let m, out = '';
  while ((m = re.exec(s))) out += Buffer.from(m[1], 'hex').toString('latin1');
  return out;
}
```

## 3. Double-BOM bug

If the CSV service returns a string already prefixed with `\uFEFF` AND the
controller also prepends a BOM `Buffer`, the output has the BOM twice. Keep the
BOM only at the controller (bytes); service returns plain text.

## 4. bufferPages footer pattern (verified correct)

The footer loop must run AFTER all content and use `bufferedPageRange()`:
```js
const doc = new PDFDocument({ margin: 50, size: 'A4', bufferPages: true, compress: false });
// ... draw content, addPage() as needed for row overflow ...
const range = doc.bufferedPageRange();
for (let i = range.start; i < range.start + range.count; i++) {
  doc.switchToPage(i);
  doc.font('Helvetica').fontSize(8).fillColor('#64748b');
  doc.text(`Pagina ${i + 1} de ${range.count}`, 50, 800, { align: 'left' });
}
doc.flushPages();
```
Running the footer loop BEFORE content finished, or letting an unguarded
`doc.addPage()` fire inside the body draw, produced 3 blank pages for a 4-row
table and a "Pagina 1 de 1" footer only on page 1. Always gate row overflow with
`if (y + rowH > pageBottom) { doc.addPage(); y = topOfBody; redrawHeader(); }`
before writing the row.
