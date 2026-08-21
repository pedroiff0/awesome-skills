---
name: document-exports
description: Generate and TEST downloadable document exports (PDF/CSV) from a Node/Express backend — pdfkit streaming, CSV BOM, cents formatting, and the supertest/pdfkit pitfalls that silently break tests.
author: Pandoc / Document Tools Community
---

# Document Exports (PDF / CSV) for Node + Express

Class of work: build a backend endpoint that returns a binary PDF or a text
CSV for download (`Content-Disposition: attachment`), then write a test that
actually verifies the bytes — not just `status === 200`.

Load this skill when the task is "export to PDF", "generate a CSV report",
"statement/extrato as PDF", or any downloadable-file endpoint that must be
tested with supertest/Jest.

## When to use
- PDF generation with `pdfkit` streamed to `res`.
- CSV generation (Excel-pt-BR friendly, BOM, quoted fields).
- Any test that must assert on PDF *content* or CSV *bytes*.

## Stack assumptions
Node, Express, `pdfkit` (PDF), `jest` + `supertest` (tests), Mongoose-style
`userId` scoping. Money is stored/aggregated as integer **cents** (`amountCents`)
— never float. Format to `R$ 1.234,56` or decimal `1234.56` only at render time.

---

## PDF with pdfkit (streamed, do NOT buffer whole file)

Pipe the pdfkit `Document` straight to the response. `pdfkit` is a WritableStream.

```js
const PDFDocument = require('pdfkit');

function gerarExtratoPDF({ usuario, month, resumo, lancamentos }) {
  const doc = new PDFDocument({ margin: 50, size: 'A4', compress: false });
  // ... draw header, summary, table ...
  doc.flushPages();
  return doc; // caller does: doc.pipe(res); doc.end();
}

// controller
const doc = pdfService.gerarExtratoPDF({ /*...*/ });
res.setHeader('Content-Type', 'application/pdf');
res.setHeader('Content-Disposition', `attachment; filename="extrato-${month}.pdf"`);
doc.pipe(res);
doc.end();
```

`compress: false` keeps text readable in the binary (useful for test inspection /
auditing). Set `bufferPages: true` only if you need to draw a footer on every page.

## CSV (Excel pt-BR friendly)

- Emit CRLF line endings (`\r\n`) and a **UTF-8 BOM** so Excel opens acentos
  correctly. Add the BOM **once, in bytes**, at the controller — do NOT prepend
  a BOM character inside the string (double-BOM bug).
- Escape fields containing `, " \n \r` by wrapping in `"..."` and doubling inner
  quotes (`"` → `""`).

```js
function csvEscape(v) {
  const s = String(v ?? '');
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}
// service returns plain text (NO bom):
const conteudo = [cabecalho.join(','), ...linhas].join('\r\n');
return conteudo;
// controller adds BOM in bytes:
const BOM = Buffer.from([0xef, 0xbb, 0xbf]);
res.setHeader('Content-Type', 'text/csv; charset=utf-8');
res.setHeader('Content-Disposition', `attachment; filename="extrato-${month}.csv"`);
res.send(Buffer.concat([BOM, Buffer.from(csv, 'utf-8')]));
```

## Money formatting (cents → string)
```js
function formatarBRL(cents) {
  const neg = cents < 0; const abs = Math.abs(Math.trunc(cents));
  const r = Math.floor(abs / 100), c = abs % 100;
  return `${neg ? '-' : ''}R$ ${r.toLocaleString('pt-BR')},${String(c).padStart(2, '0')}`;
}
function formatarDecimal(cents) { /* 1234.56 with sign */ }
```
Right-align the value column and render it in a **monospace font** (Courier) so
the decimal points line up across rows — this is the "bem diagramado" detail that
makes a statement look professional.

---

## PAGE LAYOUT — known-good footer + pagination pattern

The trap: drawing a footer with `bufferPages` requires `doc.switchToPage(i)` over
`bufferedPageRange()` AFTER all content is added, then `doc.flushPages()`. If you
run the footer loop too early, or let `doc.addPage()` fire inside the body draw,
you get **extra blank pages** and a footer that only says "Página 1 de 1".

Known-good sequence (verified):
1. `doc = new PDFDocument({ bufferPages: true, compress: false })`.
2. Draw everything (header, summary, table). Track a running `y`. Check
   `if (y + rowH > pageBottom) { doc.addPage(); y = topOfBody; redrawHeader(); }`
   BEFORE writing each row.
