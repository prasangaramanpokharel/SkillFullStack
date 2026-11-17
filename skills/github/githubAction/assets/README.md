# GitHub Actions Documentation Assets & Starter Workflows

Official offline starter workflows from `actions/starter-workflows` (`https://github.com/actions/starter-workflows`) and specification references from GitHub Docs (`https://docs.github.com/en/actions`).

## Directory Structure

```
assets/
├── starter-workflows/           # Official Production Starter Workflows
│   ├── ci/
│   │   ├── node.js.yml          # Node.js CI matrix build
│   │   ├── python-app.yml       # Python lint & pytest
│   │   ├── go.yml               # Go test & build
│   │   ├── rust.yml             # Rust cargo test & clippy
│   │   ├── docker-image.yml     # Docker build & push
│   │   ├── maven.yml            # Java Maven pipeline
│   │   └── blank.yml            # Minimal starter workflow
│   ├── code-scanning/
│   │   └── codeql.yml           # Official CodeQL static analysis matrix
│   └── automation/
│       └── stale.yml            # Automated issue & PR stale triage
│
├── reference/                   # Workflow Syntax & Mechanics
│   ├── workflow-syntax.md       # Complete .github/workflows YAML syntax
│   ├── events-that-trigger-workflows.md # push, pull_request, schedule, workflow_dispatch
│   ├── dependency-caching.md    # actions/cache & native package manager caching
│   ├── metadata-syntax.md       # action.yml definition specification
│   ├── variables.md             # Environment variables & vars context
│   ├── workflow-commands.md     # ::set-output, ::error, ::warning syntax
│   ├── workflow-cancellation.md # Concurrency groups & auto-cancelation
│   ├── contexts.md              # github, env, job, steps, runner contexts
│   └── expressions.md           # Conditionals, functions, and string filters
│
└── rest-api/                    # REST Endpoints for Actions
    ├── workflows.md
    ├── workflow-runs.md
    └── secrets.md
```
