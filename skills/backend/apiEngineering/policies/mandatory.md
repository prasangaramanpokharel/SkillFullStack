# Mandatory API Engineering Policies

These policies are non-negotiable requirements for all APIs created or maintained under the API Engineering System.

---

## 1. Architectural Boundaries

- **Separation of Concerns**:
  - `Transport Layer (Controllers/Routes)`: Only parse HTTP request headers, query parameters, body, validate DTO schemas, and map results to HTTP status codes.
  - `Domain Service Layer`: Encapsulates pure business logic, calculations, invariants, and authorization rules.
  - `Persistence Layer (Repositories)`: Encapsulates database queries, ORM calls, and transactional boundaries.
- **DTO Isolation**:
  - Database models/entities must NEVER be returned directly in API responses.
  - Request DTOs and Response DTOs must be explicitly defined separate types.

---

## 2. HTTP Protocol Semantics

- **Status Code Precision**:
  - `200 OK`: Successful read or synchronous update returning representation.
  - `201 Created`: Resource created. MUST include `Location: /v1/<resource>/<id>` header.
  - `202 Accepted`: Long-running asynchronous request queued.
  - `204 No Content`: Successful deletion or action returning no body. MUST NOT include response body.
  - `304 Not Modified`: ETag / conditional request validation match.
  - `400 Bad Request`: Generic malformed syntax (missing required header, malformed JSON).
  - `401 Unauthorized`: Missing, expired, or invalid authentication credentials.
  - `403 Forbidden`: Authenticated caller lacks permission for the resource.
  - `404 Not Found`: Resource does not exist or caller should not know it exists.
  - `409 Conflict`: Request conflicts with current server state (duplicate unique key, concurrent idempotency lock, optimistic lock failure).
  - `422 Unprocessable Content`: Semantically invalid request payload (validation errors, idempotency payload mismatch).
  - `429 Too Many Requests`: Rate limit exhausted. MUST include `Retry-After` header.
  - `500 Internal Server Error`: Unhandled crash. MUST NOT expose stack traces or DB errors to caller.
  - `502 Bad Gateway` / `503 Service Unavailable` / `504 Gateway Timeout`: Upstream dependency failure.

---

## 3. Response Contract Format

- **Success Envelope**:
  ```json
  {
    "data": { ... },
    "meta": { ... }
  }
  ```
- **Error Format**: Strictly RFC 9457 `application/problem+json` content-type.
