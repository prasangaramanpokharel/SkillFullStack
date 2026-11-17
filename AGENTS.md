# AGENTS.md — AI Agent Guidance & Execution Protocol

> This file defines the mandatory operational protocol for all AI coding agents (Claude Code, Cursor, Antigravity, OpenAI Codex, Gemini CLI, etc.) working inside or consuming skills from the **SkillFullStack** repository.

---

## 1. High-Accuracy Offline Documentation Protocol (`assets/`)

### ⚡ Rule 1: Always Prioritize Local Bundled Documentation
When working with any framework, library, or engineering domain covered by a skill:
1. **Check for Bundled Assets First**: Check if the skill contains an `assets/` directory:
   - Next.js App Router: [`skills/frontend/nextjs/assets/`](skills/frontend/nextjs/assets/)
   - Astro 5.x: [`skills/frontend/astro/assets/`](skills/frontend/astro/assets/)
   - shadcn/ui: [`skills/frontend/shadcn-ui/assets/`](skills/frontend/shadcn-ui/assets/)
   - GitHub Platform & Actions:
     - Shared REST API: [`skills/github/assets/rest-api/`](skills/github/assets/rest-api/)
     - Setup & Rulesets: [`skills/github/githubSetup/assets/`](skills/github/githubSetup/assets/)
     - Actions & Starter Workflows: [`skills/github/githubAction/assets/`](skills/github/githubAction/assets/)
     - Security (CodeQL, Dependabot, Push Protection): [`skills/github/githubSecurity/assets/`](skills/github/githubSecurity/assets/)
     - Quality (PRs, Reviews, CODEOWNERS): [`skills/github/githubQuality/assets/`](skills/github/githubQuality/assets/)
     - Teams & Organizations: [`skills/github/githubTeam/assets/`](skills/github/githubTeam/assets/)
   - Git Version Control & CLI:
     - Git Remote Workflows & `gh` CLI: [`skills/gitVersionControl/gitWorkflow/assets/`](skills/gitVersionControl/gitWorkflow/assets/)
2. **Zero-Hallucination Mandate**:
   - **Do NOT rely on pre-training weights** or outdated training data when local documentation exists. Framework APIs change rapidly (e.g., Next.js 16 `"use cache"`, React 19 Action states, Tailwind CSS v4 CSS-first theming, shadcn CLI v4).
   - Read the exact markdown specification in `assets/` before generating boilerplate, components, or configuration.
   - Using bundled documentation guarantees **100% accuracy**, exact parameter compatibility, and zero deprecation warnings.

---

## 2. Standard Format for Skill Documentation Assets

When authoring, augmenting, or upgrading skills with official documentation, agents **MUST** format the `assets/` folder to mirror the official framework documentation sidebar:

```
skills/<taxonomy>/<skillName>/assets/
├── README.md                    # Catalog index detailing the sidebar layout
├── getting-started/ (or overview/)  # Sequential tutorials and quickstarts
├── api-reference/ (or components/)  # Technical reference for each API, directive, or primitive
│   ├── directives/              # e.g., use client, use server, use cache
│   ├── components/              # e.g., Image, Link, Form, Button, Dialog
│   ├── file-conventions/        # e.g., layout.md, page.md, loading.md
│   └── functions/               # e.g., cookies, headers, redirect, notFound
├── architecture/ (or advanced/) # Deep internal runtime mechanics and compiler specs
├── community/                   # Ecosystem guides, migrations, and plugins
└── glossary.md                  # Terminology definitions and concepts
```

### Conventions for Documentation Files
1. **File Extension**: Must strictly be standard Markdown (`.md`).
2. **File Naming**: Lowercase kebab-case (e.g., `project-structure.md`, `components-json.md`). Use `index.md` for folder index pages (never uppercase `Index.md`).
3. **Completeness**: Never save partial stubs or placeholders. Fetch the full, un-truncated markdown content from the vendor's raw markdown endpoint (e.g. `https://nextjs.org/docs/app/{path}.md` or `https://ui.shadcn.com/docs/{path}.md`).
4. **Index Catalog**: Always maintain an `assets/README.md` that acts as the navigation sitemap for other agents.

---

## 3. Skill Architecture & Frontmatter Standards

Every skill in `skills/<taxonomy>/<skillName>/` must strictly conform to the open Agent Skills standard:

1. **`SKILL.md` (Required)**:
   - Must contain YAML frontmatter:
     ```yaml
     ---
     name: <skillName>
     description: <High-density description of capabilities and scope>
     version: <e.g., v4, 16.x>
     last-verified: YYYY-MM-DD
     compatibility: <Supported frameworks, runtimes, and languages>
     slash-commands:
       - command: /<skillName>-action
         description: <Concise explanation of the command>
         argument-hint: "[--flag=value]"
     ---
     ```
2. **`references/`**: High-density engineering guides, deep production checklists, security headers, and implementation architectural plans.
3. **`evals/evals.json`**: Deterministic test and evaluation suites with concrete prompt scenarios and assert criteria.
4. **`scripts/`**: Automation tools and deterministic scanners for the skill.

---

## 4. Code Generation Rules for Agents

When implementing code using skills from this repository:
- **Strict Typing**: TypeScript 5+ in strict mode. No `any` without explicit justification.
- **Modern Standards**: React 19, Next.js 16, Tailwind CSS v4, Go 1.23+, Python 3.12+.
- **Security Boundaries**: Enforce `server-only`, Data Access Layer (DAL) patterns, and React Taint APIs for server-side code.
- **Verification**: Always run linting, type-checking, and tests before claiming completion.
