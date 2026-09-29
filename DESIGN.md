# DESIGN — Awesome Skills Architecture & Design Rules

## 1. Arquitetura do Catálogo

```mermaid
graph TD
    Root["awesome-skills/"] --> Skills["skills/ (Instruções Especializadas)"]
    Root --> MCP["mcp/ (Model Context Protocol Servers)"]
    Root --> Plugins["plugins/ (Integrações e Ferramentas)"]
    Root --> Templates["templates/ (Geradores de Novas Skills)"]
    Skills --> SkillDoc["SKILL.md (Frontmatter + Markdown)"]
```

---

## 2. Padrões de Especificação de Skills

1. **Frontmatter Obrigatório:**
   - Todo arquivo `SKILL.md` deve conter `name` e `description`.
2. **Atomicidade:**
   - Cada skill deve ter escopo delimitado, evitando sobreposição de responsabilidades entre agentes.
