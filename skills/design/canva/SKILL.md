---
name: canva
description: Master Canva design automation and programmatic creative skill. Covers CLI workflows, brand kit audits, CSV bulk creation, safe transactional design editing, visual feedback critique, comment resolution, and multi-channel social media resizing.
version: 2026.x
last-verified: 2026-11-20
compatibility: Canva REST API, @canva/cli, Canva MCP Server, Node.js 24+, npm 11+
slash-commands:
  - command: /canva-cli
    description: Execute programmatic Canva REST API commands and discovery with @canva/cli
    argument-hint: "<group> <command> [--flags]"
  - command: /canva-brand-check
    description: Audit designs against brand kit colors, typography, logos, and voice guidelines
    argument-hint: "<design_id_or_url> [--brand-kit=<id>]"
  - command: /canva-bulk-create
    description: Batch-generate designs from CSV, TSV, JSON, or URL data tags using Brand Templates
    argument-hint: "<template_id> --data=<file.csv>"
  - command: /canva-edit
    description: Execute safe transactional edits (text, formatting, fills, layout, titles)
    argument-hint: "<design_id> [--op=<operation>]"
  - command: /canva-feedback
    description: Generate structured visual design critique across 7 quality lenses
    argument-hint: "<design_id_or_url>"
  - command: /canva-implement
    description: Triage reviewer comments and automatically apply supported changes to completion
    argument-hint: "<design_id_or_url>"
  - command: /canva-resize
    description: Generate multi-channel aspect ratio variants (1080x1920, 1080x1350, 1200x627, etc.)
    argument-hint: "<design_id> [--platform=<name>|--ratio=<w:h>|--all]"
---

# Canva Master Engineering & Creative Automation Guide

## 1. Core Architecture & Transaction Safety Protocol

The Canva automation platform exposes two complementary integration models for AI agents and developers:
1. **Programmatic CLI & REST API (`@canva/cli` / `canva api ...`)**: Designed for local file access, automated CI/CD pipelines, bulk CSV processing, and asset staging.
2. **Model Context Protocol (`canva_canva` MCP Server)**: Direct agentic tool calling in Claude Code, Cursor, and Antigravity for conversational workflows, visual audits, and real-time editing.

### The Atomic Transaction Protocol

Every mutation against a Canva design follows an atomic lifecycle: **start transaction $\rightarrow$ perform operations $\rightarrow$ user visual approval $\rightarrow$ commit (or cancel)**.

```
[Start Session]              [Draft Operations]             [Visual Gate]              [Save or Discard]
Canva:start-editing-trans. -> perform-editing-operations -> Review Thumbnails -> commit-editing-transaction
(allocates transaction_id)    (batches JSON operations)     & Change Summary     (or cancel-editing-trans.)
```

- **Draft Isolation**: Modifications remain in an isolated buffer and never touch the live design until explicitly committed.
- **Fail-Safe Rollback**: If an operation fails, the user cancels, or the agent times out, calling `cancel-editing-transaction` discards the draft cleanly.
- Detailed transaction specifications: [references/transactionEditingEngine.md](references/transactionEditingEngine.md).

---

## 2. Canva CLI & Programmatic REST API Engine (`/canva-cli`)

Use `/canva-cli` when direct terminal automation, scripting, or local asset uploads are required.

### Setup & Discovery
- **Runtime Requirement**: Node.js 24+ and npm 11+.
- **Install**: `npm install -g @canva/cli@latest`
- **Verify**: `canva --version`
- **Authentication**: `canva login` (use `canva login --mode manual` in remote or headless containers).

### CLI Command Matrix

```bash
# Discover resources without guessing
canva api --help
canva api designs --help
canva api describe designs get

# Safe dry-run pre-flight
canva api designs update --design-id DABcd1234ef --dry-run

# Inspect or upload assets
canva api assets upload --file ./creative/hero.png --name "Q3 Hero Banner"

# Manage profiles
canva login --profile marketing-team
canva api designs list --profile marketing-team
```

### Result Schema & Job Polling
All CLI requests return a standard JSON envelope: `{ "ok": bool, "data": ..., "error": ..., "next": ... }`.
For asynchronous operations returning a `job` identifier, execute exponential backoff polling until `status` transitions to `success` or `failed`.
Complete API contracts: [references/apiReference.md](references/apiReference.md) and [assets/README.md](assets/README.md).

---

## 3. Brand Kit Governance & Visual Verification (`/canva-brand-check`)

Audit designs against corporate brand kits and guidelines. **Brand checks are strictly read-only and never mutate designs.**

### The Brand-Kit Data Gap Architecture
When querying `Canva:list-brand-kits`, the API provides kit IDs, names, and visual thumbnails, but machine-readable hex colors and font families may be omitted depending on organizational scopes:
- **Exposed Palette**: Match exact hex codes and font families programmatically.
- **Data Gap Fallback**: Conduct visual inspection comparing design thumbnails against kit thumbnails, and request the developer's brand palette for exact verification. Never invent brand tokens.

