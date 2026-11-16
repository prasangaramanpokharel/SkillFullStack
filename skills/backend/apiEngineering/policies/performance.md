# API Performance & Scalability Policies

All API implementations must enforce resource boundaries and operational scalability policies.

---

## 1. Resource Boundaries & Query Safeguards

- **Mandatory Collection Pagination**:
  - Every collection endpoint must enforce pagination.
  - Default page size: `20` items.
  - Absolute maximum ceiling: `100` items (`limit <= 100`). Requests exceeding the maximum must be clamped or rejected with `422`.
- **Database Index Alignment**:
  - Every filtered or sorted query parameter must map to a database index.
  - Sorting must be deterministic: always tie-break with a unique indexed column (e.g., `ORDER BY created_at DESC, id DESC`).
- **Connection Pool Sizing**:
  - Set explicit pool boundaries (`min_connections`, `max_connections`) and connection acquisition timeouts ($\le 3$ seconds) to prevent cascading thread starvation.

---

## 2. Caching & HTTP Conditional Requests

- **ETags & Validation**:
  - Read-heavy resources should return strong ETags (`ETag: "hash"`) and support conditional requests (`If-None-Match`).
  - Cacheable GET responses must return `Cache-Control: private, max-age=...` or `no-cache, must-revalidate`.
- **Rate Limiting**:
  - Standard rate limit headers must accompany responses:
    - `RateLimit-Limit`: Maximum allowed requests per time window.
    - `RateLimit-Remaining`: Remaining request quota.
    - `RateLimit-Reset`: Seconds until window resets.

---

## 3. Idempotency & Safe Mutation Retries

- State-mutating endpoints (`POST /payments`, `POST /orders`, `POST /transfers`) must enforce the `Idempotency-Key` header (IETF Internet-Draft `idempotency-key-08`).
- Key retention TTL: Minimum 24 hours.
- In-flight lock: Reject concurrent identical keys with `409 Conflict`.
- Fingerprint verification: Reject mismatched payloads using identical keys with `422 Unprocessable Content`.
