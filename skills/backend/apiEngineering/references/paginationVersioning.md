# Contextual Pagination, Idempotency & Versioning Reference

---

## 1. Contextual Pagination Selection Matrix

| Context | Recommended Model | Request Signature | Behavior & Trade-offs |
| :--- | :--- | :--- | :--- |
| **Small Admin Tables** ($< 1,000$ rows) | **Offset** | `?page=2&limit=20` | Simple for users to jump to page N. Degrades on large tables (`OFFSET 100000`). |
| **Large Datasets** ($> 10,000$ rows) | **Cursor** | `?cursor=eyJpZCI6...&limit=50` | Constant $O(1)$ database execution using indexed comparison (`WHERE id > :cursor_id`). |
| **Frequently Mutated Data** | **Cursor** | `?after=token&limit=25` | Prevents duplicate or skipped records when rows are inserted/deleted mid-browse. |
| **Data Exports / Analytics** | **Keyset** | `?since_id=105400&limit=500` | High throughput sequential scanning without pagination state overhead. |

### Universal Constraint
Every strategy must enforce a hard limit: `limit = Math.min(requestedLimit || 20, 100)`.

---

## 2. Safe Retries via IETF Internet-Draft `Idempotency-Key`

Status: **IETF Internet-Draft (`draft-ietf-httpapi-idempotency-key-header-08`)**

### Protocol State Machine
```
Client Request
      |
      v
Has Idempotency-Key Header?
      |
      +---> NO  --> Execute normal request flow.
      |
      +---> YES --> Query Cache/DB for key
                     |
                     +---> Found in Cache?
                            |
                            +-- Status: IN_FLIGHT --> Return 409 Conflict
                            |
                            +-- Payload Fingerprint Mismatch? --> Return 422 Unprocessable Content
                            |
                            +-- Status: COMPLETED --> Replay Cached Status Code & Body
```

### Fingerprint Generation (SHA-256)
Compute hash over: `HTTP_METHOD + PATH + REQUEST_BODY`. Store alongside the idempotency token for 24 hours.

---

## 3. Deprecation Header Standards

When retiring an endpoint, emit exact headers:
```http
Deprecation: @1794787200
Sunset: Tue, 17 Nov 2026 00:00:00 GMT
Link: <https://api.example.com/docs/v2-migration>; rel="deprecation"
```
- `Deprecation`: RFC 9651 Structured Field Date prefixed with `@`.
- `Sunset`: RFC 8594 HTTP-date timestamp.
