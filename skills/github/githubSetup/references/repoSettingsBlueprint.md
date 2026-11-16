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
