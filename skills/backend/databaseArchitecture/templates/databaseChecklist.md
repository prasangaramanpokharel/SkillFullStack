# Pre-Flight Production Database Readiness Checklist

Verify all items prior to launching any database service into staging or production:

## 1. Schema & Data Integrity
- [ ] Every table has a designated, immutable primary key.
- [ ] Multi-tenant tables include `tenant_id` and enforce database RLS.
- [ ] Foreign keys define explicit referential actions (`ON DELETE RESTRICT/CASCADE`).
- [ ] Essential numeric boundaries and state machines are enforced via `CHECK` constraints.
- [ ] Columns default to `NOT NULL` unless nullability is explicitly justified.

## 2. Performance & Indexing
- [ ] All foreign key columns have supporting secondary indexes.
- [ ] Composite indexes order equality columns first, followed by range columns.
- [ ] No redundant or duplicate indexes exist.
- [ ] Query plans for high-frequency queries confirm Index Scans, avoiding full table scans.
- [ ] Connection pool limits are sized to CPU cores with max acquisition timeout $\le 3$s.

## 3. Scalability & Maintenance
- [ ] High-volume historical tables have an explicit partitioning or archival strategy.
- [ ] Sharding is only used if vertical scaling and read replicas have been empirically exhausted.
- [ ] All production indexes are created with `CREATE INDEX CONCURRENTLY`.

## 4. Disaster Recovery & Security
- [ ] Automated daily physical snapshots configured with retention policy.
- [ ] Continuous Write-Ahead Log (WAL) archiving active to off-region object storage.
- [ ] Scheduled restore drill tested and validated against RTO and RPO targets.
- [ ] Database credentials isolated in secure vault; application connects as unprivileged user.
- [ ] TLS 1.3 enforced on all client connections.
