# API Security Policies (OWASP API Top 10 Enforced)

All API implementations must adhere to these enforceable security policies.

---

## 1. Authorization & Access Control

- **BOLA Protection (API1:2023)**:
  - Every endpoint accepting an object identifier (e.g. `/v1/invoices/{id}`) must scope database lookups to the authenticated user's tenant or account ID:
    ```sql
    -- Compliant:
    SELECT * FROM invoices WHERE id = :id AND tenant_id = :auth_tenant_id;
    -- Non-Compliant (BOLA Vulnerability):
    SELECT * FROM invoices WHERE id = :id;
    ```
- **BOPLA & Mass Assignment (API3:2023)**:
  - Request DTOs must use strict allowlisting. Unrecognized properties must be stripped or rejected with `422`.
  - Properties such as `role`, `is_admin`, `verified`, or `tenant_id` must NEVER be bindable from client requests.
- **BFLA (API5:2023)**:
  - Administrative routes must enforce explicit role assertions at the controller gateway or middleware, never relying on UI invisibility.

---

## 2. Authentication & Credential Safety

- Short-lived access tokens ($\le 15$ minutes) paired with rotating refresh tokens stored in `HttpOnly`, `Secure`, `SameSite=Strict` cookies.
- Sensitive credentials, API keys, or JWT tokens must NEVER be accepted in query strings (`?token=...`). Use `Authorization: Bearer <token>`.
- Passwords must be hashed using Argon2id or bcrypt (cost factor $\ge 12$).

---

## 3. Input Sanitization & SSRF Defense

- Outbound webhooks or external HTTP requests (API7:2023) must parse and validate target hostnames against an allowlist, strictly blocking loopback (`127.0.0.1`, `localhost`) and cloud metadata IPs (`169.254.169.254`).
- SQL queries must exclusively use parameterized queries or type-safe query builders. Raw string concatenation is forbidden.
