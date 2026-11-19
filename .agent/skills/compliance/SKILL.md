---
name: compliance
description: Universal AI Compliance Engineer skill. Dynamically ingests any target skill from the catalog (e.g. nextjs, astro, apiEngineering, cloudflare, internetComputer, vulnerabilityScanner) or prompts developer input, deconstructs its rules, anti-patterns, and directives into an atomic compliance matrix, and audits the codebase file-by-file and function-by-function. Enforces a zero-stopping continuous verification loop that does not terminate until 100% compliance is reached. Dynamically adapts to execution environments by orchestrating multi-agent swarms in Google Antigravity or running deterministic verification loops in Claude Code, Cursor, and Windsurf, producing certified reports at compliance-report.md.
version: 2026.x
last-verified: 2026-11-19
compatibility: Universal (Claude Code, Cursor, Google Antigravity, Windsurf, Copilot), Python 3.12+, TS/JS, Go, Rust, C/C++, all catalog skills
slash-commands:
  - command: /compliance-audit
    description: Audit the current codebase against a designated skill standard and generate compliance-report.md.
    argument-hint: "[--skill=<name>] [--path=<dir>]"
  - command: /compliance-fix
    description: Apply line-level compliance refactorings and remediation diffs for all detected non-compliance issues.
    argument-hint: "[--rule=<id>] [--interactive]"
  - command: /compliance-loop
    description: Run the continuous zero-stopping compliance loop (inspect -> detect -> patch -> re-verify) until 100% adherence.
    argument-hint: "[--max-iterations=50]"
  - command: /compliance-matrix
    description: Deconstruct any skill in the catalog into an atomic rule-by-rule verification checklist.
    argument-hint: "[--skill=<name>]"
  - command: /compliance-swarm
    description: (Antigravity mode) Parallelize compliance verification across multiple agents using the native swarm or subagent pattern.
    argument-hint: "[--workers=3]"
  - command: /compliance-verify
    description: Execute automated assertions and type/test validation to certify 100% compliance.
    argument-hint: "[--strict]"
---

# AI Compliance Engineer Master Guide

This skill establishes the rigorous operational protocol for auditing, enforcing, and certifying codebase compliance against any skill, framework standard, or architectural ruleset across the SkillFullStack catalog.

---

## ⚡ Zero-Hallucination Offline Assets Notice
Before auditing code or evaluating compliance, agents **MUST** consult the bundled official specifications in [`assets/`](assets/README.md):
- ISO/IEC 25010 Software Quality Model: [`assets/standards/iso-iec-25010.md`](assets/standards/iso-iec-25010.md)
- Static Compliance Methodology: [`assets/standards/static-compliance-methodology.md`](assets/standards/static-compliance-methodology.md)

---

## 1. Compliance Engineer Mandate

As the Compliance Engineer, you are the final authority on code quality, safety boundaries, and architectural discipline:
1. **No Approximations**: Every single directive and anti-pattern in the target skill must be verified against actual code.
2. **Small-Code Granularity**: Audit every function, module, component, and configuration file one by one.
3. **Zero-Stopping Invariant**: Never conclude an audit turn while non-compliant code remains. Continue cycling through the loop until 100% compliance is certified.

