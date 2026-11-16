# Promptfoo Configuration Specification

## Key Configuration Sections
1. **`prompts`**: Array of prompt strings, file paths (`file://prompt.txt`), or function handlers.
2. **`providers`**: Target models to test against (e.g., `openai:gpt-4o`, `anthropic:messages:claude-3-5-sonnet`, `vertex:gemini-1.5-pro`).
3. **`defaultTest`**: Global assertions applied across every test case (e.g., latency threshold, cost cap, moderation).
4. **`tests`**: Test cases containing `vars` inputs and an `assert` array.

## Common Assertion Types
- `equals`: Exact string match.
- `icontains`: Case-insensitive substring match.
- `contains-json` / `is-json`: Validates output is valid JSON.
- `javascript`: Custom JS evaluation script (e.g. `output.length < 500`).
- `llm-rubric`: Model-graded semantic assertion according to natural language criteria.
- `cost`: Asserts that token cost does not exceed a dollar threshold.
- `latency`: Asserts response time in milliseconds.