3. AFTER all rows, compute `const range = doc.bufferedPageRange();`.
4. Loop `for (let i = range.start; i < range.start + range.count; i++) { doc.switchToPage(i); doc.text(\`Página ${i+1} de ${range.count}\`, ...); }`.
5. `doc.flushPages(); return doc;` (caller pipes + ends).

Do NOT call `flushPages()` more than once, and do NOT add a page after the footer
loop unless you re-run it.

### PITFALL: footer `doc.text()` without `lineBreak: false` invents pages
Writing the footer moves the text cursor. At `rodapeY` (near the bottom margin)
the cursor has nowhere to go, so pdfkit **creates a new page per footer line**.
Symptom: a 1-page statement comes out as 3 pages — page 2 contains only
"Pagina 1 de 1", page 3 only "Gerado em ...". Tests pass (status 200, `%PDF`,
phrase present) because none of them count pages.

```js
doc.text(`Pagina ${i + 1} de ${range.count}`, margem, rodapeY,
  { align: 'left',  lineBreak: false, width: larguraUtil });
doc.text(`Gerado em ${geradoEm}`,          margem, rodapeY,
  { align: 'right', lineBreak: false, width: larguraUtil });
```
`lineBreak: false` (plus an explicit `width`) is mandatory for ANY absolutely
positioned text near a page edge — footers, headers, watermarks.

**`lineBreak: false` alone is NOT enough.** If `rodapeY` lands *outside* the
usable box, pdfkit paginates anyway. The footer Y must sit INSIDE the content
area, not below it:
```js
// WRONG — below the bottom margin, still spawns pages
const rodapeY = pageAltura - doc.page.margins.bottom + 14;
// RIGHT — inside the usable area
const rodapeY = pageAltura - doc.page.margins.bottom - 12;
```
Symptom is identical (1 page → 3), so fix both together and re-count pages.

### PITFALL: right-aligned cells truncate to a single letter
Offsetting `x` by the padding AND shrinking `width` by it subtracts the padding
twice; the box gets too narrow for the word and pdfkit renders `VALOR` as `V`.
pdfkit's `align: 'right'` already positions text within the given width — pick
one mechanism, not both.

Write ONE cell helper and use it for header and body, so columns can never
drift apart (this codebase had five copies with padding 16 in some and 12 in
others):
```js
function celula(texto, c, ty, opcoes = {}) {
  const pad = 8;
  doc.text(texto, c.x + pad, ty, {
    width: c.largura - pad * 2,
    align: c.align, lineBreak: false, ellipsis: true, ...opcoes,
  });
}
```
`ellipsis: true` replaces any hand-rolled `truncar()` measuring loop — delete it.

### PITFALL: column too narrow silently wraps to two lines
An ISO date (`2026-08-03`) in a 56pt column wraps, shifting every row below and
destroying the grid. Extracted text shows the tell: `2026-08-\n03`. Use a short
format and widen the column:
```js
const data = new Date(l.date).toLocaleDateString('pt-BR', {
  timeZone: 'UTC', day: '2-digit', month: '2-digit', year: '2-digit',
});
```
`timeZone: 'UTC'` is required — dates stored at `T00:00Z` render one day earlier
in UTC-3 without it. Keep full ISO in the **CSV** (spreadsheets sort it), short
form only in the PDF. After widening a column, re-render and check the longest
real value ("Cartão de crédito", not "Conta").

### NOT A PITFALL: pdfkit's built-in fonts DO render pt-BR accents
An earlier version of this skill claimed `Helvetica`/`Courier` drop accents.
**That is false** — they use WinAnsi encoding and render `ç ã é í ó ê` fine.
Verified in isolation before touching any code:
```bash
node -e "const P=require('pdfkit'),fs=require('fs');const d=new P({compress:false});
d.pipe(fs.createWriteStream('/tmp/a.pdf'));
d.font('Helvetica').fontSize(14).text('Descrição · Usuário · lançamento · Março');d.end();"
sleep 1 && python3 -c "import pymupdf;print(repr(pymupdf.open('/tmp/a.pdf')[0].get_text()))"
# → 'Descrição · Usuário · lançamento · Março'
```
When a generated PDF comes out unaccented, the cause is almost always that the
**source strings were written without accents** (common when a subagent or a
codebase with ASCII-only comments authored them), or that the **seed/database
data itself is unaccented**. Fix the strings, not the font.

Grep both layers before concluding anything about encoding:
```bash
grep -n "doc.text(\|nome: \|rotulo: \|cabecalho = " src/services/pdfService.js
grep -rn "Salario\|Descricao\|periodo\|lancamento" src/seeds/ src/services/
```
General rule: **isolate the suspected component with a 5-line repro before
blaming a library.** A wrong "the library can't do X" note is worse than no
note — it gets cited as a constraint for months after.

