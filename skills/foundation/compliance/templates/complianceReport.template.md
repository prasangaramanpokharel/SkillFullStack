# Compliance Audit Report: {TARGET_SKILL}

- **Audit Date**: {TIMESTAMP}
- **Target Skill**: `{SKILL_NAME}` (v{SKILL_VERSION})
- **Evaluated Codebase**: `{CODEBASE_PATH}`
- **Overall Compliance Score**: {PERCENTAGE}% ({PASSED_COUNT}/{TOTAL_RULES} Rules Passed)
- **Compliance Status**: {FULLY_COMPLIANT | REMEDIATION_REQUIRED}
- **Agent Execution Mode**: {ANTIGRAVITY_SWARM | CLAUDE_CODE | CURSOR | STANDALONE_CLI}

---

## 1. Compliance Executive Summary
{SUMMARY_OF_FINDINGS_AND_ADHERENCE}

---

## 2. Rule-by-Rule Compliance Verification Matrix

| Rule ID | Rule Category | Requirement / Constraint | Status | Violations Found | Verified Location |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `R-01` | Architecture | {RULE_TITLE} | {STATUS_PASS_FAIL} | {VIOLATION_COUNT} | `{FILE_PATH}:{LINE}` |

---

## 3. Detailed Line-by-Line Non-Compliance Diffs

### Violation {INDEX}: {RULE_TITLE}
- **File**: `{FILE_PATH}:{LINE_NUMBER}`
- **Violated Constraint**: `{RULE_DESCRIPTION}`
- **Technical Explanation**: {WHY_IT_VIOLATES_THE_SKILL_STANDARD}

```diff
--- a/{FILE_PATH}
+++ b/{FILE_PATH}
@@ -{LINE_NUMBER},1 +{LINE_NUMBER},1 @@
- {NON_COMPLIANT_LINE}
+ {COMPLIANT_HARDENED_LINE}
```

---

## 4. Remediation Action Plan & Loop Progression
- **Total Iterations Completed**: {ITERATION_COUNT}
- **Remaining Deviations**: {REMAINING_COUNT}
- **Continuous Loop State**: {TERMINATED_100_PERCENT_COMPLIANT | LOOPING_NEXT_MODULE}
