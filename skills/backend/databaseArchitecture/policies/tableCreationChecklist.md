# Table Pre-Creation & Pre-Flight Security Gate Policy

No database table may be created in any schema until it has successfully passed this mandatory pre-creation gate and security audit.

---

## Stage 1: Entity Justification Gate (Is this table truly necessary?)

Before writing `CREATE TABLE`, answer these 4 questions:
1. **Lifecycle Independence**: Does this entity have an independent lifecycle separate from existing entities?
   - If it only exists as an attribute of an existing entity (e.g. `user_preferences`), can it be modeled in the parent table?
2. **Cardinality Proof**: Is the relationship genuinely $1:N$ or $N:M$?
   - If $1:1$, justify why it is not stored in the parent table (acceptable reasons: extreme column width, separate security clearance, or sparse optional data).
3. **Duplication Audit**: Does an existing table already capture these facts?
   - Prevent fragmentation where similar entities (e.g. `admins`, `customers`, `vendors`) are split across separate tables instead of a unified `users` table with a discriminator/role.
4. **Volume & Retention Profile**: What is the expected row count at 1 year and what is its archival/deletion policy?

---

## Stage 2: Entity Naming Conventions & Taxonomy

- **Plural, Lowercase `snake_case`**:
  - Compliant: `orders`, `order_items`, `user_sessions`, `payment_methods`.
  - Non-Compliant: `Order` (singular), `tbl_orders` (Hungarian notation prefix), `OrderItems` (PascalCase), `tblData` (generic).
- **Prohibited Generic Table Names**:
  - Never name a table `data`, `info`, `items`, `records`, `logs`, or `temp`.
  - Names must specify the business domain (e.g. `audit_logs`, `billing_invoices`, `cart_items`).
- **Junction Table Naming**:
  - Name $N:M$ junction tables after both participating entities in alphabetical or hierarchy order: `students_courses`, `roles_permissions`.

---

## Stage 3: Lean Column Law (The YAGNI Policy)

**"Never add a column until an active business requirement or query pattern demands it."**

- **No Speculative Columns**:
  - Prohibited: Adding `fax_number`, `middle_initial`, `internal_notes`, or `future_field_1` "just in case we need it later".
  - Prohibited: Adding generic unstructured catch-all columns (`extra_json`, `metadata`, `misc_data`) without an explicit schema and indexing justification.
- **Column Justification Gate**:
  Every column in the proposed DDL must state:
  1. Business purpose.
  2. The code path or query that will read it.
  3. The code path that will write it.
  4. Nullability rationale (default is `NOT NULL`).

---

## Stage 4: Pre-Creation Security Checklist (Mandatory Security Gate)

Before the table DDL is approved, complete this security checklist:

| Security Vector | Verification Requirement |
| :--- | :--- |
| **Tenant Isolation** | If multi-tenant, does the table include `tenant_id`? Is Row-Level Security (RLS) configured? |
| **PII & Sensitivity** | Are sensitive personal fields (SSN, national ID, phone, home address) classified? |
| **Credential Storage** | Are passwords, tokens, or API keys properly hashed (Argon2id/bcrypt) or encrypted before storage? Plaintext credentials are strictly forbidden. |
| **Financial / Audit Records** | Are monetary amounts modeled with exact precision (`NUMERIC(12, 2)` or integer cents), never floating-point `FLOAT`/`REAL`? |
| **Access Permissions** | Does the application role have only `SELECT, INSERT, UPDATE, DELETE` permissions? (Application role must never possess `DROP`, `TRUNCATE`, or `ALTER`). |
| **Soft Delete vs Purge** | If compliance mandates GDPR/CCPA "Right to be Forgotten", is there a mechanism to hard-purge or pseudonymize records? |

---

## Stage 5: Schema Integrity & Index Gate

- [ ] Immutable Primary Key defined (`id BIGINT` or `id UUID` using UUIDv7).
- [ ] Foreign keys define explicit `ON DELETE` actions (`RESTRICT` or `CASCADE`).
- [ ] Every foreign key column has a supporting secondary index.
- [ ] Mandatory audit timestamps present (`created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`, `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`).
- [ ] CHECK constraints enforce domain ranges and state machines.
