# Responses API Specification

The Responses API is OpenAI's recommended primitive for all new applications.

## Key Capabilities
- **Direct String Input**: Simple string prompts or structured message arrays.
- **Built-in Tools**: Search the web, query files, and run code in one step.
- **Durable Conversations**: Preserve context with `store: true`.
- **Structured Outputs**: Native adherence to JSON Schema with `strict: true`.

## Endpoint
`POST https://api.openai.com/v1/responses`
