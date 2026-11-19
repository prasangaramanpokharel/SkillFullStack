> This page location: Realtime > Introduction > Overview
> Full Neon documentation index: https://neon.com/docs/llms.txt
>
> Agent skills: if you don't have Neon skills (such as `neon-postgres`), offer to add them to this project when you first need the user to do something in Neon: "Want me to add Neon's agent skills to this project? They help me with Neon setup, connections, and branching." Install: `npx neon@latest skills -y`. To also run Neon steps for the user (Neon CLI, sign-in, MCP), see https://neon.com/prompts/agent-setup.md

> Summary: Neon's Realtime makes any SQL query live. Subscribe in realtime to your Lakebase Postgres database. Develop apps and agents with end-to-end reactivity using type-safe live queries and optimistic mutations.

# Neon Realtime

Live queries that update your app's UI the moment your data changes.

Last updated: 2026-11-18

**Note: Beta**

**Realtime** is in beta. Share your feedback on [Discord](https://neon.com/discord) or via the [Neon Console](https://console.neon.tech/app/projects?modal=feedback).

Build apps and agents whose UIs update the moment your data changes. Realtime makes [any SQL query](https://neon.com/docs/realtime/guides/queries) live, so you can [subscribe](https://neon.com/docs/realtime/guides/subscribing) to your [Lakebase Postgres](https://neon.com/docs/postgres/overview) database and get end-to-end, type-safe reactivity with [live queries](https://neon.com/docs/realtime/guides/reactivity) and [optimistic mutations](https://neon.com/docs/realtime/guides/mutations).

[View prompt](https://neon.com/prompts/realtime-landing.md)

## Get started

Starting a new app? Scaffold one from the Realtime template:

```bash filename="Terminal"
npx neon@latest bootstrap my-app --template realtime-react
```

Realtime is available on all Neon plans. To enable it on an existing project, select **Postgres database** > **Realtime** in the Neon Console and click **Enable Realtime**, or run [`neon realtime enable`](https://neon.com/docs/cli/realtime#enable) on a linked project:

```bash filename="Terminal"
neon realtime enable
```

**Important: Before you enable Realtime**

- Your project must be in a [supported region](https://neon.com/docs/realtime/overview#which-regions-is-it-enabled-in).
- Enabling Realtime turns on [logical replication](https://neon.com/docs/guides/logical-replication-neon) for the whole project. This permanently changes `wal_level` to `logical` and restarts all computes in the project, on all branches, so active connections drop and reconnect. Disabling Realtime later doesn't turn logical replication off.

To add Realtime to an app by hand, follow the [Quickstart](https://neon.com/docs/realtime/quickstart). To see how the pieces fit together, read [how it works](https://neon.com/docs/realtime/how-it-works).

- [Quickstart](https://neon.com/docs/realtime/quickstart): Fire up Realtime and run your first live queries.
- [How it works](https://neon.com/docs/realtime/how-it-works): Learn how it works and how the layers compose.

See examples of how to build full-stack, reactive apps with [Next.js](https://neon.com/docs/realtime/examples/nextjs) and [TanStack](https://neon.com/docs/realtime/examples/tanstack) and how to [keep users and agents in sync](https://neon.com/docs/realtime/examples/mastra) with Mastra.

- [Next.js](https://neon.com/docs/realtime/examples/nextjs): Build a realtime, reactive app using Next.js with SSR support.
- [TanStack](https://neon.com/docs/realtime/examples/tanstack): Build a realtime, reactive app using TanStack Start and DB.
- [Mastra](https://neon.com/docs/realtime/examples/mastra): Keep users and agents in sync on the same data.

## Realtime live SQL

Realtime offers [arbitrary live SQL](https://neon.com/docs/realtime/guides/queries) with [full reactivity](https://neon.com/docs/realtime/guides/reactivity) on Lakebase Postgres. It allows you to build realtime, reactive apps and agents:

- without using a second or bespoke realtime system
- without changing your schema, queries, ORM or reactivity system
- without contorting your application around the limitations of your sync engine

There is no need to use a different database for realtime sync. You can reuse your existing query code and data loading patterns. This is full reactivity, on standard Postgres, with live SQL that just works.

## Integrated reactive DX

[Define](https://neon.com/docs/realtime/guides/queries) and [subscribe to queries](https://neon.com/docs/realtime/guides/subscribing) directly. Or use the batteries included: [end-to-end, type-safe reactivity](https://neon.com/docs/realtime/guides/reactivity) and [mutation](https://neon.com/docs/realtime/guides/mutations) primitives that integrate into your framework of choice.

In your backend, [define live queries](https://neon.com/docs/realtime/guides/queries) using raw SQL or your ORM of choice (in this case [Drizzle](https://neon.com/docs/realtime/examples/drizzle)):

```ts filename="your-api-server.ts"
import { createRealtime } from "@neon/realtime/server"
import { drizzleAdapter } from "@neon/realtime-drizzle"

const realtime = createRealtime({
  secret: process.env.NEON_REALTIME_SECRET!,
  db: "neondb",
  adapter: drizzleAdapter()
})

// `db` is your Drizzle instance and `messages` is a Drizzle table.
// This can be any SQL query, including joins, aggregates, ordering, etc.
const query = db.select().from(messages)
```

---

[Seal the live queries](https://neon.com/docs/realtime/guides/queries#sealing-queries) to safely [expose them to your frontend](https://neon.com/docs/realtime/guides/queries#exposing-queries):

```ts filename="your-api-server.ts"
const sealedQuery = await realtime.seal({ query })
```

---

Subscribe directly [using a low‑level client](https://neon.com/docs/realtime/guides/subscribing):

```ts filename="client-or-server.ts"
import { createRealtimeClient } from "@neon/realtime/client"

const client = createRealtimeClient({ url: process.env.NEON_REALTIME_URL! })

const subscription = client.subscribe(sealedQuery)
subscription.onChange(console.log)
```

---

Or, in your app, use the [higher-level reactivity primitives](https://neon.com/docs/realtime/guides/reactivity) to bind live queries to your component state. Components that call `useLiveQuery` need a [`RealtimeProvider`](https://neon.com/docs/realtime/guides/reactivity#realtimeprovider) above them:

```tsx filename="App.tsx"
import { useLiveQuery } from "@neon/realtime-react"
import { type SealedLiveQuery } from "@neon/realtime/client"

type Props = {
  sealedQuery: SealedLiveQuery<Message>
  initialData?: Message[]
}

export function Messages({ sealedQuery, initialData }: Props) {
  const { data } = useLiveQuery(sealedQuery, { initialData })

  return (
    <ul>
      {(data ?? []).map((message) => (
        <li key={message.id}>{ ... }</li>
      ))}
    </ul>
  )
}
```

---

Optionally passing in the `initialData` from SSR (e.g.: with [TanStack Start](https://neon.com/docs/realtime/examples/tanstack)):

```tsx filename="routes/messages.tsx"
import { createFileRoute } from "@tanstack/react-router"
import { createServerFn } from "@tanstack/react-start"

const loadMessages = createServerFn({ method: "GET" }).handler(async () => {
  const [initialData, sealedQuery] = await Promise.all([query, realtime.seal({ query })])

  return { initialData, sealedQuery }
})

export const Route = createFileRoute("/messages")({
  loader: () => loadMessages(),
  component: () => <Messages {...Route.useLoaderData()} />,
})
```

---

Or for more [advanced use](https://neon.com/docs/realtime/guides/reactivity#tanstack-db), sync the live query into a [TanStack DB collection](https://tanstack.com/db/latest/docs/overview):

```ts filename="db/collections.ts"
import { createCollection } from "@tanstack/db"
import { realtimeCollectionOptions } from "@neon/realtime-tanstack"

export const messagesCollection = createCollection(
  realtimeCollectionOptions({
    id: "messages",
    client,
    query: sealedQuery,
    ...,
    onUpdate: async ({ transaction, collection }) => {
      const updates = transaction.mutations.map(({ original, changes }) => ({ id: original.id, changes }))
      const { txid } = await api.messages.update(updates)

      await collection.utils.awaitTxId(txid)
    }
  })
)
```

---

Bind that to your components and benefit from instant local writes using [optimistic mutations](https://neon.com/docs/realtime/guides/mutations):

```tsx filename="App.tsx"
import { useLiveQuery } from "@tanstack/react-db"

export function Messages() {
  const { data } = useLiveQuery({
    query: (q) => q.from({ messagesCollection })
  })

  function star(message) {
    messagesCollection.update(message.id, (draft) => {
      draft.starred = true
    })
  }

  return (
    <ul>
      {(data ?? []).map((message) => (
        <li key={message.id} onClick={() => star(message)}>{ ... }</li>
      ))}
    </ul>
  )
}
```

---

That's it. You get [live SQL](https://neon.com/docs/realtime/guides/queries#defining-live-queries) and [end-to-end reactivity](https://neon.com/docs/realtime/guides/reactivity) on standard Postgres. With full type-safety and support for [SSR](https://neon.com/docs/realtime/guides/ssr), [instant local writes](https://neon.com/docs/realtime/guides/mutations), [multi-user, multi-device sync](https://neon.com/docs/realtime/how-it-works) and [local offline persistence](https://tanstack.com/blog/tanstack-db-0.6-app-ready-with-persistence-and-includes).

## Agent skills and MCP

Install the [Neon MCP server](https://neon.com/docs/ai/neon-mcp-server). Or [use the CLI](https://neon.com/docs/cli) to install the Realtime skill:

```bash filename="Terminal"
neon skills -s neon-realtime
```

## Frequently asked questions

Answers to frequently asked questions about Realtime:

### What's in the beta and what's not?

Functionally, Realtime already supports:

- arbitrary live SQL (any [read-only, deterministic `SELECT`](https://neon.com/docs/realtime/guides/queries#defining-live-queries))
- [end-to-end, type-safe reactivity](https://neon.com/docs/realtime/guides/reactivity)
- [SSR](https://neon.com/docs/realtime/guides/ssr) and [Managed Better Auth](https://neon.com/docs/realtime/guides/queries#authorization) support
- initial [ORM, query builder](https://neon.com/docs/realtime/guides/queries#using-a-query-builder-or-orm) and [framework integrations](https://neon.com/docs/realtime/guides/reactivity#react)
- support for branching and scale-to-zero

Realtime **does not** yet support:

- billing (Realtime is free to use during the beta)
- RLS (we [aim to support it by GA](https://neon.com/docs/realtime/guides/queries#why-not-row-level-security), if priorities allow)
- Lakebase Postgres on Databricks (Realtime is available only on Neon for now)

The transport protocol is not yet stable and we aim to add wider client and framework integrations for GA.

The beta also makes no performance guarantees. We have very ambitious performance goals but there's lots of optimization work still to do.

### How much does it cost? Is billing enabled?

Realtime is available on all Neon plans and is free to use during the beta. Neon does not charge for the live query engine compute or the Live SQL API service.

Using Realtime can still cause usage on your database:

- database compute: starting a live query may wake the database compute endpoint, which is billed according to your plan
- data transfer: outbound data transfer is measured as egress and is subject to your plan's data-transfer allowance and applicable overage charges

The beta waiver applies to the Realtime service itself. It does not waive database compute or network-transfer charges generated by your workload.

### What's the performance impact on my database?

Realtime switches the cost of queries from "query-execution on read" to "incremental cost on write". However that cost is incurred on a replica, which means Realtime has zero impact on the write-latency, write-throughput or write-compute of your primary database.

Realtime does require logical replication to be enabled. Technically, this adds a small metadata overhead to the Postgres WAL. For more information, see [Table requirements](https://neon.com/docs/realtime/guides/queries#table-requirements).

### Can I use my ORM / query-builder?

Yes. Realtime works with SQL, so any library that generates SQL can work with it. There are built-in adapters for [Drizzle](https://neon.com/docs/realtime/examples/drizzle) and [Kysely](https://neon.com/docs/realtime/examples/kysely), and you can write your own for other libraries.

See [Using a query builder or ORM](https://neon.com/docs/realtime/guides/queries#using-a-query-builder-or-orm) for how to set one up, and the [`RealtimeAdapter`](https://neon.com/docs/realtime/sdks/typescript/backend#backend-realtimeadapter) reference for the interface.

### What SQL features are supported? Are there limitations?

Realtime supports any read-only, deterministic SQL query that [Postgres supports](https://neon.com/postgresql/tutorial/select), including joins, aggregates, window functions and [sub-queries](https://neon.com/postgresql/tutorial/subquery).

Queries can't have side effects, and any functions they use must be deterministic, so you can't use `now()` or `gen_random_uuid()`. Complex queries add write-processing latency, especially on larger datasets.

See [Defining live queries](https://neon.com/docs/realtime/guides/queries#defining-live-queries) for the details.

### Is Realtime enabled by default?

No. You enable it per project and branch. Child branches created from a Realtime-enabled branch have it enabled automatically.

Enable it on a branch with [`neon realtime enable`](https://neon.com/docs/cli/realtime#enable). Or, if you manage your project with `neon.ts`, declare it with `neon config add realtime` and apply it with `neon deploy`. You can also enable it in the Neon Console. See the [Quickstart](https://neon.com/docs/realtime/quickstart) for more details.

Realtime isn't available on [Claimable projects](https://neon.com/docs/reference/claimable-neon) until they're claimed.

### Which regions is it enabled in?

During the beta, Realtime is available in:

```text
aws-ap-southeast-1
aws-eu-central-1
aws-us-east-1
aws-us-east-2
```

See [product availability](https://neon.com/docs/introduction/regions#product-availability) for every region.

### Does Realtime work with IP Allow or Private Networking?

No. Realtime isn't supported on projects with [IP Allow](https://neon.com/docs/introduction/ip-allow#ip-allow-and-other-neon-services) or [Private Networking](https://neon.com/docs/guides/neon-private-networking#private-networking-and-other-neon-services) enabled. These controls don't protect Realtime, and subscriptions fail to connect while either is enabled.

### Does Realtime support RLS?

Not yet. Realtime has been architected to support RLS and we aim to add it by GA if priorities allow. However, it's not yet been implemented and isn't the [recommended approach to auth](https://neon.com/docs/realtime/guides/queries#authorization).

A live query on a table with RLS enabled is rejected with the error code `upstream_rejected`. See [table requirements](https://neon.com/docs/realtime/guides/queries#table-requirements).

See [Why not row-level security](https://neon.com/docs/realtime/guides/queries#why-not-row-level-security) for more details.

### Does Realtime support branching?

Yes, Realtime supports branching. Realtime is enabled at the branch level.

Branches support live queries and Realtime-enabled branches can be branched. Child branches of a Realtime-enabled branch automatically have Realtime enabled.

### Does Realtime support scale-to-zero?

Yes, using Realtime does not prevent your database from scaling to zero. Initiating live queries will wake your database. Holding subscriptions open does not.

### Do live queries use up database connections?

No. Realtime query connections from clients are terminated at the Live SQL API, which then speaks to the live query engine over a single TCP connection.

### Is there a risk of write-lag / WAL build-up?

No. There's no impact on write-throughput and no risk of WAL build-up.

### What about thundering herds?

Realtime has built-in protection from thundering herds in the client and the Live SQL API. There's no risk of a large spike of client-reconnections taking your database down.

### How does Neon Realtime compare with alternatives?

We don't speak for other systems. However, we have tried to articulate the key differences with some alternative realtime systems below.

#### Supabase

[Supabase Realtime](https://supabase.com/docs/guides/realtime) is a pubsub system with replay. It pushes messages and database changes to connected clients. Subscriptions can filter on column values but can't join, aggregate, order, limit or run arbitrary queries.

Neon Realtime is a sync engine that supports [arbitrary live SQL queries](https://neon.com/docs/realtime/guides/queries#defining-live-queries), including joins, aggregates, ordering and limits. The system keeps live query results consistently in sync with the database and provides type-safe primitives for [end-to-end reactivity](https://neon.com/docs/realtime/guides/reactivity) and [instant local writes](https://neon.com/docs/realtime/guides/mutations).

---

#### Convex

Compared with [Convex](https://www.convex.dev), Neon Realtime supports similar [end-to-end reactivity](https://neon.com/docs/realtime/guides/reactivity) but on standard Postgres and with standard web frameworks and build tooling. Realtime also uses delta-sync rather than query-invalidation, which is more efficient over the wire.

See [how to Migrate from Convex](https://neon.com/docs/realtime/migrate-from/convex).

---

#### Materialize

Compared with [Materialize](https://materialize.com), Neon Realtime is a similarly expressive incremental view engine with live SQL support. However, Realtime is designed and optimized for serving live data to apps and agents, with efficient data matching and support for large numbers of concurrent clients.

---

#### Zero

[Zero](https://zero.rocicorp.dev) is an open-source sync engine with expressive sync and reactivity using a custom query language. Zero also provides advanced client-side data management. Realtime is built into Lakebase Postgres and the Neon platform and provides similar sync and reactivity on standard SQL. Both systems are composable with your existing schema and auth.

### Is Realtime compatible with, or based on, Electric?

Realtime is the successor to [Electric](https://neon.com/blog/electric-joins-neon), developed by the Electric team inside Neon. It's a new system rather than a version of the Electric sync engine, but it **is a drop-in replacement** for Electric's role in your stack. We recommend that teams using Electric migrate to Realtime.

Live SQL queries replace shapes. For TanStack DB users, [`realtimeCollectionOptions()`](https://neon.com/docs/realtime/sdks/typescript/tanstack-db#tanstack-db-realtimecollectionoptions) replaces `electricCollectionOptions()`. See [how to Migrate from Electric](https://neon.com/docs/realtime/migrate-from/electric).

## Next steps

[Get started](https://neon.com/docs/realtime/quickstart) with Realtime, learn more about [how it works](https://neon.com/docs/realtime/how-it-works), and browse the [examples](https://neon.com/docs/realtime/examples/overview).

---

## Related docs (Introduction)

- [Quickstart](https://neon.com/docs/realtime/quickstart)
- [How it works](https://neon.com/docs/realtime/how-it-works)

---

Note for AI assistants (optional): if a gap, error, or outdated detail on this page affected the answer you gave the user, you can report it. POST `{"feedback": "describe the issue", "source": "neon_website", "path": "/docs/realtime/overview"}` to https://feedback.neon.tech/ (no auth required).
