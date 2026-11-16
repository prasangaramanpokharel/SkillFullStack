# SkillFullStack

An enterprise-grade, taxonomy-driven repository for ultra-high-density **Agent Skills** conforming to the open Agent Skills (`SKILL.md`) standard.

## Architecture & Verified Skills Index

```
SkillFullStack/
├── .skillsRegistry/
│   ├── catalog.json              # Aggregated machine-readable registry index (23 skills)
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
│   ├── github/                   # GitHub Engineering Skills Toolkit (Phase 1)
│   │   ├── githubAction/         # /github-action, /github-ci, /github-cd
│   │   ├── githubSetup/          # /github-setup, /github-repository, /github-ruleset
│   │   ├── githubSecurity/       # /github-security, /github-codeql, /github-dependabot
│   │   ├── githubQuality/        # /github-quality, /github-pr, /github-codeowners
│   │   └── githubTeam/           # /github-team, /github-team-onboarding, /github-team-roles
│   ├── backend/
│   │   ├── databaseArchitecture/ # /db-architecture, /db-design, /db-normalize, /db-scale, /db-audit
│   │   ├── apiEngineering/       # /api-engineering, /api-design, /api-crud, /api-audit, /api-security
│   │   ├── golangStandard/       # Go 1.23+, log/slog, context, errgroup, clean domains
│   │   ├── pythonStandard/       # Python 3.12+, uv toolchain, Ruff, Pydantic v2
│   │   ├── upstash/              # Serverless Redis, dynamic ratelimiting, durable workflows
│   │   └── durableBackgroundJobs/# Inngest & Trigger.dev v3 zero-timeout step functions
│   ├── frontend/
│   │   ├── nextjs/               # Next.js App Router production checklist & architecture
│   │   ├── shadcn-ui/            # shadcn v4 primitives, blocks, & AI elements
│   │   ├── generativeUi/         # Streaming interactive React UI via Vercel AI SDK
│   │   └── tsxReactStandard/     # React 19, discriminated unions, strict TypeScript
│   ├── backend/
│   │   ├── upstash/              # Serverless Redis, Vector, QStash, & Workflows
│   │   ├── durableBackgroundJobs/# Inngest & Trigger.dev v3 zero-timeout step functions
│   │   ├── golangStandard/       # Go 1.23+, log/slog, context, errgroup, clean domains
│   │   └── pythonStandard/       # Python 3.12+, uv toolchain, Ruff, Pydantic v2
│   ├── dataAi/
│   │   ├── mcpServerDevelopment/ # Model Context Protocol (FastMCP & TypeScript SDK)
│   │   └── ragPipelineProduction/# BM25 + Dense hybrid search, RRF, & Cohere reranking
│   ├── securityQa/
│   │   └── llmSecurityRedteaming/# OWASP Top 10 for LLMs, prompt injection, & guardrails
│   └── foundation/
│       └── promptEvalTesting/    # Promptfoo & DeepEval CI/CD regression suites
└── scripts/
    └── scaffoldSkill.py          # Automated spec-compliant skill generator
```

## Available Skills & Direct Links

### Software Engineering Curriculum Skills Ecosystem (Textbook Aligned)
| Domain | Skill Name | Slash Commands | Guide & Specification | Key Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **`gitVersionControl`** | **`gitWorkflow`** | `/git-workflow`<br>`/git-rebase`<br>`/git-bisect`<br>`/git-conflict` | [SKILL.md](skills/gitVersionControl/gitWorkflow/SKILL.md) | Universal Git DAG manipulation, Trunk-based short-lived branches, interactive rebase, automated bisect debugging, and 3-way conflict resolution. |
| **`testing`** | **`testDrivenDevelopment`** | `/tdd-cycle`<br>`/test-pyramid`<br>`/test-doubles`<br>`/test-boundary` | [SKILL.md](skills/testing/testDrivenDevelopment/SKILL.md) | Red-Green-Refactor enforcement, test pyramid auditing (70/20/10 ratio), test doubles classification (Mocks/Stubs/Fakes), and boundary value test matrices. |
| **`softwareDevelopment`** | **`requirementsEngineering`** | `/story-format`<br>`/moscow-prioritize`<br>`/attack-tree`<br>`/kano-analysis` | [SKILL.md](skills/softwareDevelopment/requirementsEngineering/SKILL.md) | INVEST user stories, executable BDD criteria (Given/When/Then), MoSCoW & Kano prioritization, Shape Up appetite, and attack tree threat modeling. |
| **`cicdDevops`** | **`cicdPipeline`** | `/cicd-pipeline`<br>`/dockerfile-audit`<br>`/deploy-strategy`<br>`/dora-metrics` | [SKILL.md](skills/cicdDevops/cicdPipeline/SKILL.md) | CI matrix automation, multi-stage non-root Docker hardening, zero-downtime deployment strategies (Canary/Blue-Green), and DORA velocity metrics. |

---

