# CODEOWNERS Patterns & Precedence Reference

## 1. Syntax Rules
- Comments start with `#`.
- Paths starting with `/` match relative to repository root.
- A wildcard `*` matches all files.
- Last matching rule wins.

## 2. Multi-Domain Architecture Example
```text
# Global catch-all
* @org/maintainers

# Frontend application
/apps/web/ @org/frontend-leads
/packages/ui/ @org/design-system

# Backend services
/apps/api/ @org/backend-leads
/proto/ @org/backend-leads @org/mobile-leads

# Cloud Infrastructure
/.github/ @org/devops-infra
/infra/ @org/devops-infra
/k8s/ @org/devops-infra
```
