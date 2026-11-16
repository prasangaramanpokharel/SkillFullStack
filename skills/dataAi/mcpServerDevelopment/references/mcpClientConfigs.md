# MCP Host Client Configuration Specs

How to configure MCP servers across popular host agents:

## 1. Claude Desktop (`claude_desktop_config.json`)
Location: `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac)

```json
{
  "mcpServers": {
    "myPythonServer": {
      "command": "python3",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "API_KEY": "secret"
      }
    },
    "myNodeServer": {
      "command": "node",
      "args": ["/absolute/path/to/dist/index.js"]
    }
  }
}
```

## 2. Cursor (`.cursor/mcp.json`)
Location: Project root or global Cursor config:

```json
{
  "mcpServers": {
    "localTools": {
      "command": "uv",
      "args": ["run", "python", "scripts/mcpServer.py"]
    }
  }
}
```
