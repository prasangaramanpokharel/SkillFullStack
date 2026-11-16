---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}}
compatibility: {{COMPATIBILITY}}
version: {{VERSION}}
last-verified: {{VERIFIED_DATE}}
---

# {{SKILL_TITLE}}

## Critical Mental Models & Best Practices
- Focus on the latest stable patterns and idioms (verified against current official documentation).
- Avoid bloat: rely on concise, high-leverage guidance and battle-tested defaults.

## Workflow & Step-by-Step Implementation
1. **Analyze Requirements**: Validate inputs, constraints, and target runtime.
2. **Execute via Scripts**: Use deterministic helper scripts in `scripts/` where appropriate.
3. **Reference Deep Specs**: Consult `references/` for full schemas, API signatures, or anti-patterns.

## Anti-Patterns & Common Traps
- ❌ **Avoid**: Legacy idioms, outdated package versions, or deprecated APIs.
- ❌ **Avoid**: Bloating prompts with full documentation text that belongs in `references/`.
- ✅ **Prefer**: Modern, canonical syntax, strict type safety, and direct, verifiable code.

## References & Utilities
- Refer to [references/documentation.md](references/documentation.md) for deep dives.
- Execute tools in [scripts/](scripts/) for repeatable workflows.
