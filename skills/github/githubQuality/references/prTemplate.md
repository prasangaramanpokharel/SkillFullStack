# Enterprise Pull Request Template Reference

```markdown
## Overview
<!-- Concise context: What does this PR change and why? -->

Fixes / Closes #(issue_number)

## Architecture & Design Notes
<!-- Describe trade-offs, alternative approaches considered, or state diagrams -->

## Impact Analysis
- [ ] Breaking API change (requires semver major bump)
- [ ] Database schema migration required
- [ ] New environment variables required (documented in README.md)

## Verification & Testing
- Unit tests added: `npm test` or `pytest` passes
- End-to-end flow verified locally or in preview deployment
```
