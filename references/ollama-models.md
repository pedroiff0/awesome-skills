# 🦙 Curated Ollama Open-Source Models Catalog (2026 Edition)

A tiered, high-performance catalog of local LLMs and Reasoning models for coding, debugging, RAG, and autonomous AI agents with direct clickable links to the official [Ollama Model Library](https://ollama.com/library).

---

## 🪶 Tier 1: Ultra-Lightweight (1B - 3B)
*Ideal for laptops, CPU-only machines, Raspberry Pi 5, and lightweight background workers (< 4GB VRAM / < 8GB RAM).*

| Model Tag | Size | VRAM | Direct Ollama Link | Specialty & Capabilities | Quick Pull Command |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5:1.5b`** | 1.5B | ~1.5 GB | [ollama.com/library/qwen2.5](https://ollama.com/library/qwen2.5) | Ultra-fast JSON parsing, fast routing, and background tasks | `ollama run qwen2.5:1.5b` |
| **`deepseek-r1:1.5b`** | 1.5B | ~1.8 GB | [ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1) | Step-by-step mathematical reasoning and logic on pure CPU | `ollama run deepseek-r1:1.5b` |
| **`llama3.2:1b`** | 1.2B | ~1.3 GB | [ollama.com/library/llama3.2](https://ollama.com/library/llama3.2) | Instant text classification and lightweight instruction filtering | `ollama run llama3.2:1b` |
| **`llama3.2:3b`** | 3.2B | ~2.8 GB | [ollama.com/library/llama3.2](https://ollama.com/library/llama3.2) | Best lightweight balance for daily conversational chat | `ollama run llama3.2:3b` |
| **`phi3.5:3.8b`** | 3.8B | ~3.2 GB | [ollama.com/library/phi3.5](https://ollama.com/library/phi3.5) | Microsoft Phi-3.5 Mini - high reasoning and prompt accuracy | `ollama run phi3.5:3.8b` |

---

## ⚡ Tier 2: Balanced & Daily Coding (7B - 9B)
*The gold standard for local software engineering, pair programming, and coding agents (8GB - 12GB VRAM / 16GB RAM).*

| Model Tag | Size | VRAM | Direct Ollama Link | Specialty & Capabilities | Quick Pull Command |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5-coder:7b`** | 7.6B | ~5.5 GB | [ollama.com/library/qwen2.5-coder](https://ollama.com/library/qwen2.5-coder) | 🏆 Benchmark leader in code generation, refactoring, and AST fixes | `ollama run qwen2.5-coder:7b` |
| **`deepseek-r1:7b`** | 7.6B | ~6.0 GB | [ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1) | Deep reasoning and debugging with `<think>` verification | `ollama run deepseek-r1:7b` |
| **`llama3.1:8b`** | 8.0B | ~6.2 GB | [ollama.com/library/llama3.1](https://ollama.com/library/llama3.1) | Meta flagship general model for diverse multi-step instructions | `ollama run llama3.1:8b` |
| **`gemma2:9b`** | 9.2B | ~7.5 GB | [ollama.com/library/gemma2](https://ollama.com/library/gemma2) | Google Gemma 2 - highest prose synthesis & documentation clarity | `ollama run gemma2:9b` |
| **`mistral:7b`** | 7.2B | ~5.8 GB | [ollama.com/library/mistral](https://ollama.com/library/mistral) | Fast, structured, and deterministic JSON tool responses | `ollama run mistral:7b` |

---

## 🚀 Tier 3: Advanced & Pro Coding (14B - 35B)
*Complex architectural design, deep mathematical reasoning, and full-codebase agents (16GB - 24GB VRAM / 32GB RAM).*

| Model Tag | Size | VRAM | Direct Ollama Link | Specialty & Capabilities | Quick Pull Command |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5-coder:14b`** | 14.7B | ~10.5 GB | [ollama.com/library/qwen2.5-coder](https://ollama.com/library/qwen2.5-coder) | Enterprise-grade coding matching proprietary model quality | `ollama run qwen2.5-coder:14b` |
| **`deepseek-r1:14b`** | 14.7B | ~11.0 GB | [ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1) | Advanced mathematical, algorithmic, and concurrency reasoning | `ollama run deepseek-r1:14b` |
| **`qwen2.5-coder:32b`** | 32.5B | ~20.0 GB | [ollama.com/library/qwen2.5-coder](https://ollama.com/library/qwen2.5-coder) | 👑 State-of-the-art open-source software engineer (Top coding eval) | `ollama run qwen2.5-coder:32b` |
| **`deepseek-r1:32b`** | 32.5B | ~21.0 GB | [ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1) | Deep analytical problem solving for tricky edge cases | `ollama run deepseek-r1:32b` |
| **`command-r:35b`** | 35.0B | ~22.0 GB | [ollama.com/library/command-r](https://ollama.com/library/command-r) | Cohere Command-R - specialized for Tool Use and massive RAG | `ollama run command-r:35b` |

---

## 🧠 Tier 4: Heavyweights & Servers (70B+)
*Datacenter and multi-GPU workstations (48GB+ VRAM / 64GB+ RAM).*

| Model Tag | Size | VRAM | Direct Ollama Link | Specialty & Capabilities | Quick Pull Command |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`deepseek-r1:70b`** | 70B | ~42.0 GB | [ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1) | 🧠 Uncensored extreme reasoning on complex science and systems | `ollama run deepseek-r1:70b` |
| **`llama3.3:70b`** | 70B | ~42.0 GB | [ollama.com/library/llama3.3](https://ollama.com/library/llama3.3) | Meta flagship 70B model with full tool calling & instruction fidelity | `ollama run llama3.3:70b` |
| **`qwen2.5:72b`** | 72B | ~44.0 GB | [ollama.com/library/qwen2.5](https://ollama.com/library/qwen2.5) | Maximum performance in global academic benchmarks | `ollama run qwen2.5:72b` |
