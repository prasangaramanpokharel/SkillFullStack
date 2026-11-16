# Data Modeling Lifecycle & Identifier Engineering Reference

---

## 1. The Three Levels of Data Modeling

1. **Conceptual Data Model (CDM)**:
   - Identifies business entities, domains, and overarching relationships.
   - Independent of any database software or technical storage format.
   - Artifact: High-level Domain ERD.
2. **Logical Data Model (LDM)**:
   - Specifies entities, attributes, primary/foreign keys, cardinality ($1:1, 1:N, N:M$), and normalization rules.
   - Abstracted from engine-specific physical storage parameters.
3. **Physical Data Model (PDM)**:
   - Defines concrete database implementation: exact data types (`BIGINT`, `TIMESTAMPTZ`, `VARCHAR(255)`), table spaces, indexes, partitions, and engine-specific constraints.

---

## 2. Identifier Engineering Decision Matrix

| Identifier Type | Size | Monotonic Ordering | Distributed Generation | Information Leakage | B-Tree Locality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BIGINT (`IDENTITY` / `AUTO_INCREMENT`)** | 8 bytes | Yes | Requires DB Coordinator | High (sequential IDs reveal volume) | Excellent ($O(1)$ append) |
| **UUIDv4** | 16 bytes | No (Random) | Yes (Local client) | None | Terrible (Page thrashing on large tables) |
| **UUIDv7 (RFC 9562)** | 16 bytes | Yes (Time-ordered ms) | Yes (Local client) | None (Timestamp encoded) | Excellent (Preserves B-tree append locality) |
| **ULID** | 16 bytes | Yes (Time-ordered ms) | Yes (Crockford base32) | None | Excellent |
| **Snowflake ID** | 8 bytes | Yes (64-bit integer) | Yes (Machine node ID) | Low | Excellent |

### Recommended Standard
For distributed, secure, and performant modern architectures, **UUIDv7** is the primary recommended identifier. It eliminates database-roundtrip ID generation, hides commercial transaction volume, and maintains near-zero B-tree index fragmentation.
