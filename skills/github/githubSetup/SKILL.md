---
name: githubSetup
description: Audit, initialize, and configure GitHub repositories, modern rulesets, branch protections, and organization foundations. Commands: /github-setup, /github-repository, /github-ruleset.
version: v2
last-verified: 2026-11-17
compatibility: GitHub Enterprise, GitHub Free/Pro, GitHub CLI 2.40+
slash-commands:
  - command: /github-setup
    description: Audit or initialize repository configuration
    argument-hint: "[init | ruleset | branches | settings]"
  - command: /github-repository
    description: Configure repository settings and visibility
    argument-hint: "[--name=<repo>] [--visibility=public|private]"
  - command: /github-ruleset
    description: Create and enforce modern repository rulesets
    argument-hint: "[--target=branch|tag] [--enforce=active|evaluate]"
---

# GitHub Setup & Repository Architecture Guide

Configure enterprise-grade repository foundations adhering to the **Understand $\rightarrow$ Inspect $\rightarrow$ Plan $\rightarrow$ Execute $\rightarrow$ Validate $\rightarrow$ Report** lifecycle.

## 1. Execution Lifecycle Protocol

```
┌────────────────────────────────────────────────────────┐
│ 1. UNDERSTAND                                          │
│    Determine visibility (public/private), compliance,  │
│    target branch model (Trunk-based), and admin roles. │
├────────────────────────────────────────────────────────┤
│ 2. INSPECT                                             │
│    Run `gh repo view --json isPrivate,defaultBranchRef`│
│    and `gh ruleset list` to detect existing safeguards.│
├────────────────────────────────────────────────────────┤
│ 3. PLAN                                                │
│    Draft Ruleset JSON: require PR review, passing CI   │
│    checks, linear history, and squash-merge defaults.  │
├────────────────────────────────────────────────────────┤
│ 4. EXECUTE                                             │
│    Apply configuration via `gh api` or the bundled      │
│    script `python3 scripts/configureRepoBaseline.py`.   │
├────────────────────────────────────────────────────────┤
│ 5. VALIDATE                                            │
│    Verify ruleset active status and test branch push   │
│    rejection on simulated unprotected direct commits.  │
├────────────────────────────────────────────────────────┤
│ 6. REPORT                                              │
│    Output repository baseline status and active rules. │
└────────────────────────────────────────────────────────┘
```

---

## 2. Production Ruleset Standard (Replacing Legacy Branch Protection)

GitHub Rulesets provide granular, multi-branch governance with bypass lists and status check assertions:

```json
{
  "name": "Production Protected Default",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["~DEFAULT_BRANCH"],
      "exclude": []
    }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "required_linear_history" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 1,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true,
        "require_last_push_approval": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [
          { "context": "quality" },
          { "context": "test-matrix" }
        ]
      }
    }
  ]
}
```

---

## 3. Dual-Mode Execution Commands

### GitHub CLI (`gh`) Operations
```bash
# 1. Initialize or view repository
gh repo view :owner/:repo

# 2. Configure repository baseline flags
gh repo edit :owner/:repo \
  --enable-squash-merge=true \
  --enable-merge-commit=false \
  --enable-rebase-merge=false \
  --delete-branch-on-merge=true \
  --enable-auto-merge=true

# 3. Create or inspect rulesets via API
gh api -X POST /repos/:owner/:repo/rulesets \
  --input skills/github/githubSetup/references/rulesetTemplates.json
```

### Direct Automation Tool
```bash
python3 skills/github/githubSetup/scripts/configureRepoBaseline.py --repo owner/repo
```

---

## 4. Anti-Patterns & Pitfalls
- ❌ **Legacy Branch Protection for New Repos**: Avoid configuring deprecated legacy branch protection APIs; use modern **GitHub Rulesets** which support import/export and bypass controls.
- ❌ **Multiple Merge Types**: Avoid enabling both Merge Commit, Rebase, and Squash simultaneously; standardize on **Squash Merging** to maintain clean linear commit histories.
- ❌ **Retaining Merged Head Branches**: Leaving merged branches undeleted bloats git references; always enable `--delete-branch-on-merge=true`.
- ❌ **Zero Status Checks in PR Gate**: Requiring PR reviews without requiring CI status checks allows broken builds into main.

---

## 5. References & Bundled Utilities
- **Official Offline Documentation Assets**: [assets/](assets/) — Comprehensive offline guides for repository creation, settings, branch management, rulesets, and REST endpoints.
- Ruleset template JSON: [references/rulesetTemplates.json](references/rulesetTemplates.json)
- Repository settings blueprint: [references/repoSettingsBlueprint.md](references/repoSettingsBlueprint.md)
- Automated configuration script: [scripts/configureRepoBaseline.py](scripts/configureRepoBaseline.py)
