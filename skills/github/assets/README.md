# GitHub Documentation Assets, REST API & CLI Reference

Official offline documentation specifications from GitHub Docs (`https://docs.github.com/en/rest`), GitHub Docs API, and the GitHub CLI (`gh`).

## Directory Structure

```
skills/github/assets/
├── rest-api/                    # Core GitHub REST API Reference Specifications
│   ├── overview.md              # REST API Architecture & Root Endpoint
│   ├── quickstart.md            # Quickstart for GitHub REST API
│   ├── authenticating.md        # Authentication, OAuth, and Personal Access Tokens
│   ├── using-the-rest-api.md    # Headers, pagination, media types, rate limits
│   ├── repos.md                 # Repositories API (create, edit, delete, transfer)
│   ├── branches.md              # Branches & Branch Protection Rules API
│   ├── rules.md                 # Modern Rulesets API
│   ├── pulls.md                 # Pull Requests API
│   ├── pull-reviews.md          # Pull Request Reviews & Comments API
│   ├── actions-workflows.md     # Actions Workflows API
│   ├── actions-workflow-runs.md # Workflow Runs & Triggering API
│   ├── actions-secrets.md       # Actions Secrets & Variables API
│   ├── code-scanning.md         # CodeQL & SARIF Uploads API
│   ├── secret-scanning.md       # Secret Scanning Alerts API
│   ├── dependabot-alerts.md     # Dependabot Security & Version Alerts API
│   ├── teams.md                 # Teams & Permissions API
│   ├── orgs.md                  # Organizations & Members API
│   ├── collaborators.md         # Repository Collaborators API
│   ├── commits.md               # Git Commits & Status API
│   ├── checks-runs.md           # Checks & Check Suites API
│   └── releases.md              # GitHub Releases & Assets API
│
├── cli/                         # Official GitHub CLI (gh) Reference Manual
│   ├── gh-reference.md          # Complete reference manual (all gh commands & flags)
│   ├── gh-environment.md        # GH_TOKEN, GH_HOST, GH_DEBUG environment variables
│   └── gh-formatting.md         # JSON templating and jq output options
│
└── docs-api/                    # GitHub Docs Programmatic API
    └── github-docs-api.md       # /api/article/body, /api/pagelist, and /llms.txt
```
