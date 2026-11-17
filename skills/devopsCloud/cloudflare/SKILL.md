---
name: cloudflare
description: Master Cloudflare engineering guide. Architect, scaffold, implement, deploy, and troubleshoot applications across the entire Cloudflare ecosystem (Workers, Static Assets, D1, R2, KV, Durable Objects, Queues, Workflows, Hyperdrive, Vectorize, WAF, Tunnels, Workers AI, and Agents SDK). Supports both Wrangler CLI and cf CLI.
version: 2026.x
last-verified: 2026-11-17
compatibility: Workers runtime (workerd), Wrangler v3+, cf CLI (beta), TypeScript 5+, Node.js 20+
slash-commands:
  - command: /cf-architect
    description: End-to-end Cloudflare system design, product selection, and cost estimation
    argument-hint: "[--workload=fullstack|api|ai|storage|iot]"
  - command: /cf-worker
    description: Scaffold and configure Cloudflare Workers with Static Assets and Service Bindings
    argument-hint: "[--entry=src/index.ts] [--assets=./dist]"
  - command: /cf-database
    description: Schema design, migrations, and bindings for D1, Hyperdrive, or Vectorize
    argument-hint: "[--engine=d1|hyperdrive|vectorize]"
  - command: /cf-storage
    description: State and storage architecture for R2, KV, Durable Objects, Queues, or Workflows
    argument-hint: "[--type=r2|kv|do|queues|workflows]"
  - command: /cf-security
    description: Cloudflare WAF, Rate Limiting, Zero Trust Tunnels, and DNS configuration
    argument-hint: "[--domain=example.com]"
  - command: /cf-ai
    description: Workers AI, AI Gateway, Agents SDK, and Vectorize implementation
    argument-hint: "[--model=@cf/meta/llama-3.3-70b-instruct]"
  - command: /cf-troubleshoot
    description: Diagnose proxied HTTP errors (52x status, 1xxx error codes, WAF 403 blocks)
    argument-hint: "[--status=522|524|1020|403]"
---

# Cloudflare Master Engineering Guide (2026)

Cloudflare is a unified global developer platform built on V8 isolates, anycast networking, and distributed storage primitives. It eliminates traditional container cold starts, delivers sub-10ms response times worldwide, and provides zero-egress object storage and serverless SQL.

> [!IMPORTANT]
> **Zero-Hallucination Protocol**: Always consult local offline documentation in [`assets/`](assets/README.md) and official deep product references in [`references/`](references/) before generating configuration, bindings, or CLI commands.

---

## 1. Cloudflare Platform Architecture

```
                                 CLOUDFLARE EDGE (300+ Cities)
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Anycast DNS ──► WAF / DDoS Mitigation ──► Edge Cache / CDN ──► Cloudflare Workers (workerd)  │
│                                                                        │                    │
│   ┌────────────────────┬────────────────────┬────────────────────┐     │                    │
│   ▼                    ▼                    ▼                    ▼     │                    │
│ D1 SQL             KV Store             R2 Storage           Durable   │                    │
│ (SQLite Replica)   (Global Read-Heavy)  (Zero-Egress Object) Objects   │                    │
│                                                                        │                    │
│   ┌────────────────────┬────────────────────┬────────────────────┐     │                    │
│   ▼                    ▼                    ▼                    ▼     │                    │
│ Hyperdrive         Queues               Workflows            Workers   │                    │
│ (Postgres Accel)   (Async Batching)     (Durable Steps)      AI (GPUs) │                    │
└────────────────────────────────────────────────────────────────────────┴────────────────────┘
                                         │ (Outbound Encrypted WireGuard)
                                         ▼
                            Cloudflare Tunnel (cloudflared)
                                         │
                               Origin Servers / VPC / Docker
```

1. **V8 Isolates (`workerd`)**: Workers run in lightweight V8 isolates instead of Docker containers. Cold starts are under 5ms, memory overhead is microscopic (< 5 MB), and compute scales automatically across 300+ data centers.
2. **Global Anycast Network**: Traffic hits the closest geographic data center automatically without regional load balancers.
3. **Workers Static Assets (Modern Replacement for Pages)**: Serve static SPAs, frontend bundles, and static files directly from CDN edge storage while combining dynamic serverless logic in the same worker.
4. **Service Bindings**: Direct memory-to-memory RPC calls between separate Workers with zero HTTP serialization, zero DNS lookups, and zero network latency.

---

## 2. CLI Strategy: `wrangler` vs `cf` CLI

Cloudflare operates two official CLIs in 2026:

