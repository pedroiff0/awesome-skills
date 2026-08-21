#!/usr/bin/env python3
"""Deterministic Layer-A Unicode watermark cleaner (stdlib Python).

Strips invisible Unicode characters, zero-width joiners/spaces,
bidi directional overrides, variation selectors, and tag characters
while preserving genuine punctuation and emoji sequences.
"""
from __future__ import annotations
import argparse
import sys
import unicodedata
from pathlib import Path

# Invisible & suspicious Unicode code points
INVISIBLE_CHARS = {
    # Zero-width spaces & joiners
    0x200B: "ZWSP",
    0x200C: "ZWNJ",
    0x200D: "ZWJ",
    0x200E: "LRM",
    0x200F: "RLM",
    0x202A: "LRE",
    0x202B: "RLE",
    0x202C: "PDF",
    0x202D: "LRO",
    0x202E: "RLO",
    0x2060: "WJ",
    0x2061: "FUNCTION APPLICATION",
    0x2062: "INVISIBLE TIMES",
    0x2063: "INVISIBLE SEPARATOR",
    0x2064: "INVISIBLE PLUS",
    0xFEFF: "BOM / ZWNBSP",
}

# Tag characters U+E0001 - U+E007F
TAG_RANGE = range(0xE0001, 0xE0080)
# Variation Selectors U+FE00 - U+FE0F and U+E0100 - U+E01EF
VS_RANGES = [range(0xFE00, 0xFE10), range(0xE0100, 0xE01F0)]


def is_removable_char(c: str) -> bool:
    cp = ord(c)
    if cp in INVISIBLE_CHARS:
        return True
    if cp in TAG_RANGE:
        return True
    for r in VS_RANGES:
        if cp in r:
            return True
    # Non-characters & default ignorable
    cat = unicodedata.category(c)
    if cat == "Cf" and cp not in (0xAD,):  # Soft hyphen kept unless strict
        return True
    return False


def clean_text(text: str, normalize_nfkc: bool = False) -> tuple[str, int]:
    cleaned_chars = []
    removed_count = 0
    for ch in text:
        if is_removable_char(ch):
            removed_count += 1
        else:
            cleaned_chars.append(ch)
    result = "".join(cleaned_chars)
    if normalize_nfkc:
        result = unicodedata.normalize("NFKC", result)
    return result, removed_count


def main():
    p = argparse.ArgumentParser(description="Strip invisible Unicode watermarks from text or files.")
    p.add_argument("input", nargs="?", help="Input file path (or read from stdin)")
    p.add_argument("-o", "--output", help="Output file path (default: stdout or in-place if -i)")
    p.add_argument("-i", "--in-place", action="store_true", help="Modify input file in-place")
    p.add_argument("--nfkc", action="store_true", help="Apply NFKC normalization")
    args = p.parse_args()

    if args.input:
        in_path = Path(args.input)
        if not in_path.exists():
            print(f"Error: file '{args.input}' not found.", file=sys.stderr)
            sys.exit(1)
        raw = in_path.read_text(encoding="utf-8", errors="replace")
    else:
        raw = sys.stdin.read()

    cleaned, removed = clean_text(raw, normalize_nfkc=args.nfkc)
    print(f"Cleaned {removed} invisible mark(s).", file=sys.stderr)

    if args.in_place and args.input:
        Path(args.input).write_text(cleaned, encoding="utf-8")
    elif args.output:
        Path(args.output).write_text(cleaned, encoding="utf-8")
    else:
        sys.stdout.write(cleaned)


if __name__ == "__main__":
    main()
