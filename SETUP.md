# Multi-Agent Setup & Slash Commands Guide (`SETUP.md`)

This guide explains how to install, configure, and invoke skills from **SkillFullStack** across major AI development assistants including **Google Antigravity**, **Claude Code**, **Cursor**, **Windsurf**, and **Universal AI Agents**.

---

## Quick Reference: Skill Directories & Slash Command Support

| AI Environment | Recommended Skill Path | Slash Command / Rule Mechanism | Native Auto-Complete |
| :--- | :--- | :--- | :---: |
| **Google Antigravity / Gemini** | `.gemini/antigravity/skills/<name>/SKILL.md`<br>*(or `.agent/skills/<name>/`)* | Reads `SKILL.md` frontmatter & registered triggers | Native (`/<command>`) |
| **Claude Code** | `.claude/skills/<name>/SKILL.md`<br>*(and `.claude/commands/<command>.md`)* | Custom commands in `.claude/commands/` | Native (`/<command>`) |
| **Cursor** | `.cursor/skills/<name>/SKILL.md`<br>*(and `.cursor/rules/<name>.mdc`)* | Auto-trigger rules & `@skills/<name>` | Via `@`, Rules, or Prompt |
| **OpenCode / OpenAI Codex** | `.opencode/skills/<name>/SKILL.md`<br>*(or `.agent/skills/<name>/`)* | Agent capability loading | Via Prompt / Slash Command |
| **Windsurf (Cascade)** | `.windsurf/skills/<name>/SKILL.md`<br>*(and `.windsurf/rules/<name>.md`)* | System prompt rules & `@mention` | Via `@` or Rules |
| **GitHub Copilot** | `.github/skills/<name>/SKILL.md` | Workspace instructions | Via Prompt / Reference |
| **Universal Agent Standard** | `.agent/skills/<name>/SKILL.md` | Open `agentskills.io` standard | Universal |

---

## 1. Google Antigravity Setup

Google Antigravity natively discovers Agent Skills conforming to the open `SKILL.md` specification and maps declared slash commands directly into the chat UI auto-complete menu.

### Project-Level Installation (Current Workspace)
Install skills directly inside your project repository so any collaborator using Antigravity automatically shares them:

```bash
# Example: Install Database Architecture skill
mkdir -p .gemini/antigravity/skills/databaseArchitecture
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/databaseArchitecture/SKILL.md \
  -o .gemini/antigravity/skills/databaseArchitecture/SKILL.md

# Example: Install Production API Engineering skill
mkdir -p .gemini/antigravity/skills/apiEngineering
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/apiEngineering/SKILL.md \
  -o .gemini/antigravity/skills/apiEngineering/SKILL.md
```

### Global Installation (Available Across All Workspaces)
To make skills available in every project on your machine:
```bash
mkdir -p ~/.gemini/antigravity/skills/databaseArchitecture
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/databaseArchitecture/SKILL.md \
  -o ~/.gemini/antigravity/skills/databaseArchitecture/SKILL.md
```

### How Slash Commands Work in Antigravity:
Type `/` in the Antigravity chat prompt. The declared slash commands will immediately appear in the auto-complete popup:
- `/db-architecture` or `/db-design`: Launches schema design and normal form auditing.
- `/api-engineering` or `/api-design`: Launches contract-first OpenAPI 3.2.1 and RFC 9457 design.
- `/tdd-cycle`: Enforces Red-Green-Refactor test cycle.
- `/git-workflow`: Guides DAG rebasing and conflict resolution.

---

## 2. Claude Code Setup

Claude Code supports custom slash commands and skills defined in `.claude/commands/` or `.claude/skills/`.

### Method A: Single Command Setup (`.claude/commands/`)
Claude Code automatically converts any markdown file inside `.claude/commands/` into a native slash command:

```bash
# Create the commands directory
mkdir -p .claude/commands

# Install /api-engineering command
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/apiEngineering/SKILL.md \
  -o .claude/commands/api-engineering.md

# Install /db-architecture command
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/databaseArchitecture/SKILL.md \
  -o .claude/commands/db-architecture.md

# Install /tdd-cycle command
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/testing/testDrivenDevelopment/SKILL.md \
  -o .claude/commands/tdd-cycle.md
```

### Method B: Claude Code Skills Directory (`.claude/skills/`)
```bash
mkdir -p .claude/skills/databaseArchitecture
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/databaseArchitecture/SKILL.md \
  -o .claude/skills/databaseArchitecture/SKILL.md
```