### GitHub Engineering Skills Toolkit (`skills/github/*`)
| Skill | Slash Commands | Guide & Specification | Key Capabilities |
| :--- | :--- | :--- | :--- |
| **`githubAction`** | `/github-action`<br>`/github-ci`<br>`/github-cd` | [SKILL.md](skills/github/githubAction/SKILL.md) | Matrix builds, concurrency cancelation, SHA action pinning, least-privilege token permissions, and YAML security linting. |
| **`githubSetup`** | `/github-setup`<br>`/github-repository`<br>`/github-ruleset` | [SKILL.md](skills/github/githubSetup/SKILL.md) | Modern GitHub Rulesets (stale approval dismissal, status checks), squash-merge enforcement, and branch auto-deletion. |
| **`githubSecurity`** | `/github-security`<br>`/github-codeql`<br>`/github-dependabot` | [SKILL.md](skills/github/githubSecurity/SKILL.md) | Grouped Dependabot updates (`minor`/`patch`), CodeQL multi-language matrix, secret scanning push protection. |
| **`githubQuality`** | `/github-quality`<br>`/github-pr`<br>`/github-codeowners` | [SKILL.md](skills/github/githubQuality/SKILL.md) | Hierarchical `CODEOWNERS`, Conventional Commit enforcement (`type(scope): subject`), PR checklist validation. |
| **`githubTeam`** | `/github-team`<br>`/github-team-onboarding`<br>`/github-team-roles` | [SKILL.md](skills/github/githubTeam/SKILL.md) | Nested team hierarchies, repository permission tiers (Triage/Write/Maintain), and automated round-robin review delegation. |

---

### Language Standards & Frameworks
| Domain | Skill Name | Specification & Guide | Key Capabilities |
| :--- | :--- | :--- | :--- |
| **`frontend`** | **`nextjs`** | [SKILL.md](skills/frontend/nextjs/SKILL.md) | Official Next.js Production Checklist: RSC boundaries, Data Access Layer (DAL), Taint API, CSP nonces, Core Web Vitals, and Docker standalone. |
| **`frontend`** | **`shadcn-ui`** | [SKILL.md](skills/frontend/shadcn-ui/SKILL.md) | Atomic primitives, blocks (`dashboard-01`), AI components (`@ai-elements`), and direct MDX fetching. |
| **`frontend`** | **`generativeUi`** | [SKILL.md](skills/frontend/generativeUi/SKILL.md) | Streaming interactive React components, tools mapping, and `createDataStreamResponse`. |
| **`frontend`** | **`tsxReactStandard`** | [SKILL.md](skills/frontend/tsxReactStandard/SKILL.md) | React 19 primitives (ref props, Server Actions, `use()`), discriminated unions, strict tsconfig, and no `React.FC`/enums. |
| **`backend`** | **`databaseArchitecture`** | [SKILL.md](skills/backend/databaseArchitecture/SKILL.md) | Universal database architecture: relational normalization (1NF-BCNF), NoSQL/OLAP selection, sharding, ACID, and zero-downtime migrations. |
| **`backend`** | **`apiEngineering`** | [SKILL.md](skills/backend/apiEngineering/SKILL.md) | Contract-first OpenAPI 3.2.1, RFC 9457 errors, IETF Idempotency-Key draft-08, contextual pagination, and breaking-change detection. |
| **`backend`** | **`golangStandard`** | [SKILL.md](skills/backend/golangStandard/SKILL.md) | Standard `log/slog` (JSON/text), context propagation, `fmt.Errorf("%w")`, clean domain layout, and `errgroup`. |
| **`backend`** | **`pythonStandard`** | [SKILL.md](skills/backend/pythonStandard/SKILL.md) | Astral `uv` toolchain, `Ruff` linter/formatter, PEP 585/604 modern typing, Pydantic v2 models, and `asyncio.TaskGroup`. |
| **`backend`** | **`upstash`** | [SKILL.md](skills/backend/upstash/SKILL.md) | Serverless Redis, dynamic ratelimiting, durable workflows, and QStash flow control. |
| **`backend`** | **`durableBackgroundJobs`**| [SKILL.md](skills/backend/durableBackgroundJobs/SKILL.md) | Inngest & Trigger.dev v3 step memoization, pauses, and zero-timeout execution. |
| **`dataAi`** | **`mcpServerDevelopment`** | [SKILL.md](skills/dataAi/mcpServerDevelopment/SKILL.md) | FastMCP Python & TypeScript SDKs, Tools, Resources, Prompts, and stdio/SSE transports. |
| **`dataAi`** | **`ragPipelineProduction`** | [SKILL.md](skills/dataAi/ragPipelineProduction/SKILL.md) | Dense Vector + BM25 Hybrid Retrieval, Reciprocal Rank Fusion (RRF), and Cohere rerankers. |
| **`securityQa`** | **`llmSecurityRedteaming`** | [SKILL.md](skills/securityQa/llmSecurityRedteaming/SKILL.md) | OWASP LLM Top 10 defenses, data/instruction separation, PII scrubbing, and injection test harnesses. |
| **`foundation`** | **`promptEvalTesting`** | [SKILL.md](skills/foundation/promptEvalTesting/SKILL.md) | CI/CD prompt regression testing with Promptfoo and DeepEval (LLM-as-a-judge). |

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
