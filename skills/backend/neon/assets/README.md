# Neon Serverless Postgres Official Documentation Catalog

This directory contains offline, un-truncated official documentation mirrored from Neon's official markdown endpoints (`neon.com/docs/...md`) for zero-hallucination agent execution.

## Catalog Sitemap

### Getting Started & Frameworks
- [Framework Integration Guides](get-started/frameworks.md): Connect from Next.js, Node.js, Astro, Bun, Hono, Django, and more.
- [Full Backend Quickstart](get-started/full-backend-quickstart.md): Build a complete backend with Postgres, Object Storage, and AI Functions.
- [Database Branching Workflow Primer](get-started/workflow-primer.md): Integrating Postgres branching into development and CI/CD.
- [Production Readiness Checklist](get-started/production-checklist.md): Optimize price, performance, and connection limits for production.

### Lakebase Architecture & Concepts
- [Architecture Overview](introduction/architecture-overview.md): Decoupled compute and durable storage layers.
- [Autoscaling](introduction/autoscaling.md): Dynamic compute scaling based on workload demand.
- [Scale to Zero](introduction/scale-to-zero.md): Suspend inactive compute endpoints to minimize costs.
- [Branching](introduction/branching.md): Instant copy-on-write database branches with data and schema.
- [Read Replicas](introduction/read-replicas.md): Horizontal read scaling and analytical query isolation.

### Connection & Drivers
- [Choose Your Connection Method](connect/choose-connection.md): Direct connections, connection pooling (PgBouncer), and serverless WebSocket/HTTP driver (`@neondatabase/serverless`).

### Auth & Realtime
- [Managed Better Auth](auth/overview.md): Managed authentication stored in your database that branches with your data.
- [Neon Realtime](realtime/overview.md): Reactive live Postgres queries and UI synchronization without Redis.

### Framework-Specific Guides
- [Next.js Connection Guide](guides/nextjs.md): App Router, Server Components, Server Actions, and Cache Components with Neon.
- [Astro Connection Guide](guides/astro.md): Connecting Astro Server Endpoints and Actions.
- [Node.js Connection Guide](guides/node.md): Native Node.js pg and pooling.
- [Bun Connection Guide](guides/bun.md): High-performance Bun native SQL client with Neon.
- [Hono Connection Guide](guides/hono.md): Lightweight Edge APIs with Hono and `@neondatabase/serverless`.
- [Django Connection Guide](guides/django.md): Connecting Python Django ORM to Neon.

### Platform References
- [neon.ts Reference](reference/neon-ts.md): Declare your entire backend (Postgres, Functions, Storage, AI) in one file.
- [Neon CLI Reference](reference/cli.md): CLI commands, automation, and branch provisioning (`neonctl`).
