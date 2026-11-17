---
name: githubAction
description: Design and implement production GitHub Actions CI/CD workflows. Supports matrix builds, concurrency cancelation, dependency caching, least-privilege permissions, and commit SHA action pinning. Commands: /github-action, /github-ci, /github-cd.
version: v2
last-verified: 2026-11-17
compatibility: GitHub Actions, GitHub CLI 2.40+, act, YAML 1.2
slash-commands:
  - command: /github-action
    description: Generate or audit modular GitHub Actions workflows
    argument-hint: "[workflow-name | lint | test | build | deploy]"
  - command: /github-ci
    description: Scaffold multi-platform matrix CI pipelines with dependency caching
    argument-hint: "[--lang=node|python|go|rust|docker]"
  - command: /github-cd
    description: Implement automated production deployment workflows with concurrency control
    argument-hint: "[--target=cloud|registry]"
---

# GitHub Actions CI/CD Engineering Guide

Modular workflow automation adhering to the **Understand $\rightarrow$ Inspect $\rightarrow$ Plan $\rightarrow$ Execute $\rightarrow$ Validate $\rightarrow$ Report** lifecycle.

## 1. Execution Lifecycle Protocol

```
┌────────────────────────────────────────────────────────┐
│ 1. UNDERSTAND                                          │
│    Identify triggers (push, pull_request, workflow_dispatch),
│    target runtimes, deployment environments, and secrets.
├────────────────────────────────────────────────────────┤
│ 2. INSPECT                                             │
│    Examine .github/workflows/, package locks, linters,  │
│    and run `gh auth status` / `gh workflow list`.      │
├────────────────────────────────────────────────────────┤
│ 3. PLAN                                                │
│    Design DAG dependencies (needs:), concurrency rules, │
│    timeout limits, and least-privilege permissions.    │
├────────────────────────────────────────────────────────┤
│ 4. EXECUTE                                             │
│    Write/update workflow YAMLs with pinned actions,    │
│    automated cache restore/save, and test matrices.    │
├────────────────────────────────────────────────────────┤
│ 5. VALIDATE                                            │
│    Run `python3 scripts/validateWorkflowYaml.py` to     │
│    catch open permissions, missing timeouts, and traps. │
├────────────────────────────────────────────────────────┤
│ 6. REPORT                                              │
│    Summarize jobs, required repository secrets,        │
│    and provide `gh workflow run` dispatch instructions. │
└────────────────────────────────────────────────────────┘
```

---

## 2. Production Workflow Blueprint

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

# 1. Least-Privilege Permissions Standard
permissions:
  contents: read

# 2. Concurrency Cancellation
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}

jobs:
  quality:
    name: Lint & Typecheck
    runs-on: ubuntu-latest
    timeout-minutes: 10 # Mandatory timeout
    steps:
      - name: Checkout Code
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

      - name: Setup Node.js
        uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
        with:
          node-version: 22
          cache: "pnpm"

      - name: Run Linters
        run: |
          pnpm install --frozen-lockfile
          pnpm lint
          pnpm typecheck

  test-matrix:
    name: Test Suite (${{ matrix.os }} - Node ${{ matrix.node }})
    needs: quality
    runs-on: ${{ matrix.os }}
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest]
        node: [20, 22]
    steps:
      - name: Checkout Code
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683

      - name: Setup Runtime
        uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af
        with:
          node-version: ${{ matrix.node }}
          cache: "pnpm"

      - name: Execute Tests
        run: |
          pnpm install --frozen-lockfile
          pnpm test -- --coverage
```

---

## 3. Dual-Mode Execution Commands

### GitHub CLI (`gh`) Operations
```bash
# List all configured workflows
gh workflow list

# Trigger workflow manually with inputs
gh workflow run ci.yml --ref main

# Inspect live execution and logs
gh run list --workflow=ci.yml
gh run watch <run-id>
gh run view <run-id> --log-failed
```

### Direct Validation Tool
```bash
python3 skills/github/githubAction/scripts/validateWorkflowYaml.py --file .github/workflows/ci.yml
```

---

## 4. Anti-Patterns & Security Guardrails
- ❌ **`permissions: write-all`**: Never grant blanket write access. Define `permissions:` explicitly at the top level (`contents: read`) or per-job.
- ❌ **Missing `timeout-minutes`**: Jobs without timeouts can hang indefinitely on stuck network calls, exhausting billing quotas.
- ❌ **Unpinned Actions in Production**: Do not use mutable tags (`@v1`, `@master`) in production security workflows; pin to immutable commit SHAs.
- ❌ **Untrusted `pull_request_target` Triggers**: Never run checkout on untrusted fork PR code with `pull_request_target`, which exposes secrets to third-party code execution.

---

## 5. References & Bundled Utilities
- **Official Starter Workflows & Syntax Specs**: [assets/](assets/) — Bundled official workflows (`node.js.yml`, `python-app.yml`, `go.yml`, `rust.yml`, `codeql.yml`) and workflow syntax specifications.
- Production CI, CD, and Docker build-push templates: [references/workflowPatterns.md](references/workflowPatterns.md)
- Automated workflow security linter: [scripts/validateWorkflowYaml.py](scripts/validateWorkflowYaml.py)
