---
name: durableBackgroundJobs
description: Durable background execution, long-running agent workflows, and zero-timeout event orchestration with Inngest, Trigger.dev v3, and Upstash Workflow. Use when running multi-step AI tasks, retries, and sleep delays in serverless environments.
version: 3.x
last-verified: 2026-11-15
compatibility: Next.js, Node.js 18+, Python 3.10+, Inngest SDK, Trigger.dev v3
slash-commands:
  - command: /jobs-workflow
    description: Design durable multi-step workflows with Inngest or Trigger.dev
    argument-hint: "[--engine=inngest|triggerdev]"
  - command: /jobs-step
    description: Implement zero-timeout step function with automatic retries
    argument-hint: "[--step=Name]"
  - command: /jobs-cron
    description: Configure scheduled background cron jobs with jitter
    argument-hint: "[--schedule='*/5 * * * *']"

---

# Durable Background Jobs & Workflows Engineering Guide

## 1. Core Architecture (Overcoming Serverless Timeouts)
Serverless functions enforce hard 10–60s timeouts. Durable execution breaks code into **memoized steps**:

```
┌────────────────────────────────┐
│   Trigger: event received      │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│ step.run("fetch-source-data")  │──► Succeeded & Memoized
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│ step.run("call-llm-analysis")  │──► Fails? Retried in isolation without
└──────────────┬─────────────────┘    re-executing Step 1!
               ▼
┌────────────────────────────────┐
│ step.sleep("wait-for-human")   │──► Zero compute cost while paused
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│ step.run("send-final-payload") │
└────────────────────────────────┘
```

---

## 2. Inngest Step Orchestration Pattern

```typescript
import { Inngest } from "inngest";

export const inngest = new Inngest({ id: "fullstack-ai-app" });

export const autonomousResearchAgent = inngest.createFunction(
  {
    id: "autonomous-research-agent",
    retries: 3,
    concurrency: { limit: 5, key: "event.data.userId" },
  },
  { event: "agent/research.requested" },
  async ({ event, step }) => {
    // Step 1: Scrape & decompose queries
    const searchResults = await step.run("search-web-sources", async () => {
      return executeWebSearch(event.data.query);
    });

    // Step 2: Multi-step LLM synthesis
    const synthesizedReport = await step.run("synthesize-findings", async () => {
      return callLlmSynthesis(searchResults);
    });

    // Step 3: Sleep or wait for user webhook approval
    await step.sleep("wait-for-cooldown", "30m");

    // Step 4: Dispatch notifications
    await step.run("publish-report", async () => {
      return emailReportToUser(event.data.userId, synthesizedReport);
    });

    return { status: "completed", reportId: synthesizedReport.id };
  }
);
```

---

## 3. Trigger.dev v3 Managed Container Task Pattern

```typescript
import { task, wait } from "@trigger.dev/sdk/v3";

export const heavyAiBatchTask = task({
  id: "heavy-ai-batch-pipeline",
  retry: { maxAttempts: 4 },
  run: async (payload: { items: string[] }) => {
    const results = [];
    for (const item of payload.items) {
      // Automatic container checkpointing across long loops
      const processed = await processItemWithLlm(item);
      results.push(processed);
      await wait.for({ seconds: 2 });
    }
    return { count: results.length, data: results };
  },
});
```

---

## 4. Anti-Patterns & Critical Pitfalls
- ❌ **Monolithic Step Traps**: Putting your entire multi-minute script inside a single `step.run()` block defeats durable execution. Break distinct network boundaries into separate steps.
- ❌ **Non-Serializable Return Values**: Every value returned by `step.run()` is serialized to JSON. Never return Class instances, database sockets, or non-serializable objects.
- ❌ **Ephemeral Local Disk Reliance**: Steps can run across different container invocations or machines. Never store intermediate data in `/tmp` expecting it to survive between steps; pass data via step return values or S3/Blob storage.
- ❌ **Unconstrained Parallel Fan-out**: Spawning 10,000 sub-steps simultaneously crashes downstream third-party APIs. Always set concurrency throttle limits.

---

## 5. References & Bundled Utilities
- Step patterns & retry policies: [references/durableStepPatterns.md](references/durableStepPatterns.md)
- Idempotency key strategies: [references/idempotencyKeys.md](references/idempotencyKeys.md)
- Event dispatch tester: [scripts/testWorkflowDispatch.py](scripts/testWorkflowDispatch.py)
