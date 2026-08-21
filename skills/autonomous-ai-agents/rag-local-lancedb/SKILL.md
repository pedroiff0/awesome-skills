---
name: rag-local-lancedb
description: "Build, query, and manage local vector embeddings and semantic search pipelines using LanceDB and HuggingFace/SentenceTransformers embeddings without cloud dependencies."
version: 1.0.0
author: Pedro Henrique Rocha de Andrade
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [lancedb, vector-search, rag, embeddings, local-ai]
    related_skills: [huggingface-hub, llm-wiki]
---

# Local RAG with LanceDB

This skill guides the construction and query execution of serverless, high-performance local vector databases using LanceDB and local embeddings.

## When to Use

- Building offline semantic search across local Markdown files, codebases, or documentation.
- Storing vector embeddings with zero external cloud API costs.
- Performing hybrid full-text + vector similarity queries.

## Quick Setup & Python Usage

```python
import lancedb

# Connect to local database directory
db = lancedb.connect("~/.local/share/agent_rag")
```
