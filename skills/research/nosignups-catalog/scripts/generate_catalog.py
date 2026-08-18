#!/usr/bin/env python3
"""
NoSignups Catalog Generator
Gera o catálogo curado de ferramentas open source sem signup.
Lê tools.json do repositório BraveOPotato/FckSignups e produz:
- references/full-catalog.md: lista completa das 234 tools
- references/curated-list.md: lista curada por relevância (DevOps/self-hosted)
"""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
REFERENCES_DIR = SKILL_DIR / "references"
TOOLS_JSON_URL = "https://raw.githubusercontent.com/BraveOPotato/FckSignups/refs/heads/main/tools.json"

# Categorias de relevância para o perfil do Pedro (DevOps/Operations)
HIGH_RELEVANCE_KEYWORDS = {
    'devops': [
        'docker', 'deploy', 'ci', 'cd', 'monitor', 'server', 'hosting', 'cloud',
        'kubernetes', 'container', 'nginx', 'proxy', 'reverse', 'ssl', 'dns',
        'backup', 'linux', 'terminal', 'ssh', 'devops', 'infrastructure',
        'automation', 'log', 'logging', 'observability', 'metrics', 'alerting'
    ],
    'security': [
        'privacy', 'encrypt', 'security', 'vpn', 'password', '2fa', 'auth',
        'anonymous', 'tor', 'secure', 'protect', 'hardening', 'firewall',
        'malware', 'virus', 'privacy', 'metadata', 'redact', 'scrub'
    ],
    'development': [
        'code', 'ide', 'editor', 'debug', 'api', 'git', 'github', 'json',
        'regex', 'sql', 'database', 'diagram', 'schema', 'ast', 'parser',
        'compiler', 'wasm', 'typescript', 'javascript', 'python', 'dart',
        'assembly', 'converter', 'formatter', 'minifier', 'diff', 'lint',
        'testing', 'bundle', 'build', 'package', 'dependency', 'mcp'
    ],
    'self-hosted': [
        'self-host', 'self host', 'local', 'offline', 'on-premise', 'private',
        'client-side', 'browser-based', 'zero-install', 'no signup', 'no account'
    ],
    'productivity': [
        'pdf', 'document', 'spreadsheet', 'office', 'notes', 'calendar',
        'task', 'todo', 'habit', 'pomodoro', 'resume', 'cv', 'flowchart',
        'mindmap', 'whiteboard', 'collaboration', 'typing', 'file', 'convert',
        'compress', 'merge', 'split', 'download', 'upload', 'transfer', 'qr',
        'url', 'shortener', 'pastebin', 'notepad', 'text', 'markdown', 'epub',
        'reader', 'spreadsheet', 'database'
    ],
    'media': [
        'video', 'audio', 'image', 'photo', 'svg', 'png', 'jpg', 'gif',
        'compress', 'resize', 'crop', 'filter', 'effect', 'editor', 'subtitle',
        'music', 'daw', 'midi', 'pixel', 'sprite', 'animation', '3d', 'model',
        'render', 'shader', 'webgl', 'canvas', 'draw', 'paint', 'sketch',
        'diagram', 'icon', 'font', 'color', 'palette', 'gradient', 'pattern',
        'mockup', 'screenshot'
    ],
    'data': [
        'data', 'analytics', 'visualization', 'chart', 'graph', 'csv', 'json',
        'xml', 'yaml', 'parquet', 'sqlite', 'sql', 'query', 'dashboard',
        'osint', 'intelligence', 'satellite', 'tracking', 'conversion',
        'encoding', 'decoding', 'hash', 'base64', 'random', 'generator',
        'validator', 'formatter', 'parser', 'extractor'
    ]
}

def fetch_tools_json():
    """Baixa o tools.json do GitHub."""
    import urllib.request
    url = TOOLS_JSON_URL
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())

def calc_relevance(tool):
    """Calcula score de relevância por domínio."""
    text = f"{tool['name']} {tool['description']} {' '.join(tool.get('tags', []))} {tool['category']}".lower()
    scores = {}
    for domain, keywords in HIGH_RELEVANCE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        scores[domain] = score
    return scores

