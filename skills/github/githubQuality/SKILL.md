---
name: githubQuality
description: Enforce engineering quality, pull request standards, structured code reviews, and CODEOWNERS rules. Commands: /github-quality, /github-pr, /github-codeowners.
argument-hint: "[pr-template | codeowners | review-checklist | contributing]"
commands:
  - /github-quality
  - /github-pr
  - /github-codeowners
version: v2
last-verified: 2026-11-16
compatibility: GitHub CLI 2.40+, Markdown, Git
---

# GitHub Code Quality & Pull Request Engineering Guide

Enforce high engineering velocity and code ownership adhering to the **Understand $\rightarrow$ Inspect $\rightarrow$ Plan $\rightarrow$ Execute $\rightarrow$ Validate $\rightarrow$ Report** lifecycle.

## 1. Execution Lifecycle Protocol

```
┌────────────────────────────────────────────────────────┐
│ 1. UNDERSTAND                                          │
│    Identify critical system boundaries (auth, infra),  │
│    team handles, and commit style (Conventional Commits).
├────────────────────────────────────────────────────────┤
│ 2. INSPECT                                             │
│    Inspect `.github/CODEOWNERS`, PR templates, and run │
│    `gh pr list --state open` to audit active reviews.  │
├────────────────────────────────────────────────────────┤
│ 3. PLAN                                                │
│    Map directories to team handles, formulate PR gate  │
│    checklists (testing, security, migration notes).    │
├────────────────────────────────────────────────────────┤
│ 4. EXECUTE                                             │
│    Deploy `.github/CODEOWNERS`, `.github/PULL_REQUEST_TEMPLATE.md`
│    and PR review guidelines.                           │
├────────────────────────────────────────────────────────┤
│ 5. VALIDATE                                            │
│    Run `python3 scripts/auditPrQuality.py --pr <id>` to│
│    check conventional commit title, issue links, and tests.
├────────────────────────────────────────────────────────┤
│ 6. REPORT                                              │
│    Summarize code coverage rules, reviewer rosters, and│
│    ownership boundaries.                               │
└────────────────────────────────────────────────────────┘
```

---

## 2. Production `CODEOWNERS` Standard (`.github/CODEOWNERS`)

Order matters: rules later in the file take precedence over earlier matching rules:

```text
# Default catch-all owners
* @org/engineering-core

# Infrastructure & CI/CD
/.github/workflows/ @org/platform-devops
/terraform/ @org/platform-devops
/docker/ @org/platform-devops

# Security-critical modules
/src/auth/ @org/security-reviewers
/src/crypto/ @org/security-reviewers
/secrets/ @org/security-reviewers

# Database migrations
/prisma/migrations/ @org/db-admins
/migrations/ @org/db-admins
```

---

## 3. Pull Request Template (`.github/PULL_REQUEST_TEMPLATE.md`)

```markdown
## Description
<!-- Provide a concise summary of the changes and motivation -->

Closes #(issue)

## Type of Change
- [ ] 🚀 Feature (`feat:`)
- [ ] 🐛 Bug fix (`fix:`)
- [ ] 🧹 Refactoring (`refactor:`)
- [ ] ⚡ Performance improvement (`perf:`)
- [ ] 🔒 Security fix

## Quality & Safety Checklist
- [ ] My code follows the project's style standards and passes all linters.
- [ ] I have added automated unit/integration tests covering these changes.
- [ ] Database migrations (if any) are backward-compatible.
- [ ] No private keys, secrets, or sensitive logs are committed.
```

---

## 4. Dual-Mode Execution Commands

### GitHub CLI (`gh`) Operations
```bash
# Create compliant PR with conventional commit title
gh pr create \
  --title "feat(auth): implement session token rotation" \
  --body-file .github/PULL_REQUEST_TEMPLATE.md \
  --reviewer org/security-reviewers

# Review and approve with structured feedback
gh pr review <pr-number> --approve --body "LGTM. Verified backward compatibility of token rotation."
```

### Direct PR Quality Audit Tool
```bash
python3 skills/github/githubQuality/scripts/auditPrQuality.py --pr 42
```

---

## 5. Anti-Patterns & Traps
- ❌ **Single-Person Catch-All CODEOWNERS**: Setting `* @solo-developer` creates a bottleneck where one person must approve every documentation typo. Use team handles (`@org/frontend`).
- ❌ **Unfilled PR Checklists**: Merging pull requests with raw uncompleted checklist brackets `[ ]`.
- ❌ **Vague PR Titles**: Writing titles like `"updates"` or `"fix stuff"` breaking automated semantic versioning and changelogs. Always require conventional commit formats (`type(scope): subject`).

---

## 6. References & Bundled Utilities
- Production PR template: [references/prTemplate.md](references/prTemplate.md)
- Multi-team CODEOWNERS patterns: [references/codeownersExample.md](references/codeownersExample.md)
- PR quality validation script: [scripts/auditPrQuality.py](scripts/auditPrQuality.py)
