# Database Taxonomy & Workload-Driven Selection Reference

Comparative analysis across all primary database paradigms.

---

## 1. The 13 Database Families

| Family | Representative Engines | Best-Fit Workload | Trade-offs & Limitations |
| :--- | :--- | :--- | :--- |
| **Relational (RDBMS)** | PostgreSQL, MySQL, SQLite | Structured data, complex multi-entity transactions, strict ACID. | Horizontal write scaling requires manual sharding or Vitess/Citus. |
| **Document** | MongoDB, Firestore, Couchbase | Hierarchical polymorphic entities, rapid schema evolution. | Multi-document transactions carry higher latency; risk of unbounded nested documents. |
| **Key-Value** | Redis, Valkey, DynamoDB | Session storage, caching, token management, $< 5$ms lookups. | Limited query flexibility; secondary indexing is costly or unsupported. |
| **Wide-Column** | Apache Cassandra, ScyllaDB | High-volume write ingestion (IoT, telemetry, messaging), multi-datacenter. | Query-driven tables; no ad-hoc joins; eventual consistency model. |
| **Columnar (OLAP)** | ClickHouse, DuckDB, Snowflake | Analytical aggregations over billions of rows (`SUM`, `AVG`, `GROUP BY`). | Inefficient for point lookups or frequent single-row updates. |
| **Graph** | Neo4j, Amazon Neptune | Deep relationship traversals, fraud detection, social networks, ACLs. | Difficult to scale horizontally; higher memory overhead per edge. |
| **Time-Series** | TimescaleDB, InfluxDB | Metrics, sensor readings, financial tick data with automatic downsampling. | Specialized for sequential time-stamped inserts; updates are discouraged. |
| **Search** | Elasticsearch, OpenSearch | Inverted full-text search, fuzzy matching, faceted filtering. | Higher write amplification; eventual consistency; heavy memory consumption. |
| **Vector** | Qdrant, Milvus, pgvector | High-dimensional embedding similarity search (HNSW, IVFFlat), RAG. | Compute-intensive cosine/L2 distance calculations; memory-heavy indexes. |
| **Object Storage** | S3, GCS, MinIO | Unstructured files, images, videos, large analytical Parquet dumps. | High latency per request (50-100ms); immutable object semantics. |
| **Embedded** | SQLite, DuckDB, RocksDB | Local desktop apps, mobile devices, edge devices, zero-network daemon cache. | Single-writer limitations (concurrency bottleneck under heavy concurrent web writes). |
| **In-Memory** | Redis, Dragonfly, SAP HANA | Ultra-low latency $(< 1$ms) real-time leaderboards, rate limit counters. | RAM cost is higher than SSDs; persistence depends on periodic snapshots/AOF. |
| **Ledger** | ImmuDB, Amazon QLDB alternatives | Cryptographically verifiable immutable audit logs and legal transaction history. | Append-only; higher storage growth; specialized query interfaces. |

---

## 2. Polyglot Persistence Architecture Rules

Polyglot persistence combines specialized databases (e.g. PostgreSQL + Redis + ClickHouse).
- **Law 1**: Explicitly designate the single **System of Record (SoR)** (usually PostgreSQL).
- **Law 2**: Secondary read stores (Redis cache, Elastic search index, ClickHouse analytics) must be populated asynchronously via **Change Data Capture (CDC)** (Debezium, Kafka) or outbox domain events.
- **Law 3**: Never perform dual-writes synchronously from application code without two-phase commit or transactional outbox patterns.
