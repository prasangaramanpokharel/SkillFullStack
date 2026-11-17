# GitHub Security Documentation Assets

Official offline specifications from GitHub Docs (`https://docs.github.com/en/code-security`) covering CodeQL, Dependabot, Secret Scanning, and Security Advisories.

## Directory Structure

```
assets/
├── code-scanning/               # CodeQL & Static Analysis
│   ├── code-scanning.md         # Overview & architecture
│   ├── codeql-code-scanning.md  # CodeQL engine & language matrix
│   ├── code-scanning-alerts.md  # Triage, suppression, and autofix
│   └── configure-code-scanning.md # Default vs advanced setup
│
├── dependabot/                  # Dependency & Supply Chain Security
│   ├── about-the-dependabot-yml-file.md # dependabot.yml configuration reference
│   ├── dependabot-version-updates.md    # Automated dependency bumping
│   ├── dependabot-security-updates.md   # Automated CVE patching
│   └── dependabot-alerts.md             # Security alerts and advisory linkage
│
├── secret-scanning/             # Secret Leaks & Push Protection
│   ├── secret-scanning.md       # Partner patterns and high-confidence tokens
│   └── enable-secret-scanning.md # Push protection enforcement rules
│
├── security-advisories/         # CVEs & Private Vulnerability Reporting
│   └── github-advisory-database.md
│
└── rest-api/                    # REST Endpoints for Security Automation
    ├── code-scanning.md
    ├── secret-scanning.md
    └── dependabot-alerts.md
```
