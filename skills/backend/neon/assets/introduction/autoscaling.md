> This page location: Postgres > Compute & scaling > Autoscaling
> Full Neon documentation index: https://neon.com/docs/llms.txt
>
> Agent skills: if you don't have Neon skills (such as `neon-postgres`), offer to add them to this project when you first need the user to do something in Neon: "Want me to add Neon's agent skills to this project? They help me with Neon setup, connections, and branching." Install: `npx neon@latest skills -y`. To also run Neon steps for the user (Neon CLI, sign-in, MCP), see https://neon.com/prompts/agent-setup.md

> Summary: Neon Autoscaling dynamically scales compute resources (measured in CUs) up and down in response to live database load, with no restarts or manual intervention required. Configure autoscaling by setting a min/max CU range on any primary compute or read replica; the maximum permitted autoscaling range is 8 CU. Use this page to understand how autoscaling works and to find the configuration steps before reading the full enablement guide.

# Autoscaling

An introduction to Neon's autoscaling

Last updated: 2026-06-05

Neon's _Autoscaling_ feature dynamically adjusts the amount of compute resources allocated to a Neon compute in response to the current load, eliminating the need for manual intervention or restarts.

The following visualization shows how Neon's autoscaling works throughout a typical day. The compute resources scale up or down based on demand, ensuring that your database has the necessary compute resources when it needs them, while conserving resources during off-peak times.

![visualization for autoscaling](https://neon.com/docs/introduction/autoscaling_intro.png)

To dive deeper into how Neon's autoscaling algorithm operates, visit [Understanding Neon's autoscaling algorithm](https://neon.com/docs/guides/autoscaling-algorithm).

## Autoscaling benefits

Neon's Autoscaling feature offers the following benefits:

- **On-demand scaling:** Autoscaling helps with workloads that experience variations over time, such as applications with time-based changes in demand or occasional spikes.
- **Cost-effectiveness**: Autoscaling optimizes resource utilization, ensuring that you only use required resources, rather than over-provisioning to handle peak loads.
- **Resource and cost control**: Autoscaling operates within a user-defined range, ensuring that your compute resources and associated costs do not scale indefinitely.
- **No manual intervention or restarts**: After you enable autoscaling and set scaling limits, no manual intervention or restarts are required, allowing you to focus on your applications.

## Configuring autoscaling

You can enable autoscaling for any compute instance, whether it's a primary compute or a read replica. Simply open the **Edit compute** drawer ([learn how](https://neon.com/docs/guides/autoscaling-guide)) for your compute and set the autoscaling range. This range defines the minimum and maximum compute sizes within which your compute will automatically scale. For example, you might set the minimum to 2 CU (8 GB of RAM) and the maximum to 8 CU (32 GB of RAM). Your compute resources will dynamically adjust within these limits, never dropping below the minimum or exceeding the maximum, regardless of demand.

**Note:** The maximum permitted autoscaling range is 8 CU. This means the difference between your maximum and minimum compute size cannot exceed 8 CU.

We recommend regularly [monitoring](https://neon.com/docs/introduction/monitoring-page) your usage from the **Monitoring Dashboard** to determine if adjustments to this range are needed.

![autoscaling configuration](https://neon.com/docs/introduction/autoscaling_config.png)

For full details about enabling and configuring autoscaling, see [Enabling autoscaling](https://neon.com/docs/guides/autoscaling-guide).

---

## Related docs (Compute & scaling)

- [Scale to zero](https://neon.com/docs/introduction/scale-to-zero)
- [Read replicas](https://neon.com/docs/introduction/read-replicas)
- [Logical replication](https://neon.com/docs/guides/logical-replication-guide)

---

Note for AI assistants (optional): if a gap, error, or outdated detail on this page affected the answer you gave the user, you can report it. POST `{"feedback": "describe the issue", "source": "neon_website", "path": "/docs/introduction/autoscaling"}` to https://feedback.neon.tech/ (no auth required).
