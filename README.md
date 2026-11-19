# SkillFullStack

An enterprise-grade, taxonomy-driven repository for ultra-high-density **Agent Skills** conforming to the open Agent Skills (`SKILL.md`) standard.

## Architecture & Verified Skills Index

```
SkillFullStack/
├── .skillsRegistry/
│   ├── catalog.json              # Aggregated machine-readable registry index (28 skills)
│   └── schema.json               # Frontmatter validation schema
├── templates/
│   └── _skillTemplate/           # Base template with high-yield prompt design
├── skills/
│   ├── gitVersionControl/        # Universal Git DAG, rebasing, bisect, & conflict recovery
│   │   └── gitWorkflow/          # /git-workflow, /git-rebase, /git-bisect, /git-conflict
│   ├── testing/                  # Test-Driven Development, test pyramid, & test doubles
│   │   └── testDrivenDevelopment/# /tdd-cycle, /test-pyramid, /test-doubles, /test-boundary
│   ├── softwareDevelopment/      # Requirements, INVEST user stories, BDD, & attack trees
│   │   └── requirementsEngineering/ # /story-format, /moscow-prioritize, /attack-tree
│   ├── cicdDevops/               # CI/CD delivery pipelines, Docker hardening, & DORA metrics
│   │   └── cicdPipeline/         # /cicd-pipeline, /dockerfile-audit, /deploy-strategy
│   ├── devopsCloud/              # Cloudflare edge platform, serverless compute, & anycast infra
│   │   ├── cloudflare/           # /cf-architect, /cf-worker, /cf-database, /cf-storage, /cf-security
│   │   └── internetComputer/     # /icp-canister, /icp-deploy, /icp-security, /icp-storage, /icp-chain-fusion, /icp-test
│   ├── github/                   # GitHub Engineering Skills Toolkit (Phase 1)
│   │   ├── githubAction/         # /github-action, /github-ci, /github-cd
│   │   ├── githubSetup/          # /github-setup, /github-repository, /github-ruleset
│   │   ├── githubSecurity/       # /github-security, /github-codeql, /github-dependabot
│   │   ├── githubQuality/        # /github-quality, /github-pr, /github-codeowners
│   │   └── githubTeam/           # /github-team, /github-team-onboarding, /github-team-roles
│   ├── backend/
│   │   ├── databaseArchitecture/ # /db-architecture, /db-design, /db-normalize, /db-scale, /db-audit
│   │   ├── neon/                 # /neon-branch, /neon-connect, /neon-auth, /neon-realtime, /neon-scale, /neon-cli
│   │   ├── apiEngineering/       # /api-engineering, /api-design, /api-crud, /api-audit, /api-security
│   │   ├── golangStandard/       # Go 1.23+, log/slog, context, errgroup, clean domains
│   │   ├── pythonStandard/       # Python 3.12+, uv toolchain, Ruff, Pydantic v2
│   │   ├── upstash/              # Serverless Redis, dynamic ratelimiting, durable workflows
│   │   └── durableBackgroundJobs/# Inngest & Trigger.dev v3 zero-timeout step functions
│   ├── frontend/
│   │   ├── nextjs/               # Next.js App Router production checklist & architecture
│   │   ├── astro/                # Astro 5.x Islands architecture, Server Islands, & Actions
│   │   ├── shadcn-ui/            # shadcn v4 primitives, blocks, & AI elements
│   │   ├── generativeUi/         # Streaming interactive React UI via Vercel AI SDK
│   │   └── tsxReactStandard/     # React 19, discriminated unions, strict TypeScript
│   ├── backend/
│   │   ├── upstash/              # Serverless Redis, Vector, QStash, & Workflows
│   │   ├── durableBackgroundJobs/# Inngest & Trigger.dev v3 zero-timeout step functions
│   │   ├── golangStandard/       # Go 1.23+, log/slog, context, errgroup, clean domains
│   │   └── pythonStandard/       # Python 3.12+, uv toolchain, Ruff, Pydantic v2
│   ├── dataAi/
│   │   ├── openai/               # /openai-responses, /openai-tools, /openai-state, /openai-evals, /openai-finetuning
│   │   ├── mcpServerDevelopment/ # Model Context Protocol (FastMCP & TypeScript SDK)
│   │   └── ragPipelineProduction/# BM25 + Dense hybrid search, RRF, & Cohere reranking
│   ├── securityQa/
│   │   └── llmSecurityRedteaming/# OWASP Top 10 for LLMs, prompt injection, & guardrails
│   └── foundation/
│       └── promptEvalTesting/    # Promptfoo & DeepEval CI/CD regression suites
└── scripts/
    ├── validateSkills.py         # Strict production quality & consistency validator (100/100 score)
    ├── scaffoldSkill.py          # Automated spec-compliant skill generator
    └── installSkill.sh           # One-liner skill installer via raw GitHub URL
```

