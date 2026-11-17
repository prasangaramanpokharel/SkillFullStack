# GitHub Engineering Quality Documentation Assets

Official offline specifications from GitHub Docs (`https://docs.github.com/en/pull-requests`) covering PR workflows, CODEOWNERS, merge methods, and status checks.

## Directory Structure

```
assets/
├── pull-requests/               # Pull Request Engineering Standards
│   ├── creating-a-pull-request.md # Scaffolding & PR templates
│   ├── merging-a-pull-request.md  # Merge strategies (Squash, Rebase, Merge)
│   ├── giving-reviews.md          # Review guidelines and inline comments
│   ├── resolving-reviews.md       # Conversation threads and sign-offs
│   ├── about-merge-methods.md     # Fast-forward, rebase, and linear DAG
│   ├── managing-a-merge-queue.md  # Merge queues for high-velocity teams
│   ├── about-code-owners.md       # CODEOWNERS syntax and review routing
│   └── status-checks.md           # Required status checks & branch protection
│
└── rest-api/                    # REST Endpoints for PRs & Status Checks
    ├── pulls.md
    ├── reviews.md
    ├── checks-runs.md
    └── checks-suites.md
```
