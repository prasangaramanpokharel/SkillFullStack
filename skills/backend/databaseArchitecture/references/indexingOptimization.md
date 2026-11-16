# Indexing Fundamentals & Query Optimization Reference

---

## 1. Physical Index Types

| Index Architecture | Engine Examples | Ideal Query Pattern | Limitations |
| :--- | :--- | :--- | :--- |
| **B-Tree** | PostgreSQL, MySQL, SQLite | Equality (`=`), Range (`<`, `>`, `BETWEEN`), Sorting (`ORDER BY`). | Inefficient for high-dimensional vectors or full text. |
| **Hash** | PostgreSQL, MySQL (Memory) | Exact equality (`=`) lookups only. | Does not support range scans or sorting. |
| **GIN (Generalized Inverted)** | PostgreSQL | JSONB containment (`@>`), full-text search, arrays (`&&`). | Higher write amplification during inserts/updates. |
| **GiST** | PostgreSQL | Geometric data, spatial coordinates, full-text search. | Slower build times and larger size than B-tree. |
| **BRIN (Block Range Index)** | PostgreSQL | Huge tables naturally ordered by insertion (`created_at`). | Tiny footprint ($< 1\%$ size of B-tree), but requires physical sorting. |
| **HNSW / IVFFlat** | pgvector, Qdrant, Milvus | Approximate nearest neighbor vector similarity search. | Memory intensive; trade-off between recall and search latency. |

---

## 2. Composite Index Column Ordering Heuristic

When creating composite index `CREATE INDEX idx_orders ON orders (tenant_id, status, created_at)`:
1. **Rule 1 (Equality Columns First)**: Place columns tested with strict equality (`WHERE tenant_id = ? AND status = ?`) at the leading edge.
2. **Rule 2 (Range Columns Second)**: Place columns tested with range operators (`WHERE created_at >= ?`) after the equality columns.
3. **Rule 3 (Covering Columns via INCLUDE)**: Add non-filter payload columns to `INCLUDE (amount, currency)` to enable **Index-Only Scans** without bloating the B-tree navigation key.

---

## 3. Query Plan Diagnostics (`EXPLAIN ANALYZE`)

Key indicators to inspect in execution plans:
- **Index Scan vs Index Only Scan vs Sequential Scan**: Verify that large tables avoid full sequential scans (`Seq Scan`).
- **Buffers (`BUFFERS` flag)**: Check `shared hit` vs `shared read`. High `read` indicates disk I/O bottlenecks.
- **Rows Estimation Divergence**: If estimated rows differ from actual rows by orders of magnitude, update database statistics via `ANALYZE <table>`.
