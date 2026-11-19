---
name: openai
description: Production OpenAI engineering master guide. Implements the modern Responses API (/v1/responses), Decisions API, stateful conversations, background mode, built-in tools (web search, file search, computer use, MCP), streaming/WebSockets, mid-turn steering, multi-agent patterns, evals, fine-tuning (DPO, supervised), and Amazon Bedrock/Google Cloud deployments.
version: 2026.x
last-verified: 2026-11-19
compatibility: OpenAI Python SDK v1.60+, OpenAI Node/TS SDK v4.80+, OpenAI CLI, REST API v1
slash-commands:
  - command: /openai-responses
    description: Implement or migrate from Chat Completions / Assistants API to the unified Responses API (/v1/responses).
    argument-hint: "[--stream] [--store=true]"
  - command: /openai-tools
    description: Configure built-in tools (web search, file search, code interpreter, MCP servers) and structured outputs.
    argument-hint: "[--tool=mcp|web_search|file_search]"
  - command: /openai-state
    description: Manage durable conversation state, background mode, compaction, and mid-turn steering.
    argument-hint: "[--conversation-id=<id>]"
  - command: /openai-evals
    description: Set up prompt optimization, model evaluation matrices, and LLM graders.
    argument-hint: "[--eval-set=<path>]"
  - command: /openai-finetuning
    description: Guide supervised fine-tuning, vision fine-tuning, and Direct Preference Optimization (DPO).
    argument-hint: "[--method=dpo|supervised]"
  - command: /openai-cloud
    description: Deploy OpenAI models on Amazon Bedrock or Google Cloud with enterprise IAM.
    argument-hint: "[--provider=bedrock|gcp]"
---

# OpenAI Production Engineering Master Guide

This skill governs the architecture, development, optimization, and deployment of production AI applications built on OpenAI's state-of-the-art APIs and cloud integrations.

---

## ⚡ Zero-Hallucination Offline Assets Notice
Before generating OpenAI code or configuring models, agents **MUST** consult bundled official specifications in [`assets/`](assets/README.md):
- Quickstart & Overview: [`assets/quickstart/quickstart.md`](assets/quickstart/quickstart.md)
- Responses API: [`assets/core-concepts/responses-api.md`](assets/core-concepts/responses-api.md)
- Decisions API: [`assets/core-concepts/decisions-api.md`](assets/core-concepts/decisions-api.md)
- Conversation State: [`assets/core-concepts/conversation-state.md`](assets/core-concepts/conversation-state.md)
- Background Mode: [`assets/core-concepts/background-mode.md`](assets/core-concepts/background-mode.md)
- Compaction: [`assets/core-concepts/compaction.md`](assets/core-concepts/compaction.md)
- Agents Overview: [`assets/core-concepts/agents.md`](assets/core-concepts/agents.md)
- Function Calling: [`assets/core-concepts/function-calling.md`](assets/core-concepts/function-calling.md)
- Async Tool Calling: [`assets/core-concepts/async-tool-calling.md`](assets/core-concepts/async-tool-calling.md)
- Code Interpreter: [`assets/core-concepts/tools-code-interpreter.md`](assets/core-concepts/tools-code-interpreter.md)
- Custom MCP Server: [`assets/core-concepts/custom-mcp-server.md`](assets/core-concepts/custom-mcp-server.md)
- Migration from Chat/Assistants: [`assets/guides/migrate-to-responses.md`](assets/guides/migrate-to-responses.md)
- Model Optimization: [`assets/guides/model-optimization.md`](assets/guides/model-optimization.md)
- Amazon Bedrock Integration: [`assets/guides/amazon-bedrock.md`](assets/guides/amazon-bedrock.md)
- Evals Guide: [`assets/guides/evals.md`](assets/guides/evals.md)
- Batch API: [`assets/guides/batch.md`](assets/guides/batch.md)

---

## 1. Core Architecture: The Unified Responses API (`/v1/responses`)

OpenAI has unified Chat Completions and the deprecated Assistants API into the **Responses API (`/v1/responses`)**. 

```
┌────────────────────────────────────────────────────────────────────────┐
│                   UNIFIED RESPONSES API (/v1/responses)                │
├────────────────────────────────────────────────────────────────────────┤
│  • Single execution loop replacing complex Run / RunStep polling       │
│  • Native Built-in Tools: web_search, file_search, code_interpreter,   │
│    computer_use, and remote Model Context Protocol (MCP) servers       │
│  • Stateful Conversations: store: true / conversation_id tracking      │
│  • Background Mode: Long-running asynchronous execution & Webhooks     │
│  • Mid-Turn Steering: Inject dynamic constraints or human oversight   │
│  • High-Efficiency Prompt Caching: Automatic prefix cache hits         │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.1 Standard Responses API Invocation (Python & TypeScript)

#### Python Standard:
```python
import os
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class ExtractionSchema(BaseModel):
    summary: str
    action_items: list[str]
    urgency_score: int

# Responses API with structured output and built-in search
response = client.responses.create(
    model="gpt-4o",
    input="Summarize the latest quarterly AI regulations and draft immediate compliance steps.",
    tools=[
        {"type": "web_search_preview"},
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "regulatory_summary",
            "schema": ExtractionSchema.model_json_schema(),
            "strict": True,
        }
    },
    store=True,  # Enables stateful conversation tracking
)

