# Neon Realtime Reactive Sync

Neon Realtime turns ordinary Postgres tables into reactive live streams directly to clients, eliminating the need for Redis, Kafka, or third-party sync engines.

---

## 1. Architecture

Neon Realtime tails Postgres Logical Replication slots directly in the storage engine:
1. When an `INSERT`, `UPDATE`, or `DELETE` executes on Postgres, Neon streams the change events to connected subscribers.
2. Clients subscribe to parameterized queries or table channels over WebSockets.
3. Latency is sub-50ms from database write to frontend UI re-render.

---

## 2. React / Next.js Implementation

```tsx
'use client';
import { useRealtimeQuery } from '@neondatabase/react';

export function ActiveOrdersList() {
  const { data: orders, loading } = useRealtimeQuery(
    `SELECT id, customer, status, total FROM orders WHERE status = 'pending' ORDER BY created_at DESC LIMIT 20`
  );

  if (loading) return <div>Connecting to live stream...</div>;

  return (
    <ul>
      {orders.map((o) => (
        <li key={o.id}>{o.customer}: ${o.total} - {o.status}</li>
      ))}
    </ul>
  );
}
```
