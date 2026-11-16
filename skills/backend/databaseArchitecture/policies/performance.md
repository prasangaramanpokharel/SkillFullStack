# Database Performance & Scalability Policies

Policies governing indexing, query optimization, connection pooling, and resource boundaries.

---

## 1. Indexing Policies

- **Foreign Key Indexing**:
  - Every foreign key column must have a supporting index to avoid full table scans during child lookups and cascade operations.
- **Selectivity & Index Pruning**:
  - Do not create indexes on columns with low cardinality (e.g. boolean flags) unless using partial/filtered indexes (e.g. `WHERE is_processed = false`).
  - Regularly audit and drop unused indexes (`pg_stat_user_indexes` where `idx_scan = 0`).

---

## 2. Concurrency & Connection Governance

- **Connection Pool Bounds**:
  - Applications must use external or internal connection pooling (e.g. PgBouncer, HikariCP).
  - Explicit limits: `max_connections` sized according to CPU cores:
    $$\text{pool\_size} = 2 \times \text{CPU\_cores} + \text{effective\_spindle\_count}$$
  - Connection acquisition timeout must not exceed 3 seconds.
- **Lock Contention**:
  - Avoid long-running exclusive locks (`ALTER TABLE ...`, `LOCK TABLE ...`).
  - Create indexes concurrently in production (`CREATE INDEX CONCURRENTLY` in PostgreSQL).
