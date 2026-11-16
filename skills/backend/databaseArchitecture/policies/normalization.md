# Relational Normalization & Denormalization Policies

Policies governing normal forms, dependency preservation, and controlled denormalization.

---

## 1. Normalization by Default (OLTP)

- **3NF / BCNF Target**:
  - All transactional relational models must achieve **Third Normal Form (3NF)** by default, and **Boyce-Codd Normal Form (BCNF)** wherever functional dependencies dictate.
- **Verification Criteria**:
  - **1NF**: Atomic attributes, no repeating columns (`phone1`, `phone2`), and a defined primary key.
  - **2NF**: No partial dependencies of non-key attributes on part of a composite primary key.
  - **3NF**: No transitive dependencies (non-key attribute depending on another non-key attribute).
  - **BCNF**: Every determinant must be a candidate key.

---

## 2. Controlled Denormalization Discipline

Denormalization is strictly prohibited as a shortcut for lazy modeling. It is allowed ONLY under these conditions:
1. **Measured Read Latency**: A specific high-frequency query exceeds the latency SLO due to expensive joins.
2. **Immutable Historical Snapshots**: Preserving facts at a specific point in time (e.g. `order_items.unit_price`, `shipping_address_snapshot`).
3. **CQRS Read Projections**: Dedicated read-model tables or materialized views updated asynchronously via CDC or domain events.
4. **Authoritative Master Copy**: The system must explicitly document which table holds the authoritative single source of truth.
