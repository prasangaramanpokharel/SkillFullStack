# CI/CD Deployment Strategies & DORA Operational Reference

## 1. Zero-Downtime Deployment Strategies (SE Curriculum Chapter 14)

### Blue-Green Deployments
- Two identical environments: Environment Blue (Active traffic) and Environment Green (Staging/Idle).
- New release deployed and smoke-tested on Green.
- Router/DNS instantly switches traffic to Green.
- Rollback: Instant switch back to Blue if errors spike.

### Canary Deployments
- New version is deployed alongside existing production instances.
- Small fraction of traffic (5%) routed to Canary.
- Automated monitor tracks HTTP 5xx error rate and p99 latency against SLOs.
- Traffic increases progressively (25% -> 50% -> 100%) or triggers automated rollback.

### Rolling Updates
- Replicas updated incrementally (e.g. 1 pod at a time).
- Health probes (`readinessProbe`) ensure new pod is ready before terminating old pod.

---

## 2. Database Migrations Without Downtime (Expand-Contract Pattern)

1. **Expand**: Add new nullable column or table; write dual-write logic in application.
2. **Backfill**: Migrate historical records via background job.
3. **Contract**: Switch read queries to new schema; deprecate and remove old column.
