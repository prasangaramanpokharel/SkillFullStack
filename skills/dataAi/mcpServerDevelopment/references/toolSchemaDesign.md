# MCP Tool Schema Design & Best Practices

1. **Clear Descriptions**: Tool descriptions are consumed by the LLM's planner. State exactly what the tool does, expected inputs, and error modes.
2. **Strict Property Types**: Every property in `properties` must define an explicit `type`, and non-optional keys must be listed in `required`.
3. **Enum Values for Restricted Fields**: When selecting predefined actions or formats, supply `enum: [...]` to prevent model hallucinations.
4. **Error Handling**: Return clean error strings in the `content: [{ type: "text", text: "Error: ..." }]` block rather than throwing unhandled exceptions that terminate the stdio connection.
