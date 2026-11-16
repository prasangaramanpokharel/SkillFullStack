# Idempotency Key Strategies

When dispatching background events:
- Always supply an `idempotencyKey` when publishing events from webhooks (e.g., Stripe charge ID, GitHub commit SHA).
- Inngest and QStash deduplicate identical keys within their configured window (typically 24 hours), preventing double-charges, duplicate emails, and repeated LLM token spend.
