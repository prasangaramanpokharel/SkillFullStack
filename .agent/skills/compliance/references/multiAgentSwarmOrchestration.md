# Multi-Agent Swarm Orchestration (`/compliance-swarm`)

The compliance engine dynamically adapts to the host AI environment, maximizing parallel auditing throughput when multi-agent coordination is available.

---

## 1. Environment Detection & Strategy

### 1.1 Google Antigravity Mode (Swarm & Subagent)
In Antigravity, the compliance coordinator can orchestrate specialized workers via `swarm`:
- **Coordinator Agent**:
  - Sets swarm title: `title: "Codebase Compliance Audit"`
  - Adds author/verifier workers:
    - `add: { name: "frontend-auditor", brief: "Audit client components and layouts against target skill rules" }`
    - `add: { name: "backend-auditor", brief: "Audit server actions, API routes, and DB layers against target skill rules" }`
    - `add: { name: "security-auditor", brief: "Verify auth gates, taint flows, and boundaries" }`
  - Aggregates findings into the shared `compliance-report.md`.

### 1.2 Claude Code / Cursor / Windsurf Mode (Deterministic Sequential Loop)
In single-agent CLI environments, the agent executes the sequential loop:
- Scans files in topological or directory order.
- Evaluates rules file-by-file.
- Updates `compliance-report.md` incrementally.
- Loops through iterations until all rules pass.

---

## 2. Swarm Task Division Principles
- **No Shared File Mutations**: When workers generate remediations, each worker owns an independent file slice (`share` or `branch` workspace mode).
- **Public Board Synthesis**: Workers post verified deviations to the board; coordinator compiles the master scorecard.
