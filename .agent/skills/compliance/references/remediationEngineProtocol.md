# Remediation Engine Protocol (`/compliance-fix`)

This guide governs how compliance remediations must be applied to source code.

---

## 1. Remediation Quality Principles

1. **Behavior Preservation**: Remediations must enforce skill compliance without altering the business logic or breaking existing functional tests.
2. **Minimal Surface Diffs**: Only modify the specific lines and tokens required to satisfy the rule.
3. **Type-Safe Transformations**: Ensure TypeScript, Go, Rust, or Python types compile cleanly after the patch.
4. **Immediate Post-Patch Validation**:
   - Run type checks (`tsc --noEmit`, `go vet`, `cargo check`).
   - Run unit test suites.
   - Re-evaluate the rule to confirm the deviation is cleared.

---

## 2. Iteration Loop Guardrails
If a remediation fails unit tests or introduces syntax errors:
1. Revert to pre-patch state.
2. Formulate an alternate compliance refactoring.
3. Re-test before proceeding to the next rule in the matrix.
