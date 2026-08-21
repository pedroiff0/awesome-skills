# Vendor-Specific Provenance Surfaces

| Vendor / Model | Primary Marking Mechanism | Mitigation Strategy |
| :--- | :--- | :--- |
| **Claude / Anthropic** | Statistical stylistic patterns + occasional Unicode formatting | Layer A Unicode cleaning + structural rewrite |
| **Gemini / Google SynthID** | SynthID-Text (tournament sampling on logits) | Multi-pass semantic rewrite (Layer B) |
| **OpenAI / ChatGPT** | C2PA hard-bound metadata (images/audio) | File metadata scrub (`exiftool` / re-encoding) |
| **Open-Source LLMs** | Kirchenbauer green-list sampling / Gumbel watermarks | Rephrasing, vocabulary expansion |