| Scenario | Tool to Choose | Reason |
| :--- | :--- | :--- |
| **Existing Worker with `wrangler.jsonc` or `wrangler.toml`** | **`wrangler`** | Preserve existing deployment pipeline and scripts. |
| **New Full-Stack App (Next.js, Astro, Remix, SvelteKit)** | **`wrangler`** (`npm create cloudflare@latest`) | Framework adapters (OpenNext, Astro) currently hook into Wrangler build targets. |
| **Account-Level Infrastructure (DNS, Tunnels, WAF, AI Gateway)** | **`cf` CLI** | Declarative multi-resource management across your entire account. |
| **AI Coding Agent Workflows / MCP** | **`cf` CLI** + **Cloudflare MCP** | Machine-readable outputs and `cf cli search` command discovery. |

> [!TIP]
> Do not mix CLIs haphazardly within a single project. Use `wrangler` for worker code and deployment; use `cf` for account-wide infrastructure orchestration.

---

## 3. Product Selection Decision Tree

Consult [`references/productSelectionMatrix.md`](references/productSelectionMatrix.md) for full trade-off specifications:

- **Relational SQL**: Use **D1** for native serverless SQLite with read replication. Use **Hyperdrive** when connecting to existing external PostgreSQL/MySQL to pool connections and cache queries at the edge.
- **Key-Value Data**: Use **KV** for low-write, massive-read global caches (e.g. feature flags, auth config, redirect tables). Eventual consistency converges globally in ~60s.
- **Blob / File Storage**: Use **R2** for images, videos, backups, and user uploads. Zero egress fees and full S3 API compatibility.
- **Stateful Actors & WebSockets**: Use **Durable Objects (DO)** when you need strong serializable consistency, in-memory coordination, distributed mutex locks, or persistent WebSocket connections.
- **Asynchronous Decoupling**: Use **Queues** for fire-and-forget message processing with automatic batching, dead-letter queues, and retries.
- **Durable Step Pipelines**: Use **Workflows** for multi-step jobs that sleep for hours/days, require deterministic retries, or coordinate external human approval.
- **AI & Vector Embeddings**: Use **Workers AI** for on-demand GPU inference (Llama, DeepSeek, Whisper) and **Vectorize** for low-latency similarity search.

---

## 4. Modern Configuration Standard (`wrangler.jsonc`)

Always use `wrangler.jsonc` (JSON with comments) over legacy `wrangler.toml`:

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "enterprise-api",
  "main": "src/index.ts",
  "compatibility_date": "2026-11-01",
  "compatibility_flags": ["nodejs_compat"],

  // 1. Static Assets (SPA / Frontend)
  "assets": {
    "directory": "./dist",
    "binding": "ASSETS",
    "html_handling": "auto-trailing-slash",
    "not_found_handling": "single-page-application"
  },

  // 2. D1 Relational Database
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "production-db",
      "database_id": "xxxx-xxxx-xxxx-xxxx"
    }
  ],

  // 3. R2 Object Storage
  "r2_buckets": [
    {
      "binding": "STORAGE",
      "bucket_name": "user-media-production"
    }
  ],

  // 4. KV Namespace
  "kv_namespaces": [
    {
      "binding": "CONFIG_KV",
      "id": "yyyy-yyyy-yyyy-yyyy"
    }
  ],

  // 5. Workers AI
  "ai": {
    "binding": "AI"
  },

  // 6. Service Binding (RPC to microservice)
  "services": [
    {
      "binding": "AUTH_SERVICE",
      "service": "auth-microservice"
    }
  ]
}
```

---

## 5. Implementation Standard Patterns

### A. Core Worker ESM Entrypoint (`src/index.ts`)
```typescript
import { WorkerEntrypoint } from 'cloudflare:workers';

export interface Env {
  DB: D1Database;
  STORAGE: R2Bucket;
  CONFIG_KV: KVNamespace;
  AI: Ai;
  AUTH_SERVICE: Service<AuthService>;
  JWT_SECRET: string; // Secret set via `wrangler secret put`
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // 1. Query D1 with parameterized SQL
    if (url.pathname === '/api/users') {
      const { results } = await env.DB.prepare('SELECT id, name, email FROM users LIMIT ?').bind(20).all();
      return Response.json(results);
    }

    // 2. Serve / upload to R2
    if (url.pathname.startsWith('/api/files/')) {
      const key = url.pathname.replace('/api/files/', '');
      if (request.method === 'PUT') {
        await env.STORAGE.put(key, request.body);
        return new Response('Uploaded', { status: 201 });
      }
      const object = await env.STORAGE.get(key);
      if (!object) return new Response('Not Found', { status: 404 });
      return new Response(object.body);
    }

    // 3. Run AI Inference on Cloudflare GPUs
    if (url.pathname === '/api/chat') {
      const { prompt } = await request.json<{ prompt: string }>();
      const response = await env.AI.run('@cf/meta/llama-3.3-70b-instruct', {
        messages: [{ role: 'user', content: prompt }],
      });
      return Response.json(response);
    }

    // Fallback to static assets
    return env.ASSETS ? env.ASSETS.fetch(request) : new Response('Not Found', { status: 404 });
  },

  // Background Cron Trigger handler
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    ctx.waitUntil(cleanupStaleSessions(env.DB));
  },
};

