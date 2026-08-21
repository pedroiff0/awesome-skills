# 🦙 Curated Ollama Open-Source Models Catalog

A tiered selection of the best open-source local LLMs and Reasoning models for development, coding, and autonomous agents using [Ollama](https://ollama.com/).

---

## 🪶 Tier 1: Ultra-Leves (1B - 3B)
*Ideal para laptops, CPU pura, Raspberry Pi e workers em background (< 4GB VRAM / < 8GB RAM).*

| Modelo | Tamanho | VRAM Recomendada | Especialidade | Comando de Instalação |
| :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5:1.5b`** | 1.5B | ~1.5 GB | Velocidade extrema, parsing JSON e stubs | `ollama run qwen2.5:1.5b` |
| **`deepseek-r1:1.5b`** | 1.5B | ~1.8 GB | Raciocínio matemático e lógica leve | `ollama run deepseek-r1:1.5b` |
| **`llama3.2:1b`** | 1.2B | ~1.3 GB | Classificação ultra-rápida de texto | `ollama run llama3.2:1b` |
| **`llama3.2:3b`** | 3.2B | ~2.8 GB | Melhor equilíbrio leve para conversação | `ollama run llama3.2:3b` |
| **`phi3.5:3.8b`** | 3.8B | ~3.2 GB | Alta precisão de instruções e raciocínio | `ollama run phi3.5:3.8b` |

---

## ⚡ Tier 2: Equilibrados & Coding Diário (7B - 9B)
*Padrão para desenvolvimento local, agentes autônomos e pair programming (8GB - 12GB VRAM / 16GB RAM).*

| Modelo | Tamanho | VRAM Recomendada | Especialidade | Comando de Instalação |
| :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5-coder:7b`** | 7.6B | ~5.5 GB | 🏆 Topo em geração de código e refatoração | `ollama run qwen2.5-coder:7b` |
| **`deepseek-r1:7b`** | 7.6B | ~6.0 GB | Raciocínio passo a passo e resolução de bugs | `ollama run deepseek-r1:7b` |
| **`llama3.1:8b`** | 8.0B | ~6.2 GB | Modelo geral para tarefas complexas | `ollama run llama3.1:8b` |
| **`gemma2:9b`** | 9.2B | ~7.5 GB | Excelente compreensão de texto e síntese | `ollama run gemma2:9b` |
| **`mistral:7b`** | 7.2B | ~5.8 GB | Rápido, direto e confiável para instruções | `ollama run mistral:7b` |

---

## 🚀 Tier 3: Avançados & Pro Coding (14B - 35B)
*Arquiteturas complexas, raciocínio profundo e agentes de alta precisão (16GB - 24GB VRAM / 32GB RAM).*

| Modelo | Tamanho | VRAM Recomendada | Especialidade | Comando de Instalação |
| :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5-coder:14b`** | 14.7B | ~10.5 GB | Qualidade comparável a modelos proprietários | `ollama run qwen2.5-coder:14b` |
| **`deepseek-r1:14b`** | 14.7B | ~11.0 GB | Raciocínio matemático e algorítmico profundo | `ollama run deepseek-r1:14b` |
| **`qwen2.5-coder:32b`** | 32.5B | ~20.0 GB | 👑 State-of-the-art em engenharia de software | `ollama run qwen2.5-coder:32b` |
| **`deepseek-r1:32b`** | 32.5B | ~21.0 GB | Raciocínio lógico extremo | `ollama run deepseek-r1:32b` |
| **`command-r:35b`** | 35.0B | ~22.0 GB | Mestre em chamadas de ferramentas e RAG | `ollama run command-r:35b` |

---

## 🧠 Tier 4: Heavyweights & Servidores (70B+)
*Para servidores dedicados com multi-GPU (48GB+ VRAM / 64GB+ RAM).*

| Modelo | Tamanho | VRAM Recomendada | Especialidade | Comando de Instalação |
| :--- | :--- | :--- | :--- | :--- |
| **`deepseek-r1:70b`** | 70B | ~42.0 GB | 🧠 Raciocínio topo absoluto em código e lógica | `ollama run deepseek-r1:70b` |
| **`llama3.3:70b`** | 70B | ~42.0 GB | Modelo open source flagship de uso geral | `ollama run llama3.3:70b` |
| **`qwen2.5:72b`** | 72B | ~44.0 GB | Máxima performance em benchmarks globais | `ollama run qwen2.5:72b` |