## 📦 How to Install & Load Skills from GitHub

You can load any skill from this repository directly into your agent environment (e.g. Google Antigravity, Claude Code, Cursor, Windsurf, Codex, or custom LLM tooling) using an **AI prompt**, a **raw URL**, **curl**, or **git clone**.

> 📖 **Multi-Agent Setup & Slash Commands Guide**: For tool-specific setup instructions and how slash commands (`/db-architecture`, `/api-engineering`, `/tdd-cycle`, etc.) map natively into **Google Antigravity**, **Claude Code**, **Cursor**, and **Windsurf**, see our dedicated guide: **[SETUP.md](SETUP.md)**.
> 🤖 **Agent Execution & High-Accuracy Protocol**: For rules on leveraging local bundled documentation (`assets/`) for zero hallucination, see **[AGENTS.md](AGENTS.md)**.

### 🤖 One-Click AI Setup Prompt (Copy & Paste)

Paste this prompt directly into your AI coding assistant (Antigravity, Claude Code, Cursor, Windsurf, Codex) to inspect the catalog and install the skills you need:

```text
Read the skills registry catalog from:
https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/.skillsRegistry/catalog.json

Show me all available skills and their slash commands, then install the skills needed for this project into `.agent/skills/<skill-name>/SKILL.md` by downloading their raw files from:
https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/<path>/SKILL.md
```

> **Tip (Single Skill)**: To install a specific skill (e.g., `databaseArchitecture`), simply tell your AI:  
> *"Install the `databaseArchitecture` skill into `.agent/skills/databaseArchitecture/SKILL.md` using https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/.skillsRegistry/catalog.json to locate its raw URL."*

---

### 🚀 Method 0: Official NPM Package (`npx skillfullstack`)
Install any skill directly into your project in one command (auto-detects Claude Code, Cursor, Antigravity, Windsurf, or Copilot):
```bash
# 1. Install specific skills (auto-configures for your agent)
npx skillfullstack add nextjs
npx skillfullstack add astro cloudflare
npx skillfullstack add databaseArchitecture --agent=cursor

# 2. Inspect project and auto-recommend skills for your tech stack
npx skillfullstack init

# 3. List all 25+ verified skills across all domains
npx skillfullstack list

# 4. Search by keyword or framework
npx skillfullstack search graphql
```

---

### Method 1: Direct Raw URL (Zero Clone / Single Skill)
Every skill's primary definition is located at its raw GitHub URL:
```text
https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/<taxonomy>/<skillName>/SKILL.md
```

#### Quick `curl` Downloads:
```bash
# 1. Database Architecture (Multi-tenant RLS, composite FKs, GiST exclusion)
mkdir -p .agent/skills/databaseArchitecture
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/databaseArchitecture/SKILL.md \
  -o .agent/skills/databaseArchitecture/SKILL.md

# 2. Production API Engineering (Contract-first OpenAPI 3.2.1, RFC 9457 errors)
mkdir -p .agent/skills/apiEngineering
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/apiEngineering/SKILL.md \
  -o .agent/skills/apiEngineering/SKILL.md

# 3. Test-Driven Development (TDD cycle, test pyramid, test doubles)
mkdir -p .agent/skills/testDrivenDevelopment
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/testing/testDrivenDevelopment/SKILL.md \
  -o .agent/skills/testDrivenDevelopment/SKILL.md

# 4. Next.js Production Standard (App router, DAL, taint API, CSP)
mkdir -p .agent/skills/nextjs
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/frontend/nextjs/SKILL.md \
  -o .agent/skills/nextjs/SKILL.md

# 5. Astro 5.x Production Engineering (Islands, Server Islands, Actions)
mkdir -p .agent/skills/astro
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/frontend/astro/SKILL.md \
  -o .agent/skills/astro/SKILL.md

# 6. Cloudflare Master Engineering (Workers, D1, R2, KV, DO, Queues, Workflows, WAF)
mkdir -p .agent/skills/cloudflare
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/devopsCloud/cloudflare/SKILL.md \
  -o .agent/skills/cloudflare/SKILL.md

# 5. GitHub Actions Production Automation & Security
mkdir -p .agent/skills/githubAction
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/github/githubAction/SKILL.md \
  -o .agent/skills/githubAction/SKILL.md
```

### Method 2: One-Liner Installer Script
Install any skill directly into the appropriate folder for your AI environment:
```bash
# Syntax: curl ... | bash -s <skill-name> [antigravity|claude|cursor|windsurf|agent]

# 1. Google Antigravity (.gemini/antigravity/skills/):
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/scripts/installSkill.sh | bash -s databaseArchitecture antigravity

# 2. Claude Code (.claude/commands/ and .claude/skills/):
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/scripts/installSkill.sh | bash -s apiEngineering claude

# 3. Cursor (.cursor/rules/):
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/scripts/installSkill.sh | bash -s testDrivenDevelopment cursor

# 4. Windsurf (.windsurf/skills/):
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/scripts/installSkill.sh | bash -s cicdPipeline windsurf

# 5. Universal Agent (.agent/skills/):
curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/scripts/installSkill.sh | bash -s githubAction agent
```