print(response.output_text)
```

#### TypeScript Standard:
```typescript
import OpenAI from "openai";
import { z } from "zod";
import { zodResponseFormat } from "openai/helpers/zod";

const openai = new OpenAI();

const AnalysisSchema = z.object({
  sentiment: z.enum(["bullish", "neutral", "bearish"]),
  confidence: z.number().min(0).max(1),
  keyDrivers: z.array(z.string()),
});

const response = await openai.responses.create({
  model: "gpt-4o",
  input: "Analyze this market update for enterprise SaaS.",
  response_format: zodResponseFormat(AnalysisSchema, "market_analysis"),
  store: true,
});

console.log(response.output_text);
```

---

## 2. Migration from Legacy APIs to Responses API

### 2.1 From Chat Completions (`/v1/chat/completions`)
| Chat Completions (Legacy) | Responses API (Modern Standard) |
| :--- | :--- |
| `client.chat.completions.create(...)` | `client.responses.create(...)` |
| `messages: [{"role": "user", ...}]` | `input: "..."` or structured items |
| Manual client-side tool loop | Native built-in tool execution loop |
| No conversation state persistence | `store: true` or `conversation_id: "conv_..."` |
| `choices[0].message.content` | `response.output_text` or typed `response.output` items |

### 2.2 From Assistants API (`/v1/assistants`, `/v1/threads`)
| Assistants API (Sunsetted) | Responses API (Modern Standard) |
| :--- | :--- |
| Server-side Assistant objects | Managed Prompts or system instructions in code |
| Threads (`thread_id`) | Conversations (`conversation_id`) |
| Runs & RunSteps polling loops | Single request execution or background webhooks |
| Vector store attachments | `file_search` tool with managed or local vector indexes |

Detailed migration patterns: [`references/migrateToResponsesGuide.md`](references/migrateToResponsesGuide.md).

---

## 3. Advanced Capabilities & Real-Time Patterns

### 3.1 Background Execution & Webhooks
For long-running tasks or heavy tool chains:
```python
# Launch asynchronous background task
bg_response = client.responses.create(
    model="o3-mini",
    input="Perform deep mathematical proof verification on the submitted dataset.",
    background=True,
    webhook_url="https://api.yourdomain.com/webhooks/openai",
)
print(f"Queued response ID: {bg_response.id}, status: {bg_response.status}")
```

### 3.2 Streaming & Mid-Turn Steering
Use WebSockets or server-sent events (SSE) for low-latency streaming and steer mid-flight generation:
- Reference guide: [`references/conversationStateAndSteering.md`](references/conversationStateAndSteering.md)
- Official specification: [`assets/core-concepts/async-tool-calling.md`](assets/core-concepts/async-tool-calling.md)

### 3.3 Model Context Protocol (MCP) Integration
Connect external databases, APIs, and microservices directly into the Responses API toolchain:
- Guide: [`references/toolsAndMcpIntegration.md`](references/toolsAndMcpIntegration.md)

---

## 4. Model Optimization, Evals & Fine-Tuning

1. **Prompt Optimization**: Automatically refine instructions using OpenAI's prompt optimizer.
2. **LLM Graders & Evaluation Suites**: Run deterministic regression tests against gold-standard datasets.
3. **Direct Preference Optimization (DPO)**: Align models on custom style, domain tone, or safety constraints.
4. **Cloud Providers (Bedrock & GCP)**: Deploy OpenAI models through enterprise VPC boundaries via Amazon Bedrock or Google Cloud.
   - Reference: [`references/cloudProvidersBedrockGcp.md`](references/cloudProvidersBedrockGcp.md)

---

## 5. Anti-Patterns to Avoid

| Anti-Pattern | Why It Breaks Production | Correct Modern Standard |
| :--- | :--- | :--- |
| **New projects on Assistants API** | Assistants API is deprecated; creates brittle polling loops and high latency. | Use the unified Responses API (`/v1/responses`) with `store: true`. |
| **Parsing JSON without `strict: true`** | LLMs occasionally omit required keys or emit trailing commas. | Enforce Structured Outputs with `strict: true` and Pydantic/Zod schemas. |
| **Uncached repetitive prompt prefixes** | Spikes inference cost and increases Time-to-First-Token (TTFT). | Structure prompts with identical static system prefixes to leverage OpenAI automatic prompt caching (>50% cost savings). |
| **Hardcoding API Keys in Client Code** | Vulnerable to key extraction and abuse. | Use backend proxy routes or IAM authentication with Amazon Bedrock / Google Cloud. |
| **Polling active runs in a tight loop** | Hits rate limits and burns server CPU cycles. | Use streaming SSE, WebSockets, or background webhooks (`background=True`). |
| **Ignoring Reasoning Token Limits (`max_completion_tokens`)** | Reasoning models (o-series) can exhaust token budget before completing output. | Always allocate adequate `max_completion_tokens` separating reasoning vs visible tokens. |

---

## 6. Verification & Automated Diagnostics

Run the bundled OpenAI integration auditor before deploying:
```bash
python3 skills/dataAi/openai/scripts/auditOpenaiIntegration.py --path ./src
```
