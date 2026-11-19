# Conversation State Management

Manage multi-turn context natively without manually sending full history back and forth.

## Creating Stateful Conversations
Pass `store: true` when creating a response to persist the exchange. The returned `conversation_id` is passed into subsequent requests:

```python
response = client.responses.create(
    model="gpt-4o",
    conversation_id="conv_123456",
    input="Continue from our previous discussion on system scaling."
)
```
