# GitHub Team Permission Matrix Reference

## 1. Permission Levels Breakdown

| Permission Name | API Value | Recommended Use |
| :--- | :--- | :--- |
| **Pull** | `pull` | Read-only. Base permission for all org members. |
| **Triage** | `triage` | QA engineers, product owners, triage bots. |
| **Push** | `push` | Standard development engineers. Can push to non-protected branches and open PRs. |
| **Maintain** | `maintain` | Engineering leads. Can lock discussions, manage issue templates and labels. |
| **Admin** | `admin` | DevOps leads and security administrators. Can configure Rulesets and repository secrets. |

## 2. Onboarding Workflow Checklist
1. Add user to GitHub Organization as Member.
2. Require multi-factor authentication (MFA) check.
3. Add user to primary discipline team (`@org/backend` or `@org/frontend`).
4. Ensure user is enrolled in automated round-robin review pools.
