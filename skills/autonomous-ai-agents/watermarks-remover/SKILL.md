---
name: watermarks-remover
description: "Strip multi-vendor AI provenance marks, invisible Unicode characters (ZWSP, ZWNJ, Bidi, variation selectors), statistical text watermarks, and C2PA/EXIF/XMP metadata from files (PNG, JPEG, PDF, DOCX, MD, TXT)."
version: 1.0.0
author: Guillaume Meyer & Pedro Henrique Rocha de Andrade
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [watermarks, ai-hygiene, unicode, c2pa, exif, privacy, synthid]
    related_skills: [security-sast-audit, docx-analysis-conversion]
---

# Multi-Vendor AI Watermark & Provenance Remover

> **Purity rules**: Open hygiene and privacy tool for user-owned content. No proprietary keys or closed endpoints embedded.

This skill strips **multi-vendor AI provenance marks** from text and document files, covering invisible Unicode injection (Layer A), statistical sampling watermarks (Layer B), and signed C2PA / EXIF / XMP container metadata.

---

## When to Use

- Stripping invisible Unicode characters (`ZWSP`, `ZWNJ`, `VS16`, BiDi controls) from AI-generated text or copy.
- Cleaning signed C2PA / Content Credentials and EXIF/XMP metadata from images and documents.
- Sanitizing Markdown, DOCX, PDF, or text files for clean publishing and privacy hygiene.
- Triggered by requests like *"remove AI watermarks"*, *"clean invisible unicode"*, *"strip C2PA"*, or `/remove-ai-marks`.

---

## Architecture & Layers

```
┌────────────────────────────────────────────────────────────────────────────┐
│                             INPUT ARTIFACT                                 │
└──────────────────────┬───────────────────────────────┬─────────────────────┘
                       │                               │
             [Text / Code / Markdown]        [Media & Document Files]
                       │                               │
                       ▼                               ▼
       ┌───────────────────────────────┐ ┌───────────────────────────┐
       │   LAYER A: Invisible Unicode  │ │   LAYER C: Container Meta │
       │ (ZWSP, Tags, BiDi, Selectors) │ │ (C2PA, EXIF, XMP, OOXML)  │
       │   -> scripts/clean_unicode.py │ │   -> exiftool / zip scrub │
       └───────────────┬───────────────┘ └─────────────┬─────────────┘
                       │                               │
                       ▼                               │
       ┌───────────────────────────────┐               │
       │   LAYER B: Statistical Tokens │               │
       │   (SynthID, Green-list LLM)   │               │
       │   -> Paraphrase / Rewrite     │               │
       └───────────────┬───────────────┘               │
                       │                               │
                       └───────────────┬───────────────┘
                                       ▼
                              CLEANED ARTIFACT
```

---

## 1. Quick Layer A Text Cleaning (Deterministic)

Use the included helper script to strip invisible Unicode code points from any text or file:

```bash
# Clean a file in-place
python3 skills/autonomous-ai-agents/watermarks-remover/scripts/clean_unicode.py -i document.md

# Pipe through stdin / stdout
cat input.txt | python3 skills/autonomous-ai-agents/watermarks-remover/scripts/clean_unicode.py > clean.txt
```

---

## 2. Remote / Service Cleaning (HTTP API)

When connected to a `watermarks-remover` HTTP service (`http://127.0.0.1:8765`):

```bash
WM="${WATERMARKS_SERVICE_URL:-http://127.0.0.1:8765}"

# 1. Inspect file for invisible marks and metadata
curl -s -X POST "$WM/inspect" -H 'Content-Type: application/json' \
  -d "{\"file\": \"$(base64 < notes.md | tr -d '\n')\", \"name\": \"notes.md\"}"

# 2. Clean file and receive sanitized payload
curl -s -X POST "$WM/clean" -H 'Content-Type: application/json' \
  -d "{\"file\": \"$(base64 < notes.md | tr -d '\n')\", \"name\": \"notes.md\"}"
```

---

## 3. Metadata Stripping (C2PA / EXIF)

```bash
# Strip EXIF and C2PA metadata from images
exiftool -all= -overwrite_original image.png

# Re-encode image to drop auxiliary signed chunks
ffmpeg -i input.png -map_metadata -1 -c:v png output.png
```

---

## References

- [Mark Classes Guide](references/mark-classes.md) — Breakdown of edit-based, statistical, and container marks.
- [Vendor Notes](references/vendor-notes.md) — Claude, Gemini (SynthID), OpenAI, and open LLM notes.
- Standalone Python cleaner: `scripts/clean_unicode.py`.
