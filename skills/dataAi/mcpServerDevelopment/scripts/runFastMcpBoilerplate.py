#!/usr/bin/env python3
"""
runFastMcpBoilerplate.py
Production-ready starter FastMCP server boilerplate with tools, resources, and prompts.
"""

import sys

def main():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        sys.stderr.write("mcp package not installed. Run: pip install mcp or uv add mcp\n")
        sys.exit(1)

    mcp = FastMCP("StarterMcpServer")

    @mcp.tool()
    def echo_message(message: str) -> str:
        """Echo a message back to the agent with confirmation."""
        return f"Echo received: {message}"

    @mcp.resource("system://info")
    def get_system_info() -> str:
        """Return system status context."""
        return "System status: Healthy. All MCP endpoints operational."

    @mcp.prompt()
    def summarize_system_prompt() -> str:
        """Prompt template to summarize system state."""
        return "Review the resource at system://info and give an operational summary."

    mcp.run()

if __name__ == "__main__":
    main()
