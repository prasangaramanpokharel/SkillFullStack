---
name: apiEngineering
description: Enterprise API engineering framework covering contract-first OpenAPI 3.2.1, RFC 9457 errors, IETF Idempotency-Key, OWASP API Top 10, and breaking-change detection
version: 2026.11
last-verified: 2026-11-16
slash-commands:
  - command: /api-engineering
    description: Full API engineering orchestrator from research to verification
    argument-hint: "[--spec=path] [--stack=node|python|go|java]"
  - command: /api-design
    description: Contract-first API design with OpenAPI 3.2.1 and resource modeling
    argument-hint: "[--resource=Name] [--operations=crud|actions]"
  - command: /api-crud
    description: Design and implement semantic HTTP REST/CRUD and action endpoints
    argument-hint: "[--entity=Name] [--dto]"
  - command: /api-audit
    description: Audit API endpoints against RFC 9110, RFC 9457, and OWASP API Top 10
    argument-hint: "[--spec=path] [--strict]"
  - command: /api-security
    description: Threat model and audit endpoints for BOLA, BOPLA, SSRF, and auth flaws
    argument-hint: "[--target=route] [--owasp]"
  - command: /api-breaking
    description: Compare two API specifications to detect breaking changes in CI
    argument-hint: "[--old=v1.json] [--new=v2.json]"
---

# Production API Engineering System (2026 Standards)

Enterprise engineering methodology for designing, implementing, auditing, and maintaining production-grade APIs across any backend stack.

---

## 1. Non-Negotiable Engineering Laws

1. **Contract-First & API-First**: The machine-readable contract (OpenAPI 3.2.1) is the source of truth, authored and validated before implementing route code.
2. **Never Put Business Logic in Route Handlers**: Controllers parse inputs, invoke domain services, and serialize response DTOs. Zero SQL or business rules in handlers.
3. **Never Expose Database Entities Directly**: Public API contracts must use isolated Request/Response DTOs to prevent mass assignment (BOPLA) and internal schema leakage.
4. **Never Return 200 OK for Errors**: Use accurate RFC 9110 status codes paired with RFC 9457 `application/problem+json` error envelopes.
5. **Never Allow Unbounded Collection Queries**: Enforce context-driven pagination (Cursor/Keyset/Offset) with an absolute ceiling (`limit <= 100`).
6. **Mandatory Object-Level Authorization (BOLA)**: Check tenant and user ownership on every single access to an object identifier.
7. **Safe Retries via Idempotency**: State-mutating operations (`POST`, `PATCH`) must support `Idempotency-Key` (IETF Internet-Draft `idempotency-key-08`) with SHA-256 payload fingerprinting.
8. **Additive Changes by Default**: Never silently modify existing field semantics. All removals or signature changes require RFC 9745 (`Deprecation`) and RFC 8594 (`Sunset`) headers with a minimum 180-day deprecation cycle.

---

## 2. Six-Stage Execution Lifecycle

```mermaid
flowchart LR
    U["1. Understand"] --> I["2. Inspect"]
    I --> P["3. Plan"]
    P --> E["4. Execute"]
    E --> V["5. Validate"]
    V --> R["6. Report"]
```

### Stage 1: Understand
- Identify client consumers (mobile, SPA, 3rd-party webhook, microservice).
- Clarify domain invariants, concurrency model, scale ceiling, and tenant isolation rules.

### Stage 2: Inspect
- Scan existing repository code, routes, ORM models, and existing OpenAPI specs using `python3 scripts/auditApiContract.py`.
- Identify missing error formats, unbounded endpoints, or raw entity leakage.

### Stage 3: Plan
- Author or update OpenAPI 3.2.1 contract (`templates/openapi.yaml`).
- Design request/response DTOs:
  - Success Envelope: `{ "data": T, "meta": Meta }`
  - Error Envelope: RFC 9457 `application/problem+json`
- Select pagination model (see [references/paginationVersioning.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/references/paginationVersioning.md)).
- Conduct OWASP API Security Top 10 threat modeling.

### Stage 4: Execute
- Scaffold route handlers adhering to `policies/mandatory.md` and `policies/security.md`.
- Implement service layer, data validation boundaries, and transaction boundaries (`policies/performance.md`).
- Implement `Idempotency-Key` middleware:
  - Cache active request key $\rightarrow$ return `409 Conflict` if in flight.
  - Verify payload SHA-256 fingerprint $\rightarrow$ return `422 Unprocessable Content` if mismatched.
  - Cache response with TTL $\rightarrow$ replay stored status and payload on identical retry.

### Stage 5: Validate
1. Run contract and security linter: `python3 scripts/auditApiContract.py --spec=openapi.yaml --strict`.
2. Run CI breaking-change detector: `python3 scripts/checkBreakingChanges.py --old=v1.json --new=v2.json`.
3. Assert all tests pass in `evals/evalApiEngineering.py`.

### Stage 6: Report
Produce the final API delivery summary:
- Verified OpenAPI 3.2.1 specification path.
- Enforced security policies and authorization checks.
- Benchmark and latency SLO profile.
- Deprecation schedule (RFC 9745 / RFC 8594) if replacing legacy endpoints.

---

## 3. Core Architecture Separation

| Architectural Layer | Location & Purpose |
| :--- | :--- |
| **Policies** | [policies/mandatory.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/policies/mandatory.md), [policies/security.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/policies/security.md), [policies/performance.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/policies/performance.md), [policies/compatibility.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/policies/compatibility.md) — Enforceable rulebooks. |
| **Methods & References** | [references/responseStandards.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/references/responseStandards.md), [references/openApi32Standards.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/references/openApi32Standards.md), [references/apiSecurityOwasp.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/references/apiSecurityOwasp.md), [references/paginationVersioning.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/references/paginationVersioning.md), [references/databaseTransactions.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/references/databaseTransactions.md), [references/distributedReliability.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/references/distributedReliability.md), [references/contractCompatibility.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/references/contractCompatibility.md), [references/multiTenancy.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/references/multiTenancy.md), [references/apiObservability.md](file:///Users/prasangaramanpokharel/projects/SkillFullStack/skills/backend/apiEngineering/references/apiObservability.md) — Implementation guides. |
| **Automation Tooling** | `scripts/auditApiContract.py`, `scripts/generateResponseEnvelope.py`, `scripts/checkBreakingChanges.py` — Deterministic CLI tools. |
| **Templates** | `templates/openapi.yaml`, `templates/problemDetails.json`, `templates/apiChecklist.md` — Starter blueprints. |
