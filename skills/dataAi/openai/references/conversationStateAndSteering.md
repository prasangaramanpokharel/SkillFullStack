# Conversation State & Mid-Turn Steering

The Responses API provides native capabilities to maintain context across sessions and steer agent execution in real time.

---

## 1. Stateful Conversations

Pass `store=True` to create a managed conversation, or supply an existing `conversation_id`:

```python
# Turn 1: Initialize conversation
turn1 = client.responses.create(
    model="gpt-4o",
    input="My team is building an e-commerce platform in Next.js 16.",
    store=True
)
conv_id = turn1.conversation_id

# Turn 2: Follow-up without re-sending Turn 1 text
turn2 = client.responses.create(
    model="gpt-4o",
    conversation_id=conv_id,
    input="Recommend the best payment integration strategy for this stack."
)
```

---

## 2. Mid-Turn Steering & Human-in-the-Loop

Mid-turn steering enables human reviewers or automated safety monitors to modify active generation:

1. **Pause & Inspect**: Listen to tool call events before execution.
2. **Inject Feedback**: Submit clarification or cancellation tokens back into the active stream.
3. **Compaction**: Automatically summarize older conversation segments to avoid token exhaustion.
