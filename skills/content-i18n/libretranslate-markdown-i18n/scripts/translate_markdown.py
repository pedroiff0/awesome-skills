#!/usr/bin/env python3
"""
Translate a Markdown/Obsidian content tree with LibreTranslate, preserving
markup: frontmatter, headings, emojis, bold/italic, wikilinks (![[...]]/[[...]])
and internal links (pt-br/...). Self-hosted LT at http://localhost:5000.

CUSTOMIZE the 4 constants below, then:
  python3 translate_markdown.py --check
  python3 translate_markdown.py --dry-run            # preview (default)
  python3 translate_markdown.py --apply              # WRITE files
  python3 translate_markdown.py --lang en,es,fr --section media
"""
import argparse
import re
import sys
import time
import urllib.parse
import urllib.request
import json
from pathlib import Path

# ---- CONFIGURE ----
CONTENT_ROOT = Path("/home/pedro/Repositorios/pessoal/page/content")
SRC_LANG = "pt-br"
TARGETS = ["en", "es", "fr"]
SECTIONS = ["media", "research"]   # subdirs under CONTENT_ROOT/<SRC_LANG>/
# ----------------

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
PREFIX_RE = re.compile(r"^(?:#{1,6}\s+|>\s*|[-*]\s+|\d+\.\s+|!\s*)?" + EMOJI_CLASS + r"*")
CALLOUT_RE = re.compile(r"^(>\s*\[!.*?\]\s*)(.*)$")


def lt_translate(text, target, src="pt"):
    if not text.strip():
        return text
    data = urllib.parse.urlencode(
        {"q": text, "source": src, "target": target, "format": "text"}
    ).encode()
    req = urllib.request.Request(
        LT_URL, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())["translatedText"]
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    return text


def protect(text):
    store = {}
    def stash(tok):
        key = f"§{len(store)}§"
        store[key] = tok
        return key
    text = BOLD_RE.sub(lambda m: stash("**" + m.group(1) + "**"), text)
    text = ITAL_RE.sub(lambda m: stash("*" + m.group(1) + "*"), text)
    return text, store


def restore(text, store):
    def repl(m):
        return store.get(f"§{m.group(1)}§", m.group(0))
    return re.sub(r"§\s*(\d+)\s*§", repl, text)


def translate_spans(text, target):
    if not text.strip():
        return text
    protected, store = protect(text)
    return restore(lt_translate(protected, target), store)


def translate_with_links(text, target):
    parts, last = [], 0
    for mm in LINK_RE.finditer(text):
        if mm.start() > last:
            parts.append(translate_spans(text[last:mm.start()], target))
        parts.append(f"[{translate_spans(mm.group(1), target)}]({mm.group(2)})")
        last = mm.end()
    if last < len(text):
        parts.append(translate_spans(text[last:], target))
    return "".join(parts)


def translate_text_preserving_wiki(text, target):
    if not WIKI_RE.search(text):
        return translate_with_links(text, target)
    parts, last = [], 0
    for mm in WIKI_RE.finditer(text):
        if mm.start() > last:
            parts.append(translate_with_links(text[last:mm.start()], target))
        parts.append(mm.group(0))          # wikilink literal, never translated
        last = mm.end()
    if last < len(text):
        parts.append(translate_with_links(text[last:], target))
    return "".join(parts)


def translate_line(line, target):
    if not line.strip():
        return line
    mc = CALLOUT_RE.match(line)
    if mc:
        label, rest = mc.group(1), mc.group(2)
        return label + (translate_text_preserving_wiki(rest, target) if rest.strip() else rest)
    m = PREFIX_RE.match(line)
    if m and m.end() < len(line):
        prefix, rest = line[:m.end()], line[m.end():]
        translated = re.sub(r"^[\-\*\#]\s+", "", translate_text_preserving_wiki(rest, target))
        if not prefix.endswith(" "):
            prefix += " "
        return prefix + translated
    if m and m.end() == len(line):
        return line
    return translate_text_preserving_wiki(line, target)


def translate_body(body, target):
    return "\n".join(translate_line(l, target) for l in body.split("\n"))


def split_frontmatter(md):
    if md.startswith("---"):
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", md, re.S)
        if m:
            return m.group(1), m.group(2)
    return "", md


def list_target_files(section):
    base = CONTENT_ROOT / SRC_LANG / section
    if not base.exists():
        return []
    return [p.relative_to(CONTENT_ROOT / SRC_LANG)
            for p in sorted(base.rglob("*.md")) if p.name != "index.md"]


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
        except Exception as e:
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
            md = (CONTENT_ROOT / SRC_LANG / rel).read_text(encoding="utf-8")
            fm, body = split_frontmatter(md)
            for lang in targets:
                if args.apply:
                    out = CONTENT_ROOT / lang / rel
                    out.parent.mkdir(parents=True, exist_ok=True)
                    out.write_text(f"---\n{fm}\n---\n{translate_body(body, lang)}", encoding="utf-8")
                    print(f"  gravado {lang}/{rel}")
                else:
                    sample = "\n".join(l for l in body.splitlines() if l.strip())[:240]
                    print(f"  [{lang}] {rel}\n    {(translate_text_preserving_wiki(sample, lang) if sample.strip() else '')[:140]}")
        print()
    if args.apply:
        print(f"PRONTO: {total} arquivos x {len(targets)} idiomas gravados.")


if __name__ == "__main__":
    main()
