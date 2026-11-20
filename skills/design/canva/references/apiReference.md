# Canva REST API & MCP Integration Reference

**Last verified:** 2026-11-20  
**Runtimes & CLI:** Node.js 24+, npm 11+, `@canva/cli@latest`, Canva MCP Server (`canva_canva`)

---

## 1. Authentication & Scopes

The Canva Developer Platform uses OAuth 2.0 bearer tokens for API requests and standard user-authorized connection profiles for CLI and MCP operations.

### Required OAuth Scopes Matrix

| Capability / Workflow | Required Scopes | Description |
| :--- | :--- | :--- |
| **Inspect Designs** | `design:read` | Read design metadata, content, and export URLs |
| **Edit Designs** | `design:content:write`, `design:meta:write` | Perform transactional edits, mutate text, styles, and titles |
| **Brand Kits** | `brandkit:read` | Retrieve brand kits, logos, palettes, and typography presets |
| **Assets & Media** | `asset:read`, `asset:write` | Upload assets from local files or remote URLs, query asset library |
| **Comments & Triage** | `comment:read`, `comment:write` | Fetch threads, read replies, post automated triage resolutions |
| **Autofill & Bulk** | `brandtemplate:read`, `brandtemplate:meta:read` | Query brand template datasets and trigger bulk autofill jobs |

> [!WARNING]
> If any API or MCP call fails with `MISSING_SCOPE`, prompt the user to re-authenticate:
> - CLI: Run `canva login`
> - MCP: Disconnect and reconnect the Canva connector in the host client (Antigravity, Claude Code, Cursor) to refresh the OAuth token grant.

---

## 2. Canva CLI (`@canva/cli`) Protocols

The Canva CLI executes REST API operations directly against the logged-in profile.

### Installation & Prerequisites
- Minimum Runtime: Node.js 24 and npm 11
- Install command: `npm install -g @canva/cli@latest`
- Verification: `canva --version`

### Core CLI Commands

```bash
# Login & authentication
canva login
canva login --mode manual              # Headless / remote server environments
canva login --profile <name>           # Select specific account profile

# Resource discovery (no guessing)
canva api --help                       # List available resource groups
canva api <group> --help               # List group commands
canva api <group> <command> --help     # Inspect parameters and flags
canva api describe <group> <command>   # Return JSON schema of command contract

# Dry-run validation (safe pre-flight)
canva api designs update --dry-run ... # Validate arguments and authentication
```

### CLI Response Contract

All CLI commands return a structured JSON object on standard output:

```json
{
  "ok": true,
  "data": {
    "id": "DAGfA-xxxxxx",
    "title": "Q3 Executive Summary",
    "urls": {
      "edit_url": "https://www.canva.com/design/DAGfA-xxxxxx/edit",
      "view_url": "https://www.canva.com/design/DAGfA-xxxxxx/view"
    }
  },
  "error": null,
  "next": null
}
```

On failure:
```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "permission_denied",
    "message": "Missing required scope: design:content:write"
  },
  "meta": {
    "status": 403
  }
}
```

---

## 3. Asynchronous Jobs Protocol

Long-running operations (such as asset uploads, large exports, and batch autofill) return a job identifier rather than an immediate resource payload.

### Polling Algorithm & Backoff Protocol

```
1. Initiate asynchronous request -> receive { "job": { "id": "<job_id>", "status": "in_progress" } }
2. Set initial delay = 1000ms
3. Loop while status == "in_progress":
     a. Sleep(delay)
     b. Poll job endpoint: `canva api jobs get --id <job_id>` (or corresponding MCP get-job)
     c. If status == "success":
          Extract resource ID and URLs
          Break and return
     d. If status == "failed":
          Extract error.code and error.message
          Raise error and terminate (do NOT blind-retry)
     e. Update delay = min(delay * 1.5, 10000ms)
```

---

## 4. Canva MCP Tool Mapping

When running in an MCP-connected agent environment, use the corresponding MCP tool primitives:

| Workflow Area | Canonical MCP Tool Name | Primary Parameters |
| :--- | :--- | :--- |
| **Link Resolution** | `Canva:resolve-shortlink` | `url`: Short link (`canva.link/...`) |
| **Design Inspection** | `Canva:get-design` | `design_id`: Raw ID starting with `D` |
| **Content Reading** | `Canva:get-design-content` | `design_id`: Design ID |
| **Thumbnail Retrieval**| `Canva:get-design-thumbnail` | `design_id`: Design ID |
| **Brand Kits** | `Canva:list-brand-kits` | `continuation`: (optional cursor) |
| **Transaction Start** | `Canva:start-editing-transaction`| `design_id`: Target design |
| **Apply Operations** | `Canva:perform-editing-operations`| `transaction_id`, `pages`, `page_index`, `operations` |
| **Commit Transaction** | `Canva:commit-editing-transaction`| `transaction_id` |
| **Cancel Transaction** | `Canva:cancel-editing-transaction`| `transaction_id` |
| **Template Search** | `Canva:search-brand-templates` | `dataset: "non_empty"`, `query`: (optional) |
| **Dataset Schema** | `Canva:get-brand-template-dataset`| `template_id`: Template ID |
| **Autofill Single** | `Canva:autofill-design` | `template_id`, `data`, `title` |
| **Asset Upload** | `Canva:upload-asset-from-url` | `url`, `name` |
| **Comment Threads** | `Canva:list-comments` | `design_id` |
| **Comment Replies** | `Canva:list-replies` | `design_id`, `comment_id` |
| **Reply to Comment** | `Canva:reply-to-comment` | `design_id`, `comment_id`, `message` |
| **Resize Design** | `Canva:resize-design` | `design_id`, `design_type`, `user_intent` |