### How Slash Commands Work in Claude Code:
In your Claude Code CLI terminal:
```text
> /api-engineering Design a multi-tenant subscription billing API with OpenAPI 3.2.1
> /db-architecture Create a hospital bed allocation schema with temporal GiST exclusion
```

---

## 3. Cursor Setup

Cursor supports structured context via `.cursor/rules/` (`.mdc` files) or `.cursor/skills/`.

### Installing into `.cursor/rules/` (Auto-Triggered Rules)
Cursor `.mdc` files allow automatic activation based on file patterns (e.g. `*.sql` or `*.ts`):

```bash
mkdir -p .cursor/rules

# 1. Database Architecture Rule (triggers on SQL, migrations, and Prisma/Drizzle schemas)
cat << 'EOF' > .cursor/rules/database-architecture.mdc
---
description: Database architecture, normalization (1NF-BCNF), RLS, and zero-downtime migrations.
globs: **/*.sql, **/schema.prisma, **/migrations/**
---
EOF
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/databaseArchitecture/SKILL.md \
  >> .cursor/rules/database-architecture.mdc

# 2. Production API Engineering Rule (triggers on route handlers and OpenAPI specs)
cat << 'EOF' > .cursor/rules/api-engineering.mdc
---
description: Contract-first OpenAPI 3.2.1, RFC 9457 problem details, and REST API standards.
globs: **/routes/**, **/api/**, **/openapi.yaml, **/openapi.json
---
EOF
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/apiEngineering/SKILL.md \
  >> .cursor/rules/api-engineering.mdc
```

### How to Invoke in Cursor:
- **Auto-Activation**: When editing SQL or route files, Cursor automatically applies the rules.
- **Manual Mention**: In Cursor Composer / Chat, type `@database-architecture.mdc` or `@api-engineering.mdc` to explicitly invoke the skill.

---

## 4. Windsurf (Cascade) Setup

Windsurf uses `.windsurfrules` or `.windsurf/skills/` for workspace-level rules and capabilities.

### Installing into `.windsurfrules`:
```bash
# Append skill guidance directly into .windsurfrules
echo -e "\n\n# --- Database Architecture Standards ---" >> .windsurfrules
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/databaseArchitecture/SKILL.md >> .windsurfrules

echo -e "\n\n# --- API Engineering Standards ---" >> .windsurfrules
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/apiEngineering/SKILL.md >> .windsurfrules
```

### How to Invoke in Windsurf:
In Windsurf Cascade, simply prompt:
```text
Apply the Database Architecture skill guidelines to design our new ordering system.
```

---

## 5. Universal Automated Setup Script

Use our bundled installer script [scripts/installSkill.sh](scripts/installSkill.sh) to automatically route any skill into the correct directory for your AI environment:

```bash
# Syntax:
# curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/scripts/installSkill.sh | bash -s <skill-name> [agent]

# 1. Install for Antigravity (installs into .gemini/antigravity/skills/):
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/scripts/installSkill.sh | bash -s databaseArchitecture antigravity

# 2. Install for Claude Code (installs into .claude/commands/ and .claude/skills/):
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/scripts/installSkill.sh | bash -s apiEngineering claude

# 3. Install for Cursor (installs into .cursor/rules/):
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/scripts/installSkill.sh | bash -s testDrivenDevelopment cursor

# 4. Install for Universal Agent (installs into .agent/skills/):
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/scripts/installSkill.sh | bash -s githubAction agent
```

---

## 6. Complete Slash Command Catalog

Every skill in SkillFullStack defines dedicated slash commands. Use this table as a cheat sheet for all 23 skills:

