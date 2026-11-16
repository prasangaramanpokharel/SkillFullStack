# Database Scalability, Partitioning & Sharding Reference

---

## 1. Partitioning vs. Sharding

```
PARTITIONING (Single Database Node / Engine Managed)
[ Logical Table: orders ]
   ├── Partition 2026-Q1 (Physical Table orders_2026_q1)
   ├── Partition 2026-Q2 (Physical Table orders_2026_q2)
   └── Partition 2026-Q3 (Physical Table orders_2026_q3)
   --> Queries with WHERE created_at = ... trigger Partition Pruning.

SHARDING (Multiple Independent Database Nodes / Distributed Cluster)
[ Cluster Coordinator / Router ]
   ├── Shard 01 (Database Server A) -> Tenants 001 - 250
   ├── Shard 02 (Database Server B) -> Tenants 251 - 500
   └── Shard 03 (Database Server C) -> Tenants 501 - 750
   --> Queries without Shard Key trigger expensive scatter-gather cross-node queries.
```

---

## 2. Partitioning Strategies

- **Range Partitioning**: Partition by continuous values (e.g. `created_at` by month/year). Ideal for time-series and log data where old partitions can be detached or archived.
- **List Partitioning**: Partition by explicit categorical values (e.g. `region IN ('EU', 'US', 'APAC')`).
- **Hash Partitioning**: Partition by modulus hash over a key. Guarantees uniform distribution across $N$ physical tables.

---

## 3. Sharding Architecture & Shard-Key Selection

- **High Cardinality**: The shard key must have millions of distinct values (e.g., `user_id` or `tenant_id`). Never shard on low-cardinality flags (e.g., `country` or `status`).
- **Even Distribution**: Avoid sequential timestamps or monotonically increasing counters as shard keys; otherwise, all writes hit a single node (Hot Partition).
- **Cross-Shard Query Penalty**: Avoid shard keys that require distributed joins across nodes. Design tables so that all related entity reads (`orders`, `order_items`, `invoices`) colocate on the same shard via a shared `tenant_id` or `account_id`.