```
┌────────────────────────────────────────────────────────┐
│           AI COMPLIANCE ENGINEER MANDATE               │
├────────────────────────────────────────────────────────┤
│  1. INGEST TARGET SKILL (e.g. nextjs, cloudflare, etc.)│
│  2. EXTRACT RULES (Directives, anti-patterns, schemas) │
│  3. GRANULAR SWEEP (Function-by-function inspection)   │
│  4. EMIT REPORT (Generate compliance-report.md)        │
│  5. APPLY DIFFS (Remediate deviations safely)          │
│  6. RE-VERIFY (Loop until 100% Compliance is reached)  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Dynamic Target Skill Ingestion (`/compliance-matrix`)

The compliance engine dynamically accepts any target skill name via `--skill=<name>`. If none is provided, prompt the developer using interactive questions.

### Extraction Pipeline:
1. Load the target skill's `SKILL.md` from the repository catalog.
2. Extract the **Anti-Patterns Table**:
   - Column 1 becomes the *Prohibited Pattern*.
   - Column 2 becomes the *Violation Rationale*.
   - Column 3 becomes the *Mandatory Invariant*.
3. Extract core architectural directives (e.g., `server-only`, Data Access Layer, parameterized queries, memory nullification).
4. Deep Reference: [`references/skillRuleDeconstruction.md`](references/skillRuleDeconstruction.md).

---

## 3. Zero-Stopping Continuous Enforcement Loop (`/compliance-loop`)

When running `/compliance-loop`, the agent operates as a persistent daemon:
1. Evaluates Rule $R_i$ against file $F_j$.
2. If non-compliant:
   - Records violation in `compliance-report.md`.
   - Generates minimal-surface remediation diff.
   - Applies the patch.
   - Runs compiler/type-checker (`tsc`, `cargo check`, `go vet`, `ruff`) and test suite.
   - Re-evaluates Rule $R_i$.
3. Advances to the next file only after the current deviation is cleared.
4. Terminates **only** when all rules evaluate to `100% PASS`.
5. Deep Reference: [`references/complianceEngineProtocol.md`](references/complianceEngineProtocol.md).

---

## 4. Multi-Agent Swarm Orchestration (`/compliance-swarm`)

The skill dynamically adapts to the host execution environment:

### 4.1 Google Antigravity Mode
When running inside Antigravity, the coordinator leverages native `swarm` tools:
- Spawns specialized workers:
  - `@frontend-auditor`: Checks UI boundaries, Server/Client component directives, CVA styling.
  - `@backend-auditor`: Checks API routes, database transactions, DAL patterns, error envelopes.
  - `@security-auditor`: Checks memory nullification, taint tracking, input sanitization, auth gates.
- Public Board Synthesis: Workers post verified deviations to the board; coordinator compiles the final `compliance-report.md`.

### 4.2 Claude Code / Cursor / Windsurf Mode
When running in single-agent CLI environments:
- Operates in sequential topological sweep.
- Incrementally validates each module.
- Deep Reference: [`references/multiAgentSwarmOrchestration.md`](references/multiAgentSwarmOrchestration.md).

---

## 5. Canonical Dossier Standard: `compliance-report.md` (`/compliance-audit`)

All audit executions generate or update `compliance-report.md` in the scanned workspace root:
- **Header Metadata**: Timestamp, evaluated codebase, target skill name, version, and compliance score percentage ($0\% - 100\%$).
- **Executive Summary**: High-level evaluation for engineering leads.
- **Rule-by-Rule Matrix**: Table listing Rule ID, Category, Requirement, Status (`PASS` / `FAIL`), and Violations Found.
- **Line-by-Line Diffs**: Exact line numbers with side-by-side git diffs showing the non-compliant code and the compliant fix.
- **Loop Progression**: Iterations executed, remaining deviations, and continuous loop state.
- **Canonical Template**: [`templates/complianceReport.template.md`](templates/complianceReport.template.md).
- **Deep Reference**: [`references/complianceDossierStandard.md`](references/complianceDossierStandard.md).

---

## 6. Anti-Patterns to Avoid

| Anti-Pattern | Why It Breaks Quality | Correct Modern Standard |
| :--- | :--- | :--- |
| **Stopping with Unresolved Deviations** | Leaves code partially non-compliant, defeating the compliance engineer mandate. | Enforce the continuous loop until 100% adherence is certified. |
| **Modifying Business Logic During Remediation** | Breaks functional contracts or introduces regressions. | Use minimal-surface diffs that enforce structural/security rules while preserving logic. |
| **Hardcoding Skill Rules** | Breaks compatibility when skills evolve or when auditing other frameworks. | Dynamically parse the target skill's `SKILL.md` and anti-pattern tables at runtime. |
| **Skipping Type and Test Verification** | Remediation patches may introduce syntax errors or broken imports. | Always run typecheckers and test suites immediately after applying compliance diffs. |

---

## 7. Automated CLI Diagnostics & Execution (`/compliance-verify`)

Run the automated compliance CLI tool directly:

```bash
# 1. Audit codebase against Next.js skill
python3 skills/foundation/compliance/scripts/runComplianceAudit.py --skill nextjs --path ./my-app

# 2. Audit codebase against API Engineering skill
python3 skills/foundation/compliance/scripts/runComplianceAudit.py --skill apiEngineering --path ./backend

# 3. Output JSON for CI/CD pipeline integration
python3 skills/foundation/compliance/scripts/runComplianceAudit.py --skill vulnerabilityScanner --path ./src --format json
```
