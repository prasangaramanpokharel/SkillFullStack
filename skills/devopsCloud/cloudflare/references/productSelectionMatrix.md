# Cloudflare Product Selection Matrix (2026)

When designing systems on the Cloudflare Developer Platform, choose the right product based on data shape, consistency requirements, access patterns, and latency boundaries.

---

## 1. Databases & Storage Selection

| Requirement / Workload | Recommended Product | Alternative | Key Deciding Factor |
| :--- | :--- | :--- | :--- |
| **Relational Data / SQL Queries** | **D1** | Hyperdrive (External Postgres/MySQL) | Serverless SQLite with automatic read replication. Best for SaaS relational state. |
| **Existing External Postgres/MySQL** | **Hyperdrive** | Direct TCP connection | Connection pooling and query caching at 300+ edge locations without origin connection exhaustion. |
| **Blob / File / Object Storage** | **R2** | KV (for < 25 MB items) | Zero egress fees, S3 API compatibility, direct streaming with presigned URLs. |
| **Global Read-Heavy Key-Value** | **KV** | D1 / Workers Cache | Low latency reads at edge, eventual consistency (60s global convergence), 25 MB value limit. |
| **Strongly Consistent State / Realtime Actor** | **Durable Objects (DO)** | D1 | Single-point-of-coordination, WebSockets, in-memory transactional state, distributed locks. |
| **Asynchronous Decoupling / Buffering** | **Queues** | Workflows | High-throughput at-least-once message delivery, automatic batching and retry backoff. |
| **Multi-Step Stateful Durable Pipelines** | **Workflows** | Queues + Durable Objects | Human-in-the-loop, sleeping for days/weeks, deterministic step retries, zero timeout limit. |
| **Semantic / Vector Search** | **Vectorize** | External Pinecone/Qdrant | Native serverless vector database integrated with Workers AI embeddings. |

---

## 2. Compute Selection

| Application Type | Primary Architecture | Configuration / Tool |
| :--- | :--- | :--- |
| **Full-Stack Web App / SPA** | **Workers + Static Assets** | `wrangler.jsonc` with `"assets": { "directory": "./dist" }` |
| **Microservices / REST API** | **Workers (ESM)** | `export default { fetch(req, env, ctx) }` |
| **Zero-Latency Microservice Mesh** | **Service Bindings** | Direct memory RPC between Workers without HTTP serialization overhead |
| **Long-Running WebSockets / Chat Rooms** | **Durable Objects** | WebSockets hibernated when idle, pay only for active compute |
| **Periodic Background Jobs** | **Cron Triggers** | `scheduled(event, env, ctx)` handler in Workers |
| **Heavy Containerized Workloads** | **Cloudflare Containers** | OCI containers running alongside Workers |

---

## 3. AI & Agent Infrastructure Selection

| AI Task | Primary Product | Features |
| :--- | :--- | :--- |
| **Serverless LLM / Embedding Inference** | **Workers AI** | Llama 3.3, DeepSeek, Mistral, BGE embeddings running on global GPUs |
| **Gateway / Observability / Caching** | **AI Gateway** | Universal proxy for OpenAI, Anthropic, Google with edge caching and rate limiting |
| **Managed Hybrid RAG** | **AI Search** | Turnkey document ingestion, chunking, embedding, BM25 + dense search |
| **Autonomous Stateful Agents** | **Agents SDK** | Durable state, WebSockets, scheduled wakeups, MCP server/client integration |
| **Headless Browser Automation** | **Browser Rendering** | Puppeteer-compatible cloud Chromium for scraping, PDF generation, UI testing |

---

## 4. Networking & Edge Security

| Security Layer | Product | Function |
| :--- | :--- | :--- |
| **Zero-Trust Origin Ingress** | **Cloudflare Tunnel (`cloudflared`)** | Secure outbound-only tunnel connecting private servers/Docker without opening public ports |
| **Edge Web Application Firewall** | **Cloudflare WAF** | Managed OWASP Core Ruleset, custom expression rules, credential stuffing protection |
| **Abuse & Scraping Mitigation** | **Rate Limiting & Bot Management** | Dynamic IP/cookie rate counters, Turnstile non-intrusive CAPTCHA alternative |
| **Authoritative DNS** | **Cloudflare DNS** | Anycast DNS with sub-second propagation, DNSSEC, CNAME flattening |