| Domain | Skill Name | Supported Slash Commands | Description |
| :--- | :--- | :--- | :--- |
| **`backend`** | **`databaseArchitecture`** | `/db-architecture`, `/db-design`, `/db-normalize`, `/db-scale`, `/db-audit`, `/db-migration` | Relational 3NF/BCNF normalization, PostgreSQL RLS, composite FKs, GiST exclusion, and zero-downtime expand-contract migrations. |
| **`backend`** | **`apiEngineering`** | `/api-engineering`, `/api-design`, `/api-crud`, `/api-audit`, `/api-security`, `/api-breaking` | Contract-first OpenAPI 3.2.1, RFC 9457 problem details, IETF Idempotency-Key draft-08, and breaking-change CI gating. |
| **`backend`** | **`golangStandard`** | `/go-standard`, `/go-layout`, `/go-slog`, `/go-context` | Go 1.23+ enterprise layout, `log/slog`, context propagation, and clean domain boundaries. |
| **`backend`** | **`pythonStandard`** | `/python-standard`, `/uv-project`, `/ruff-check`, `/pydantic-v2` | Python 3.12+ standards, Astral `uv` toolchain, `Ruff` formatting, and Pydantic v2 schemas. |
| **`backend`** | **`upstash`** | `/upstash-redis`, `/upstash-ratelimit`, `/upstash-workflow`, `/upstash-qstash` | Serverless Redis, dynamic token bucket ratelimiting, and durable workflow orchestrations. |
| **`backend`** | **`durableBackgroundJobs`** | `/durable-jobs`, `/inngest-step`, `/trigger-step`, `/job-idempotency` | Inngest and Trigger.dev v3 durable step functions, zero-timeout operations, and failure recovery. |
| **`frontend`** | **`nextjs`** | `/nextjs-production`, `/nextjs-dal`, `/nextjs-rsc`, `/nextjs-security` | Next.js App Router checklist: RSC boundaries, Data Access Layer (DAL), CSP nonces, and Docker standalone. |
| **`frontend`** | **`shadcn-ui`** | `/shadcn-atomic`, `/shadcn-blocks`, `/shadcn-ai`, `/shadcn-fetch` | Official shadcn/ui components, blocks (`dashboard-01`), and AI elements (`@ai-elements`). |
| **`frontend`** | **`generativeUi`** | `/generative-ui`, `/ui-stream`, `/tools-component-mapping` | Streaming interactive React components via Vercel AI SDK and Data Stream Protocol. |
| **`frontend`** | **`tsxReactStandard`** | `/tsx-react19`, `/discriminated-unions`, `/strict-props` | React 19 primitives (ref props, Server Actions), discriminated unions, and zero `React.FC`. |
| **`gitVersionControl`** | **`gitWorkflow`** | `/git-workflow`, `/git-rebase`, `/git-bisect`, `/git-conflict` | Universal Git DAG, Trunk-based rebase, automated bisect debugging, and 3-way conflict resolution. |
| **`testing`** | **`testDrivenDevelopment`** | `/tdd-cycle`, `/test-pyramid`, `/test-doubles`, `/test-boundary` | Red-Green-Refactor discipline, 70/20/10 test pyramid ratio, test doubles, and boundary value analysis. |
| **`softwareDevelopment`** | **`requirementsEngineering`**| `/story-format`, `/moscow-prioritize`, `/attack-tree`, `/kano-analysis` | INVEST user stories, Given/When/Then BDD acceptance criteria, MoSCoW, and attack tree threat modeling. |
| **`cicdDevops`** | **`cicdPipeline`** | `/cicd-pipeline`, `/dockerfile-audit`, `/deploy-strategy`, `/dora-metrics` | Multi-stage non-root Docker hardening, Canary/Blue-Green deployments, and DORA metrics. |
| **`github`** | **`githubAction`** | `/github-action`, `/github-ci`, `/github-cd` | GitHub Actions matrix testing, concurrency cancelation, SHA pinning, and YAML security linting. |
| **`github`** | **`githubSetup`** | `/github-setup`, `/github-repository`, `/github-ruleset` | Modern GitHub Rulesets, branch auto-deletion, and squash-merge enforcement. |
| **`github`** | **`githubSecurity`** | `/github-security`, `/github-codeql`, `/github-dependabot`, `/github-secrets` | Supply chain security, grouped Dependabot updates, CodeQL analysis, and secret push protection. |
| **`github`** | **`githubQuality`** | `/github-quality`, `/github-pr`, `/github-codeowners` | Conventional Commits, enterprise PR checklists, and hierarchical CODEOWNERS. |
| **`github`** | **`githubTeam`** | `/github-team`, `/github-team-onboarding`, `/github-team-roles` | Team hierarchies, repository permission tiers, and automated round-robin review assignment. |
| **`dataAi`** | **`mcpServerDevelopment`** | `/mcp-server`, `/mcp-tools`, `/mcp-prompts`, `/mcp-resources` | Model Context Protocol servers in Python (FastMCP) and TypeScript. |
| **`dataAi`** | **`ragPipelineProduction`** | `/rag-hybrid`, `/rrf-fusion`, `/rerank-cohere` | BM25 + Dense vector hybrid retrieval, Reciprocal Rank Fusion, and Cohere cross-encoder rerankers. |
| **`securityQa`** | **`llmSecurityRedteaming`** | `/prompt-injection`, `/jailbreak-defense`, `/guardrail-audit` | OWASP Top 10 for LLMs, prompt injection mitigation, and automated red-teaming test suites. |
| **`foundation`** | **`promptEvalTesting`** | `/promptfoo-eval`, `/deepeval-test`, `/prompt-regression` | CI/CD prompt evaluation, regression testing, and LLM-as-a-judge scoring. |
