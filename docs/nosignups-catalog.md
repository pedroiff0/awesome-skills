# NoSignups Catalog — Ferramentas Recomendadas

> Catálogo de ferramentas open source sem signup, curadas para o perfil DevOps/Self-Hosted.

**Fonte:** [NoSignups.net](https://nosignups.net) (234 tools)  
**Skill:** `skills/research/nosignups-catalog/`  
**Atualização:** `python3 skills/research/nosignups-catalog/scripts/generate_catalog.py`

---

## TOP 10 — Altamente Recomendadas

### 1. CyberChef (35k★) — Workbench "Cyber"
- **O que faz:** Encode, decode, encrypt, compress, hash, parse dados no browser
- **Uso pra ops:** Diagnosticar tokens JWT, headers, encoding de logs, extrair dados de strings codificadas
- **URL:** https://gchq.github.io/CyberChef/
- **GitHub:** https://github.com/gchq/CyberChef

### 2. Croc (39k★) — Transferência Segura P2P
- **O que faz:** Enviar arquivos entre máculos sem servidor, com criptografia end-to-end
- **Uso pra ops:** Substituir `scp` sem configurar chaves. Comando único, funciona em LAN/WAN.
- **URL:** https://getcroc.com/
- **GitHub:** https://github.com/schollz/croc

### 3. Stirling-PDF (87k★) — Editor PDF Self-Hosted
- **O que faz:** Merge, split, compress, convert, rotate, adicionar páginas — 100% local
- **Uso pra ops:** Substituir serviços PDF online (iLovePDF, Smallpdf) por instância self-hosted
- **Docker:** `docker run -p 8080:8080 frooodle/s-pdf:latest`
- **GitHub:** https://github.com/Stirling-Tools/Stirling-PDF

### 4. privacy.sexy (6k★) — Hardening Scripts
- **O que faz:** Scripts pra forçar boas práticas de privacidade/segurança em Windows/macOS/Linux
- **Risco:** Scripts podem quebrar coisas — SEMPRE revisar antes de rodar
- **URL:** https://privacy.sexy
- **GitHub:** https://github.com/undergroundwires/privacy.sexy

### 5. drawDB (38k★) — Diagramas ER + SQL
- **O que faz:** Editor de diagramas entidade-relacionamento, gera SQL automaticamente
- **Uso pra ops:** Documentar arquitetura de bancos rapidinho
- **URL:** https://www.drawdb.app
- **GitHub:** https://github.com/drawdb-io/drawdb

### 6. IT-Tools (40k★) — Canivete Suíço Dev
- **O que faz:** 50+ ferramentas web (JSON formatter, regex tester, QR generator, hash, color picker, date converter)
- **URL:** https://it-tools.tech/
- **GitHub:** https://github.com/CorentinTh/it-tools
- **Self-hosted:** `docker run -p 8080:80 corentinth/it-tools`

### 7. Markmap (13k★) — Markdown → Mind Map
- **O que faz:** Transforma Markdown em mapas mentais interativos
- **Uso pra ops:** Documentação técnica + visualização de arquitetura
- **URL:** https://markmap.js.org/
- **GitHub:** https://github.com/markmap/markmap

### 8. Logseq (44k★) — Base de Conhecimento Privacy-First
- **O que faz:** Knowledge base local-first, alternativa ao Notion/Obsidian sync
- **URL:** https://logseq.com/
- **GitHub:** https://github.com/logseq/logseq

### 9. PairDrop (11k★) — AirDrop Cross-Platform
- **O que faz:** Transferir arquivos entre dispositivos sem servidor, via WebRTC
- **URL:** https://pairdrop.net/
- **GitHub:** https://github.com/schlagmichdoch/pairdrop

### 10. VERT (15k★) — Conversor de Arquivos
- **O que faz:** Conversão de arquivos 100% no browser (sem upload pra servidor)
- **URL:** https://vert.sh/
- **GitHub:** https://github.com/VERT-sh/VERT

---

## SELF-HOSTED / DEVOPS

| Tool | Descrição | Stars | Docker |
|------|-----------|-------|--------|
| Grist | Spreadsheet + database (alt. Airtable) | 11k | Sim |
| CryptPad | Escritório E2E encrypted (docs/sheets) | 8k | Sim |
| MiroTalk P2P | Video conferência WebRTC P2P | 5k | Sim |
| Markmap | Mind maps a partir de Markdown | 13k | — |
| Stirling-PDF | Editor PDF completo | 87k | `frooodle/s-pdf` |
| IT-Tools | 50+ ferramentas dev | 40k | `corentinth/it-tools` |

---

## UTILITÁRIOS DIÁRIOS

| Tool | Descrição | Stars |
|------|-----------|-------|
| OmniTools | 52 ferramentas web (canivete suíço) | 10k |
| ffmpeg.wasm | FFmpeg no browser (sem instalar) | 18k |
| explainshell.com | Decodifica comandos shell complexos | 14k |
| Regexr | Testar regex no browser | 10k |
| AST explorer | Explorar ASTs de código | 7k |
| Carbon | Screenshots bonitas de código | 36k |
| Transform.tools | Conversor polyglot (JSON/YAML/XML/etc) | 9k |

---

## POR CATEGORIA

### Development (63 tools)
- **VS Code Web** (188k★) — VS Code no navegador, zero-install
- **Godot Web** (115k★) — Engine de jogos no navegador
- **hoppscotch** (80k★) — Alternativa open source ao Postman
- **JSON Crack** (44k★) — JSON → grafos interativos
- **CodeGraphContext** (4k★) — MCP server que indexa código local em graph database

### Privacy & Security (8 tools)
- **CyberChef** (35k★) — Encode/decode/encrypt
- **privacy.sexy** (6k★) — Hardening scripts
- **Cryptii** (1.5k★) — Conversão/encoding/encryption
- **Cryptgeon** (1.5k★) — Notas E2E encrypted com expiração

### Media (21 tools)
- **OpenCut** (72k★) — Alternativa open source ao CapCut
- **Cobalt** (42k★) — Downloader de mídia (YouTube, etc)
- **Squoosh** (25k★) — Compressão de imagens

### Data & Analytics (10 tools)
- **World Monitor** (62k★) — Dashboard de inteligência global em tempo real
- **RAWGraphs** (9k★) — Visualização de dados customizada
- **Datasette Lite** (405★) — Datasette (Python SQL) rodando no browser

---

## COMANDOS ÚTEIS

```bash
# Stirling-PDF (self-hosted)
docker run -d --name stirling-pdf -p 8080:8080 frooodle/s-pdf:latest

# IT-Tools (self-hosted)
docker run -d --name it-tools -p 8080:80 corentinth/it-tools

# Croc (enviar arquivo)
croc send arquivo.txt

# Croc (receber)
croc código-de-recebimento

# CyberChef (local)
git clone https://github.com/gchq/CyberChef.git
cd CyberChef && python3 -m http.server 8000
```

---

## RISCOS/ATENÇÕES

| Ferramenta | Risco | Mitigação |
|------------|-------|-----------|
| privacy.sexy | Pode quebrar configurações | Revisar scripts antes de rodar |
| Stirling-PDF (self-hosted) | Exposição de arquivos | Usar só em LAN/VPN, ou adicionar auth |
| MiroTalk/CryptPad | WebRTC vaza IP real | Usar VPN se precisar de anonimato |
| Croc | Transferência sem autenticação | Código de uso único, mas quem pega o código pega o arquivo |
| Qualquer ferramenta web | Dados passam pelo servidor | Pra dados sensíveis, usar self-hosted |

---

## ATUALIZAÇÃO

O catálogo completo (234 tools) está em:
- `skills/research/nosignups-catalog/references/full-catalog.md`
- `skills/research/nosignups-catalog/references/curated-list.md`
- `skills/research/nosignups-catalog/references/tools-data.json` (JSON para queries)

Pra atualizar:
```bash
python3 skills/research/nosignups-catalog/scripts/generate_catalog.py
```

Pra buscar por keyword:
```bash
# Buscar tools de PDF
cat skills/research/nosignups-catalog/references/tools-data.json | python3 -c "import sys,json; tools=json.load(sys.stdin); [print(t['name'], t['url']) for t in tools if 'pdf' in t['description'].lower()]"
```
