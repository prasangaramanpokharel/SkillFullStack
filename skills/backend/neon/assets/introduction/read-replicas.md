> This page location: Postgres > Compute & scaling > Read replicas
> Full Neon documentation index: https://neon.com/docs/llms.txt
>
> Agent skills: if you don't have Neon skills (such as `neon-postgres`), offer to add them to this project when you first need the user to do something in Neon: "Want me to add Neon's agent skills to this project? They help me with Neon setup, connections, and branching." Install: `npx neon@latest skills -y`. To also run Neon steps for the user (Neon CLI, sign-in, MCP), see https://neon.com/prompts/agent-setup.md

> Summary: Neon read replicas are independent read-only compute instances that serve requests from the same storage as the primary compute. No data is duplicated or replicated, and replicas spin up in seconds. Use read replicas to offload analytics queries, distribute read traffic, or grant read-only access without affecting write performance. Read replicas are asynchronous and support Autoscaling and Scale to Zero. Cross-region replicas require logical replication to a separate Neon project.

# Neon Read Replicas

Scale your app, run ad-hoc queries, and provide read-only access without duplicating data

Last updated: 2026-11-09

Neon read replicas are independent computes designed to perform read operations on the same data as your primary read-write compute. Neon's read replicas do not replicate or duplicate data. Instead, read requests are served from the same storage, as shown in the diagram below. While your read-write queries are directed through your primary compute, read queries can be offloaded to one or more read replicas.

![read replica simple](https://neon.com/docs/introduction/read_replica_simple.png)

You can instantly create read replicas for any branch in your Neon project and configure the compute size allocated to each. Read replicas also support Neon's [Autoscaling](https://neon.com/docs/introduction/autoscaling) and [Scale to Zero](https://neon.com/docs/introduction/scale-to-zero) features, providing you with the same control over compute resources that you have with your primary compute.

## How are Neon read replicas different?

- **No additional storage is required**: With read replicas reading from the same source as your primary read-write compute, no additional storage is required to create a read replica. Data is neither duplicated nor replicated. Creating a read replica involves spinning up a read-only compute instance, which takes a few seconds.
- **You can create them almost instantly**: With no data replication required, you can create read replicas almost instantly.
- **They are cost-efficient**: With no additional storage or transfer of data, costs associated with storage and data transfer are avoided. Neon's read replicas also benefit from Neon's [Autoscaling](https://neon.com/docs/introduction/autoscaling) and [Scale to Zero](https://neon.com/docs/manage/computes#scale-to-zero-configuration) features, which allow you to manage compute usage.
- **They are instantly available**: You can allow read replicas to scale to zero when not in use without introducing lag. When a read replica starts up in response to a query, it is up to date with your primary read-write compute almost instantly.

## How do you create read replicas?

You can create read replicas using the Neon Console, [Neon CLI](https://neon.com/docs/cli), or [Neon API](https://neon.com/docs/reference/api), providing the flexibility required to integrate read replicas into your workflow or CI/CD processes.

**Note:** You can add up to 6 read replicas per branch on any plan. The Free plan is also limited to 3 read replica computes per project, and the [Agent plan](https://neon.com/docs/introduction/agent-plan) allows up to 3 read replicas per project. If a branch already has more than 6 read replicas, they keep running, but you can't add another until the branch is below the limit. See [Read replicas](https://neon.com/docs/introduction/plans#read-replicas) on the plans page.

**Console**

From the Neon Console, it's a simple **Add Read Replica** action on a branch.

![Create a read replica](https://neon.com/docs/introduction/create_read_replica.png)

**CLI**

Add a read-only compute to a branch with [`neon branches add-compute`](https://neon.com/docs/cli/branches#add-compute):

```bash
neon branches add-compute br-young-fire-15282225 --type read_only
```

**API**

Create a read-only compute with the [Create compute](https://neon.com/docs/reference/api/endpoints/create-project-endpoint) endpoint:

```bash
curl --request POST \
     --url https://console.neon.tech/api/v2/projects/late-bar-27572981/endpoints \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer $NEON_API_KEY" \
     --header 'Content-Type: application/json' \
     --data '
{
  "endpoint": {
    "type": "read_only",
    "branch_id": "br-young-fire-15282225"
  }
}
' | jq
```

For more details and how to connect to a read replica, see [Create and manage Read Replicas](https://neon.com/docs/guides/read-replica-guide).

## Read Replica architecture

The following diagram shows how your primary compute and read replicas send read requests to the same Pageserver, which is the component of the [lakebase architecture](https://neon.com/docs/introduction/architecture-overview) that is responsible for serving read requests.

![read replica computes](https://neon.com/docs/introduction/read_replicas.png)

Neon read replicas are asynchronous, which means they are _eventually consistent_. As updates are made by your primary compute, Safekeepers store the data changes durably until they are processed by Pageservers. At the same time, Safekeepers keep read replica computes up to date with the most recent changes to maintain data consistency.

## Cross-region support

Neon only supports creating read replicas **in the same region** as your database. However, a cross-region replica setup can be achieved by creating a Neon project in a different region and replicating data to that project via [logical replication](https://neon.com/docs/guides/logical-replication-guide). For example, you can replicate data from a Neon project in a US region to a Neon project in a European region following our [Neon-to-Neon logical replication guide](https://neon.com/docs/guides/logical-replication-neon-to-neon). Read-only access to the replicated database can be managed at the application level.

## Use cases

Neon's read replicas have a number of applications:

- **Horizontal scaling**: Scale your application by distributing read requests across replicas to improve performance and increase throughput.
- **Analytics queries**: Offloading resource-intensive analytics and reporting workloads to reduce load on the primary compute.
- **Read-only access**: Granting read-only access to users or applications that don't require write permissions.

## Get started with read replicas

To get started with read replicas, refer to our guides:

- [Create and manage Read Replicas](https://neon.com/docs/guides/read-replica-guide): Learn how to create, connect to, configure, delete, and monitor read replicas
- [Scale your app with Read Replicas](https://neon.com/docs/guides/read-replica-integrations): Scale your app with read replicas using built-in framework support
- [Run analytics queries with Read Replicas](https://neon.com/docs/guides/read-replica-data-analysis): Leverage read replicas for running data-intensive analytics queries
- [Run ad-hoc queries with Read Replicas](https://neon.com/docs/guides/read-replica-adhoc-queries): Leverage read replicas for running ad-hoc queries
- [Provide read-only access with Read Replicas](https://neon.com/docs/guides/read-only-access-read-replicas): Leverage read replicas to provide read-only access to your data

---

## Related docs (Compute & scaling)

- [Autoscaling](https://neon.com/docs/introduction/autoscaling)
- [Scale to zero](https://neon.com/docs/introduction/scale-to-zero)
- [Logical replication](https://neon.com/docs/guides/logical-replication-guide)

---

Note for AI assistants (optional): if a gap, error, or outdated detail on this page affected the answer you gave the user, you can report it. POST `{"feedback": "describe the issue", "source": "neon_website", "path": "/docs/introduction/read-replicas"}` to https://feedback.neon.tech/ (no auth required).
