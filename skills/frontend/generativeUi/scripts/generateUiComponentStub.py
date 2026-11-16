#!/usr/bin/env python3
"""
generateUiComponentStub.py
Scaffolds a Generative UI tool definition and corresponding React component pair.
"""

import sys
import argparse

def generate_stub(tool_name: str):
    cap_name = tool_name[:1].upper() + tool_name[1:]
    server_snippet = f"""// Server Tool Definition (app/api/chat/route.ts)
{tool_name}: tool({{
  description: 'Display interactive {tool_name} component',
  parameters: z.object({{
    id: z.string(),
    title: z.string(),
    status: z.enum(['pending', 'completed']),
  }}),
  execute: async (args) => {{
    return {{ ...args, timestamp: Date.now() }};
  }},
}}),
"""
    client_snippet = f"""// Client Component (components/{cap_name}Card.tsx)
import React from 'react';

export function {cap_name}Card({{ data }}: {{ data: any }}) {{
  return (
    <div className="border rounded-lg p-4 shadow-sm bg-card text-card-foreground">
      <h3 className="font-semibold text-lg">{{data.title}}</h3>
      <p className="text-sm text-muted-foreground">ID: {{data.id}} | Status: {{data.status}}</p>
    </div>
  );
}}
"""
    print("=== Server Tool ===")
    print(server_snippet)
    print("=== Client Component ===")
    print(client_snippet)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", default="orderStatus", help="Tool name in camelCase")
    args = parser.parse_args()
    generate_stub(args.tool)
