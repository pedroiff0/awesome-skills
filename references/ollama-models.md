# 🦙 Curated Local Ollama Models Registry (2026 Comprehensive Edition)

A complete directory of strictly **LOCAL open-weight models** (no cloud API dependencies) for Ollama, categorized into 4 hardware tiers from edge devices to datacenter servers, with direct clickable links to the official [Ollama Model Library](https://ollama.com/library).

---

## 🪶 1. Leve (Lightweight: 0.5B - 3.8B)
*Ultra-fast inference on laptops, CPU-only machines, Raspberry Pi 5, and background workers (< 4GB VRAM / < 8GB RAM).*

| Model Tag | Size | VRAM | Direct Library Link | Organization | Specialty & Capabilities |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5:0.5b`** | 0.5B | ~0.8 GB | [ollama.com/library/qwen2.5](https://ollama.com/library/qwen2.5) | Alibaba Qwen | Microscopic footprint, instant text classification |
| **`qwen2.5:1.5b`** | 1.5B | ~1.5 GB | [ollama.com/library/qwen2.5](https://ollama.com/library/qwen2.5) | Alibaba Qwen | Ultra-fast JSON parsing, fast routing, and background tasks |
| **`deepseek-r1:1.5b`** | 1.5B | ~1.8 GB | [ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1) | DeepSeek | Step-by-step mathematical reasoning and logic on pure CPU |
| **`llama3.2:1b`** | 1.2B | ~1.3 GB | [ollama.com/library/llama3.2](https://ollama.com/library/llama3.2) | Meta AI | Instant text classification and lightweight instruction filtering |
| **`llama3.2:3b`** | 3.2B | ~2.8 GB | [ollama.com/library/llama3.2](https://ollama.com/library/llama3.2) | Meta AI | Best lightweight balance for daily conversational chat |
| **`phi3.5:3.8b`** | 3.8B | ~3.2 GB | [ollama.com/library/phi3.5](https://ollama.com/library/phi3.5) | Microsoft | High reasoning density and instruction following accuracy |
| **`smollm2:135m`** | 135M | ~0.3 GB | [ollama.com/library/smollm2](https://ollama.com/library/smollm2) | Hugging Face | Ultra-compact edge intelligence on micro-controllers |
| **`smollm2:360m`** | 360M | ~0.6 GB | [ollama.com/library/smollm2](https://ollama.com/library/smollm2) | Hugging Face | Lightweight edge reasoning |
| **`smollm2:1.7b`** | 1.7B | ~1.6 GB | [ollama.com/library/smollm2](https://ollama.com/library/smollm2) | Hugging Face | Top quality on consumer laptops without discrete GPU |
| **`tinyllama:1.1b`** | 1.1B | ~1.1 GB | [ollama.com/library/tinyllama](https://ollama.com/library/tinyllama) | Community | Classic lightweight pre-trained model |
| **`granite3-dense:2b`** | 2.0B | ~1.9 GB | [ollama.com/library/granite3-dense](https://ollama.com/library/granite3-dense) | IBM Research | Enterprise grade small model for code & tabular data |
| **`moondream:1.8b`** | 1.8B | ~2.0 GB | [ollama.com/library/moondream](https://ollama.com/library/moondream) | Vikhyat | Lightweight multimodal vision model for image inspection |

---

## ⚡ 2. Intermediário (Intermediate / Mainstream: 7B - 9B)
*The daily workhorse tier for software development, coding agents, and local pair programming (6GB - 12GB VRAM / 16GB RAM).*

| Model Tag | Size | VRAM | Direct Library Link | Organization | Specialty & Capabilities |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5-coder:7b`** | 7.6B | ~5.5 GB | [ollama.com/library/qwen2.5-coder](https://ollama.com/library/qwen2.5-coder) | Alibaba Qwen | 🏆 Gold standard for local code generation, refactoring & AST fixes |
| **`deepseek-r1:7b`** | 7.6B | ~6.0 GB | [ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1) | DeepSeek | Step-by-step reasoning with transparent `<think>` traces |
| **`llama3.1:8b`** | 8.0B | ~6.2 GB | [ollama.com/library/llama3.1](https://ollama.com/library/llama3.1) | Meta AI | Meta flagship 8B general instruction & tool-calling model |
| **`gemma2:9b`** | 9.2B | ~7.5 GB | [ollama.com/library/gemma2](https://ollama.com/library/gemma2) | Google | Exceptional synthesis, prose, and docstring formatting |
| **`mistral:7b`** | 7.2B | ~5.8 GB | [ollama.com/library/mistral](https://ollama.com/library/mistral) | Mistral AI | Fast, deterministic JSON outputs and structured task parsing |
| **`hermes3:8b`** | 8.0B | ~6.2 GB | [ollama.com/library/hermes3](https://ollama.com/library/hermes3) | Nous Research | Uncensored agentic model optimized for autonomous loops & skills |
| **`codellama:7b`** | 7.0B | ~5.5 GB | [ollama.com/library/codellama](https://ollama.com/library/codellama) | Meta AI | Specialized code completion and infilling |
| **`starcoder2:7b`** | 7.0B | ~5.5 GB | [ollama.com/library/starcoder2](https://ollama.com/library/starcoder2) | BigCode | Multi-language code completion trained on 600+ languages |
| **`deepseek-coder-v2:16b`** | 16B | ~9.0 GB | [ollama.com/library/deepseek-coder-v2](https://ollama.com/library/deepseek-coder-v2) | DeepSeek | Efficient MoE (2.4B active) coding model |
| **`granite3-dense:8b`** | 8.0B | ~6.2 GB | [ollama.com/library/granite3-dense](https://ollama.com/library/granite3-dense) | IBM Research | Enterprise tabular, code and RAG workflows |
| **`llava:7b`** | 7.0B | ~6.5 GB | [ollama.com/library/llava](https://ollama.com/library/llava) | LLaVA Team | Visual question answering, chart reading, and UI analysis |
| **`nomic-embed-text`** | 137M | ~0.5 GB | [ollama.com/library/nomic-embed-text](https://ollama.com/library/nomic-embed-text) | Nomic AI | 8192 context text embeddings for vector RAG |
| **`bge-m3`** | 567M | ~1.2 GB | [ollama.com/library/bge-m3](https://ollama.com/library/bge-m3) | BAAI | Multilingual multi-granularity dense/sparse embedding |

---

## 🚀 3. Pesado (Heavy / Pro Coding & High Reasoning: 14B - 35B)
*Complex codebase refactoring, deep algorithmic puzzles, and autonomous planning (16GB - 24GB VRAM / 32GB RAM).*

| Model Tag | Size | VRAM | Direct Library Link | Organization | Specialty & Capabilities |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5-coder:14b`** | 14.7B | ~10.5 GB | [ollama.com/library/qwen2.5-coder](https://ollama.com/library/qwen2.5-coder) | Alibaba Qwen | Enterprise-grade coding matching proprietary model quality |
| **`deepseek-r1:14b`** | 14.7B | ~11.0 GB | [ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1) | DeepSeek | Deep mathematical, algorithmic, and concurrency reasoning |
| **`qwen2.5-coder:32b`** | 32.5B | ~20.0 GB | [ollama.com/library/qwen2.5-coder](https://ollama.com/library/qwen2.5-coder) | Alibaba Qwen | 👑 State-of-the-art open-source software engineer (Top coding eval) |
| **`deepseek-r1:32b`** | 32.5B | ~21.0 GB | [ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1) | DeepSeek | Extreme logical reasoning for complex architectural bugs |
| **`qwen2.5:14b`** | 14.7B | ~10.5 GB | [ollama.com/library/qwen2.5](https://ollama.com/library/qwen2.5) | Alibaba Qwen | Balanced 14B general model with 128k context support |
| **`qwen2.5:32b`** | 32.5B | ~20.0 GB | [ollama.com/library/qwen2.5](https://ollama.com/library/qwen2.5) | Alibaba Qwen | High-capacity reasoning without requiring a 70B setup |
| **`command-r:35b`** | 35.0B | ~22.0 GB | [ollama.com/library/command-r](https://ollama.com/library/command-r) | Cohere | Cohere Command-R - specialized for Tool Use and massive RAG |
| **`gemma2:27b`** | 27.2B | ~17.5 GB | [ollama.com/library/gemma2](https://ollama.com/library/gemma2) | Google | High-throughput 27B model rivaling previous 70B class models |
| **`codellama:13b`** | 13.0B | ~9.8 GB | [ollama.com/library/codellama](https://ollama.com/library/codellama) | Meta AI | Mid-tier code generation and unit testing |
| **`codellama:34b`** | 34.0B | ~22.0 GB | [ollama.com/library/codellama](https://ollama.com/library/codellama) | Meta AI | High-precision Python/C++/Rust code synthesis |
| **`starcoder2:15b`** | 15.0B | ~11.5 GB | [ollama.com/library/starcoder2](https://ollama.com/library/starcoder2) | BigCode | Multi-language code repository comprehension |
| **`mixtral:8x7b`** | 47B | ~26.0 GB | [ollama.com/library/mixtral](https://ollama.com/library/mixtral) | Mistral AI | Sparse MoE with 13B active parameters per token |
| **`deepseek-coder:33b`** | 33.0B | ~21.5 GB | [ollama.com/library/deepseek-coder](https://ollama.com/library/deepseek-coder) | DeepSeek | Established high-performance code completion engine |

---

## 🏢 4. DataCenter (Multi-GPU Flagships: 70B - 405B)
*Datacenter clusters, multi-GPU workstations, and enterprise rigs (48GB - 80GB+ VRAM / 128GB+ RAM).*

| Model Tag | Size | VRAM | Direct Library Link | Organization | Specialty & Capabilities |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`deepseek-r1:70b`** | 70B | ~42.0 GB | [ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1) | DeepSeek | 🧠 Absolute pinnacle in open mathematical and coding reasoning |
| **`llama3.3:70b`** | 70B | ~42.0 GB | [ollama.com/library/llama3.3](https://ollama.com/library/llama3.3) | Meta AI | Meta flagship 70B with full tool calling & 128k context fidelity |
| **`qwen2.5:72b`** | 72.7B | ~44.0 GB | [ollama.com/library/qwen2.5](https://ollama.com/library/qwen2.5) | Alibaba Qwen | Benchmark champion across MMLU, GSM8k, HumanEval |
| **`mixtral:8x22b`** | 141B | ~80.0 GB | [ollama.com/library/mixtral](https://ollama.com/library/mixtral) | Mistral AI | Massive MoE (39B active) with high math & multilingual prowess |
| **`command-r-plus:104b`** | 104B | ~65.0 GB | [ollama.com/library/command-r-plus](https://ollama.com/library/command-r-plus) | Cohere | Enterprise RAG, multilingual routing and business intelligence |
| **`llama3.1:70b`** | 70B | ~42.0 GB | [ollama.com/library/llama3.1](https://ollama.com/library/llama3.1) | Meta AI | Proven flagship open weights model |
| **`llama3.1:405b`** | 405B | 240GB+ | [ollama.com/library/llama3.1](https://ollama.com/library/llama3.1) | Meta AI | The largest open foundation model in history (FP8 / distributed) |
