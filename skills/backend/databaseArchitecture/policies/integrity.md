# Data Integrity & Constraint Policies

Policies governing data validity, invariants, and referential integrity.

---

## 1. Engine-Level Constraints

- **Mandatory Non-Nullability**:
  - Columns must be defined `NOT NULL` by default. Nullable columns must be explicitly justified.
- **CHECK Constraints**:
  - Valid numeric ranges (e.g. `CHECK (amount >= 0)`, `CHECK (quantity > 0)`) and status state machines (e.g. `CHECK (status IN ('pending', 'active', 'canceled'))`) must be enforced at the schema level.
- **Referential Integrity**:
  - Foreign keys must define explicit referential actions:
    - `ON DELETE RESTRICT` (Default): Prevent deletion of referenced parent rows.
    - `ON DELETE CASCADE`: Permitted ONLY for strict child ownership (e.g. `order_items` owned by `orders`).
    - `ON DELETE SET NULL`: Permitted only for optional associations.
  - Cascading deletes on core master data entities are strictly forbidden.

---

## 2. Uniqueness & Primary Identity

- Natural business attributes (e.g., `email`, `slug`) must be guarded by `UNIQUE` constraints with unique indexes.
- Primary keys must never change over the lifetime of a record. Surrogate keys (UUIDv7 or BIGINT) are strongly preferred over mutable natural strings.
