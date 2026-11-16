# OWASP API Security Top 10 (2023 / 2026) Deep Reference

Comprehensive threat defense checklist across all 10 vectors.

---

## The 10 Vectors & Engineering Mitigations

### 1. API1:2023 - Broken Object Level Authorization (BOLA)
- **Threat**: Attacker changes resource ID in URL to access unauthorized data.
- **Defense**: Always enforce tenant/user context in the SQL WHERE clause or repository call. Never trust client IDs.

### 2. API2:2023 - Broken Authentication
- **Threat**: Weak password policies, token leakage in URLs, flawed JWT signature verification.
- **Defense**: Asymmetric token signing (RS256/EdDSA), 15-minute token TTL, no credentials in query strings.

### 3. API3:2023 - Broken Object Property Level Authorization (BOPLA)
- **Threat**: Mass assignment where client submits internal fields (`is_admin`, `verified`, `credit_balance`).
- **Defense**: Strict DTO allowlisting. Reject or ignore non-permitted fields. Never bind raw JSON directly into ORM entities.

### 4. API4:2023 - Unrestricted Resource Consumption
- **Threat**: DoS via huge payload uploads, unbounded database queries, or regex exponential backtracking.
- **Defense**: Mandatory `limit <= 100` on collections, request body size limits (`1MB` default), rate limiting.

### 5. API5:2023 - Broken Function Level Authorization (BFLA)
- **Threat**: Standard user invokes administrative endpoints (e.g. `POST /v1/users/{id}/ban`).
- **Defense**: Role and scope verification at middleware entry point before handler execution.

### 6. API6:2023 - Unrestricted Access to Sensitive Business Flows
- **Threat**: Automated scalping bots, credential stuffing, fake account bulk creation.
- **Defense**: Progressive delays, CAPTCHA on sensitive flows, device risk scoring.

### 7. API7:2023 - Server Side Request Forgery (SSRF)
- **Threat**: Attacker inputs `http://169.254.169.254/latest/meta-data` as webhook URL to exfiltrate cloud credentials.
- **Defense**: IP resolution check blocking RFC 1918 private IPs, loopback, and cloud metadata endpoints.

### 8. API8:2023 - Security Misconfiguration
- **Threat**: Verbose error stack traces, unpatched dependencies, overly permissive CORS (`Access-Control-Allow-Origin: *` with credentials).
- **Defense**: Generic RFC 9457 errors in production, hardened TLS (TLS 1.3), specific CORS origin allowlists.

### 9. API9:2023 - Improper Inventory Management
- **Threat**: Old API versions (`/v1`) running unpatched while `/v2` is secured.
- **Defense**: Maintain central OpenAPI inventory, automated deprecation header emission (RFC 9745), and decommissioned route gating.

### 10. API10:2023 - Unsafe Consumption of APIs
- **Threat**: Blindly trusting third-party API payloads leading to SQLi or command injection.
- **Defense**: Validate all inbound payloads from third parties against strict JSON schemas with timeouts.
