# Database Security & Multi-Tenant Isolation Policies

Policies governing database authentication, authorization, encryption, and multi-tenant isolation.

---

## 1. Multi-Tenant Isolation

- **Tenant Scoping Requirement**:
  - In shared-database multi-tenant systems, every table holding tenant data MUST include a `tenant_id` column.
  - Multi-tenant tables must enforce database Row-Level Security (RLS) with `FORCE ROW LEVEL SECURITY` to prevent table owners and background connections from accidentally bypassing tenant filters.
  - Foreign keys between tenant-scoped entities must enforce composite foreign keys `(tenant_id, id)` to prevent cross-tenant referencing.
- **Connection Isolation**:
  - Web application database connections must run under an unprivileged application role (e.g. `app_user`), never `postgres`, `root`, or `db_owner`.
  - DDL schema modifications must run via dedicated migration runners with elevated privileges isolated from the web runtime.

---

## 2. Encryption & Data Protection

- **Encryption at Rest**: Tablespaces and storage volumes must enforce AES-256 encryption at rest.
- **Encryption in Transit**: Connections must enforce TLS 1.3 with valid certificate verification (`sslmode=verify-full`).
- **Cryptographic PII Protection (HMAC vs Raw Hashing)**:
  - Never store raw SHA-256 hashes of short or predictable PII (e.g. 9-digit SSNs, phone numbers). Raw hashes are vulnerable to GPU rainbow-table recovery in seconds.
  - Exact-match lookups must use an **HMAC with an isolated secret key** (e.g. `HMAC-SHA256(ssn, pepper_secret)`).
  - Reversible PII must use authenticated AES-GCM envelope encryption with KMS key rotation.
