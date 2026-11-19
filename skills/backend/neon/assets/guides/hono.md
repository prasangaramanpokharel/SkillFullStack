> This page location: Frontend & Frameworks > Frameworks > Hono
> Full Neon documentation index: https://neon.com/docs/llms.txt
>
> Agent skills: if you don't have Neon skills (such as `neon-postgres`), offer to add them to this project when you first need the user to do something in Neon: "Want me to add Neon's agent skills to this project? They help me with Neon setup, connections, and branching." Install: `npx neon@latest skills -y`. To also run Neon steps for the user (Neon CLI, sign-in, MCP), see https://neon.com/prompts/agent-setup.md

> Summary: To connect a Hono app to Lakebase Postgres on Neon, create a Neon project, run neon link to write DATABASE_URL to your env file, and query it from a Hono route with node-postgres, postgres.js, or the Neon serverless driver. Covers Hono 4 on Node.js 24 with TypeScript: loading env files with Node's --env-file-if-exists flags instead of dotenv, an optional Neon development branch and agent skills, deployment, troubleshooting, and Neon's other backend services from Hono.

# Connect a Hono application to Neon

Create a Neon project, link it with neon link, and query Lakebase Postgres from a Hono route with node-postgres, postgres.js, or the Neon serverless driver

Last updated: 2026-11-18

This prompt is for pasting into an AI coding agent. If it brought you to this page, you are already following it, so continue with the rest of the page.

```text
Connect my Hono app to Neon.

- Fetch https://neon.com/prompts/agent-setup.md and follow it.

- Offer to install Hono's agent skill with `npx skills add honojs/skills --skill hono -a <your agent id> -y`. Look up Hono docs at https://hono.dev/llms.txt

- Fetch Neon's Hono guide and follow it: https://neon.com/docs/guides/hono.md
- Keep my app's runtime and Hono version. If it doesn't run on Node.js, or it uses `@hono/node-server` 1.x, follow the guide's notes for them.
- Ask me before you pick or create a Neon project.
- Finish by showing me the Postgres version from the running server.
- If my app needs sign-in, file uploads, long-running or scheduled work, LLM calls, or live updates, suggest the matching service from the guide's "Add more of your backend" section.
```

## Create a Hono app

