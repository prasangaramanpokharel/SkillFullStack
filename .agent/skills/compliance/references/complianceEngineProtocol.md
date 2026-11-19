# Compliance Engine Protocol

This guide establishes the step-by-step operating protocol for the AI Compliance Engineer.

---

## 1. Operating Mandate

The compliance engineer's goal is total adherence to an engineering standard.
1. Ingest the target skill or framework standard.
2. Formulate an atomic Rule Verification Matrix.
3. Inspect the codebase file-by-file, function-by-function.
4. Verify each small code block against each rule.
5. Provide line-level diffs for every non-compliant block.
6. **Zero-Stopping Invariant**: Never conclude an audit turn while non-compliant code remains unaddressed.

---

## 2. Execution State Machine

```
┌────────────────────────────────────────────────────────┐
│            COMPLIANCE ENGINE EXECUTION LOOP            │
├────────────────────────────────────────────────────────┤
│ 1. INGEST TARGET SKILL (e.g. nextjs, apiEngineering)   │
│         │                                              │
│         ▼                                              │
│ 2. BUILD RULE MATRIX (Extract directives & anti-pat)   │
│         │                                              │
│         ▼                                              │
│ 3. CODEBASE SWEEP (Scan AST, imports, boundaries)      │
│         │                                              │
│         ▼                                              │
│ 4. EMIT COMPLIANCE REPORT (compliance-report.md)       │
│         │                                              │
│         ▼                                              │
│ 5. CHECK ADHERENCE SCORE                               │
│         ├── 100% PASS ──> CERTIFY & FINALIZE           │
│         └── < 100%   ──> GENERATE REMEDIATION DIFFS    │
│                                 │                      │
│                                 ▼                      │
│                             APPLY FIXES                │
│                                 │                      │
│                                 ▼                      │
│                           RE-VERIFY CODE               │
│                                 │                      │
│                           (LOOP TO STEP 4)             │
└────────────────────────────────────────────────────────┘
```
