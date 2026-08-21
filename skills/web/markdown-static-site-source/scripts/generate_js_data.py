#!/usr/bin/env python3
"""Generalized MD(frontmatter YAML) -> JS data-file generator.

Adapt `normalize(data)` to map your MD schema onto the SAME object shape the
site's render engine expects (see the original data.js). Emits valid JS, not
YAML. The consumer (main.js/index.html) is NEVER touched, so render is identical.

Usage: python3 generate_js_data.py SRC.md OUT.js
"""
import sys, re
import yaml

def load(path):
    t = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    if not m:
        raise SystemExit('no frontmatter in ' + path)
    return yaml.safe_load(m.group(1))

def jstr(s):
    s = s.replace('\\', '\\\\').replace('"', '\\"')
    s = s.replace('\r', '').replace('\n', '\\n').replace('\t', '\\t')
    return '"' + s + '"'

def is_plain(v):
    return isinstance(v, (str, int, float, bool)) or v is None

def py_to_js(v, indent=0):
    pad = '  ' * indent
    pad1 = '  ' * (indent + 1)
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if v is None:
        return 'null'
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return jstr(v)
    if isinstance(v, list):
        if not v:
            return '[]'
        items = [py_to_js(x, indent + 1) for x in v]
        if all(is_plain(x) for x in v) and len('[ ' + ', '.join(items) + ' ]') <= 90:
            return '[ ' + ', '.join(items) + ' ]'
        return '[\n' + ',\n'.join(pad1 + it for it in items) + '\n' + pad + ']'
    if isinstance(v, dict):
        if not v:
            return '{}'
        entries = []
        for k, val in v.items():
            key = k if re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', str(k)) else jstr(str(k))
            entries.append((key, val))
        if all(is_plain(val) for _, val in entries):
            single = '{ ' + ', '.join(f'{k}: {py_to_js(val)}' for k, val in entries) + ' }'
            if len(single) <= 90:
                return single
        lines = [f'{pad1}{k}: {py_to_js(val, indent + 1)}' for k, val in entries]
        return '{\n' + ',\n'.join(lines) + '\n' + pad + '}'
    raise TypeError('unsupported: ' + str(type(v)))

# ---- ADAPT THIS to your schema ----
def normalize(data):
    repos = []
    for r in data.get('repos', []):
        obj = {
            'name': r.get('name', ''),
            'cat': r.get('cat', ''),
            'visibility': r.get('visibility', 'privado'),
            'icon': r.get('icon', 'star'),
            'repo': r.get('repo', ''),
            'stack': r.get('stack', []) or [],
            'tags': r.get('tags', []) or [],
            'brief': r.get('brief', {}).get('pt', ''),
        }
        i18n = {l: r['brief'][l] for l in ('en', 'es', 'fr') if r.get('brief', {}).get(l)}
        if i18n:
            obj['i18n'] = i18n
        repos.append(obj)
    return {'REPOS': repos}

def main():
    src, out = sys.argv[1], sys.argv[2]
    norm = normalize(load(src))
    body = ',\n'.join(f'  {k}: {py_to_js(v, 1)}' for k, v in norm.items())
    js = f'window.PORTFOLIO_DATA = {{\n{body}\n}};\n'
    open(out, 'w', encoding='utf-8').write(js)
    print(f'wrote {out} ({len(js)} bytes)')

if __name__ == '__main__':
    main()
