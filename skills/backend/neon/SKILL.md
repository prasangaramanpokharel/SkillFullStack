---
name: neon
description: Master Neon serverless Postgres engineering guide. Implements Lakebase Postgres, instant database branching, scale-to-zero, autoscaling, connection pooling via @neondatabase/serverless, Managed Better Auth, Neon Realtime reactive sync, neon.ts backend declaration, and framework integrations (Next.js, Astro, Node, Bun, Django).
version: 2026.x
last-verified: 2026-11-19
compatibility: Neon CLI (neonctl), @neondatabase/serverless 0.10+, Drizzle ORM, Prisma, Next.js 14-16, Astro 4-5
slash-commands:
  - command: /neon-branch
    description: Create, list, switch, or reset instantaneous copy-on-write database branches for PRs and testing.
    argument-hint: "[--name=<branch>] [--parent=main]"
  - command: /neon-connect
    description: Configure pooled vs direct connection strings for Serverless, Edge, and container environments.
    argument-hint: "[--driver=serverless|pg|drizzle]"
  - command: /neon-auth
    description: Scaffold Managed Better Auth with database-backed authentication that branches with your data.
    argument-hint: "[--framework=nextjs|astro]"
  - command: /neon-realtime
    description: Implement reactive Postgres live queries and real-time UI synchronization without Redis.
    argument-hint: "[--table=<name>]"
  - command: /neon-scale
    description: Configure compute autoscaling limits, scale-to-zero timeouts, and read replica topologies.
    argument-hint: "[--min-cu=<n>] [--max-cu=<n>]"
  - command: /neon-cli
    description: Automate project provisioning, branch management, and migrations using neonctl.
    argument-hint: "[--action=init|branch|migrate]"
---

# Neon Serverless Postgres Engineering Master Guide

This skill governs the architecture, development, connection pooling, branching workflows, and production deployment of serverless Postgres applications built on **Neon**.

---

## ⚡ Zero-Hallucination Offline Assets Notice
Before generating database connection code or configuring Neon branches, agents **MUST** consult bundled official specifications in [`assets/`](assets/README.md):
- Framework Integration Guides: [`assets/get-started/frameworks.md`](assets/get-started/frameworks.md)
- Full Backend Quickstart: [`assets/get-started/full-backend-quickstart.md`](assets/get-started/full-backend-quickstart.md)
- Branching Workflow Primer: [`assets/get-started/workflow-primer.md`](assets/get-started/workflow-primer.md)
- Production Checklist: [`assets/get-started/production-checklist.md`](assets/get-started/production-checklist.md)
- Lakebase Architecture: [`assets/introduction/architecture-overview.md`](assets/introduction/architecture-overview.md)
- Autoscaling Mechanics: [`assets/introduction/autoscaling.md`](assets/introduction/autoscaling.md)
- Scale to Zero: [`assets/introduction/scale-to-zero.md`](assets/introduction/scale-to-zero.md)
- Branching Concepts: [`assets/introduction/branching.md`](assets/introduction/branching.md)
- Read Replicas: [`assets/introduction/read-replicas.md`](assets/introduction/read-replicas.md)
- Choosing Connection Method: [`assets/connect/choose-connection.md`](assets/connect/choose-connection.md)
- Managed Better Auth: [`assets/auth/overview.md`](assets/auth/overview.md)
- Neon Realtime: [`assets/realtime/overview.md`](assets/realtime/overview.md)
- Next.js Guide: [`assets/guides/nextjs.md`](assets/guides/nextjs.md)
- Astro Guide: [`assets/guides/astro.md`](assets/guides/astro.md)
- Bun Guide: [`assets/guides/bun.md`](assets/guides/bun.md)
- Hono Guide: [`assets/guides/hono.md`](assets/guides/hono.md)
- neon.ts Specification: [`assets/reference/neon-ts.md`](assets/reference/neon-ts.md)
- Neon CLI Reference: [`assets/reference/cli.md`](assets/reference/cli.md)

---

## 1. Core Architecture: Decoupled Lakebase Postgres

Neon separates stateless compute instances from persistent multi-tenant storage (Page Servers):
- **Scale-to-Zero**: Inactive development endpoints suspend compute in 5 minutes, resuming in <500ms on incoming queries.
- **Autoscaling**: Scale dynamically between 0.25 Compute Units (CU) and 8+ CUs based on CPU/RAM load.
- **Copy-on-Write Branching**: Fork entire multi-gigabyte production databases in <1 second with zero initial storage duplication.

