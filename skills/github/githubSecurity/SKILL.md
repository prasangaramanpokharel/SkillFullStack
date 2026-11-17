---
name: githubSecurity
description: Secure repositories and software supply chains. Automates Dependabot grouping, CodeQL static analysis matrix, secret scanning push protection, and security advisories. Commands: /github-security, /github-codeql, /github-dependabot, /github-secrets.
version: v2
last-verified: 2026-11-17
compatibility: GitHub Advanced Security (GHAS), GitHub Free/Pro, GitHub CLI 2.40+
slash-commands:
  - command: /github-security
    description: Run repository security audit across CodeQL, Dependabot, and Secret Scanning
    argument-hint: "[audit | codeql | dependabot | secret-scanning]"
  - command: /github-codeql
    description: Generate and tune CodeQL static analysis matrix workflows
    argument-hint: "[--languages=javascript,typescript,python,go]"
  - command: /github-dependabot
    description: Scaffold grouped Dependabot configuration for zero PR spam
    argument-hint: "[--ecosystem=npm|pip|gomod|cargo|docker]"
  - command: /github-secrets
    description: Configure Secret Scanning Push Protection and bypass auditing
    argument-hint: "[--enforce=strict]"
---

# GitHub Code & Supply Chain Security Guide

Implement enterprise repository defenses adhering to the **Understand $\rightarrow$ Inspect $\rightarrow$ Plan $\rightarrow$ Execute $\rightarrow$ Validate $\rightarrow$ Report** lifecycle.

## 1. Execution Lifecycle Protocol

```
┌────────────────────────────────────────────────────────┐
│ 1. UNDERSTAND                                          │
│    Identify dependencies, active programming languages,│
│    compliance requirements, and threat surface.        │
├────────────────────────────────────────────────────────┤
│ 2. INSPECT                                             │
│    Run `gh api /repos/:owner/:repo/dependabot/alerts`  │
│    and `gh api /repos/:owner/:repo/secret-scanning/alerts`.
├────────────────────────────────────────────────────────┤
│ 3. PLAN                                                │
│    Design grouped Dependabot PR schedules to prevent   │
│    alert fatigue, and map CodeQL language matrices.    │
├────────────────────────────────────────────────────────┤
│ 4. EXECUTE                                             │
│    Deploy `.github/dependabot.yml` and CodeQL workflow │
│    with security-extended query suites.                │
├────────────────────────────────────────────────────────┤
│ 5. VALIDATE                                            │
│    Execute `python3 scripts/auditRepoSecurity.py` to   │
│    assert zero open critical CVEs or secret leaks.     │
├────────────────────────────────────────────────────────┤
│ 6. REPORT                                              │
│    Generate security posture scorecard with remediation│
│    milestones for engineering leadership.              │
└────────────────────────────────────────────────────────┘
```

---

## 2. Dependabot Grouped Updates Standard (`.github/dependabot.yml`)

Eliminate PR notification fatigue by batching minor/patch updates into a single periodic Pull Request:

```yaml
version: 2
updates:
  # 1. GitHub Actions Workflows
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      actions:
        patterns: ["*"]

  # 2. Package Ecosystem (e.g. npm, pip, gomod)
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      production-dependencies:
        dependency-type: "production"
        update-types: ["minor", "patch"]
      development-dependencies:
        dependency-type: "development"
        update-types: ["minor", "patch"]
```

---

## 3. CodeQL Static Application Security Testing (`codeql.yml`)

Run deep taint and semantic analysis across PRs targeting `main`:

```yaml
name: "CodeQL Analysis"

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1' # Monday 6 AM weekly scan

permissions:
  actions: read
  contents: read
  security-events: write

jobs:
  analyze:
    name: Analyze (${{ matrix.language }})
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        include:
          - language: javascript-typescript
            build-mode: none
    steps:
      - name: Checkout
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: security-extended

      - name: Perform Analysis
        uses: github/codeql-action/analyze@v3
```

---

## 4. Dual-Mode Execution Commands

### GitHub CLI (`gh`) Operations
```bash
# Audit active Dependabot security alerts
gh api /repos/:owner/:repo/dependabot/alerts --jq '.[] | {number, state, security_advisory: .security_advisory.summary, severity: .security_advisory.severity}'

# Audit secret scanning alerts
gh api /repos/:owner/:repo/secret-scanning/alerts

# Enable push protection (prevents commits with secrets from pushing)
gh api -X PATCH /repos/:owner/:repo \
  -f security_and_analysis[secret_scanning_push_protection][status]=enabled
```

### Direct Security Audit Tool
```bash
python3 skills/github/githubSecurity/scripts/auditRepoSecurity.py --repo owner/repo
```

---

## 5. Anti-Patterns & Pitfalls
- ❌ **Ungrouped Dependabot Schedules**: Running daily updates without grouping floods repositories with dozens of competing PRs that break CI queues.
- ❌ **Ignoring Push Protection**: Relying strictly on post-push secret scanning leaks credentials to Git history; always enable **Secret Scanning Push Protection**.
- ❌ **Running Heavy CodeQL on Every Feature Push**: CodeQL takes 5–20 minutes to compile and analyze ASTs; run on PRs to `main` and weekly schedules, not every push to feature branches.

---

## 6. References & Bundled Utilities
- **Official Security Documentation Assets**: [assets/](assets/) — Official specifications for CodeQL scanning, dependabot.yml schema, secret scanning push protection, and security REST APIs.
- Grouped Dependabot blueprint: [references/dependabotConfig.yml](references/dependabotConfig.yml)
- Production CodeQL matrix workflow: [references/codeqlAnalysis.yml](references/codeqlAnalysis.yml)
- Security audit scanner: [scripts/auditRepoSecurity.py](scripts/auditRepoSecurity.py)
