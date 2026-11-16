---
name: mcpServerDevelopment
description: Build Model Context Protocol (MCP) servers exposing tools, resources, and prompt templates to AI agents. Use when connecting Claude, Cursor, or custom agents to databases, APIs, and local services via stdio or SSE.
version: 1.x
last-verified: 2026-11-15
compatibility: Node.js 18+, Python 3.10+, uv, TypeScript 5+
---

# MCP Server Development Engineering Guide

## 1. Core Architecture & Primitives
Model Context Protocol (MCP) standardizes agent-to-environment integration across three core primitives:

```
┌────────────────────────────────────────────────────────┐
│                   MCP Server Core                      │
├─────────────────┬───────────────────┬──────────────────┤
│     Tools       │     Resources     │     Prompts      │
│ Model-controlled│ Client-controlled │ User-controlled  │
│ Action execution│ URI-based context │ Workflow presets │
└─────────────────┴───────────────────┴──────────────────┘
```

- **Tools**: Model-invoked functions with typed JSON Schema input/output (calculating, querying SQL, writing files).
- **Resources**: Read-only structured data accessed via custom URI schemes (`db://schema`, `file:///logs`).
- **Prompts**: Parameterized reusable prompts registered by the server for client slash commands.
- **Transports**:
  - `stdio`: Default for local agent hosts (Cursor, Claude Desktop). Standard in/out JSON-RPC stream.
  - `SSE` (Server-Sent Events) / Streamable HTTP: For distributed or multi-tenant remote deployments.

---

## 2. Python FastMCP Canonical Pattern

```python
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("ProductionDataServer")

# 1. Expose Tool (Model-invoked action)
@mcp.tool()
def query_database(sql_query: str, limit: int = 50) -> list[dict]:
    """Execute a read-only query against the database and return records."""
    # Enforce read-only safety
    if any(kw in sql_query.upper() for kw in ["DROP", "DELETE", "UPDATE", "INSERT"]):
        raise ValueError("Only read-only SELECT queries are allowed.")
    return db.execute(sql_query, limit=limit)

# 2. Expose Resource (URI context)
@mcp.resource("schema://main")
def get_database_schema() -> str:
    """Return schema DDL definitions for the active database."""
    return db.get_schema_ddl()

# 3. Expose Prompt (Slash command preset)
@mcp.prompt()
def analyze_slow_queries() -> str:
    """Prompt template to inspect execution plans of queries."""
    return "Analyze the database schema at schema://main and suggest composite indexes for slow queries."

if __name__ == "__main__":
    mcp.run() # Defaults to stdio transport
```

---

## 3. TypeScript SDK Canonical Pattern

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "ts-production-mcp", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {}, prompts: {} } }
);

// Register Tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "fetch_customer_data",
    description: "Fetch customer profile by ID",
    inputSchema: {
      type: "object",
      properties: { customerId: { type: "string" } },
      required: ["customerId"]
    }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "fetch_customer_data") {
    const { customerId } = request.params.arguments as { customerId: string };
    const data = await getCustomer(customerId);
    return { content: [{ type: "text", text: JSON.stringify(data) }] };
  }
  throw new Error(`Tool not found: ${request.params.name}`);
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## 4. Anti-Patterns & Critical Guardrails
- ❌ **Polluting stdout in stdio Mode**: Never use raw `print()` or `console.log()` in stdio servers! Doing so corrupts JSON-RPC payloads and breaks the client. Direct all debugging logs strictly to `stderr`.
- ❌ **Unvalidated Tool Arguments**: Always define strict schemas (Zod or Pydantic) with explicit validation; never accept unvalidated open objects.
- ❌ **Unchecked Destructive Mutations**: Tool calls that drop, alter, or send external emails should require human-in-the-loop confirmation (`confirm: true`).
- ❌ **Missing Resource URIs**: Never serve non-standard arbitrary strings as resource identifiers; use valid RFC 3986 URI schemes (`postgres://...`, `memo://...`).

---

## 5. References & Bundled Utilities
- Client configuration specs: [references/mcpClientConfigs.md](references/mcpClientConfigs.md)
- Tool schema best practices: [references/toolSchemaDesign.md](references/toolSchemaDesign.md)
- Standalone boilerplate server: [scripts/runFastMcpBoilerplate.py](scripts/runFastMcpBoilerplate.py)
