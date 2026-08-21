#!/usr/bin/env python3
"""
Markup-preserving machine translation for a Quartz/Obsidian vault using a
self-hosted LibreTranslate. Translates content/pt-br/{media,research}/** into
en/es/fr, mirroring slugs, preserving frontmatter + ALL markdown/obsidian markup.

Blinding strategy (see skill SKILL.md + references/libretranslate-notes.md):
  * per-line: strip block prefix + emoji, translate only the text, re-prepend
  * tables: translate CELL BY CELL (never the whole row)
  * bold/italic: convert to <strong>/<em>, call with format=html, revert after
  * wikilinks ![[...]] and internal links (pt-br/...) are never translated
  * placeholders (§N§/ZZ) are intentionally NOT used for bold (engine mangles them)

Usage:
  python3 translate_quartz.py --check
  python3 translate_quartz.py --dry-run                 # preview (default)
  python3 translate_quartz.py --apply --section media --lang en,es,fr
"""
import argparse
import re
import sys
import time
import urllib.parse
import urllib.request
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]   # repo root (this script lives in tools/)
CONTENT = ROOT / "content"
SRC = "pt-br"
TARGETS = ["en", "es", "fr"]
SECTIONS = ["media", "research"]
LT_URL = "http://localhost:5000/translate"

EMOJI_CLASS = (
    r"[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    r"\U00002190-\U000021FF\U00002B00-\U00002BFF\U0000FE00-\U0000FE0F"
    r"\U00002700-\U000027BF\u200d\u20e3]"
)
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITAL_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
WIKI_RE = re.compile(r"!?\[\[[^\]]+\]\]")
LINK_RE = re.compile(r"\[([^\]]*)\]\((pt-br/[^)]+)\)")
PREFIX_RE = re.compile(
    r"^(?:#{1,6}\s+|>\s*|[-*]\s+|\d+\.\s+|!\s*)?" + EMOJI_CLASS + r"*"
)
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:\-|]+\|\s*$")  # | :--- | :--- |
CALLOUT_RE = re.compile(r"^(>\s*\[!.*?\])\s*(.*)$")


def lt_translate(text: str, target: str, fmt="text", src="pt") -> str:
    if not text.strip():
        return text
    data = urllib.parse.urlencode({
        "q": text, "source": src, "target": target, "format": fmt,
    }).encode()
    req = urllib.request.Request(LT_URL, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())["translatedText"]
        except Exception:  # noqa
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    return text


def protect(text: str):
    """bold/italic -> HTML (LT preserves in format=html); wikilinks stashed."""
    store = {}

    def stash(tok):
        key = f"§{len(store)}§"
        store[key] = tok
        return key

    text = WIKI_RE.sub(lambda m: stash(m.group(0)), text)
    text = BOLD_RE.sub(lambda m: f"<strong>{m.group(1)}</strong>", text)
    text = ITAL_RE.sub(lambda m: f"<em>{m.group(1)}</em>", text)
    usa_html = ("<strong>" in text) or ("<em>" in text) or ("<br" in text)
    return text, store, usa_html


def restore(text: str, store: dict) -> str:
    def repl(m):
        return store.get(f"§{m.group(1)}§", m.group(0))

    text = re.sub(r"§(\d+)§", repl, text)
    text = re.sub(r"<\s*strong\s*>", "**", text)
    text = re.sub(r"<\s*/\s*strong\s*>", "**", text)
    text = re.sub(r"<\s*em\s*>", "*", text)
    text = re.sub(r"<\s*/\s*em\s*>", "*", text)
    text = re.sub(r"<\s*br\s*/?\s*>", "<br>", text)
    return text


def translate_spans(text: str, target: str) -> str:
    if not text.strip():
        return text
    protected, store, usa_html = protect(text)
    out = lt_translate(protected, target, fmt="html" if usa_html else "text")
    return restore(out, store)


