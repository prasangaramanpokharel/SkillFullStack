# Production API Standards & Latency Budgets (`/web-api`)

Web application backends and edge APIs require predictable error envelopes, strict latency SLOs, and idempotent state mutations.

---

## 1. Latency Budgets & SLO Targets

| Metric | SLO Target | Failure Action |
| :--- | :---: | :--- |
| **p50 (Median Latency)** | $\le 50\text{ms}$ | Optimize database indexing and connection pooling. |
| **p95 (95th Percentile)** | $\le 150\text{ms}$ | Profile external microservice calls and slow queries. |
| **p99 (Worst Case)** | $\le 300\text{ms}$ | Implement query timeouts, circuit breakers, and edge caching. |

---

## 2. Standardized Error Envelope (RFC 9457)
All error responses ($4\text{xx}$ and $5\text{xx}$) MUST return `Content-Type: application/problem+json`:

```json
{
  "type": "https://api.example.com/errors/invalid-credentials",
  "title": "Invalid Credentials",
  "status": 401,
  "detail": "The provided password does not match the account.",
  "instance": "/api/v1/auth/login",
  "traceId": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
  "timestamp": "2026-11-19T16:45:00Z"
}
```

---

## 3. Idempotency & Concurrency Control
- **`Idempotency-Key` Header**: Mutating operations (`POST /payments`, `POST /orders`) must accept an idempotency token.
- If a client retries due to network failure, the server returns the cached response from the initial execution rather than executing the charge twice.
- **Optimistic Locking**: Use `ETag` and `If-Match` headers on resource updates (`PUT / PATCH`) to prevent concurrent overwrite collisions (lost updates).
