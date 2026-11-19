# Tools and Model Context Protocol (MCP) Integration

The OpenAI Responses API natively supports both built-in hosted tools and external remote tools via the Model Context Protocol (MCP).

---

## 1. Built-in Tools

OpenAI provides managed tools that execute securely on OpenAI infrastructure:

```python
response = client.responses.create(
    model="gpt-4o",
    input="What were Tesla's Q4 delivery numbers and write Python code to graph it?",
    tools=[
        {"type": "web_search_preview"},
        {"type": "code_interpreter_preview"},
    ]
)
```

1. **`web_search_preview`**: Performs real-time web retrieval with automatic citations.
2. **`file_search_preview`**: Searches uploaded documents with vector embeddings.
3. **`code_interpreter_preview`**: Runs secure sandboxed Python code to process data and output charts.
4. **`computer_use_preview`**: Operates desktop/browser UI for automated actions.

---

## 2. Remote MCP Server Integration

You can bind an MCP server directly into the Responses API toolchain:

```python
response = client.responses.create(
    model="gpt-4o",
    input="Query our internal Postgres database for churn rate in March.",
    tools=[
        {
            "type": "mcp",
            "server_url": "https://mcp.internal.company.com/sse",
            "headers": {
                "Authorization": f"Bearer {os.environ['MCP_AUTH_TOKEN']}"
            }
        }
    ]
)
```