```
┌────────────────────────────────────────────────────────┐
│                   NEON LAKEBASE ARCHITECTURE           │
├────────────────────────────────────────────────────────┤
│  Compute Layer (Stateless, Autoscaling, Scale-to-Zero) │
│  ├── Main Production Endpoint (ep-main-123456)         │
│  ├── Read Replicas (ep-replica-123456)                 │
│  └── Ephemeral PR Branch Compute (ep-pr-789-pooler)    │
│                           │ WAL Stream                 │
│  Storage Layer (Durable, Decoupled Page Servers & S3)  │
│  ├── Copy-on-Write Page Servers                        │
│  └── Immutable History Log & LSN Point-in-Time Restore │
└────────────────────────────────────────────────────────┘
```

---

## 2. Choosing the Right Connection Method

Selecting the wrong connection string causes connection exhaustion or migration failures:

```typescript
// 1. Serverless Functions & Edge Runtime (One-shot HTTP query)
import { neon } from '@neondatabase/serverless';
const sql = neon(process.env.DATABASE_URL!); // Use pooled URL: ep-...-pooler.us-east-2.aws.neon.tech
const rows = await sql`SELECT id, name FROM teams WHERE active = true`;

// 2. Multi-Statement Transactions in Serverless (WebSocket Pool)
import { Pool } from '@neondatabase/serverless';
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const client = await pool.connect();
// Execute transaction...
client.release();

// 3. Schema Migrations (Prisma / Drizzle Kit / Flyway)
// MUST use Direct Connection (non-pooler): ep-main-123456.us-east-2.aws.neon.tech:5432
```

Reference guide: [`references/serverlessDriverPooling.md`](references/serverlessDriverPooling.md).

---

## 3. Database Branching for CI/CD & Preview Deployments

Every GitHub pull request should receive an ephemeral Neon database branch containing real schema and seed data:
- Create branch: `neon branches create --name pr-$PR_NUMBER`
- Apply migrations: `DATABASE_URL=$BRANCH_URL npx drizzle-kit migrate`
- Delete on close: `neon branches delete pr-$PR_NUMBER`

Reference guide: [`references/branchingWorkflows.md`](references/branchingWorkflows.md).

---

## 4. Managed Better Auth & Realtime

- **Managed Better Auth**: Authentication schema lives directly in your Postgres database and branches automatically with every PR. Reference: [`references/managedBetterAuth.md`](references/managedBetterAuth.md).
- **Neon Realtime**: Stream reactive query results directly to React or Next.js components via Postgres logical replication without Redis. Reference: [`references/neonRealtimeSync.md`](references/neonRealtimeSync.md).

---

## 5. Anti-Patterns to Avoid

| Anti-Pattern | Why It Breaks Production | Correct Modern Standard |
| :--- | :--- | :--- |
| **Running Migrations Against Pooled Connection** | PgBouncer in transaction mode does not support session-level DDL locks or prepared statement schemas. | Use the **Direct Connection URL** (`ep-...`) without `-pooler` for migrations. |
| **Opening Raw TCP `pg.Client` in Serverless Functions** | Exhausts Postgres max connections (100-500) under concurrent lambda scale. | Use `@neondatabase/serverless` over HTTP or connect to the managed `-pooler` endpoint. |
| **Keeping Dev Compute Active 24/7** | Burns compute hours unnecessarily on inactive development environments. | Enable **Scale to Zero** (e.g. 5-minute timeout) on all non-production branches. |
| **Manually Dumping & Restoring Staging DBs** | Slow, expensive, and risks exposing production PII or credentials. | Use instant **Copy-on-Write Branching** (`/neon-branch`) to spin up isolated test branches in 1 second. |
| **Building Custom Realtime Sync with Redis** | Adds operational complexity, costs, and eventual consistency sync lag. | Use native **Neon Realtime** (`useRealtimeQuery`) backed by Postgres logical replication. |
| **Running Heavy Analytics on Primary OLTP Compute** | Starves transaction throughput and spikes query latency for end users. | Provision an auto-scaled **Read Replica** for analytics and background reporting. |

---

## 6. Verification & Automated Diagnostics

Run the bundled Neon integration auditor to verify connection strings, pooling configuration, and driver setups:
```bash
python3 skills/backend/neon/scripts/auditNeonConfig.py --path ./src
```
