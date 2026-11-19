---
name: promptEvalTesting
description: CI/CD prompt regression testing, evaluation harnesses, and LLM-as-a-judge metrics with Promptfoo and DeepEval. Use when testing prompt changes, preventing regressions, and asserting accuracy before merging.
version: latest
last-verified: 2026-11-15
compatibility: Node.js 18+, Python 3.10+, pytest, GitHub Actions, GitLab CI
slash-commands:
  - command: /prompt-eval
    description: Design CI/CD regression evaluation harness with Promptfoo and DeepEval
    argument-hint: "[--tool=promptfoo|deepeval]"
  - command: /prompt-judge
    description: Configure LLM-as-a-judge scoring metrics and assert criteria
    argument-hint: "[--metric=semantic-similarity|g-eval]"

---

# Prompt Evaluation & Regression Testing Engineering Guide

## 1. Core Architecture (Preventing Silent Prompt Regressions)
Tweaking a prompt to fix one edge case often breaks three others. Automated evaluation acts as the **CI/CD test harness for prompts**:

```
┌─────────────────────────────────┐
│     Prompt or Model Update      │
└────────────────┬────────────────┘
                 ▼
┌─────────────────────────────────┐
│     Golden Dataset Matrix       │  (100+ edge cases, malicious inputs,
└────────────────┬────────────────┘   and typical customer queries)
                 ▼
┌─────────────────────────────────┐
│   Automated Evaluation Runners  │
│  • Promptfoo (YAML / CLI-first) │
│  • DeepEval  (Python / Pytest)  │
└────────────────┬────────────────┘
                 ▼
┌─────────────────────────────────┐
│       Assertion Gateways        │
│  - Exact Match & Regex          │
│  - JSON Schema Validation       │
│  - LLM-as-a-Judge Rubric        │
└────────────────┬────────────────┘
                 │ Pass: Merge PR
                 │ Fail: Block Build (Non-zero exit code)
```

---

## 2. Promptfoo Configuration (`promptfooconfig.yaml`)

```yaml
description: "Customer Support AI Prompt Regression Suite"

prompts:
  - "You are a customer support agent. Answer concisely:\nUser: {{query}}"

providers:
  - id: openai:gpt-4o
  - id: anthropic:messages:claude-3-5-sonnet-20241022

tests:
  - description: "Refund policy assertion"
    vars:
      query: "Can I get a refund after 20 days?"
    assert:
      - type: icontains
        value: "refund"
      - type: llm-rubric
        value: "The response must clearly state that refunds are allowed within 30 days."

  - description: "JSON format enforcement"
    vars:
      query: "Return user ID 42 profile"
    assert:
      - type: is-json
      - type: javascript
        value: "output.userId === 42"
```

Run locally or in CI:
```bash
npx promptfoo@latest eval --ci
```

---

## 3. DeepEval Python / Pytest Native Pattern

```python
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric

def test_rag_faithfulness():
    query = "What is the capital of France?"
    actual_output = "The capital of France is Paris."
    retrieval_context = ["Paris is the capital and most populous city of France."]

    test_case = LLMTestCase(
        input=query,
        actual_output=actual_output,
        retrieval_context=retrieval_context
    )

    metric = FaithfulnessMetric(threshold=0.8)
    assert_test(test_case, [metric])
```

---

## 4. Anti-Patterns & Critical Traps
- ❌ **Eyeball / Vibe Testing**: Testing prompt edits by casually trying 1 or 2 prompts in a chat window. Always run against a versioned golden test matrix.
- ❌ **Unpinned Judge Models**: Using floating model tags (e.g. `gpt-4`) for LLM-as-a-judge assertions introduces drift into your CI pipeline. Pin explicit model snapshots.
- ❌ **Soft Warnings in CI**: Configuring evals that print failures but exit with code `0`. Always enforce non-zero exit codes to block Pull Requests on regressions.

---

## 5. References & Bundled Utilities
- Promptfoo config options & syntax: [references/promptfooConfigSpecs.md](references/promptfooConfigSpecs.md)
- Research-backed evaluation metrics catalog: [references/evalMetricsCatalog.md](references/evalMetricsCatalog.md)
- Evaluation suite runner script: [scripts/runPromptEvalSuite.py](scripts/runPromptEvalSuite.py)