### Five Audit Lenses & Three-State Verdict
Audit across:
1. **Color Palette**: Identify off-palette hex codes and suggest the closest brand replacement.
2. **Typography**: Audit font weight, size scale, and typeface families.
3. **Logo Integrity**: Verify clearspace, aspect ratio (no horizontal stretching), and approved logo lockups.
4. **Tone & Voice**: Proofread copy against organizational voice guidelines.
5. **Consistency**: Ensure uniform margins, gutters, and header placements across all slides.

Every item is marked **On brand**, **Off brand**, or **Can't verify**.
- Standard report template: [templates/brandCheckReport.template.md](templates/brandCheckReport.template.md).
- Complete governance rubric: [references/brandKitVerification.md](references/brandKitVerification.md).

---

## 4. Bulk Creation Engine: One Design per Row (`/canva-bulk-create`)

Batch-generate unique designs from CSV, TSV, JSON, or URL datasets by autofilling Brand Templates with data tags.

### Workflow & Image Resolution Patterns
1. **Ingest Tabular Data**: Parse rows, headers, and preview the first 3 rows.
2. **Inspect Template Schema**: Query `Canva:get-brand-template-dataset` for text, image, and chart tags.
3. **Fuzzy Field Mapping**: Map dataset columns to template fields and confirm with user.
4. **Image Field Handling**:
   - **Pattern A (Canva Asset ID)**: Pass `asset_id` directly in payload.
   - **Pattern B (Remote URL)**: Pre-upload URL via `Canva:upload-asset-from-url`, obtain `asset_id`, and bind to row.
   - **Pattern C (No Image)**: Skip image key to preserve template default graphic.
5. **Sequential Execution**: Run `Canva:autofill-design` sequentially row-by-row with error isolation.

> [!WARNING]
> Bulk autofill requires a Canva Enterprise plan. For batches $> 10$ rows, offer a 3-row test run before launching the full batch.
- Complete autofill protocol: [references/bulkAutofillProtocol.md](references/bulkAutofillProtocol.md).

---

## 5. Safe Transactional Editing Protocol (`/canva-edit`)

The canonical engine for applying mutations to existing designs.

### Capabilities Matrix (The CAN and CANNOT Boundary)

| Domain | ✅ What the API CAN Do | ❌ What the API CANNOT Do |
| :--- | :--- | :--- |
| **Text** | Replace full text (`replace_text`), substring replace (`find_and_replace_text`), change font size, weight, italic, color, alignment, line height, lists, links (`format_text`) | **Cannot change font family / typeface** (e.g. Arial $\rightarrow$ Inter); **cannot create new text boxes** |
| **Media** | Swap existing photo/video fills (`update_fill`), insert media fills (`insert_fill`), delete elements (`delete_element`) | Cannot change background canvas colors, gradients, or shape vector fills |
| **Layout** | Reposition coordinates (`position_element`), resize bounds (`resize_element`), update title (`update_title`) | Cannot reorder, duplicate, add, or delete entire pages/slides |

### Responsive Pages Protocol
Pages with `is_responsive: true` only support: `update_title`, `replace_text`, `find_and_replace_text`, `update_fill`, and `delete_element`. Layout, resizing, and text formatting are forbidden on responsive pages.

### The Commit Approval Gate
Always show the rendered preview thumbnail and plain-language summary of changes. Wait for explicit user confirmation before committing.
- Deep engine mechanics: [references/transactionEditingEngine.md](references/transactionEditingEngine.md).

---

## 6. Design Critique & Visual Feedback Rubric (`/canva-feedback`)

Act as an expert design reviewer. This workflow is **strictly read-only**; inspect elements and thumbnails, then cancel any opened inspection transactions.

### The 7 Evaluative Lenses
1. **Visual Hierarchy**: Immediate focal point and scale contrast.
2. **Layout & Spacing**: Grid alignment, whitespace, and minimum 32px edge margins.
3. **Copy & Messaging**: Scannability, single takeaway per slide, typo detection.
4. **Consistency**: Uniform color tokens and typography scale across pages.
5. **Readability & Contrast**: Scrims over photos, minimum 16pt presentation body text.
6. **Accessibility**: WCAG 2.2 AA contrast ratios ($\ge 4.5:1$ normal, $\ge 3:1$ large).
7. **Fit for Purpose**: Audience and platform medium context.

Rank findings as **[High]**, **[Med]**, or **[Low]**, pairing every problem with an actionable fix.
- Feedback template: [templates/designFeedbackReport.template.md](templates/designFeedbackReport.template.md).
- Complete critique rubric: [references/designCritiqueRubric.md](references/designCritiqueRubric.md).

---

## 7. Reviewer Feedback Triage & Resolution (`/canva-implement`)

Drive stakeholder design reviews to completion automatically.