Create a project for Hono, a lightweight web framework for Node.js and other JavaScript runtimes, with `npm create hono@latest` and its `nodejs` template. You need [Node.js](https://nodejs.org/en/download) 24.10 or later (or 22.21), for the `--env-file-if-exists` flag the `dev` script uses. Skip this step if you already have a Hono app.

```bash filename="Terminal"
npm create hono@latest my-app -- --template nodejs --pm npm --install
cd my-app
printf '\n.env.local\n' >> .gitignore
```

This creates a TypeScript project and installs its dependencies without prompts.

- The template uses Hono 4 and `@hono/node-server` 2.
- Its `.gitignore` covers `.env` and `node_modules`, but not `.env.local`, so the `printf` line adds it. That keeps the connection string out of git.
- The template doesn't create a git repository. Run `git init` if you want one.

For other runtimes, see [Quick Start](https://hono.dev/docs/getting-started/basic) in the Hono documentation. The steps below use the Node.js template.

If you're adding Neon to an existing Hono app:

- Keep its runtime and Hono version. The steps are for Node.js; for a Bun app, see the [Bun guide](https://neon.com/docs/guides/bun).
- Make sure its `.gitignore` excludes `.env.local` before you link it (the `printf` line in the command does this).
- The examples use `@hono/node-server` 2.x. If your app uses 1.x, keep your own `serve` call, or upgrade with `npm install @hono/node-server@^2`.

## Add Neon's agent skills (optional)

Run `npx neon@latest skills` from your project directory to add Neon's [agent skills](https://neon.com/docs/ai/agent-skills), which teach your AI coding agent how to use the Neon CLI, branches, and Neon's backend services. The agent prompt at the top of this page installs them, so skip this step if you used it:

```bash filename="Terminal"
npx neon@latest skills
```

To also connect the [Neon MCP Server](https://neon.com/docs/ai/neon-mcp-server), run `npx neon@latest mcp`.

Hono publishes its docs for AI agents at [hono.dev/llms.txt](https://hono.dev/llms.txt), and an agent skill you can install with `npx skills add honojs/skills --skill hono`. The agent prompt has your agent look up Hono's docs there.

## Create a Neon project

Create a Neon project in a region that runs every Neon backend service: `aws-us-east-2` (Ohio), `aws-us-east-1` (N. Virginia), `aws-eu-central-1` (Frankfurt), or `aws-ap-southeast-1` (Singapore). Postgres and Managed Better Auth run in every region; Object Storage, Neon Functions, the AI Gateway, and Realtime run in those four (see [product availability](https://neon.com/docs/introduction/regions#product-availability)). Skip this step if you already have a Neon project you want to use.

**Neon CLI**

Install the [Neon CLI](https://neon.com/docs/cli/install), sign in, and create the project:

```bash filename="Terminal"
npm i -g neon@latest
neon login
neon projects create --name my-app --region-id aws-us-east-2 --no-secrets
```

`--region-id` sets the region. `--no-secrets` keeps the connection string out of the output, since the next step pulls it into your env file. Pass `--org-id` to choose the organization (find IDs with `neon orgs list`).

**API**

Create an [API key](https://console.neon.tech/app/settings/api-keys), export it, then create the project in your organization:

```bash filename="Terminal"
export NEON_API_KEY=napi_...

curl -X POST https://console.neon.tech/api/v2/projects \
  -H "Authorization: Bearer $NEON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project": {"name": "my-app", "region_id": "aws-us-east-2", "org_id": "<org-id>"}}'
```

The response includes the project's connection string in `connection_uris[0].connection_uri`. See [Create a project with the API](https://neon.com/docs/manage/projects#create-a-project-with-the-api) for the other options.

**Console**

Go to the [Projects](https://console.neon.tech/app/projects) page in the Neon Console, click **New Project**, and pick one of the regions above.

## Connect your app to the project

Get a `DATABASE_URL` into an env file. Hono doesn't read env files itself: the `dev` script in [Run the app](https://neon.com/docs/guides/hono#run-the-app) loads them with Node's `--env-file-if-exists` flags, so you don't need `dotenv`.

**Neon CLI**

From your app's directory, link it to the Neon project (install the [Neon CLI](https://neon.com/docs/cli/install) and run `neon login` first if you haven't):

```bash filename="Terminal"
neon link
```

`neon link` prompts you to pick an organization and a project, or to create a new project. Then it:

- writes a `.neon` file with the project context;
- pins a branch (pass `--branch` to choose one);
- pulls that branch's `DATABASE_URL` into `.env.local`, or into `.env` if your project already has one;
- offers to create a [`neon.ts`](https://neon.com/docs/reference/neon-ts) file, which is optional and covered in [Add more of your backend](https://neon.com/docs/guides/hono#add-more-of-your-backend).

To skip the prompts, pass `-y` with `--org-id` and `--project-id`, or with `--org-id`, `--project-name`, and `--region-id` to create a project. Find IDs with `neon orgs list` and `neon projects list --org-id <org-id>`.

**Without the CLI**

Copy the connection string from **Connect** in the Console nav, or from the API response, and add it to a `.env.local` file in your project directory. For more information, see [Connect from any application](https://neon.com/docs/connect/connect-from-any-app).

```shell filename=".env.local"
DATABASE_URL="postgresql://[user]:[password]@[neon_hostname]/[dbname]?sslmode=require&channel_binding=require"
```

The optional development branch step and [Add more of your backend](https://neon.com/docs/guides/hono#add-more-of-your-backend) use the Neon CLI. To use them, run `neon link` in this directory.

Keep `DATABASE_URL` in only one env file: if `.env` and `.env.local` both have it, `.env.local` wins.

## Work on a development branch (optional)

Run `neon checkout dev --create` to develop on a branch of your database instead of the default branch, where production data usually lives. The default branch is `main` for projects created with the CLI or API, and `production` for projects created in the Console. A [branch](https://neon.com/docs/introduction/branching) starts from its parent's data and schema without copying them (copy-on-write: only the changes you make are stored), so you can change it freely:

```bash filename="Terminal"
neon checkout dev --create
```

This creates the `dev` branch, pins it in `.neon`, and pulls its `DATABASE_URL` into the same env file, so your app now uses the branch. To switch back, run `neon checkout main` (or `production`).

## Install a Postgres driver

Install one of three Postgres drivers. For a Hono server on Node.js, use [node-postgres](https://node-postgres.com) (`pg`) or [postgres.js](https://github.com/porsager/postgres); both keep a pool of TCP connections open. For serverless and edge hosts, use the [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver), which queries over HTTP. See [Choosing your connection method](https://neon.com/docs/connect/choose-connection).

**node-postgres**

```bash
npm install pg
npm install -D @types/pg
```

**postgres.js**

```bash
npm install postgres
```

**Neon serverless driver**

```bash
npm install @neondatabase/serverless
```

If you use node-postgres, current `pg` versions print a `SECURITY WARNING` for `sslmode=require`. Change it to `sslmode=verify-full` in your env file to keep the same behavior without the warning. `neon link`, `neon checkout`, `neon env pull`, and `neon deploy` write `sslmode=require` again, so repeat the change after you run them.

## Create the database client

Create one database client for the whole app in `src/db.ts`, and import it in your routes. The file reads `DATABASE_URL` from `process.env`, throws `DATABASE_URL is not set` at startup if the variable is missing, and exports `pool` (node-postgres) or `sql` (postgres.js and the Neon serverless driver):

**node-postgres**

```typescript filename="src/db.ts"
import pg from 'pg';

const url = process.env.DATABASE_URL;
if (!url) throw new Error('DATABASE_URL is not set');

export const pool = new pg.Pool({ connectionString: url });

// An idle connection can drop, for example when the compute scales to zero.
// Without a listener, the pool's error event stops the app.
pool.on('error', (error) => console.error('Postgres pool error:', error.message));
```

**postgres.js**

```typescript filename="src/db.ts"
import postgres from 'postgres';

const url = process.env.DATABASE_URL;
if (!url) throw new Error('DATABASE_URL is not set');

export const sql = postgres(url);
```

**Neon serverless driver**

```typescript filename="src/db.ts"
import { neon } from '@neondatabase/serverless';

const url = process.env.DATABASE_URL;
if (!url) throw new Error('DATABASE_URL is not set');

export const sql = neon(url);
```

## Query the database from a route

Query Postgres from a Hono route in `src/index.ts`, using the `pool` or `sql` client that `src/db.ts` exports. The route runs `SELECT version()` and returns the result as JSON. The template's `/` route returns "Hello Hono!"; replace it with the code below.

If your app already has a `/` route, add only the handler as a new route, such as `app.get('/neon', ...)`. Keep your other routes, middleware, and your existing `serve` call; a second `serve` call fails with `EADDRINUSE`.

**node-postgres**

```typescript filename="src/index.ts"
import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import { pool } from './db.js';

const app = new Hono();

app.get('/', async (c) => {
  const { rows } = await pool.query('SELECT version()');
  return c.json({ version: rows[0].version });
});

serve({ fetch: app.fetch, port: Number(process.env.PORT) || 3000 }, (info) => {
  console.log(`Listening on http://localhost:${info.port}`);
});
```

**postgres.js**

```typescript filename="src/index.ts"
import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import { sql } from './db.js';

const app = new Hono();

app.get('/', async (c) => {
  const [row] = await sql`SELECT version()`;
  return c.json({ version: row?.version });
});

serve({ fetch: app.fetch, port: Number(process.env.PORT) || 3000 }, (info) => {
  console.log(`Listening on http://localhost:${info.port}`);
});
```

**Neon serverless driver**

```typescript filename="src/index.ts"
import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import { sql } from './db.js';

const app = new Hono();

app.get('/', async (c) => {
  const [row] = await sql`SELECT version()`;
  return c.json({ version: row?.version });
});

serve({ fetch: app.fetch, port: Number(process.env.PORT) || 3000 }, (info) => {
  console.log(`Listening on http://localhost:${info.port}`);
});
```

The route doesn't need `try...catch`. If a handler throws, Hono logs the error and returns a `500` response, and the server keeps running.

## Run the app

Change the template's `dev` script so it loads your env files, then start the app. The new `dev` script still restarts the server when you edit a file. The template's `build` and `start` scripts stay as they are:

```bash filename="Terminal"
npm pkg set scripts.dev="tsx watch --env-file-if-exists=.env --env-file-if-exists=.env.local src/index.ts"
npm run dev
```

Node skips an env file that doesn't exist, so it's fine to have only one of them. `--env-file-if-exists` is stable from Node.js 24.10 and 22.21. Open [localhost:3000](http://localhost:3000), or the port in `PORT` if you set one. The response shows your Postgres version, confirming the connection:

```json
{"version":"PostgreSQL 18.6 (fd34222) on aarch64-unknown-linux-gnu, compiled by gcc ..."}
```

## Deploy

To deploy to a Node.js host, set `DATABASE_URL` in the host's environment, build with `npm run build`, and start with `npm start`. These steps use the Node.js template's `serve` entry point. For Cloudflare Workers, Vercel, Netlify, and other runtimes, follow Hono's [getting started guides](https://hono.dev/docs/getting-started/basic) for the entry point, and use the Neon serverless driver unless the host keeps connections open.

- Use your default branch for production. Get its pooled connection string, which goes through Neon's connection pooler and suits many short-lived connections, with `neon connection-string main --pooled` (or `production`), or from **Connect** in the Console.

- `npm start` doesn't load env files, so the host's environment must set `DATABASE_URL`.

- To try the build locally with your env files, run `node --env-file-if-exists=.env --env-file-if-exists=.env.local dist/index.js`. A variable set in your shell takes priority over the env files.

- The app listens on `PORT`, which most Node.js hosts set for you.

- The `serve` call returns the Node.js server. Hono's [Node.js guide](https://hono.dev/docs/getting-started/nodejs) shows how to close it on `SIGINT` and `SIGTERM`, so the host can stop the app cleanly.

- Pick the driver for your host:

  - node-postgres or postgres.js: long-running servers, [Vercel Fluid compute](https://vercel.com/docs/functions/fluid-compute) (which reuses function instances across requests), and Cloudflare Workers with [Hyperdrive](https://developers.cloudflare.com/hyperdrive/) (Cloudflare's connection pooler).
  - The Neon serverless driver: serverless platforms that don't keep connections open, such as Netlify Functions or Cloudflare Workers without Hyperdrive.

  See [Choosing your connection method](https://neon.com/docs/connect/choose-connection).

- On Vercel, the [Neon integration](https://neon.com/docs/guides/vercel-overview) sets `DATABASE_URL` for you and can create a Neon branch for each preview deployment.

## Add more of your backend

Add a Neon backend service to your Hono app with [`neon config add`](https://neon.com/docs/cli/config#add), then provision it with [`neon deploy`](https://neon.com/docs/cli/deploy). Each service branches with your database, so a `dev` branch gets its own copy of the service's data. Object Storage, Neon Functions, the AI Gateway, and Realtime need a project in a [supported region](https://neon.com/docs/guides/hono#create-a-neon-project). For example, to add an Object Storage bucket:

```bash filename="Terminal"
neon config add bucket uploads
neon deploy
```

`neon config add` creates a [`neon.ts`](https://neon.com/docs/reference/neon-ts) file at your project root if you don't have one, installs `@neon/config` and `@neon/env`, and declares the service. `neon deploy` provisions it and writes its variables to your env file (`.env` if it exists, otherwise `.env.local`). The `dev` script loads them into `process.env`, so SDKs that read `process.env` find them. Set them on your host too.

Managed Better Auth
: Sign-up, sign-in, and sessions stored in your database.
: Add it with `neon config add auth`. See [Managed Better Auth](https://neon.com/docs/auth/overview).

Object Storage
: S3-compatible buckets for uploads and files.
: Add a bucket with `neon config add bucket <name>`. In Hono, use it from route handlers. See [Object Storage](https://neon.com/docs/storage/overview).

AI Gateway
: One credential for models from Anthropic, OpenAI, Google, and more.
: Add it with `neon config add ai-gateway`. In Hono, call models from route handlers. See [AI Gateway](https://neon.com/docs/ai-gateway/overview).

Neon Functions
: Long-running Node.js compute next to your database.
: Add one with `neon config add function <slug>`, which also creates its handler file in `functions/`. Use a function for work that outlasts a request on your Hono host, such as agents and webhooks, and call it with `fetch`. See [Neon Functions](https://neon.com/docs/compute/functions/overview).

Realtime (beta)
: Live SQL query subscriptions.
: Add it with `neon config add realtime`. In a Hono route, [seal](https://neon.com/docs/realtime/guides/queries#sealing-queries) the live query with `@neon/realtime/server` and `NEON_REALTIME_SECRET`: sealing signs the query so the browser can subscribe to it but can't change it. Return the sealed query, and `NEON_REALTIME_URL`, from the route; the browser subscribes with `@neon/realtime/client`. Keep the secret on the server. See [Realtime](https://neon.com/docs/realtime/overview).

To declare several services at once before you have a `neon.ts`, run `neon config init --services auth,functions,realtime`, or edit the file directly. With every service declared, it looks like this. The comments list the variables each service adds:

```typescript filename="neon.ts"
import { defineConfig } from '@neon/config/v1';

export default defineConfig({
  auth: true, // NEON_AUTH_BASE_URL, NEON_AUTH_JWKS_URL
  buckets: {
    uploads: {}, // AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ENDPOINT_URL_S3, AWS_REGION
  },
  aiGateway: true, // NEON_AI_GATEWAY_TOKEN, NEON_AI_GATEWAY_BASE_URL
  functions: {
    jobs: { name: 'Jobs', source: './functions/jobs.ts' }, // NEON_FUNCTION_HOST_SUFFIX
  },
  preview: {
    realtime: true, // NEON_REALTIME_URL, NEON_REALTIME_SECRET
  },
});
```

To skip `neon.ts`, use each service's own CLI commands, such as [`neon buckets create`](https://neon.com/docs/cli/buckets) or [`neon realtime enable`](https://neon.com/docs/cli/realtime).

## Troubleshooting

`Error: DATABASE_URL is not set`
: The app started without `DATABASE_URL`. Locally, start it with `npm run dev` so the env files load, and check that one of them has the variable, or run `neon env pull`. With `npm start` or on a host, set it in the environment.

`Error: listen EADDRINUSE: address already in use :::3000`
: Another server, often an earlier `npm run dev`, is still using the port. Stop it, or set `PORT` to use another port.

`endpoint ID is not specified`
: The client doesn't send Server Name Indication (SNI), which Neon uses to route connections. Current node-postgres and postgres.js send SNI, so this usually means an older client or a libpq older than Postgres 14. If upgrading doesn't fix it, append `&options=endpoint%3D<endpoint-id>` to `DATABASE_URL` (use `?` instead of `&` if the URL has no query string), with the endpoint ID from your connection string. See [The endpoint ID is not specified](https://neon.com/docs/connect/connection-errors#the-endpoint-id-is-not-specified).

`SSL SYSCALL error: EOF detected`, or a similar connection-reset error
: The app reused a connection after the Neon compute was suspended for inactivity. This mainly affects long-running servers that keep a connection pool open, like the node-postgres example. The `pool.on('error')` listener in `src/db.ts` keeps it from stopping the app. The request that hits the closed connection can fail with a `500`; the next request opens a new connection, so retrying the request resolves it. The Neon serverless driver isn't affected, since it opens a new HTTP connection per query.

`500 Internal Server Error` from a route
: A handler threw an error, and Hono logged it in the terminal where the app runs. Read the logged error for the cause, such as a `DATABASE_URL` that doesn't point to your project.

## Next steps

- **Create your first table:** run `neon psql` in your project directory to open a SQL shell on your linked branch, or use an ORM such as [Drizzle](https://neon.com/docs/guides/drizzle) or [Prisma](https://neon.com/docs/guides/prisma) to manage your schema with migrations.
- [Build a full backend](https://neon.com/docs/get-started/full-backend-quickstart): Postgres, Object Storage, and a Neon Function declared in one `neon.ts`.
- [Branching](https://neon.com/docs/introduction/branching): Give each preview deployment or pull request its own branch of your database.

---

## Related docs (Frameworks)

- [Astro](https://neon.com/docs/guides/astro)
- [Bun](https://neon.com/docs/guides/bun)
- [Entity Framework](https://neon.com/docs/guides/dotnet-entity-framework)
- [Encore](https://neon.com/docs/guides/encore)
- [Express](https://neon.com/docs/guides/express)
- [Medusa.js](https://neon.com/docs/guides/medusajs)
- [Micronaut Kotlin](https://neon.com/docs/guides/micronaut-kotlin)
- [NestJS](https://neon.com/docs/guides/nestjs)
- [Next.js](https://neon.com/docs/guides/nextjs)
- [Node.js](https://neon.com/docs/guides/node)
- [Nuxt](https://neon.com/docs/guides/nuxt)
- [Phoenix](https://neon.com/docs/guides/phoenix)
- [Quarkus (JDBC)](https://neon.com/docs/guides/quarkus-jdbc)
- [Quarkus (Reactive)](https://neon.com/docs/guides/quarkus-reactive)
- [React](https://neon.com/docs/guides/react)
- [React Router](https://neon.com/docs/guides/react-router)
- [Reflex](https://neon.com/docs/guides/reflex)
- [Remix](https://neon.com/docs/guides/remix)
- [SolidStart](https://neon.com/docs/guides/solid-start)
- [Sveltekit](https://neon.com/docs/guides/sveltekit)
- [Symfony](https://neon.com/docs/guides/symfony)
- [TanStack Start](https://neon.com/docs/guides/tanstack-start)
- [RedwoodSDK](https://neon.com/docs/guides/redwoodsdk)
- [Vue](https://neon.com/docs/guides/vue)

---

Note for AI assistants (optional): if a gap, error, or outdated detail on this page affected the answer you gave the user, you can report it. POST `{"feedback": "describe the issue", "source": "neon_website", "path": "/docs/guides/hono"}` to https://feedback.neon.tech/ (no auth required).