def generate_full_catalog(tools):
    """Gera o catálogo completo em Markdown."""
    by_cat = {}
    for t in tools:
        cat = t['category']
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(t)

    lines = [
        "# NoSignups Full Catalog",
        "",
        f"**Total: {len(tools)} tools** across **{len(by_cat)} categories**.",
        "",
        f"Source: [BraveOPotato/FckSignups](https://github.com/BraveOPotato/FckSignups)",
        "",
        "---",
        ""
    ]

    cat_names = {
        'productivity': 'Productivity',
        'design': 'Design & Graphics',
        'development': 'Development',
        'writing': 'Writing & Docs',
        'privacy': 'Privacy & Security',
        'utilities': 'Utilities',
        'data': 'Data & Analytics',
        'media': 'Media',
        'education': 'Education',
        'lists': 'Lists'
    }

    for cat_id in ['development', 'utilities', 'design', 'productivity', 'writing', 'media', 'privacy', 'data', 'education', 'lists']:
        cat_tools = by_cat.get(cat_id, [])
        if not cat_tools:
            continue
        cat_tools.sort(key=lambda x: x.get('stars', 0), reverse=True)
        lines.append(f"## {cat_names.get(cat_id, cat_id)} ({len(cat_tools)} tools)")
        lines.append("")
        lines.append("| Tool | Stars | License | Description |")
        lines.append("|------|-------|---------|-------------|")
        for t in cat_tools:
            stars = f"{t.get('stars', 0):,}" if t.get('stars') else "—"
            license = t.get('license', '—')
            desc = t['description'][:80]
            lines.append(f"| [{t['name']}]({t['url']}) | {stars} | {license} | {desc} |")
        lines.append("")

    return "\n".join(lines)

def generate_curated_list(tools):
    """Gera a lista curada por relevância."""
    # Calcular relevância
    for t in tools:
        t['relevance'] = calc_relevance(t)
        t['max_relevance'] = max(t['relevance'].values())

    # Filtrar tools com relevância > 0 ou stars > 1000
    relevant = [t for t in tools if t['max_relevance'] > 0 or (t.get('stars', 0) > 1000)]
    relevant.sort(key=lambda x: (x['max_relevance'], x.get('stars', 0)), reverse=True)

    lines = [
        "# NoSignups Curated List",
        "",
        f"**{len(relevant)} tools** selecionadas por relevância para DevOps/Operations.",
        "",
        "Critérios:",
        "- Relevância para DevOps, self-hosted, segurança, desenvolvimento",
        "- Stars > 1000 (mesmo sem keyword match)",
        "",
        "---",
        ""
    ]

    # Agrupar por domínio de relevância
    domains = ['devops', 'security', 'development', 'self-hosted', 'productivity', 'media', 'data']
    for domain in domains:
        domain_tools = [t for t in relevant if t['relevance'].get(domain, 0) > 0]
        if not domain:
            continue
        domain_tools.sort(key=lambda x: x.get('stars', 0), reverse=True)
        lines.append(f"## {domain.upper()} ({len(domain_tools)} tools)")
        lines.append("")
        for t in domain_tools[:20]:  # Top 20 por domínio
            stars = f"{t.get('stars', 0):,}★" if t.get('stars') else ""
            license = t.get('license', '—')
            github = f"[GH]({t['github']})" if t.get('github') else ""
            lines.append(f"- **{t['name']}** {stars} `{license}` {github}")
            lines.append(f"  {t['description'][:100]}")
            lines.append(f"  🔗 {t['url']}")
            lines.append("")

    return "\n".join(lines)

def main():
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)

    print("Fetching tools.json...")
    data = fetch_tools_json()
    tools = data['tools']
    print(f"Loaded {len(tools)} tools")

    print("Generating full catalog...")
    full_md = generate_full_catalog(tools)
    (REFERENCES_DIR / "full-catalog.md").write_text(full_md)
    print(f"  → references/full-catalog.md ({len(full_md)} chars)")

    print("Generating curated list...")
    curated_md = generate_curated_list(tools)
    (REFERENCES_DIR / "curated-list.md").write_text(curated_md)
    print(f"  → references/curated-list.md ({len(curated_md)} chars)")

    # Salvar JSON local para referência
    json_path = REFERENCES_DIR / "tools-data.json"
    json_path.write_text(json.dumps(tools, indent=2, ensure_ascii=False))
    print(f"  → references/tools-data.json")

    print("\nDone! Run `python3 scripts/generate_catalog.py` to update.")

if __name__ == "__main__":
    main()
