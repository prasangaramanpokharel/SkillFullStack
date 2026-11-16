# Upstash Workflow Architecture & Patterns

Upstash Workflow provides code-first, durable execution directly inside serverless functions, surviving crashes and long pauses.

## Core Concepts
- **`context.run(id, fn)`**: Executes a step. If the workflow resumes later, completed steps are skipped and their cached results are returned instantly.
- **`context.sleep(id, seconds)`**: Suspends the workflow without keeping the serverless instance alive. QStash wakes the function up when the timer expires.
- **`context.sleepUntil(id, timestamp)`**: Suspends until a specific UNIX timestamp.
- **`context.call(id, { url, method, body })`**: Dispatches an HTTP call via QStash and awaits the response durably.

## AI Background Agent Workflow Example

```typescript
import { serve } from "@upstash/workflow/nextjs";

export const { POST } = serve(async (context) => {
  // 1. Fetch task details
  const task = await context.run("fetch-task", async () => {
    return db.tasks.findUnique({ where: { status: "pending" } });
  });

  // 2. Call LLM for generation
  const draft = await context.run("generate-draft", async () => {
    return aiClient.generateText({ prompt: task.prompt });
  });

  // 3. Sleep for user approval or scheduled window (e.g. 2 hours)
  await context.sleep("review-delay", 7200);

  // 4. Publish completed artifact
  await context.run("publish-result", async () => {
    return publishArtifact(draft);
  });
});
```
