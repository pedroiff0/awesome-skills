# MCP Server: sqlite-explorer

Inspect schemas, run SQL queries, and analyze SQLite tables directly through the Model Context Protocol.

## Configuration

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "./database.sqlite"]
    }
  }
}
```
