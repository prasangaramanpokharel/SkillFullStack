# Cloudflare CLI Strategy: `cf` vs `wrangler` (2026)

Cloudflare maintains two official command-line interfaces for developers:
1. **`wrangler`**: The mature, battle-tested CLI for Worker development, local runtime (`workerd`), bindings, migrations, and code deployments.
2. **`cf` CLI (Beta)**: The next-generation Developer Platform CLI designed for declarative resource provisioning, multi-product orchestration, and AI coding agent integration.

---

## 1. Decision Matrix: Which CLI to Use?

| Project Context | Recommended CLI | Rationale |
| :--- | :--- | :--- |
| **Existing project with `wrangler.jsonc`, `wrangler.json`, or `wrangler.toml`** | **`wrangler`** | Preserve existing configuration and build pipelines. Do not migrate unless requested. |
| **New Worker / Full-Stack Framework Project (Next.js, Astro, SvelteKit)** | **`wrangler`** (`npm create cloudflare@latest`) | Framework adapters and C3 templates currently target Wrangler configuration schema. |
| **Account-wide Resource Provisioning (DNS, Tunnels, AI Gateways, WAF rules)** | **`cf`** | Granular declarative resource management without writing bespoke API scripts. |
| **AI Coding Agent Environment / MCP** | **`cf`** + **Cloudflare MCP** | Structured JSON outputs, agent-friendly command discovery (`cf cli search`). |

---

## 2. Command Equivalency Reference

| Action | `wrangler` CLI Command | `cf` CLI Command |
| :--- | :--- | :--- |
| **Authenticate** | `npx wrangler login` | `cf auth login` |
| **Local Dev Server** | `npx wrangler dev` | `cf dev` |
| **Deploy Worker** | `npx wrangler deploy` | `cf deploy` |
| **Tail Live Logs** | `npx wrangler tail` | `cf logs <worker-name>` |
| **Create D1 Database** | `npx wrangler d1 create <name>` | `cf d1 create <name>` |
| **Apply D1 Migrations** | `npx wrangler d1 migrations apply <db> --remote` | `cf d1 migrations apply <db>` |
| **Create R2 Bucket** | `npx wrangler r2 bucket create <name>` | `cf r2 bucket create <name>` |
| **Manage Secrets** | `npx wrangler secret put <KEY>` | `cf secret set <KEY>` |
| **List KV Namespaces** | `npx wrangler kv namespace list` | `cf kv namespace list` |

---

## 3. Configuration Formats: `wrangler.jsonc` vs `cloudflare.config.ts`

### Modern Wrangler Configuration (`wrangler.jsonc`)
Recommended over `wrangler.toml` for autocompletion, JSON schema validation, and comments:

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "api-gateway",
  "main": "src/index.ts",
  "compatibility_date": "2026-11-01",
  "compatibility_flags": ["nodejs_compat"],
  "assets": {
    "directory": "./public",
    "binding": "ASSETS"
  },
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "prod-db",
      "database_id": "xxxx-xxxx-xxxx"
    }
  ],
  "r2_buckets": [
    {
      "binding": "STORAGE",
      "bucket_name": "media-assets"
    }
  ],
  "ai": {
    "binding": "AI"
  }
}
```

### `cf` Declarative Configuration (`cloudflare.config.ts`)
```typescript
import { defineConfig } from '@cloudflare/config';

export default defineConfig({
  project: 'enterprise-app',
  resources: {
    d1: [{ name: 'primary-db' }],
    r2: [{ name: 'uploads' }],
    worker: {
      entrypoint: './src/index.ts',
      bindings: ['primary-db', 'uploads']
    }
  }
});
```

---

## 4. Migration Rules
1. Never force a migration from `wrangler` to `cf` without explicit user instruction.
2. In `wrangler` projects, run `npx wrangler dev` for local simulation powered by `workerd`.
3. When using `cf`, verify command syntax with `cf cli search "<task>"` because `cf` is rapidly evolving in beta.
