# Brand Check Audit Report

**Target Design:** {{DESIGN_TITLE}} (`{{DESIGN_ID}}`)  
**Brand Kit:** {{BRAND_KIT_NAME}} (`{{BRAND_KIT_ID}}`)  
**Audit Timestamp:** {{AUDIT_TIMESTAMP}}  
**Overall Status:** {{OVERALL_STATUS}}

---

## 1. Executive Summary
{{EXECUTIVE_SUMMARY}}

---

## 2. Findings Matrix

### 🚨 Off Brand (Action Required)
{{OFF_BRAND_FINDINGS}}
<!-- Example:
- **[Color - High]** Slide 2 title is rendered in `#1A73E8` instead of primary brand blue `#0B5CD7`.
- **[Logo - High]** Slide 1 cover logo margin is 12px (minimum required: 32px).
-->

### ❓ Can't Verify (Input Needed)
{{CANT_VERIFY_FINDINGS}}
<!-- Example:
- Brand kit API did not provide secondary accent palette hex values. Please provide brand accent colors.
-->

### ✅ On Brand (Compliant)
{{ON_BRAND_FINDINGS}}
<!-- Example:
- Slide 1–5 typography weights match brand specifications.
- Primary logo mark uses official monochrome inverted variant.
-->

---

## 3. Recommended Remediation Plan
1. **Automated Mutations via `/canva-edit`**:
   {{AUTOMATED_ACTIONS}}
2. **Manual Canva UI Adjustments**:
   {{MANUAL_ACTIONS}}
