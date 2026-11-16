# Pre-Flight Production API Readiness Checklist

Execute this checklist before releasing or deploying any new API endpoint to staging or production:

## 1. Contract & Standards Compliance
- [ ] Contract is authored in OpenAPI 3.2.1 / 3.1 with zero syntax errors.
- [ ] All error responses use `application/problem+json` matching RFC 9457.
- [ ] Success responses return `{ "data": ..., "meta": ... }` envelope.
- [ ] Status codes are semantic (201 for POST creation, 204 for DELETE, 422 for validation).

## 2. Security (OWASP Top 10)
- [ ] BOLA: Object ID lookups enforce tenant and user ownership checks in SQL/ORM.
- [ ] BOPLA: Request DTOs strictly allowlist acceptable fields; mass assignment blocked.
- [ ] Authentication: Tokens validated via cryptographically secure signatures with $\le 15$ min TTL.
- [ ] SSRF: All outbound webhooks validate destination IPs, blocking loopback and cloud metadata (`169.254.169.254`).
- [ ] Secret Scrubbing: Logs and error responses contain no credentials, stack traces, or internal server tokens.

## 3. Scalability & Resilience
- [ ] Collection endpoints enforce pagination with hard upper bounds (`limit <= 100`).
- [ ] Filtered and sorted parameters are backed by database indexes.
- [ ] Critical state mutations enforce the `Idempotency-Key` header (IETF draft-08).
- [ ] Upstream external calls implement timeouts ($\le 3$s) and circuit breakers.

## 4. Observability & Operations
- [ ] Structured JSON logging emitting `traceId`, `spanId`, `route`, `status`, and `durationMs`.
- [ ] RED metrics tracked (Rate, Errors, Duration p95/p99).
- [ ] Health checks configured (`/healthz` liveness, `/readyz` dependency checks).
