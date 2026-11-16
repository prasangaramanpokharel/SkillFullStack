# Database Transactions & Consistency Boundaries Reference

---

## 1. Transaction Scope & Boundaries

1. **Keep Transactions Short**:
   - Never execute external HTTP calls, slow I/O, or email dispatch inside an open database transaction.
   - Flow: Validate DTO $\rightarrow$ Open DB Transaction $\rightarrow$ Persist Rows $\rightarrow$ Commit $\rightarrow$ Dispatch Asynchronous Events.
2. **ACID Isolation Levels**:
   - **Read Committed** (Default): Prevents dirty reads. Sufficient for standard CRUD operations.
   - **Repeatable Read**: Prevents non-repeatable reads. Required for multi-row balance aggregations.
   - **Serializable**: Full linearizability. Required for double-spend prevention where pessimistic locking is unavailable.

---

## 2. Concurrency Control: Optimistic vs. Pessimistic

### Optimistic Locking (Recommended for High Read/Write Ratio)
Add a `version` column:
```sql
UPDATE accounts 
SET balance = balance - 100, version = version + 1 
WHERE id = :id AND version = :expected_version;
```
If affected rows = 0, throw a concurrency conflict and return `409 Conflict`.

### Pessimistic Locking (Recommended for High Contention Inventory)
```sql
SELECT * FROM inventory_items WHERE id = :id FOR UPDATE;
```
Enforce short transaction timeouts to avoid deadlocks.

---

## 3. Distributed Transactions (Saga Pattern)

In microservice environments where 2-Phase Commit (2PC) impairs availability, use an **Orchestrated Saga**:
- Each local transaction commits locally.
- If step $N$ fails, compensating transactions are executed in reverse ($N-1 \dots 1$) to restore eventual consistency.
