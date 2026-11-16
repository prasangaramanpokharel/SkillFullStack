# Upstash Ratelimit Patterns

Comprehensive rate limiting algorithms for APIs and AI endpoints using `@upstash/ratelimit`.

## 1. Algorithm Selection Guide

| Algorithm | Method | Best For | Behavior |
| :--- | :--- | :--- | :--- |
| **Sliding Window** | `Ratelimit.slidingWindow(limit, window)` | General API routes, LLM chat endpoints | Smooths out bursts across sliding time frames without window-boundary spikes. |
| **Fixed Window** | `Ratelimit.fixedWindow(limit, window)` | Low-frequency operations (e.g. daily quota) | Simplest; resets strictly at the interval boundary. |
| **Token Bucket** | `Ratelimit.tokenBucket(refillRate, interval, maxTokens)` | Bursty traffic, AI generation APIs | Allows bursts up to `maxTokens`, refilling at continuous intervals. |

---

## 2. Next.js App Router Middleware / Route Handler Example

```typescript
import { NextRequest, NextResponse } from "next/server";
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const redis = Redis.fromEnv();
const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(20, "1m"),
  analytics: true,
  dynamicLimits: true,
});

export async function middleware(req: NextRequest) {
  const ip = req.headers.get("x-forwarded-for") ?? "127.0.0.1";
  const { success, pending, limit, reset, remaining } = await ratelimit.limit(ip);

  // Essential for Edge runtimes to deliver telemetry without slowing response
  // event.waitUntil(pending);

  if (!success) {
    return NextResponse.json(
      { error: "Too Many Requests", retryAfter: reset },
      { status: 429, headers: { "Retry-After": reset.toString() } }
    );
  }

  return NextResponse.next();
}
```

## 3. Dynamic Limits Pattern
Set `dynamicLimits: true`. Modify user limits on the fly in Redis without deployment:
```bash
# Key format: ratelimit:custom:<identifier>
redis-cli SET "ratelimit:custom:user_123" 100
```
