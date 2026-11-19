# Migration Guide: Upgrading to the OpenAI Responses API

This guide provides step-by-step instructions for refactoring legacy Chat Completions (`/v1/chat/completions`) and legacy Assistants API (`/v1/assistants`) workflows to the unified Responses API (`/v1/responses`).

---

## 1. Migrating from Chat Completions

### Legacy Chat Completions (Python):
```python
# DEPRECATED PATTERN
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a financial advisor."},
        {"role": "user", "content": "Analyze my portfolio risk."}
    ],
    tools=[{"type": "function", "function": {"name": "get_stock_quote", ...}}]
)
content = response.choices[0].message.content
```

### Modern Responses API Pattern:
```python
# MODERN RESPONSES PATTERN
response = client.responses.create(
    model="gpt-4o",
    instructions="You are a financial advisor.",
    input="Analyze my portfolio risk.",
    tools=[
        {"type": "web_search_preview"},
        {"type": "function", "name": "get_stock_quote", "parameters": {...}}
    ],
    store=True
)
content = response.output_text
```

---

## 2. Migrating from Assistants API

### Why Assistants API was Deprecated:
1. **Excessive Latency**: Required creating threads, creating messages, starting runs, and polling `runs.retrieve()` in a loop.
2. **Hidden State & Cost**: Hard to track token usage across multiple runs in a thread.
3. **Complex Error Handling**: Required custom recovery logic for `failed`, `expired`, and `requires_action` states.

### Step-by-Step Transition:
1. **Assistant Definitions $\rightarrow$ System Instructions / Prompts**: Store instructions in your codebase or version-controlled dashboard Prompts.
2. **Threads $\rightarrow$ Conversation IDs**: When calling `responses.create()`, pass `conversation_id="conv_..."` to automatically inherit history.
3. **File Attachments $\rightarrow$ `file_search` Tool**: Attach files directly to the input payload or pass file IDs to the built-in `file_search` tool.
4. **Run Polling $\rightarrow$ Single Direct Call**: For real-time applications, await the single response object directly. For batch or long-running tasks, pass `background=True` with a webhook URL.
