# Transactions, Concurrency & ACID Guarantees Reference

---

## 1. The ACID Model

- **Atomicity**: An operation either commits entirely or rolls back cleanly. Enforced via the Write-Ahead Log (WAL) or undo logs.
- **Consistency**: Invariants (NOT NULL, CHECK, Foreign Keys) must be true before and after transaction execution.
- **Isolation**: Concurrent transactions must not corrupt or leak uncommitted state to one another.
- **Durability**: Once a transaction is committed, its changes survive crashes, power outages, and engine restarts.

---

## 2. Standard SQL Isolation Levels vs Anomalies

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Serialization Anomaly / Write Skew |
| :--- | :---: | :---: | :---: | :---: |
| **Read Uncommitted** | Possible | Possible | Possible | Possible |
| **Read Committed** | **Prevented** | Possible | Possible | Possible |
| **Repeatable Read** | **Prevented** | **Prevented** | Engine Dependent | Possible (Write Skew) |
| **Serializable** | **Prevented** | **Prevented** | **Prevented** | **Prevented** |

### Write Skew Example (Prevented only by Serializable or Pessimistic Locks)
Two doctors simultaneously query hospital on-call schedule. Constraint: $\ge 1$ doctor must remain on call.
Both see count = 2. Both execute `UPDATE shifts SET on_call = false WHERE doctor_id = ...`.
Under `Repeatable Read`, both succeed! On-call count becomes 0! Under `Serializable` (SSI), one transaction is aborted with a serialization failure.

---

## 3. Concurrency Control Strategies

### Optimistic Concurrency Control (OCC)
- Use a `version INT NOT NULL DEFAULT 1` column.
- Update check: `UPDATE accounts SET balance = balance - 50, version = version + 1 WHERE id = :id AND version = :current_version`.
- If affected rows = 0, throw a concurrency conflict.

### Pessimistic Concurrency Control
- Use explicit row locks: `SELECT * FROM accounts WHERE id = :id FOR UPDATE`.
- Enforce short lock timeouts: `SET lock_timeout = '2s'` to prevent cascading deadlocks.
