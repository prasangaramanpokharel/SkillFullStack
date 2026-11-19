# Static Compliance & Continuous Enforcement Methodology

This standard establishes the operational methodology for static code compliance auditing.

---

## 1. Compliance Engineering Principles

### 1.1 Atomic Rule Deconstruction
Every high-level architectural rule in a skill must be decomposed into three elements:
1. **Target Selector**: File paths, imports, decorators, function signatures, or AST nodes subject to the rule.
2. **Negative Constraint (Anti-Pattern)**: The exact syntactical or logical pattern that is prohibited.
3. **Positive Invariant**: The required compliant syntax or replacement pattern.

### 1.2 Zero-Stopping Enforcement Loop
Compliance audits cannot terminate when errors exist. The agent must loop through the codebase:
$$\text{Scan} \longrightarrow \text{Detect Deviation} \longrightarrow \text{Generate Patch Diff} \longrightarrow \text{Apply & Validate} \longrightarrow \text{Advance}$$
The loop terminates **only** when all rules evaluate to `100% PASS`.

---

## 2. Multi-Agent Compliance Swarm Pattern
When auditing large enterprise repositories, compliance checks can be distributed across specialized roles:
- **Lead Compliance Auditor**: Coordinates the rules matrix and aggregates scorecard.
- **Subsystem Inspectors**: Parallel workers auditing independent directories (frontend, backend, infra).
- **Remediation Authors**: Generate git diffs for flagged deviations.
- **Quality Verifiers**: Run test suites to ensure remediations preserve business logic.
