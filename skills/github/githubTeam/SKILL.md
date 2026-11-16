---
name: githubTeam
description: Design and manage professional engineering team structures, permission hierarchies, onboarding checklists, and automated code review routing. Commands: /github-team, /github-team-onboarding, /github-team-roles.
argument-hint: "[structure | onboarding | roles | permissions]"
commands:
  - /github-team
  - /github-team-onboarding
  - /github-team-roles
version: v2
last-verified: 2026-11-16
compatibility: GitHub Organizations, GitHub Enterprise, GitHub CLI 2.40+
---

# GitHub Team Architecture & Permission Engineering Guide

Structure scalable engineering organizations adhering to the **Understand $\rightarrow$ Inspect $\rightarrow$ Plan $\rightarrow$ Execute $\rightarrow$ Validate $\rightarrow$ Report** lifecycle.

## 1. Execution Lifecycle Protocol

```
┌────────────────────────────────────────────────────────┐
│ 1. UNDERSTAND                                          │
│    Determine department boundaries, security tiers,    │
│    onboarding flows, and code review policies.         │
├────────────────────────────────────────────────────────┤
│ 2. INSPECT                                             │
│    Run `gh api /orgs/:org/teams` and check direct user │
│    collaborators with `gh api /repos/:owner/:repo/collaborators`.
├────────────────────────────────────────────────────────┤
│ 3. PLAN                                                │
│    Design nested team tree (Engineering -> Backend),   │
│    map permission tiers (Triage, Write, Maintain).     │
├────────────────────────────────────────────────────────┤
│ 4. EXECUTE                                             │
│    Create teams via `gh api`, assign repository access,│
│    and configure automated round-robin review routing. │
├────────────────────────────────────────────────────────┤
│ 5. VALIDATE                                            │
│    Assert zero direct user collaborators (all access   │
│    granted via teams) and test code review auto-ping.  │
├────────────────────────────────────────────────────────┤
│ 6. REPORT                                              │
│    Render organization team hierarchy and permission   │
│    scorecard.                                          │
└────────────────────────────────────────────────────────┘
```

---

## 2. Team Hierarchy & Permission Tier Architecture

Always organize teams hierarchically. Members of child teams automatically inherit parent team memberships:

```
@org/engineering (Parent Team - Read access to all org repos)
├── @org/frontend (Write access to web apps, UI libraries)
├── @org/backend (Write access to API microservices, databases)
├── @org/platform-sre (Maintain access to infrastructure, K8s, CI/CD)
└── @org/security (Admin access to security policies & secret scanning)
```

### GitHub Repository Permission Matrix
| Role | Recommended For | Capabilities |
| :--- | :--- | :--- |
| **Read** | General employees, cross-functional partners | Clone, view, open issues/PRs. |
| **Triage** | Product managers, QA, contractors | Manage issues and PR labels without write access. |
| **Write** | Core contributing engineers | Push to feature branches, create releases. |
| **Maintain** | Tech leads, engineering managers | Manage repo settings, webhooks, non-destructive actions. |
| **Admin** | Security leads, organization owners | Manage sensitive repo secrets, rulesets, deletion. |

---

## 3. Dual-Mode Execution Commands

### GitHub CLI (`gh`) Operations
```bash
# 1. Create a child team in an organization
gh api -X POST /orgs/:org/teams \
  -f name="Backend Team" \
  -f privacy="closed" \
  -f parent_team_id="<parent-id>"

# 2. Assign team permission to a repository
gh api -X PUT /orgs/:org/teams/:team_slug/repos/:owner/:repo \
  -f permission="push" # 'push' = Write, 'maintain' = Maintain

# 3. Add a member to a team
gh api -X PUT /orgs/:org/teams/:team_slug/memberships/:username \
  -f role="member"
```

### Direct Team Synchronization Tool
```bash
python3 skills/github/githubTeam/scripts/manageTeamSync.py --org my-org
```

---

## 4. Anti-Patterns & Traps
- ❌ **Direct User Collaborators**: Never grant individual user accounts direct access to repositories. Always grant repository permissions to **Teams** to avoid orphaned permissions when employees depart.
- ❌ **Excessive Admin Permissions**: Granting `Admin` to entire engineering teams bypasses branch protections and exposes repo deletion risk. Restrict engineers to `Write` and tech leads to `Maintain`.
- ❌ **Manual Reviewer Assigning**: Avoid requiring developers to manually pick reviewers; configure automated **Round-Robin** code review assignments on team settings.

---

## 5. References & Bundled Utilities
- Permission tier specifications: [references/permissionMatrix.md](references/permissionMatrix.md)
- Automated round-robin reviewer configuration: [references/reviewAssignment.md](references/reviewAssignment.md)
- Team sync script: [scripts/manageTeamSync.py](scripts/manageTeamSync.py)
