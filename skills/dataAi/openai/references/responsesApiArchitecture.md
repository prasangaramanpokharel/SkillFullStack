# Responses API Architecture & Specification

The OpenAI Responses API (`POST /v1/responses`) serves as the next-generation unified runtime for OpenAI models, streamlining chat completions, assistant loops, tool execution, and state persistence into a unified request cycle.

---

## 1. Core Request Parameters

```typescript
interface CreateResponseParams {
  model: string;                      // e.g. "gpt-4o", "o3-mini"
  input: string | ResponseInputItem[]; // Prompt string or multi-modal item array
  instructions?: string;              // High-level developer system instructions
  tools?: ResponseTool[];             // Built-in tools or custom function tools
  response_format?: ResponseFormat;   // Structured outputs with strict JSON schema
  store?: boolean;                    // Persist response into OpenAI conversation store
  conversation_id?: string;           // Continue existing multi-turn conversation
  background?: boolean;               // Run asynchronously for long-running workflows
  webhook_url?: string;               // Webhook target when background: true
  temperature?: number;               // Sampling temperature (0.0 - 2.0)
  max_output_tokens?: number;         // Maximum visible completion tokens
}
```

---

## 2. Response Object Anatomy

```json
{
  "id": "resp_01j8m4k8...",
  "object": "response",
  "created_at": 1740000000,
  "status": "completed",
  "model": "gpt-4o-2026-02",
  "output_text": "Here is the verified executive summary...",
  "output": [
    {
      "id": "item_01j8m4ka...",
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Here is the verified executive summary..."
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 842,
    "output_tokens": 156,
    "input_tokens_details": {
      "cached_tokens": 512
    },
    "output_tokens_details": {
      "reasoning_tokens": 64
    }
  }
}
```

---

## 3. High-Efficiency Prompt Caching

OpenAI automatically caches prompt prefixes that exceed 1,024 tokens:
1. **Cache Read Discount**: Cached input tokens are discounted by up to 50% compared to uncached inputs.
2. **Deterministic Cache Keys**: Maintain static tool declarations and system instructions at the top of the prompt.
3. **Dynamic Variables at the End**: Place per-request dynamic data, user inputs, and timestamps at the very end to maximize cache prefix hit rates.