async function cleanupStaleSessions(db: D1Database) {
  await db.prepare('DELETE FROM sessions WHERE expires_at < ?').bind(Date.now()).run();
}
```

---

## 6. HTTP Status & Error Troubleshooting Guide

When debugging proxied sites, identify whether the issue is at the Cloudflare Edge or Origin:

| Code / Status | Meaning | Source | Actionable Fix |
| :--- | :--- | :--- | :--- |
| **`520`** | Web Server Returned Unknown Error | Origin | Origin server returned an empty, malformed, or invalid response. Check origin web server logs (Nginx/Apache/Node). |
| **`521`** | Web Server Is Down | Origin | Origin server refused TCP connection on port 80/443. Check if server process crashed, or firewall dropped Cloudflare IPs. |
| **`522`** | Connection Timed Out | Network | Cloudflare could not complete TCP handshake with origin within 15 seconds. Check firewall, routing, or overload. |
| **`523`** | Origin Is Unreachable | DNS/Network | Cloudflare cannot resolve origin IP or route to it. Verify DNS A/AAAA records in Cloudflare dashboard. |
| **`524`** | A Timeout Occurred | Origin | TCP connected, but origin did not send HTTP response within 100 seconds (Enterprise configurable). Offload to Queues. |
| **`525`** | SSL Handshake Failed | TLS | SSL handshake failed between Cloudflare and origin. Verify origin certificate and check SSL/TLS encryption mode (Full Strict). |
| **`526`** | Invalid SSL Certificate | TLS | Cloudflare SSL mode is **Full (Strict)**, but origin certificate is self-signed or expired. Renew cert or install Cloudflare Origin CA. |
| **`1020`** / **WAF 403** | Access Denied | Cloudflare Edge | Blocked by WAF Custom Rule, Bot Management, or IP Access Rule. Check Security Events for the Ray ID. |

---

## 7. Production Checklist & Quality Standards

- [ ] **Lock Compatibility Date**: Pin `compatibility_date` (e.g. `"2026-11-01"`) and test upgrades in preview environments.
- [ ] **Strict Secrets Management**: Never commit API keys, database credentials, or tokens to git. Use `npx wrangler secret put <NAME>` or Cloudflare Secrets Store.
- [ ] **Zero-Trust Ingress**: Use Cloudflare Tunnel (`cloudflared`) to connect private origins without opening public ingress ports.
- [ ] **Parameterized SQL**: Always bind D1 queries using `.bind(...)`. Never concatenate raw strings into SQL.
- [ ] **Smart Placement**: Enable `"smart_placement": { "enabled": true }` when Workers make multiple roundtrips to an origin backend.
- [ ] **Observability**: Enable Workers Logs (`wrangler tail`) and configure Workers Analytics Engine for high-cardinality telemetry.
- [ ] **Fail-Safe Retries**: Wrap external fetches with timeout controllers (`AbortSignal.timeout(5000)`) to prevent 524 timeouts.

---

## 8. Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Correct Cloudflare Pattern |
| :--- | :--- | :--- |
| Using deprecated Cloudflare Pages for new projects | Missing modern Workers features & bindings | Use **Workers Static Assets** (`"assets": { "directory": "..." }`) |
| Hardcoding secrets in `wrangler.jsonc` | Exposes credentials in version control | Use `wrangler secret put` or Cloudflare Secrets Store |
| String concatenating SQL in D1 queries | SQL injection vulnerability | Always use `db.prepare('... WHERE id = ?').bind(id)` |
| Unbounded in-memory variables across requests | Isolate re-use is non-deterministic | Store persistent state in D1, KV, R2, or Durable Objects |
| Connecting directly to Postgres/MySQL from edge | Exhausts connection pool across 300+ edge nodes | Use **Hyperdrive** connection pooling |
| Long-running HTTP requests (> 100s) | Cloudflare proxy terminates with Error 524 | Decouple via **Queues** or **Workflows** |

---

## 9. Offline Documentation & References

- [Root Documentation Sitemap (`llms.txt`)](assets/llms.txt)
- [Wrangler CLI Reference](assets/cli/wrangler.md)
- [Workers Runtime API](assets/compute/workers.md)
- [Workers Static Assets](assets/compute/static-assets.md)
- [D1 SQL Database Reference](assets/database-storage/d1.md)
- [R2 Object Storage Reference](assets/database-storage/r2.md)
- [Durable Objects Reference](assets/database-storage/durable-objects.md)
- [Workers AI Reference](assets/ai/workers-ai.md)
- [Cloudflare Tunnel Reference](assets/networking-security/tunnels.md)
- [HTTP Status Codes Troubleshooting](assets/troubleshooting/http-status-codes.md)
- [Product Selection Matrix](references/productSelectionMatrix.md)
- [CLI Comparison & Migration Guide](references/cliComparison.md)
- [Framework Compatibility](references/frameworkCompatibility.md)