### Workflow & Triage Categories
1. **Harvest Comments**: Read all comment threads (`Canva:list-comments`) and replies (`Canva:list-replies`).
2. **Classify Feedback**:
   - **Actionable**: API-supported changes. Proactively interpret requests (e.g. draft punchier copy).
   - **Requires Manual Action**: Font family, background color, or new text box changes.
   - **Resolved**: Acknowledgments, approvals, or "LGTM" comments.
3. **Single Approval Gate**: Present the comprehensive triage summary to the user **ONE TIME ONLY**.
4. **Batch Commit**: Once approved, open transaction, apply all operations in one batched call, and commit immediately without asking secondary confirmation.
5. **Close Feedback Loop**: Automatically reply to comment threads via `Canva:reply-to-comment` and provide a step-by-step manual checklist for unsupported items.
- Triage protocol details: [references/feedbackTriageAndResolution.md](references/feedbackTriageAndResolution.md).

---

## 8. Multi-Channel Social Media Resizing Matrix (`/canva-resize`)

Transform master creative designs into channel-ready social variants automatically using `Canva:resize-design`.

### Target Dimension Resolution Hierarchy
1. **Exact Pixels Specified**: Use requested width $\times$ height.
2. **Platform & Placement Specified**: Lookup dimensions in the authoritative platform table.
3. **Aspect Ratio Specified**: Map `9:16` (1080x1920), `4:5` (1080x1350), `1:1` (1080x1080), or `16:9` (1920x1080).
4. **Generic "All Channels / Platform-Ready"**: Apply the Default Channel Set:
   - `1080 × 1920`: TikTok vertical, Instagram/Facebook Story & Reel, YouTube Short
   - `1080 × 1350`: Instagram & Facebook Feed portrait
   - `1200 × 627`: LinkedIn landscape, X landscape, Facebook link image (deduplicated)
   - `1920 × 1080`: YouTube standard video
5. Present results with direct, clickable Canva edit links for every created variant.
- Complete channel specifications: [references/channelFormatsAndSocialResize.md](references/channelFormatsAndSocialResize.md).

---

## 9. Anti-Patterns & Common Pitfalls

- ❌ **The Dangling Transaction Anti-Pattern**: Opening a transaction to read design content and forgetting to cancel it. Always invoke `cancel-editing-transaction` if no mutations are committed.
- ❌ **The Phantom Font Mutation**: Attempting to pass `font_family` to `format_text`. The Canva API rejects font family mutations; classify them immediately as manual editor tasks.
- ❌ **Unthrottled Concurrent Bulk Ingestion**: Firing 50 parallel `autofill-design` requests simultaneously. Always process batch rows sequentially to prevent HTTP 429 rate limits.
- ❌ **Double-Prompting on Feedback Implementation**: Asking "Shall I commit?" after the user already approved the feedback implementation plan. The initial approval covers the entire batch commit.
- ❌ **Hallucinating Brand Tokens**: Guessing hex colors or typography when brand kits omit machine-readable palettes. Mark unverified attributes as `Can't verify` and prompt for developer input.
- ❌ **Ignoring Responsive Flags**: Attempting `position_element` or `resize_element` on pages where `is_responsive: true`.

---

## 10. Offline Documentation & References

- **Complete Offline Documentation Assets**: [assets/README.md](assets/README.md)
  - REST API Architecture: [assets/rest-api/overview.md](assets/rest-api/overview.md)
  - Authentication & Scopes: [assets/rest-api/authentication.md](assets/rest-api/authentication.md)
  - Designs & Operations: [assets/rest-api/designs.md](assets/rest-api/designs.md)
  - Assets & Jobs: [assets/rest-api/assets-and-jobs.md](assets/rest-api/assets-and-jobs.md)
  - MCP Tool Contracts: [assets/mcp/tools.md](assets/mcp/tools.md)
- **High-Density Engineering References**:
  - [API & MCP Reference](references/apiReference.md)
  - [Transactional Editing Engine](references/transactionEditingEngine.md)
  - [Brand Kit Verification](references/brandKitVerification.md)
  - [Bulk Autofill Protocol](references/bulkAutofillProtocol.md)
  - [Design Critique Rubric](references/designCritiqueRubric.md)
  - [Feedback Triage & Resolution](references/feedbackTriageAndResolution.md)
  - [Social Media Channel Formats](references/channelFormatsAndSocialResize.md)
- **Diagnostic Scripts & Tools**:
  - Design Pre-flight Auditor: [scripts/auditCanvaDesign.py](scripts/auditCanvaDesign.py)
- **Report Templates**:
  - Brand Audit Template: [templates/brandCheckReport.template.md](templates/brandCheckReport.template.md)
  - Design Critique Template: [templates/designFeedbackReport.template.md](templates/designFeedbackReport.template.md)
- **Evaluation Suite**:
  - Test Harness: [evals/evals.json](evals/evals.json)
