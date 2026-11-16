# QStash Flow Control & Queues

QStash provides HTTP-first message delivery, retries, and scheduling. Modern QStash replaces strict FIFO queue blocking with **Flow Control**.

## 1. Flow Control vs Legacy Queues
- **Legacy Queues**: A single failed message blocked all downstream processing in FIFO queues.
- **Flow Control**: Controls execution rates and concurrency limits per key or globally without stalling the pipeline when errors happen.

## 2. Publishing Messages with Flow Control
```typescript
import { Client } from "@upstash/qstash";

const qstash = new Client({ token: process.env.QSTASH_TOKEN! });

// Publish with concurrency and rate limits
await qstash.publishJSON({
  url: "https://my-app.com/api/process-job",
  body: { jobId: "123" },
  flowControl: {
    key: "customer_abc",
    rate: 10,       // 10 requests
    period: "1m",   // per minute
  },
  retries: 3,
});
```

## 3. Scheduled Messages (Cron)
```typescript
await qstash.schedules.create({
  destination: "https://my-app.com/api/daily-digest",
  cron: "0 9 * * *", // 9 AM daily
});
```
