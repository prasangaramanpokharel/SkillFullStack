---
name: upstash
description: Production serverless Redis, Vector, QStash messaging, durable Workflows, and Ratelimit. Use when implementing serverless caching, rate limiting LLM APIs, queuing asynchronous background tasks, or building durable step-function workflows.
version: 2026.x
last-verified: 2026-11-15
compatibility: Node.js 18+, Vercel Edge / Serverless, Cloudflare Workers, Next.js, Python 3.10+
slash-commands:
  - command: /upstash-redis
    description: Configure low-latency serverless Redis operations and pipelines
    argument-hint: "[--pipeline=true]"
  - command: /upstash-ratelimit
    description: Implement dynamic sliding window rate limiting
    argument-hint: "[--limit=10] [--window=10s]"
  - command: /upstash-workflow
    description: Design serverless QStash durable workflows
    argument-hint: "[--step=Name]"

---

# Upstash Serverless Engineering Guide

## 1. Core Architecture & Mental Model
Upstash replaces traditional persistent TCP infrastructure with **HTTP/REST-native serverless primitives**.
- **Zero Connection Pools**: Runs directly on Edge workers and lambda functions without exhausting database connection limits.
- **Micro-Billing & Scale-to-Zero**: Eliminates idle server costs; ideal for variable traffic and agentic background loops.
- **Multi-Pillar Platform**:
  1. **Redis**: Sub-millisecond key-value caching, sessions, and pub/sub.
  2. **Ratelimit**: Token bucket & sliding window rate limiting with `dynamicLimits` for LLM protection.
  3. **QStash**: Distributed serverless message queue, retry coordinator, and cron scheduler with Flow Control.
  4. **Workflow**: Code-first durable execution (step functions) bypassing serverless execution timeouts.
  5. **Vector**: Serverless embedding index for RAG and semantic retrieval.

---

## 2. Platform Component Matrix & Canonical Usage

### A. Ratelimit (Protecting AI & API Routes)
Use `@upstash/ratelimit` with Redis to prevent token exhaustion and API abuse:
```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

export const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "10s"),
  analytics: true,
  dynamicLimits: true, // Allows modifying limits at runtime in Redis without redeploying
});
```
*Note on Edge / Serverless*: When logging analytics asynchronously in Edge routes, wrap with `context.waitUntil(pending)`.

### B. Upstash Workflow (Durable Step Functions)
Durable execution natively inside serverless endpoints—automatically retries failed steps without re-running earlier steps:
```typescript
import { serve } from "@upstash/workflow/nextjs";

export const { POST } = serve(async (context) => {
  // Step 1: Ingest input
  const userData = await context.run("fetch-user", async () => {
    return fetchUserData();
  });

  // Step 2: Long-running or rate-sensitive AI step
  const summary = await context.run("generate-ai-summary", async () => {
    return callLlmApi(userData);
  });

  // Step 3: Sleep or wait for webhook without holding serverless process alive
  await context.sleep("wait-1-hour", 3600);

  // Step 4: Follow up
  await context.run("send-notification", async () => {
    await sendAlert(summary);
  });
});
```

### C. QStash & Modern Flow Control
QStash publishes messages via HTTPS. Use **Flow Control** instead of rigid FIFO blocking queues:
- Controls concurrency and consumption rate per user/key.
- Does not block subsequent tasks if an individual job fails.

---

## 3. Environment Variables Standard
```env
UPSTASH_REDIS_REST_URL="https://...upstash.io"
UPSTASH_REDIS_REST_TOKEN="..."
QSTASH_URL="https://qstash.upstash.io/v2"
QSTASH_TOKEN="..."
UPSTASH_VECTOR_REST_URL="https://...upstash.io"
UPSTASH_VECTOR_REST_TOKEN="..."
```

---

## 4. Anti-Patterns & Critical Pitfalls
- ❌ **Traditional TCP Redis Client**: Avoid `@redis/client` or `ioredis` on serverless lambdas unless running long-lived containers; use `@upstash/redis` (REST-based) to prevent TCP connection pool crashes.
- ❌ **Blocking FIFO Queues**: Do not rely on legacy strict FIFO queues that stall pipelines on single errors; use QStash **Flow Control** for rate and concurrency quotas.
- ❌ **Hardcoded Rate Limits**: Use `dynamicLimits: true` so limits can be adjusted instantly via Redis without rebuilding code.
- ❌ **Unawaited Edge Analytics**: Forgetting `context.waitUntil(ratelimit.pending)` in Edge routes drops analytics.

---

## 5. References & Bundled Guides
- Rate limiting strategies & algorithms: [references/ratelimitPatterns.md](references/ratelimitPatterns.md)
- Durable workflow patterns & step functions: [references/workflowPatterns.md](references/workflowPatterns.md)
- QStash message queues and flow control: [references/qstashFlowControl.md](references/qstashFlowControl.md)
- Diagnostic script: [scripts/testRedisConnection.py](scripts/testRedisConnection.py)