def translate_with_links(text: str, target: str) -> str:
    parts, last = [], 0
    for mm in LINK_RE.finditer(text):
        if mm.start() > last:
            parts.append(translate_spans(text[last:mm.start()], target))
        anchor = translate_spans(mm.group(1), target)
        parts.append(f"[{anchor}]({mm.group(2)})")
        last = mm.end()
    if last < len(text):
        parts.append(translate_spans(text[last:], target))
    return "".join(parts)


def translate_text_preserving_wiki(text: str, target: str) -> str:
    if not WIKI_RE.search(text):
        return translate_with_links(text, target)
    parts, last = [], 0
    for mm in WIKI_RE.finditer(text):
        if mm.start() > last:
            parts.append(translate_with_links(text[last:mm.start()], target))
        parts.append(mm.group(0))
        last = mm.end()
    if last < len(text):
        parts.append(translate_with_links(text[last:], target))
    return "".join(parts)


def translate_line(line: str, target: str) -> str:
    if not line.strip():
        return line
    if TABLE_ROW_RE.match(line):
        if TABLE_SEP_RE.match(line):
            return line
        cells = [c for c in line.strip().strip("|").split("|")]
        translated = [translate_text_preserving_wiki(c, target) for c in cells]
        return "| " + " | ".join(translated) + " |"
    mc = CALLOUT_RE.match(line)
    if mc:
        label, rest = mc.group(1), mc.group(2)
        return label + (translate_text_preserving_wiki(rest, target) if rest.strip() else rest)
    m = PREFIX_RE.match(line)
    if m and m.end() < len(line):
        prefix, rest = line[:m.end()], line[m.end():]
        translated = translate_text_preserving_wiki(rest, target)
        translated = re.sub(r"^[\-\*\#]\s+", "", translated)
        if not prefix.endswith(" "):
            prefix += " "
        return prefix + translated
    if m and m.end() == len(line):
        return line
    return translate_text_preserving_wiki(line, target)


def translate_body(body: str, target: str) -> str:
    return "\n".join(translate_line(l, target) for l in body.split("\n"))


def split_frontmatter(md: str):
    if md.startswith("---"):
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", md, re.S)
        if m:
            return m.group(1), m.group(2)
    return "", md


def list_target_files(section: str):
    files = []
    base = CONTENT / SRC / section
    if not base.exists():
        return files
    for p in sorted(base.rglob("*.md")):
        if p.name == "index.md":
            continue
        files.append(p.relative_to(CONTENT / SRC))
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--lang", default=",".join(TARGETS))
    ap.add_argument("--section", default=",".join(SECTIONS))
    args = ap.parse_args()

    if args.check:
        try:
            print("LT OK ->", lt_translate("Olá mundo de teste!", "en"))
        except Exception as e:  # noqa
            print("LT FALHOU:", e); sys.exit(1)
        return

    targets = [t for t in args.lang.split(",") if t in TARGETS]
    sections = [s for s in args.section.split(",") if s in SECTIONS]
    if not args.apply:
        print("[DRY-RUN] nenhum arquivo gravado. Use --apply para gravar.\n")

    total = 0
    for section in sections:
        files = list_target_files(section)
        print(f"== secao '{section}': {len(files)} arquivos ==")
        for rel in files:
            total += 1
            md = (CONTENT / SRC / rel).read_text(encoding="utf-8")
            fm, body = split_frontmatter(md)
            for lang in targets:
                if args.apply:
                    translated = translate_body(body, lang)
                    out_path = CONTENT / lang / rel
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    out_path.write_text(f"---\n{fm}\n---\n{translated}", encoding="utf-8")
                    print(f"  gravado {lang}/{rel}")
                else:
                    sample = "\n".join(l for l in body.splitlines() if l.strip())[:240]
                    prev = translate_text_preserving_wiki(sample, lang) if sample.strip() else ""
                    print(f"  [{lang}] {rel}\n    {prev[:140]}")
        print()
    if args.apply:
        print(f"PRONTO: {total} arquivos x {len(targets)} idiomas gravados.")


if __name__ == "__main__":
    main()
