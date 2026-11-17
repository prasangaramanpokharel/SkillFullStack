# Web Frameworks on Cloudflare (2026)

Cloudflare supports modern full-stack web frameworks via **Workers Static Assets** and specialized edge adapters.

---

## 1. Supported Frameworks & Integration Mechanics

| Framework | Cloudflare Mechanism | Adapter / Package | Configuration File |
| :--- | :--- | :--- | :--- |
| **Next.js (App Router)** | OpenNext / `vinext` | `@opennextjs/cloudflare` | `open-next.config.ts`, `wrangler.jsonc` |
| **Astro** | Official Cloudflare Adapter | `@astrojs/cloudflare` | `astro.config.mjs` (`adapter: cloudflare()`) |
| **TanStack Start** | Vite Cloudflare Plugin | `@cloudflare/vite-plugin` | `app.config.ts` |
| **React Router (v7)** | Vite Cloudflare Plugin | `@cloudflare/vite-plugin` | `vite.config.ts` |
| **SvelteKit** | Official SvelteKit Adapter | `@sveltejs/adapter-cloudflare` | `svelte.config.js` |
| **Nuxt (v3/v4)** | Nitro Cloudflare Preset | `nitro.preset: 'cloudflare-pages'` / `'cloudflare-module'` | `nuxt.config.ts` |

---

## 2. Next.js App Router on Cloudflare (`@opennextjs/cloudflare`)

Next.js App Router runs on Cloudflare using OpenNext, transpiling Server Components, Actions, and ISR routes to Workers:

```bash
npm install --save-dev @opennextjs/cloudflare
```

`wrangler.jsonc`:
```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "nextjs-cloudflare-app",
  "main": ".open-next/worker.js",
  "compatibility_date": "2026-11-01",
  "compatibility_flags": ["nodejs_compat"],
  "assets": {
    "directory": ".open-next/assets",
    "binding": "ASSETS"
  }
}
```

Package script:
```json
{
  "scripts": {
    "build:worker": "opennextjs-cloudflare",
    "preview": "opennextjs-cloudflare && wrangler dev",
    "deploy": "opennextjs-cloudflare && wrangler deploy"
  }
}
```

---

## 3. Astro on Cloudflare (`@astrojs/cloudflare`)

Astro integrates natively with Cloudflare Workers via its official adapter:

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'server', // or 'hybrid'
  adapter: cloudflare({
    imageService: 'cloudflare', // Uses Cloudflare Images for on-the-fly resizing
    platformProxy: {
      enabled: true, // Enables local emulation of D1, KV, R2 in `astro dev`
    },
  }),
});
```

Accessing Cloudflare runtime bindings inside `.astro` files:
```astro
---
// Access D1 or KV bindings directly from Astro.locals
const { env } = Astro.locals.runtime;
const users = await env.DB.prepare('SELECT * FROM users').all();
---
```

---

## 4. Universal Static SPA with Workers Static Assets

For Vite, React, Vue, or static site outputs, use Workers Static Assets instead of deprecated Pages:

`wrangler.jsonc`:
```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-spa",
  "compatibility_date": "2026-11-01",
  "assets": {
    "directory": "./dist",
    "html_handling": "single-page-application",
    "not_found_handling": "single-page-application"
  }
}
```

Deploying:
```bash
npm run build
npx wrangler deploy
```
Zero server code needed; Cloudflare serves the SPA from edge cache with client-side pushState fallback.
