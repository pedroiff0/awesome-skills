---
name: docx-analysis-conversion
description: "Extract, analyze, edit, and convert Microsoft Word (.docx) documents to structured Markdown, JSON, or clean text preserving tables, headers, and bullet lists."
version: 1.0.0
author: Pedro Henrique Rocha de Andrade
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [docx, word, document-conversion, pandoc, python-docx]
    related_skills: [document-exports, nano-pdf]
---

# DOCX Analysis & Markdown Conversion

Extract structured content, metadata, and tables from Word (`.docx`) documents for AI processing and analysis.

## When to Use

- Analyzing business reports, contracts, or documentation provided in `.docx` format.
- Converting `.docx` to Markdown while maintaining headers and table structures.
- Generating new `.docx` files programmatically from Markdown source.

## Recommended Tools

```bash
# Convert DOCX to clean GitHub Flavored Markdown using pandoc
pandoc -f docx -t gfm input.docx -o output.md --extract-media=./media
```
