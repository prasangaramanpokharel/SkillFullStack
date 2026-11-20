---
name: githubSetup
description: Audit, initialize, and configure GitHub repositories, modern rulesets, branch protections, and organization foundations. Commands: /github-setup, /github-repository, /github-ruleset.
version: v2
last-verified: 2026-11-20
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
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [
          { "context": "test" },
          { "context": "build" }
        ]
      }
    }
  ],
  "bypass_actors": [
    {
      "actor_id": 5,
      "actor_type": "RepositoryRole",
      "bypass_mode": "always"
    }
  ]
}
```

### 2.1 Critical Ruleset Invariants

1. **Schema Validation & HTTP 422 Prevention**:
   The `pull_request` rule mandates `required_review_thread_resolution` (boolean). If omitted, GitHub's API returns `HTTP 422: Invalid property /rules/3: data matches no possible input.` Always supply all five core parameters.
2. **Solo Maintainer Lockout Prevention**:
   On GitHub, a PR author cannot approve their own pull request. Setting `"bypass_actors": []` with required reviews permanently deadlocks single-maintainer or personal repos. Always include repository Admin bypass (`actor_id: 5`, `actor_type: "RepositoryRole"`, `bypass_mode: "always"`).
3. **Preventing Phantom Status Checks**:
   Check context strings must strictly correspond to actual jobs in `.github/workflows/` (e.g. `frontend-build`, `test-matrix`). If an arbitrary non-existent check like `"quality"` is enforced, PRs will be indefinitely blocked waiting for checks that never run. Omit `required_status_checks` until corresponding CI workflows are actively present.

---

## 3. Dual-Mode Execution Commands

### GitHub CLI (`gh`) Operations

```bash
# 1. Initialize or view repository
gh repo view :owner/:repo

# 2. Configure repository baseline flags (squash merge only, auto-delete head branches)
gh repo edit :owner/:repo \
  --enable-squash-merge=true \
  --enable-merge-commit=false \
  --enable-rebase-merge=false \
  --delete-branch-on-merge=true \
  --enable-auto-merge=true

# 3. Query existing rulesets to maintain idempotency
gh api /repos/:owner/:repo/rulesets

# 4. Create new ruleset (POST) or update existing ruleset in-place (PUT)
# Create:
gh api -X POST /repos/:owner/:repo/rulesets \
  --input skills/github/githubSetup/references/rulesetTemplates.json

# Update existing (replace :id with ruleset ID from query):
gh api -X PUT /repos/:owner/:repo/rulesets/:id \
  --input skills/github/githubSetup/references/rulesetTemplates.json
```

### Direct Automation Tool

The bundled `configureRepoBaseline.py` automates repository settings, auto-detects local workflow jobs, prevents solo maintainer lockouts, and performs idempotent `PUT`/`POST` updates with detailed error diagnostics:

```bash
# 1. Idempotently configure repository flags and ruleset with auto-detected CI jobs
python3 skills/github/githubSetup/scripts/configureRepoBaseline.py \
  --repo owner/repo \
  --auto-detect-checks

# 2. Enforce specific status checks explicitly
python3 skills/github/githubSetup/scripts/configureRepoBaseline.py \
  --repo owner/repo \
  --checks "frontend-build,test-matrix"

# 3. Configure baseline without status checks (safe for repos without CI yet)
python3 skills/github/githubSetup/scripts/configureRepoBaseline.py \
  --repo owner/repo \
  --checks none

# 4. Dry-run inspection without calling GitHub API
python3 skills/github/githubSetup/scripts/configureRepoBaseline.py \
  --repo owner/repo \
  --dry-run
```

---

## 4. Anti-Patterns & Pitfalls

- ❌ **Schema 422 Invalid Property**: Omitting `required_review_thread_resolution: true` in the `pull_request` rule causes the GitHub v2 API to reject the entire payload with HTTP 422.
- ❌ **Solo Maintainer Lockout (`bypass_actors: []`)**: Requiring PR reviews with no bypass actors on a personal or small-team repo locks the owner out since authors cannot approve their own PRs. Always include Admin bypass (`actor_id: 5, actor_type: "RepositoryRole"`).
- ❌ **Hardcoded Phantom Status Checks**: Requiring checks like `"quality"` or `"test"` when workflows name their jobs differently stalls PR merges indefinitely. Always map contexts to actual workflow job IDs.
- ❌ **Non-Idempotent Ruleset Creation**: Calling `POST /repos/:owner/:repo/rulesets` blindly duplicates rulesets or causes collision errors. Always inspect existing rulesets first and use `PUT` when updating.
- ❌ **Legacy Branch Protection for New Repos**: Avoid deprecated branch protection APIs; use modern **GitHub Rulesets** which support import/export, evaluate modes, and bypass controls.
- ❌ **Multiple Merge Types**: Avoid enabling Merge Commit, Rebase, and Squash simultaneously; standardize on **Squash Merging** to maintain clean linear commit histories.
- ❌ **Retaining Merged Head Branches**: Leaving merged branches undeleted bloats git references; always enable `--delete-branch-on-merge=true`.

---

## 5. References & Bundled Utilities

- **Official Offline Documentation Assets**: [assets/](assets/) — Comprehensive offline guides for repository creation, settings, branch management, rulesets, and REST endpoints.
- Ruleset template JSON: [references/rulesetTemplates.json](references/rulesetTemplates.json)
- Repository settings blueprint: [references/repoSettingsBlueprint.md](references/repoSettingsBlueprint.md)
- Automated configuration script: [scripts/configureRepoBaseline.py](scripts/configureRepoBaseline.py)
