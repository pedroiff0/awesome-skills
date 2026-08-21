# Watermark & Provenance Mark Classes

## 1. Edit-Based Invisible Text (Layer A)
Invisible or near-invisible Unicode characters inserted between words, sentences, or tokens:
- Zero-Width Characters: `ZWSP` (U+200B), `ZWNJ` (U+200C), `ZWJ` (U+200D), `WJ` (U+2060), `BOM` (U+FEFF).
- Directional Overrides / BiDi: `LRE`, `RLO`, `LRI`, `RLI`, `PDF`.
- Tag Characters: `U+E0001` - `U+E007F`.
- Variation Selectors: `VS1` - `VS256` (`U+FE00` - `U+FE0F`, `U+E0100` - `U+E01EF`).
- Non-characters & Ignorables: `U+FDD0` - `U+FDEF`, `U+FFFE`, `U+FFFF`.

**Mitigation**: Deterministic Unicode stripping via `scripts/clean_unicode.py` or regex filtering.

---

## 2. Generative / Statistical Token Sampling (Layer B)
Statistical bias injected during next-token generation (e.g., green-list/red-list token partitioning, Kirchenbauer watermarking, Google SynthID-Text tournament sampling):
- The signal is encoded into **word frequency, vocabulary choice, and syntax patterns**, leaving no invisible bytes.

**Mitigation**: Multi-pass paraphrasing, structural restructuring, and semantic rewriting.

---

## 3. Container & File Provenance Metadata (C2PA / EXIF / XMP)
Hard-bound metadata signed into media containers:
- **C2PA / Content Credentials**: JUMBF boxes in JPEG/PNG, signed assertions.
- **EXIF & XMP**: Camera tags, generator metadata, AI software tags.
- **OOXML Document Properties**: `docProps/core.xml`, `customXml` in `.docx`, `.xlsx`, `.pptx`.

**Mitigation**: Stripping metadata tags with `exiftool`, `pandoc`, or zip scrubbers.
