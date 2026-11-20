# Repository Settings Baseline Blueprint

## Recommended Settings Matrix

| Setting | Recommended Value | Reason |
| :--- | :--- | :--- |
| **Squash Merge** | `true` | Collapses exploratory commits into one clear feature commit on `main`. |
| **Merge Commits** | `false` | Prevents messy non-linear merge bubbles. |
| **Rebase Merge** | `false` | Avoids confusing multi-commit rebases with altered commit hashes. |
| **Delete Head Branches** | `true` | Automatically deletes `feature/*` branches after PR merge to keep repo clean. |
| **Auto-Merge** | `true` | Allows developers to queue PRs to auto-merge once all status checks pass. |
| **Discussions** | Optional | Enable for open-source or RFCs; disable for internal microservices. |
| **Wiki** | `false` | Store documentation directly in Git (`/docs` or `README.md`) rather than isolated Wikis. |

---

## Production Ruleset Architecture & Invariants

Modern GitHub Rulesets replace legacy branch protections. To guarantee compatibility with GitHub's v2 REST API and prevent repository deadlocks, rulesets must respect three mandatory invariants:

### 1. Mandatory Schema Invariants (Preventing HTTP 422)
The GitHub REST API endpoint `POST /repos/:owner/:repo/rulesets` requires all parameters of the `pull_request` rule type to be present and strictly typed. Omitting parameters results in:
```
HTTP 422: Invalid property /rules/3: data matches no possible input.
```

Mandatory parameter payload:
```json
{
  "type": "pull_request",
  "parameters": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews_on_push": true,
    "require_code_owner_review": false,
    "require_last_push_approval": false,
    "required_review_thread_resolution": true
  }
}
```

### 2. Solo Maintainer Lockout Prevention (`bypass_actors`)
On GitHub, **a PR author can never approve their own pull request**. 
If a ruleset enforces `required_approving_review_count: 1` with an empty bypass list (`bypass_actors: []`), a solo developer or repo owner is permanently locked out from merging PRs into the default branch.

**Invariant**: Always grant Admin role bypass to repository maintainers:
```json
"bypass_actors": [
  {
    "actor_id": 5,
    "actor_type": "RepositoryRole",
    "bypass_mode": "always"
  }
]
```
*(In the GitHub API, `actor_type: "RepositoryRole"` with `actor_id: 5` represents the Repository Admin role).*

### 3. Real Status Check Context Mapping (Preventing Phantom Checks)
Status checks configured in `required_status_checks` must exactly match the job IDs and matrix names produced by GitHub Actions in `.github/workflows/`.

| Workflow File (`.github/workflows/*.yml`) | GitHub Actions Job Key | Ruleset `context` String |
| :--- | :--- | :--- |
| `ci.yml` | `jobs.test:` | `test` |
| `ci.yml` | `jobs.build:` | `build` |
| `frontend.yml` | `jobs.frontend-build:` | `frontend-build` |
| `test.yml` (Matrix) | `jobs.matrix (node: 20)` | `matrix (20)` |

> [!WARNING]
> If you specify status check contexts that do not exist (e.g. hardcoded `"quality"`), PR merges will be blocked indefinitely waiting for checks that will never report. If a repository has no CI workflows configured yet, omit the `required_status_checks` rule completely or pass `--checks none`.

---

## Idempotent Deployment Protocol
Ruleset creation should never blindly call `POST`. The script `configureRepoBaseline.py` implements an idempotent check:
1. `GET /repos/:owner/:repo/rulesets` — Query existing rulesets.
2. Match ruleset by `name`.
3. If existing: `PUT /repos/:owner/:repo/rulesets/:id` — Update in-place.
4. If new: `POST /repos/:owner/:repo/rulesets` — Create.
