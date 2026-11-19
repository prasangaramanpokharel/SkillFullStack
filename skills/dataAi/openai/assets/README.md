# OpenAI Developers Official Documentation Catalog

This directory contains offline, un-truncated documentation mirrored directly from OpenAI's official markdown documentation endpoints (`developers.openai.com/api/docs/*.md`) for zero-hallucination agent execution.

## Catalog Sitemap

### Quickstart & Setup
- [Developer Quickstart](quickstart/quickstart.md): Make your first API request with the OpenAI SDK and Responses API.

### Core Concepts & Primitives
- [Key Concepts](core-concepts/key-concepts.md): Fundamental primitives and token concepts.
- [Agents Overview](core-concepts/agents.md): Compare the Agents API, Agents SDK, and Responses API.
- [Function Calling](core-concepts/function-calling.md): Define tools and handle model requests to call application functions.
- [Async Tool Calling](core-concepts/async-tool-calling.md): Start asynchronous tool calls and deliver results later.
- [Background Mode](core-concepts/background-mode.md): Run long-running Responses API requests and multi-turn workflows asynchronously.
- [Compaction](core-concepts/compaction.md): Manage long-running conversations with server-side and standalone compaction.
- [Code Interpreter](core-concepts/tools-code-interpreter.md): Allow models to write and run Python to solve problems.
- [Custom MCP Server](core-concepts/custom-mcp-server.md): Connect an MCP server to ChatGPT and Responses API.

### Migration & Cloud Guides
- [Migrate to the Responses API](guides/migrate-to-responses.md): Evolution of Chat Completions into the unified Responses API.
- [Assistants Migration Guide](guides/assistants-migration.md): Migrate from the retired Assistants API to the Responses API.
- [Model Optimization Guide](guides/model-optimization.md): Fine-tune, distill, and optimize models for the best performance.
- [Amazon Bedrock Integration](guides/amazon-bedrock.md): Deploy and run OpenAI models on Amazon Bedrock with AWS IAM and VPC isolation.
- [Evals Guide](guides/evals.md): Measure and improve model and application quality with OpenAI evals.
- [Batch API Guide](guides/batch.md): Asynchronous batch requests with 50% discount and higher rate limits.
