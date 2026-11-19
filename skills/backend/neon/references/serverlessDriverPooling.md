# Serverless Driver & Connection Pooling

Serverless and Edge environments (Vercel, Cloudflare Workers, AWS Lambda) create ephemeral compute instances that can overwhelm Postgres with thousands of concurrent connections.

---

## 1. Connection String Types

Neon provides two distinct connection endpoints:
1. **Direct Connection (`ep-cool-flower-123456.us-east-2.aws.neon.tech`)**:
   - Direct connection to Postgres on port `5432`.
   - Used for: Migrations, schema DDL, Long-running stateful containers, and tools using session-level features (e.g. prepared statements, advisory locks).
2. **Pooled Connection (`ep-cool-flower-123456-pooler.us-east-2.aws.neon.tech`)**:
   - Routes through Neon's managed PgBouncer pooler on port `5432` or port `6543`.
   - Used for: Serverless functions, microservices, and auto-scaling app backends. Supports up to 10,000 concurrent client connections.

---

## 2. Using `@neondatabase/serverless`

For environments without TCP sockets (such as Cloudflare Workers, Vercel Edge Runtime, or browsers):

```typescript
import { neon, Pool } from '@neondatabase/serverless';

// 1. One-shot HTTP Query (Fastest TTFB, zero connection handshake overhead)
const sql = neon(process.env.DATABASE_URL!);
const users = await sql`SELECT id, email, created_at FROM users WHERE status = ${'active'} LIMIT 10`;

// 2. WebSocket Pool (For multi-statement transactions in serverless)
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('UPDATE accounts SET balance = balance - 50 WHERE id = $1', [fromId]);
  await client.query('UPDATE accounts SET balance = balance + 50 WHERE id = $1', [toId]);
  await client.query('COMMIT');
} catch (e) {
  await client.query('ROLLBACK');
  throw e;
} finally {
  client.release();
}
```
