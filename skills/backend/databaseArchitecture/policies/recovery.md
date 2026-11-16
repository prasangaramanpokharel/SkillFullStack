# Database Backup, Disaster Recovery & High Availability Policies

Policies governing backup retention, point-in-time recovery, and restore verification.

---

## 1. RPO & RTO Invariants

Every production database architecture must define and document explicit recovery objectives:
- **Recovery Point Objective (RPO)**: The maximum acceptable data loss measured in time (e.g. $\le 5$ minutes of transactions).
- **Recovery Time Objective (RTO)**: The maximum acceptable downtime to restore full database availability (e.g. $\le 60$ minutes).

---

## 2. Backup Architecture & Verification

- **Point-in-Time Recovery (PITR)**:
  - Base backups (physical or logical snapshots) combined with continuous Write-Ahead Log (WAL) archiving to durable object storage.
- **Geographic Redundancy**:
  - WAL archives and snapshots must be mirrored to a secondary geographic region independent of the primary availability zone.
- **Mandatory Restore Testing**:
  - Backups that have never been restored do not exist.
  - Automated restore drills must execute on a scheduled cadence (minimum monthly) to an isolated test cluster, verifying integrity and timing against the RTO target.
