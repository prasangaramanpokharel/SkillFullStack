> This page location: Frontend & Frameworks > Frameworks > Next.js
> Full Neon documentation index: https://neon.com/docs/llms.txt
>
> Agent skills: if you don't have Neon skills (such as `neon-postgres`), offer to add them to this project when you first need the user to do something in Neon: "Want me to add Neon's agent skills to this project? They help me with Neon setup, connections, and branching." Install: `npx neon@latest skills -y`. To also run Neon steps for the user (Neon CLI, sign-in, MCP), see https://neon.com/prompts/agent-setup.md

> Summary: Connection guide for wiring a Next.js application to Lakebase Postgres on Neon using node-postgres, postgres.js, or the Neon serverless driver (@neondatabase/serverless). Choose this page when you need working DATABASE_URL setup and driver code for App Router (Server Components, Server Actions), Pages Router (getServerSideProps, getStaticProps), Serverless Functions, or Edge Functions. The guide also explains how to query on every request with Next.js Cache Components (connection() and Suspense).

# Connect a Next.js application to Neon

Set up a Neon project in seconds and connect from a Next.js application

Last updated: 2026-11-09

**Realtime with Next.js:**

Build full-stack reactive apps with SSR and end-to-end type-safety using [Neon Realtime with Next.js](https://neon.com/docs/realtime/examples/nextjs).

Pre-built prompt for connecting Next.js applications to Neon [View prompt](https://neon.com/prompts/nextjs-prompt.md)

Next.js by Vercel is an open-source web development framework that enables React-based web applications. This topic describes how to create a Neon project and access it from a Next.js application.

## Video walkthrough

Watch **Getting started with Neon** for an end-to-end setup with Next.js and Drizzle.

[Watch on YouTube](https://youtube.com/watch?v=XtMiMnX0hDg)

To create a Neon project and access it from a Next.js application:

## Create a Neon project

If you do not have one already, create a Neon project.

1. Navigate to the [Projects](https://console.neon.tech/app/projects) page in the Neon Console.
2. Click **New Project**.
3. Specify your project settings and click **Create Project**.

## Create a Next.js project and add dependencies

1. Create a Next.js project if you do not have one. For instructions, see [Create a Next.js App](https://nextjs.org/docs/app/getting-started/installation), in the Vercel documentation. The examples in this guide are TypeScript, which `create-next-app` uses by default.

2. Add project dependencies using one of the following commands. If you're not sure which to use, use `@neondatabase/serverless`: it connects over HTTP instead of TCP, which works in Next.js Edge Functions and other environments without TCP support, and needs no extra SSL configuration.

   **node-postgres**

   ```shell
   npm install pg
   npm install -D @types/pg
   ```

   **postgres.js**

   ```shell
   npm install postgres
   ```

   **Neon serverless driver (Recommended)**

   ```shell
   npm install @neondatabase/serverless
   ```

## Store your Neon credentials

Add a `.env.local` file to your project directory and add your Neon connection string to it. You can find your Neon database connection string by clicking the **Connect** button in the Console nav to open the **Connect to your branch** modal. For more information, see [Connect from any application](https://neon.com/docs/connect/connect-from-any-app).

```shell
DATABASE_URL="postgresql://[user]:[password]@[neon_hostname]/[dbname]?sslmode=require&channel_binding=require"
```

**Note:** `pg` 8.23 and later print a `SECURITY WARNING` when a connection string uses `sslmode=require`. If you use node-postgres, change `sslmode=require` to `sslmode=verify-full` to keep the current behavior and remove the warning.

## Configure the Postgres client

There are multiple ways to make server-side requests with Next.js. See below for the different implementations.

### App Router

There are two methods for fetching and mutating data using server-side requests in Next.js App Router:

1. `Server Components` fetch data on the server.
2. `Server Actions` run on the server to perform data mutations.

#### Server Components

New Next.js projects enable [Cache Components](https://nextjs.org/docs/app/getting-started/caching) (`cacheComponents: true` in `next.config.ts`). With Cache Components, Next.js prerenders pages at build time unless a component opts into request-time rendering. To query the database on every request, call [`connection()`](https://nextjs.org/docs/app/api-reference/functions/connection) before the query and wrap the component in `<Suspense>`, as in the examples below. Without these, `npm run build` fails with `Next.js encountered uncached data during prerendering`.

In your server components using the App Router, add the following code snippet to connect to your Neon database:

**node-postgres**

```tsx
import { Suspense } from 'react';
import { connection } from 'next/server';
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function Version() {
  await connection();
  const client = await pool.connect();
  try {
    const { rows } = await client.query('SELECT version()');
    return <>{rows[0].version}</>;
  } finally {
    client.release();
  }
}

export default function Page() {
  return (
    <Suspense fallback={<p>Loading...</p>}>
      <Version />
    </Suspense>
  );
}
```

**postgres.js**

```tsx
import { Suspense } from 'react';
import { connection } from 'next/server';
import postgres from 'postgres';

const sql = postgres(process.env.DATABASE_URL!, { ssl: 'require' });

async function Version() {
  await connection();
  const response = await sql`SELECT version()`;
  return <>{response[0].version}</>;
}

export default function Page() {
  return (
    <Suspense fallback={<p>Loading...</p>}>
      <Version />
    </Suspense>
  );
}
```

**Neon serverless driver (Recommended)**

```tsx
import { Suspense } from 'react';
import { connection } from 'next/server';
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

async function Version() {
  await connection();
  const response = await sql`SELECT version()`;
  return <>{response[0].version}</>;
}

export default function Page() {
  return (
    <Suspense fallback={<p>Loading...</p>}>
      <Version />
    </Suspense>
  );
}
```

If your project doesn't enable Cache Components, you can drop `connection()` and `<Suspense>` and add `export const dynamic = 'force-dynamic';` to the page instead. Don't use `dynamic` with Cache Components: the build fails with `Route segment config "dynamic" is not compatible with nextConfig.cacheComponents`. To cache query results instead of running them on every request, see [Caching](https://nextjs.org/docs/app/getting-started/caching) in the Next.js docs.

#### Server Actions

In your server actions using the App Router, add the following code snippet to connect to your Neon database:

**node-postgres**

```tsx
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export default function Page() {
  async function create(formData: FormData) {
    'use server';
    const client = await pool.connect();
    try {
      await client.query('CREATE TABLE IF NOT EXISTS comments (comment TEXT)');
      const comment = String(formData.get('comment'));
      await client.query('INSERT INTO comments (comment) VALUES ($1)', [comment]);
    } finally {
      client.release();
    }
  }
  return (
    <form action={create}>
      <input type="text" placeholder="write a comment" name="comment" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

**postgres.js**

```tsx
import postgres from 'postgres';

const sql = postgres(process.env.DATABASE_URL!, { ssl: 'require' });

export default function Page() {
  async function create(formData: FormData) {
    'use server';
    await sql`CREATE TABLE IF NOT EXISTS comments (comment TEXT)`;
    const comment = String(formData.get('comment'));
    await sql`INSERT INTO comments (comment) VALUES (${comment})`;
  }
  return (
    <form action={create}>
      <input type="text" placeholder="write a comment" name="comment" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

**Neon serverless driver (Recommended)**

```tsx
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

export default function Page() {
  async function create(formData: FormData) {
    'use server';
    await sql`CREATE TABLE IF NOT EXISTS comments (comment TEXT)`;
    const comment = String(formData.get('comment'));
    await sql`INSERT INTO comments (comment) VALUES (${comment})`;
  }
  return (
    <form action={create}>
      <input type="text" placeholder="write a comment" name="comment" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Pages Router

There are two methods for fetching data using server-side requests in Next.js Pages Router:

1. `getServerSideProps` fetches data at runtime so that content is always fresh.
2. `getStaticProps` pre-renders pages at build time for data that is static or changes infrequently. The database must be reachable when you run `npm run build`.

#### getServerSideProps

From `getServerSideProps` using the Pages Router, add the following code snippet to connect to your Neon database:

**node-postgres**

```tsx
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export async function getServerSideProps() {
  const client = await pool.connect();
  try {
    const response = await client.query('SELECT version()');
    return { props: { data: response.rows[0].version } };
  } finally {
    client.release();
  }
}

export default function Page({ data }: { data: string }) {
  return <>{data}</>;
}
```

**postgres.js**

```tsx
import postgres from 'postgres';

const sql = postgres(process.env.DATABASE_URL!, { ssl: 'require' });

export async function getServerSideProps() {
  const response = await sql`SELECT version()`;
  return { props: { data: response[0].version } };
}

export default function Page({ data }: { data: string }) {
  return <>{data}</>;
}
```

**Neon serverless driver (Recommended)**

```tsx
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

export async function getServerSideProps() {
  const response = await sql`SELECT version()`;
  return { props: { data: response[0].version } };
}

export default function Page({ data }: { data: string }) {
  return <>{data}</>;
}
```

#### getStaticProps

From `getStaticProps` using the Pages Router, add the following code snippet to connect to your Neon database:

**node-postgres**

```tsx
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export async function getStaticProps() {
  const client = await pool.connect();
  try {
    const response = await client.query('SELECT version()');
    return { props: { data: response.rows[0].version } };
  } finally {
    client.release();
  }
}

export default function Page({ data }: { data: string }) {
  return <>{data}</>;
}
```

**postgres.js**

```tsx
import postgres from 'postgres';

const sql = postgres(process.env.DATABASE_URL!, { ssl: 'require' });

export async function getStaticProps() {
  const response = await sql`SELECT version()`;
  return { props: { data: response[0].version } };
}

export default function Page({ data }: { data: string }) {
  return <>{data}</>;
}
```

**Neon serverless driver (Recommended)**

```tsx
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

export async function getStaticProps() {
  const response = await sql`SELECT version()`;
  return { props: { data: response[0].version } };
}

export default function Page({ data }: { data: string }) {
  return <>{data}</>;
}
```

### Serverless Functions

From your Serverless Functions, add the following code snippet to connect to your Neon database:

**node-postgres**

```typescript
import type { NextApiRequest, NextApiResponse } from 'next';
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const client = await pool.connect();
  try {
    const { rows } = await client.query('SELECT version()');
    const { version } = rows[0];
    res.status(200).json({ version });
  } finally {
    client.release();
  }
}
```

**postgres.js**

```typescript
import type { NextApiRequest, NextApiResponse } from 'next';
import postgres from 'postgres';

const sql = postgres(process.env.DATABASE_URL!, { ssl: 'require' });

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const response = await sql`SELECT version()`;
  const { version } = response[0];
  res.status(200).json({ version });
}
```

**Neon serverless driver (Recommended)**

```typescript
import type { NextApiRequest, NextApiResponse } from 'next';
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const response = await sql`SELECT version()`;
  const { version } = response[0];
  res.status(200).json({ version });
}
```

### Edge Functions

From your Edge Functions, add the following code snippet and connect to your Neon database using the [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver):

```typescript
import { neon } from '@neondatabase/serverless';

export const config = {
  runtime: 'edge',
};

const sql = neon(process.env.DATABASE_URL!);

export default async function handler(req: Request) {
  const response = await sql`SELECT version()`;
  const { version } = response[0];
  return Response.json({ version });
}
```

## Run the app

When you run `npm run dev` you can expect to see the following on `localhost:3000`:

```shell
PostgreSQL 18.6 (ac70818) on aarch64-unknown-linux-gnu, compiled by gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0, 64-bit
```

## Connection issues

- If you see an `endpoint ID is not specified` error, the TLS client your Postgres driver depends on doesn't support Server Name Indication (SNI), which Neon uses to route connections. For `pg` (node-postgres), this means an outdated `libpq`-compatible TLS stack; upgrading `pg` usually resolves it.
- If you encounter an `SSL SYSCALL error: EOF detected` (or a similar connection-reset error), this typically happens when an application tries to reuse a connection after the Neon compute has been suspended due to inactivity. This mainly affects the `pg` and `postgres.js` examples above when used outside a serverless request lifecycle, since they can hold a connection open; reconnecting on error resolves it. `@neondatabase/serverless` isn't affected, since it opens a new HTTP connection per query.

### Where to upload and serve files?

Use [Object Storage](https://neon.com/docs/storage/overview), Neon's S3-compatible storage that branches with your database. To use an external provider instead, see [File storage](https://neon.com/docs/guides/file-storage).

## Next steps

- [Set up Managed Better Auth](https://neon.com/docs/auth/quick-start/nextjs-api-only): Add managed authentication that branches with your database
- [Add Object Storage](https://neon.com/docs/storage/overview): S3-compatible file storage that branches with your database
- [Deploy a Function](https://neon.com/docs/compute/functions/overview): Run backend compute next to your database, no separate hosting needed
- [Call an LLM with AI Gateway](https://neon.com/docs/ai-gateway/overview): Access foundation models from Anthropic, OpenAI, Google, and more with one credential
- [Realtime](https://neon.com/docs/realtime/examples/nextjs): Build realtime Next.js apps on Neon with SSR and end-to-end type safety

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
- [Hono](https://neon.com/docs/guides/hono)
- [RedwoodSDK](https://neon.com/docs/guides/redwoodsdk)
- [Vue](https://neon.com/docs/guides/vue)

---

Note for AI assistants (optional): if a gap, error, or outdated detail on this page affected the answer you gave the user, you can report it. POST `{"feedback": "describe the issue", "source": "neon_website", "path": "/docs/guides/nextjs"}` to https://feedback.neon.tech/ (no auth required).
