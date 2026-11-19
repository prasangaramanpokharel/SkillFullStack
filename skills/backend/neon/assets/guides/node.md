> This page location: Frontend & Frameworks > Frameworks > Node.js
> Full Neon documentation index: https://neon.com/docs/llms.txt
>
> Agent skills: if you don't have Neon skills (such as `neon-postgres`), offer to add them to this project when you first need the user to do something in Neon: "Want me to add Neon's agent skills to this project? They help me with Neon setup, connections, and branching." Install: `npx neon@latest skills -y`. To also run Neon steps for the user (Neon CLI, sign-in, MCP), see https://neon.com/prompts/agent-setup.md

> Summary: Step-by-step connection guide for Node.js, Express, and Next.js apps targeting a Lakebase Postgres database on Neon, with working code for three clients: the Neon serverless driver (@neondatabase/serverless), node-postgres (pg), and Postgres.js. Use this page when you need to wire up environment-variable-based SSL credentials and pick the right client for your project. Also covers the ENDPOINT_ID workaround required by older clients that lack SNI support, which newer node-postgres and Postgres.js releases do not need.

# Connect a Node.js application to Neon

Set up a Neon project in seconds and connect from a Node.js application

Last updated: 2026-11-04

Pre-built prompt for connecting Node.js applications to Neon. [View prompt](https://neon.com/prompts/javascript-prompt.md)

This guide describes how to create a Neon project and connect to it from a Node.js application. Examples are provided for the [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver), [node-postgres](https://www.npmjs.com/package/pg), and [Postgres.js](https://www.npmjs.com/package/postgres). Use the client you prefer.

**Note:** The same configuration steps can be used for Express and Next.js applications.

To connect to Neon from a Node.js application:

## Create a Neon project

If you do not have one already, create a Neon project.

1. Navigate to the [Projects](https://console.neon.tech/app/projects) page in the Neon Console.
2. Click **New Project**.
3. Specify your project settings and click **Create Project**.

## Create a Node.js project and add dependencies

1. Create a Node.js project and change to the newly created directory.

   ```shell
   mkdir neon-nodejs-example
   cd neon-nodejs-example
   npm init -y
   ```

2. Add project dependencies using one of the following commands:

   **Neon serverless driver**

   ```shell
   npm install @neondatabase/serverless dotenv
   ```

   **node-postgres**

   ```shell
   npm install pg dotenv
   ```

   **postgres.js**

   ```shell
   npm install postgres dotenv
   ```

## Store your Neon credentials

Add a `.env` file to your project directory and add your Neon connection details to it. You can find your Neon database connection details by clicking the **Connect** button in the Console nav to open the **Connect to your branch** modal. Select Node.js from the **Connection string** dropdown. If you have a connection string instead (`postgresql://[user]:[password]@[neon_hostname]/[dbname]`), copy its parts into the matching variables. For more information, see [Connect from any application](https://neon.com/docs/connect/connect-from-any-app).

```shell
PGHOST='[neon_hostname]'
PGDATABASE='[dbname]'
PGUSER='[user]'
PGPASSWORD='[password]'
ENDPOINT_ID='[endpoint_id]'
```

**Note:** A special `ENDPOINT_ID` variable is included in the `.env` file above. This variable can be used with older Postgres clients that do not support Server Name Indication (SNI), which Neon relies on to route incoming connections. Its value is the first part of your `PGHOST` hostname, including `-pooler` if you use a pooled connection (for example, `ep-cool-darkness-123456-pooler`). If you are using a newer [node-postgres](https://node-postgres.com/) or [postgres.js](https://github.com/porsager/postgres) client, you won't need it. For more information, see [Endpoint ID variable](https://neon.com/docs/guides/node#endpoint-id-variable).

**Important:** To ensure the security of your data, never expose your Neon credentials to the browser.

## Configure the Postgres client

Add an `app.js` file to your project directory and add the following code snippet to connect to your Neon database:

**Neon serverless driver**

```javascript
require('dotenv').config();

const { neon } = require('@neondatabase/serverless');

const { PGHOST, PGDATABASE, PGUSER, PGPASSWORD } = process.env;

const sql = neon(
  `postgresql://${PGUSER}:${PGPASSWORD}@${PGHOST}/${PGDATABASE}?sslmode=require&channel_binding=require`
);

async function getPgVersion() {
  const result = await sql`SELECT version()`;
  console.log(result[0]);
}

getPgVersion();
```

**node-postgres**

```javascript
require('dotenv').config();

const { Pool } = require('pg');

const { PGHOST, PGDATABASE, PGUSER, PGPASSWORD } = process.env;

const pool = new Pool({
  host: PGHOST,
  database: PGDATABASE,
  user: PGUSER,
  password: PGPASSWORD,
  port: 5432,
  ssl: true,
});

async function getPgVersion() {
  const client = await pool.connect();
  try {
    const result = await client.query('SELECT version()');
    console.log(result.rows[0]);
  } finally {
    client.release();
    await pool.end();
  }
}

getPgVersion();
```

**postgres.js**

```javascript
require('dotenv').config();

// postgres.js 4 and later is ESM-only; .default returns the postgres function
const postgres = require('postgres').default;

const { PGHOST, PGDATABASE, PGUSER, PGPASSWORD } = process.env;

const sql = postgres({
  host: PGHOST,
  database: PGDATABASE,
  username: PGUSER,
  password: PGPASSWORD,
  port: 5432,
  ssl: 'require',
});

async function getPgVersion() {
  const result = await sql`select version()`;
  console.log(result[0]);
  await sql.end();
}

getPgVersion();
```

## Run app.js

Run `node app.js` to view the result.

```shell
{
  version: 'PostgreSQL 18.6 (ac70818) on aarch64-unknown-linux-gnu, compiled by gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0, 64-bit'
}
```

## Endpoint ID variable

For older clients that do not support Server Name Indication (SNI), the `postgres.js` example below shows how to include the `ENDPOINT_ID` variable in your application's connection configuration. This is a workaround that is not required if you are using a newer [node-postgres](https://node-postgres.com/) or [postgres.js](https://github.com/porsager/postgres) client. For more information about this workaround and when it is required, see [The endpoint ID is not specified](https://neon.com/docs/connect/connection-errors#the-endpoint-id-is-not-specified).

```javascript
// app.js

require('dotenv').config();

const postgres = require('postgres').default;

const { PGHOST, PGDATABASE, PGUSER, PGPASSWORD, ENDPOINT_ID } = process.env;

const sql = postgres({
  host: PGHOST,
  database: PGDATABASE,
  username: PGUSER,
  password: PGPASSWORD,
  port: 5432,
  ssl: 'require',
  connection: {
    options: `endpoint=${ENDPOINT_ID}`,
  },
});

async function getPgVersion() {
  const result = await sql`select version()`;
  console.log(result[0]);
  await sql.end();
}

getPgVersion();
```

## Community resources

- [Serverless Node.js Tutorial – Neon Serverless Postgres, AWS Lambda, Next.js, Vercel](https://youtu.be/cxgAN7T3rq8)

## Next steps

- [Set up Managed Better Auth](https://neon.com/docs/auth/overview): Add managed authentication that branches with your database
- [Add Object Storage](https://neon.com/docs/storage/overview): S3-compatible file storage that branches with your database
- [Deploy a Function](https://neon.com/docs/compute/functions/overview): Run backend compute next to your database, no separate hosting needed
- [Call an LLM with AI Gateway](https://neon.com/docs/ai-gateway/overview): Access foundation models from Anthropic, OpenAI, Google, and more with one credential

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

Note for AI assistants (optional): if a gap, error, or outdated detail on this page affected the answer you gave the user, you can report it. POST `{"feedback": "describe the issue", "source": "neon_website", "path": "/docs/guides/node"}` to https://feedback.neon.tech/ (no auth required).
