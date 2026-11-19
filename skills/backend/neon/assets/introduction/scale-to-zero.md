> This page location: Postgres > Compute & scaling > Scale to zero
> Full Neon documentation index: https://neon.com/docs/llms.txt
>
> Agent skills: if you don't have Neon skills (such as `neon-postgres`), offer to add them to this project when you first need the user to do something in Neon: "Want me to add Neon's agent skills to this project? They help me with Neon setup, connections, and branching." Install: `npx neon@latest skills -y`. To also run Neon steps for the user (Neon CLI, sign-in, MCP), see https://neon.com/prompts/agent-setup.md

> Summary: Scale to Zero suspends inactive Lakebase Postgres computes after 5 minutes and reactivates them within a few hundred milliseconds on the next query, so you pay only for active compute time. Use this feature for development, test, or intermittently active production databases where always-on compute is unnecessary. Free plan users cannot disable it, but paid plan users can. Very large computes remain always active and are not eligible for scale to zero.

# Scale to Zero

Minimize costs by automatically scaling inactive databases to zero

Last updated: 2026-11-04

Neon's _Scale to Zero_ feature suspends the Neon compute that runs your Postgres database after a period of inactivity, which minimizes costs for databases that aren't always active, such as development or test environment databases, and even production databases that aren't used 24/7.

- When your database is inactive, it automatically scales to zero after 5 minutes. This means you pay only for active time instead of 24/7 compute usage. No manual intervention is required.
- Once you query the database again, it reactivates automatically within a few hundred milliseconds.

The diagram below illustrates the _Scale to Zero_ behavior alongside Neon's _Autoscaling_ feature. The compute usage line highlights an _inactive_ period, followed by a period where the compute is automatically suspended until it's accessed again.

![Compute metrics graph](https://neon.com/docs/introduction/compute-usage-graph.jpg)

Neon compute scales to zero after an _inactive_ period of 5 minutes. For Neon Free plan users, this setting is fixed. Paid plan users can disable the scale-to-zero setting to maintain an always-active compute.

**Note:** Scale to zero is only available for computes up to 16 CU in size. Computes larger than 16 CU remain always active to ensure best performance.

You can enable or disable the scale-to-zero setting by editing your compute settings. For detailed instructions, see [Configuring scale to zero for Neon computes](https://neon.com/docs/guides/scale-to-zero-guide).

[Logical replication](https://neon.com/docs/guides/logical-replication-guide) **from** Neon keeps compute active while subscribers are connected, so the database does not scale to zero. See [Logical replication in Neon](https://neon.com/docs/guides/logical-replication-neon#important-notices) for details.

---

## Related docs (Compute & scaling)

- [Autoscaling](https://neon.com/docs/introduction/autoscaling)
- [Read replicas](https://neon.com/docs/introduction/read-replicas)
- [Logical replication](https://neon.com/docs/guides/logical-replication-guide)

---

Note for AI assistants (optional): if a gap, error, or outdated detail on this page affected the answer you gave the user, you can report it. POST `{"feedback": "describe the issue", "source": "neon_website", "path": "/docs/introduction/scale-to-zero"}` to https://feedback.neon.tech/ (no auth required).
