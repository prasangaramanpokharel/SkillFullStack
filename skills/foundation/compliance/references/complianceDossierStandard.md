# Compliance Dossier Standard (`compliance-report.md`)

When executing an audit, the compliance engineer generates a central dossier at the workspace root: `compliance-report.md`.

---

## 1. Mandatory Dossier Sections

1. **Header Metadata**:
   - Audit Timestamp.
   - Evaluated Codebase Path.
   - Target Skill name and version.
   - Overall Compliance Score ($0\% - 100\%$).
   - Current Compliance Status (`FULLY_COMPLIANT` vs `REMEDIATION_REQUIRED`).
2. **Executive Summary**:
   - High-level overview of codebase architectural health and rule adherence.
3. **Rule Verification Matrix Table**:
   - Columns: Rule ID, Category, Requirement, Status (`PASS` / `FAIL`), Violations Count, Verified Location.
4. **Detailed Line-by-Line Deviations**:
   - For every violation, provide exact file and line number.
   - Exact rule description that was violated.
   - Side-by-side git diff showing the non-compliant code and the compliant remediation.
5. **Remediation Action Plan & Loop Progression**:
   - Total iterations completed.
   - Remaining deviations.
   - Next actions in the continuous enforcement loop.
