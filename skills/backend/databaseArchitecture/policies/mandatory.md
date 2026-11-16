# Mandatory Database Architecture Policies

These 18 non-negotiable policies govern all database architectures and data models.

---

## The 18 Mandatory Directives

1. **Workload Analysis Before Engine Selection**: Never choose a database engine based on popularity. Engine selection must be justified against access patterns, read/write ratios, and consistency needs in an ADR.
2. **Methodology Separation**: Never apply relational normal forms to document or distributed database designs, and never model relational databases like MongoDB document stores.
3. **Justified Denormalization**: Controlled data duplication is permitted only when backed by measured query bottlenecks or architectural read models (e.g. CQRS projections).
4. **Primary Key Requirement**: Every table or collection must possess an immutable, unique primary identifier. Evaluate index locality (UUIDv7 vs BIGINT).
5. **Database-Enforced Invariants**: Critical business constraints (`NOT NULL`, `CHECK`, `UNIQUE`, `FOREIGN KEY`) must exist in the database engine, never outsourced solely to application code.
6. **No Speculative Indexing**: Every index must be justified by specific query patterns; redundant indexes waste disk I/O and degrade write throughput.
7. **Exhaust Simpler Scaling**: Do not shard a database before optimizing indexes, partitioning large tables, introducing read replicas, and caching read paths.
8. **Replication $\ne$ Backup**: Replication guards against node hardware failure, NOT logical data corruption, DROP TABLE errors, or ransomware.
9. **Mandatory Disaster Recovery**: No database may deploy to production without tested point-in-time recovery (PITR) procedures and documented RPO/RTO targets.
10. **Zero Secrets in Code**: Connection credentials, SSL client certificates, and encryption keys must be managed exclusively via environment secrets or key vaults.
11. **Expand-and-Contract Migrations**: Breaking schema changes must be broken into backward-compatible phases (Expand $\rightarrow$ Dual-Write $\rightarrow$ Backfill $\rightarrow$ Contract).
12. **Transaction Scoping**: Transactions must remain microsecond-fast. External HTTP calls, mail dispatch, or complex background tasks inside an open transaction are forbidden.
13. **Measure Before Optimizing**: Every query optimization must be supported by execution plan outputs (`EXPLAIN (ANALYZE, BUFFERS)`).
14. **Portability Awareness**: Proprietary database features must be isolated so the core domain schema remains understandable and maintainable.
15. **Polyglot Justification**: Polyglot persistence architectures must explicitly document cross-database consistency mechanisms and operational overhead.
16. **Data Retention & Lifecycle**: Tables with continuous ingestion must specify retention, partitioning, downsampling, and archival strategies.
17. **No Unmeasured Capacity Claims**: Capacity plans must distinguish between empirical benchmarks and theoretical estimates.
18. **Pre-Flight Certification**: No schema may be deployed to production without passing the automated schema audit checklist.
19. **Entity Naming Standards**: Table names must use lowercase `snake_case` plural nouns (e.g. `order_items`, `customers`). Generic names (`data`, `info`, `items`, `temp`) and Hungarian notation prefixes (`tbl_`) are strictly forbidden.
20. **Lean Schema Law (YAGNI)**: Never add a column until proven necessary by an active business requirement or query pattern. Speculative "just in case" columns and unstructured catch-all columns (`misc`, `extra_data`) are prohibited.
21. **Pre-Creation Security Gate**: No table may be created without completing the pre-creation security checklist (PII classification, tenant isolation `tenant_id`, credential hashing, and RLS review).
22. **Tenant-Aware Composite Foreign Keys**: In multi-tenant databases, foreign keys between tenant-owned entities must enforce composite foreign keys `FOREIGN KEY (tenant_id, target_id) REFERENCES target_table(tenant_id, id)` to prevent cross-tenant record linking.
23. **Temporal Concurrency Protection**: Booking, scheduling, and occupancy tables must enforce PostgreSQL Exclusion Constraints (`EXCLUDE USING gist ... WITH &&`) to prevent overlapping resource allocations.
24. **Complete RLS & Policy Symmetry**: Every table with Row-Level Security enabled must define explicit policies for `SELECT`, `INSERT`, `UPDATE`, and `DELETE` with `WITH CHECK` constraints and `FORCE ROW LEVEL SECURITY`.
