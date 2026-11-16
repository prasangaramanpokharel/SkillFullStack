# Backup, Disaster Recovery & High Availability Reference

---

## 1. Physical vs. Logical Backups

| Backup Architecture | Mechanism | Advantages | Disadvantages |
| :--- | :--- | :--- | :--- |
| **Physical (Binary Snapshots)** | Block-level file copies or storage volume snapshots (EBS, ZFS). | Extremely fast restore; captures exact byte state. | Engine and architecture specific; large storage volume. |
| **Logical Backups (`pg_dump`, `mysqldump`)** | SQL text or archive emitting DDL and INSERT/COPY statements. | Engine portable, readable, supports partial table restores. | Extremely slow restore on terabyte-scale databases; high CPU load. |
| **Continuous WAL Archiving (PITR)** | Base physical backup + streaming Write-Ahead Log segments to object storage. | Zero data loss up to seconds before disaster; restore to any microsecond. | Requires dedicated tooling (pgBackRest, WAL-G, Barman). |

---

## 2. Point-in-Time Recovery (PITR) Protocol

1. Restore the most recent baseline physical snapshot before the disaster event timestamp $T$.
2. Configure `recovery_target_time = '2026-11-16 12:45:00 UTC'`.
3. Replay Write-Ahead Log (WAL) segments sequentially up to the target time.
4. Promote the restored cluster to primary.

---

## 3. High Availability & Split-Brain Defense

- **Quorum Consensus (Raft / Paxos)**: Multi-node clusters must use odd numbers of voter nodes (3, 5) to prevent network partition split-brain.
- **Fencing (STONITH)**: Automatically isolate failed primary nodes before promoting a replica to prevent dual-master data corruption.