### Assert on the RENDERED result, not just the bytes
Status 200 + `%PDF` + a hex-decoded phrase all passed while the PDF had 3 pages,
a truncated `VALOR` column header rendered as `V`, and no accents. Before
calling a PDF export done, extract the real text and eyeball it:
```bash
pip install --break-system-packages pymupdf
python3 -c "
import pymupdf; d=pymupdf.open('/tmp/extrato.pdf')
print('paginas:', d.page_count)
for i,p in enumerate(d): print(f'--- p{i+1} ---'); print(p.get_text())"
```
Check: page count is what you expect, every column header is complete (a header
rendered as a single letter means the column `width` is too narrow), accents are
present, and no page contains only footer text. Counting `/Type /Page` in the
raw bytes is unreliable — use a real parser.

---

## TESTING — the gotchas that silently break assertions

### Gotcha 1: supertest text responses land in `res.text`, NOT `res.body`
For a `text/csv` response, `res.body` stays `{}` (an Object), and
`Buffer.isBuffer(res.body)` is `false`. Read CSV content from **`res.text`**:
```js
const res = await request(app).get('/api/exportacao/extrato.csv?month=2026-03')
  .set(auth(token)).buffer(true);
// res.text is the string (incl. BOM). Build a buffer to check the BOM bytes:
const buf = Buffer.from(res.text, 'utf-8');
expect([buf[0], buf[1], buf[2]]).toEqual([0xef, 0xbb, 0xbf]); // BOM
expect(res.text).toContain('Data,Descricao,...');
```
For binary (PDF), always chain **`.buffer(true)`** so `res.body` is a Buffer;
without it supertest may not collect binary reliably. Then:
```js
const res = await request(app).get('/api/exportacao/extrato.pdf?month=2026...')
  .set(auth(token)).buffer(true);
const buf = Buffer.isBuffer(res.body) ? res.body : Buffer.from(res.body);
expect(buf[0]).toBe(0x25); // '%' → "%PDF"
```

### Gotcha 2: pdfkit embeds text as HEX — naive toString won't find it
pdfkit writes text into the content stream as a hex string operator, e.g.
`[<4e656e68756d206c616e...> -15 <696f646f> 0] TJ`. So
`pdfBuffer.toString('latin1').includes('Nenhum lancamento')` is **false** even
though the text is there. To assert on PDF text, hex-decode every `<...>` block:
```js
function extrairTextoPDF(buffer) {
  const s = buffer.toString('latin1');
  const re = /<([0-9a-fA-F]+)>/g; let m, out = '';
  while ((m = re.exec(s))) out += Buffer.from(m[1], 'hex').toString('latin1');
  return out;
}
expect(extrairTextoPDF(buf)).toContain('Nenhum lancamento no periodo');
```
This is the ONLY reliable way to assert rendered PDF text without a full PDF
parser (pdf-parse/pdfjs) in the test.

### What the tests must cover (minimum)
- PDF: `200`, `Content-Type: application/pdf`, starts with `%PDF`, contains the
  expected phrase (via hex-decode), valid even for an empty period.
- CSV: `200`, `text/csv; charset=utf-8`, BOM bytes present, header row present,
  decimal value format, commas inside a field are quoted.
- `month` invalid (e.g. `2026-13`) → `422` (Zod, not a raw 500).
- No token → `401`.
- **Cross-user isolation**: seed data for user B, request as user A, assert B's
  row is NOT in the output. (This catches the classic scoping bug.)

## Security / architecture reminders
- Scope every query by `userId` from the JWT (`req.user.id`), never from the
  request body/query.
- Validate `month` (YYYY-MM, month 01–12) with Zod → `AppError` 422; never let
  `intervaloDoMes` throw a raw Error that becomes a 500.
- Set `Content-Disposition: attachment` so the file downloads, not renders inline.

## References
- `references/pdfkit-supertest-gotchas.md` — minimal-repro snippets for the four
  test-breaking traps: supertest `res.text` vs `res.body`, pdfkit hex text,
  double-BOM, and the `bufferPages` footer/pagination pattern.
- `scripts/verify-pdf-export.sh` — downloads the PDF over real HTTP (handles
  autologin cookies) and asserts page count, accents, truncated headers and
  wrapped cells. Run it before declaring any PDF export done; the Jest suite
  cannot see these defects.
