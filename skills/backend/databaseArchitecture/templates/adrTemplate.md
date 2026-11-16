# ADR-001: Primary Database Architecture Decision Record

## Status
[ Proposed | Accepted | Deprecated | Superseded ]

## Context & Workload Requirements
Describe the business problem, entities, and anticipated operational scale:
- **Workload Type**: [ OLTP | OLAP | Time-Series | Graph | Vector | Key-Value ]
- **Data Scale**: Expected rows at launch, rows at 12 months, daily row ingestion rate.
- **Access Profile**: Read/Write ratio (e.g., 90/10 vs 30/70), peak queries per second (QPS).
- **Latency SLO**: P95 target (e.g. $< 15$ms for reads, $< 50$ms for writes).
- **Consistency Needs**: [ Strict Serializability | Read-Your-Writes | Eventual Consistency ].

## Candidate Architectures Evaluated
1. **Candidate A (e.g. PostgreSQL)**: Pros, cons, operational fit.
2. **Candidate B (e.g. MongoDB)**: Pros, cons, operational fit.
3. **Candidate C (e.g. ClickHouse)**: Pros, cons, operational fit.

## Decision
We select **[Selected Database Architecture]** because:
1. Primary architectural rationale.
2. Fit with team operational capabilities and infrastructure.

## Consequences & Trade-offs
- **Positive**: What becomes easier or faster.
- **Negative / Operational Complexity**: What requires additional monitoring, indexing, or backup discipline.
- **Mitigations**: How identified risks will be controlled.

## Verification & Acceptance Criteria
- [ ] Schema validates under automated integrity checks.
- [ ] P95 latency confirmed under load test with expected data volume.
- [ ] PITR restore drill verified.
