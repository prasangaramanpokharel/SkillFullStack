---
name: generativeUi
description: Stream interactive React components from LLMs using Vercel AI SDK, tool invocations, and createDataStreamResponse. Use when replacing text-only chat with dynamic charts, cards, confirmation forms, and interactive UI widgets.
version: v4
last-verified: 2026-11-15
compatibility: Next.js 14/15, React 18/19, Vercel AI SDK v4+
slash-commands:
  - command: /genui-stream
    description: Stream interactive React components from LLMs via Vercel AI SDK
    argument-hint: "[--transport=createDataStreamResponse]"
  - command: /genui-tool
    description: Map generative AI tool executions to interactive client components
    argument-hint: "[--component=Name]"

---

# Generative UI Engineering Guide

## 1. Core Architecture (Tool-Driven Component Streaming)
Generative UI replaces plain markdown text by allowing the LLM to trigger typed tools whose arguments and outputs map directly to interactive React client components.

```
┌────────────────────────────────┐
│   LLM triggers tool call       │
│   e.g. showWeather({ city })   │
└──────────────┬─────────────────┘
               │  Streams via DataStream Protocol
               ▼
┌────────────────────────────────┐
│   Client intercepts toolCall   │
│   state: 'call' | 'result'     │
└──────────────┬─────────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌──────────────┐ ┌──────────────┐
│ Pending State│ │ Result State │
│  <Skeleton/> │ │ <WeatherCard>│
└──────────────┘ └──────────────┘
```

---

## 2. Server Implementation (`app/api/chat/route.ts`)

```typescript
import { openai } from "@ai-sdk/openai";
import { createDataStreamResponse, streamText, tool } from "ai";
import { z } from "zod";

export const runtime = "edge";

export async function POST(req: Request) {
  const { messages } = await req.json();

  return createDataStreamResponse({
    execute: async (dataStream) => {
      const result = streamText({
        model: openai("gpt-4o"),
        messages,
        tools: {
          displayFlightBooking: tool({
            description: "Display an interactive flight booking card with confirmation controls",
            parameters: z.object({
              flightNumber: z.string(),
              origin: z.string(),
              destination: z.string(),
              price: z.number(),
            }),
            execute: async (flightData) => {
              // Server executes confirmation validation or DB fetch
              return { status: "ready_to_book", ...flightData };
            },
          }),
        },
      });

      result.mergeIntoDataStream(dataStream);
    },
  });
}
```

---

## 3. Client Component Mapping (`components/Chat.tsx`)

```tsx
"use client";

import { useChat } from "ai/react";
import { FlightCard } from "@/components/FlightCard";
import { FlightSkeleton } from "@/components/FlightSkeleton";

export function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div className="flex flex-col gap-4">
      {messages.map((m) => (
        <div key={m.id} className="space-y-2">
          <p className="font-semibold">{m.role === "user" ? "You" : "AI"}:</p>
          <div>{m.content}</div>

          {/* Map tool invocations directly to interactive components */}
          {m.toolInvocations?.map((toolInvocation) => {
            const { toolName, toolCallId, state } = toolInvocation;

            if (toolName === "displayFlightBooking") {
              if (state === "result") {
                return <FlightCard key={toolCallId} data={toolInvocation.result} />;
              }
              return <FlightSkeleton key={toolCallId} />;
            }
            return null;
          })}
        </div>
      ))}
    </div>
  );
}
```

---

## 4. Anti-Patterns & Critical Traps
- ❌ **Dumping Code Strings**: Never have the model output raw JSX/TSX as a string to be `eval()`'d on the client. Always use typed tools that map to existing client components.
- ❌ **Missing Pending State**: Forgetting to handle `state === 'call'` leaves the UI blank while the server or user executes the tool. Always show a loading skeleton or active card.
- ❌ **Breaking DataStream Merging**: Forgetting `result.mergeIntoDataStream(dataStream)` prevents tool call arguments from reaching client components.

---

## 5. References & Bundled Utilities
- Client component tool mapping patterns: [references/clientToolComponentMapping.md](references/clientToolComponentMapping.md)
- Data stream protocol lifecycle: [references/dataStreamProtocol.md](references/dataStreamProtocol.md)
- Component generator script: [scripts/generateUiComponentStub.py](scripts/generateUiComponentStub.py)