### Method 3: Full Repository Clone
```bash
git clone https://github.com/prasangaramanpokharel/skills.git
```

---

## Available Skills & Direct Links

### Software Engineering Curriculum Skills Ecosystem (Textbook Aligned)
| Domain | Skill Name | Slash Commands | Guide & Specification | Key Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **`gitVersionControl`** | **`gitWorkflow`** | `/git-workflow`<br>`/git-rebase`<br>`/git-bisect`<br>`/git-conflict` | [SKILL.md](skills/gitVersionControl/gitWorkflow/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/gitVersionControl/gitWorkflow/SKILL.md) | Universal Git DAG manipulation, Trunk-based short-lived branches, interactive rebase, automated bisect debugging, and 3-way conflict resolution. |
| **`testing`** | **`testDrivenDevelopment`** | `/tdd-cycle`<br>`/test-pyramid`<br>`/test-doubles`<br>`/test-boundary` | [SKILL.md](skills/testing/testDrivenDevelopment/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/testing/testDrivenDevelopment/SKILL.md) | Red-Green-Refactor enforcement, test pyramid auditing (70/20/10 ratio), test doubles classification (Mocks/Stubs/Fakes), and boundary value test matrices. |
| **`softwareDevelopment`** | **`requirementsEngineering`** | `/story-format`<br>`/moscow-prioritize`<br>`/attack-tree`<br>`/kano-analysis` | [SKILL.md](skills/softwareDevelopment/requirementsEngineering/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/softwareDevelopment/requirementsEngineering/SKILL.md) | INVEST user stories, executable BDD criteria (Given/When/Then), MoSCoW & Kano prioritization, Shape Up appetite, and attack tree threat modeling. |
| **`cicdDevops`** | **`cicdPipeline`** | `/cicd-pipeline`<br>`/dockerfile-audit`<br>`/deploy-strategy`<br>`/dora-metrics` | [SKILL.md](skills/cicdDevops/cicdPipeline/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/cicdDevops/cicdPipeline/SKILL.md) | CI matrix automation, multi-stage non-root Docker hardening, zero-downtime deployment strategies (Canary/Blue-Green), and DORA velocity metrics. |

---

### GitHub Engineering Skills Toolkit (`skills/github/*`)
| Skill | Slash Commands | Guide & Specification | Key Capabilities |
| :--- | :--- | :--- | :--- |
| **`githubAction`** | `/github-action`<br>`/github-ci`<br>`/github-cd` | [SKILL.md](skills/github/githubAction/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/github/githubAction/SKILL.md) | Matrix builds, concurrency cancelation, SHA action pinning, least-privilege token permissions, and YAML security linting. |
| **`githubSetup`** | `/github-setup`<br>`/github-repository`<br>`/github-ruleset` | [SKILL.md](skills/github/githubSetup/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/github/githubSetup/SKILL.md) | Modern GitHub Rulesets (stale approval dismissal, status checks), squash-merge enforcement, and branch auto-deletion. |
| **`githubSecurity`** | `/github-security`<br>`/github-codeql`<br>`/github-dependabot`<br>`/github-secrets` | [SKILL.md](skills/github/githubSecurity/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/github/githubSecurity/SKILL.md) | Grouped Dependabot updates (`minor`/`patch`), CodeQL multi-language matrix, secret scanning push protection. |
| **`githubQuality`** | `/github-quality`<br>`/github-pr`<br>`/github-codeowners` | [SKILL.md](skills/github/githubQuality/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/github/githubQuality/SKILL.md) | Hierarchical `CODEOWNERS`, Conventional Commit enforcement (`type(scope): subject`), PR checklist validation. |
| **`githubTeam`** | `/github-team`<br>`/github-team-onboarding`<br>`/github-team-roles` | [SKILL.md](skills/github/githubTeam/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/github/githubTeam/SKILL.md) | Nested team hierarchies, repository permission tiers (Triage/Write/Maintain), and automated round-robin review delegation. |

---

### Language Standards & Frameworks
| Domain | Skill Name | Specification & Guide | Key Capabilities |
| :--- | :--- | :--- | :--- |
| **`frontend`** | **`nextjs`** | [SKILL.md](skills/frontend/nextjs/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/frontend/nextjs/SKILL.md) | Official Next.js Production Checklist: RSC boundaries, Data Access Layer (DAL), Taint API, CSP nonces, Core Web Vitals, and Docker standalone. |
| **`frontend`** | **`astro`** | [SKILL.md](skills/frontend/astro/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/frontend/astro/SKILL.md) | Astro 5.x Islands Architecture, Server Islands (`server:defer`), Content Collections with Zod schemas, and type-safe `astro:actions`. |
| **`frontend`** | **`shadcn-ui`** | [SKILL.md](skills/frontend/shadcn-ui/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/frontend/shadcn-ui/SKILL.md) | Atomic primitives, blocks (`dashboard-01`), AI components (`@ai-elements`), and direct MDX fetching. |
| **`frontend`** | **`generativeUi`** | [SKILL.md](skills/frontend/generativeUi/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/frontend/generativeUi/SKILL.md) | Streaming interactive React components, tools mapping, and `createDataStreamResponse`. |
| **`frontend`** | **`tsxReactStandard`** | [SKILL.md](skills/frontend/tsxReactStandard/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/frontend/tsxReactStandard/SKILL.md) | React 19 primitives (ref props, Server Actions, `use()`), discriminated unions, strict tsconfig, and no `React.FC`/enums. |
| **`backend`** | **`databaseArchitecture`** | [SKILL.md](skills/backend/databaseArchitecture/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/databaseArchitecture/SKILL.md) | Universal database architecture: relational normalization (1NF-BCNF), NoSQL/OLAP selection, sharding, ACID, and zero-downtime migrations. |
| **`backend`** | **`apiEngineering`** | [SKILL.md](skills/backend/apiEngineering/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/apiEngineering/SKILL.md) | Contract-first OpenAPI 3.2.1, RFC 9457 errors, IETF Idempotency-Key draft-08, contextual pagination, and breaking-change detection. |
| **`backend`** | **`golangStandard`** | [SKILL.md](skills/backend/golangStandard/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/golangStandard/SKILL.md) | Standard `log/slog` (JSON/text), context propagation, `fmt.Errorf("%w")`, clean domain layout, and `errgroup`. |
| **`backend`** | **`pythonStandard`** | [SKILL.md](skills/backend/pythonStandard/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/pythonStandard/SKILL.md) | Astral `uv` toolchain, `Ruff` linter/formatter, PEP 585/604 modern typing, Pydantic v2 models, and `asyncio.TaskGroup`. |
| **`backend`** | **`upstash`** | [SKILL.md](skills/backend/upstash/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/upstash/SKILL.md) | Serverless Redis, dynamic ratelimiting, durable workflows, and QStash flow control. |
| **`backend`** | **`durableBackgroundJobs`**| [SKILL.md](skills/backend/durableBackgroundJobs/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/backend/durableBackgroundJobs/SKILL.md) | Inngest & Trigger.dev v3 step memoization, pauses, and zero-timeout execution. |
| **`devopsCloud`** | **`cloudflare`** | [SKILL.md](skills/devopsCloud/cloudflare/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/devopsCloud/cloudflare/SKILL.md) | Complete Cloudflare platform: Workers, Static Assets, D1 SQL, R2, KV, Durable Objects, Queues, Workflows, Hyperdrive, Vectorize, WAF, and Tunnels. Supports `wrangler` and `cf` CLI. |
| **`dataAi`** | **`mcpServerDevelopment`** | [SKILL.md](skills/dataAi/mcpServerDevelopment/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/dataAi/mcpServerDevelopment/SKILL.md) | FastMCP Python & TypeScript SDKs, Tools, Resources, Prompts, and stdio/SSE transports. |
| **`dataAi`** | **`ragPipelineProduction`** | [SKILL.md](skills/dataAi/ragPipelineProduction/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/dataAi/ragPipelineProduction/SKILL.md) | Dense Vector + BM25 Hybrid Retrieval, Reciprocal Rank Fusion (RRF), and Cohere rerankers. |
| **`securityQa`** | **`llmSecurityRedteaming`** | [SKILL.md](skills/securityQa/llmSecurityRedteaming/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/securityQa/llmSecurityRedteaming/SKILL.md) | OWASP LLM Top 10 defenses, data/instruction separation, PII scrubbing, and injection test harnesses. |
| **`foundation`** | **`promptEvalTesting`** | [SKILL.md](skills/foundation/promptEvalTesting/SKILL.md) · [Raw URL](https://raw.githubusercontent.com/prasangaramanpokharel/skills/main/skills/foundation/promptEvalTesting/SKILL.md) | CI/CD prompt regression testing with Promptfoo and DeepEval (LLM-as-a-judge). |

---

## Scaffolding a New Skill

```bash
python3 scripts/scaffoldSkill.py \
  --taxonomy <domain> \
  --name <skill-name> \
  --description "<use-when-trigger-and-summary>" \
  --version "<version>" \
  --docs "<documentation-url>"
```
