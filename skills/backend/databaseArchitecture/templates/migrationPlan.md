# Zero-Downtime Database Migration Plan: [Feature/Table Name]

## 1. Migration Overview
- **Target Table**: `table_name`
- **Objective**: [ Add column | Split table | Introduce index | Migrate data type ]
- **Downtime Appetite**: 0 seconds (Zero downtime deployment required)

---

## 2. Phased Execution Plan (Expand-and-Contract)

### Phase 1: Expand (Non-Breaking DDL)
- Add new nullable column or table:
  ```sql
  ALTER TABLE orders ADD COLUMN fulfillment_status VARCHAR(50) NULL;
  ```
- Deploy application release $v1.1$: Writes to both old and new columns. Reads from old column.

### Phase 2: Backfill (Async Batch Data Migration)
- Script migrating historical records in controlled batches:
  ```sql
  UPDATE orders 
  SET fulfillment_status = CASE WHEN status = 'done' THEN 'delivered' ELSE 'pending' END 
  WHERE fulfillment_status IS NULL AND id BETWEEN :start AND :end;
  ```

### Phase 3: Contract (Switch Reads & Clean Up)
- Deploy application release $v1.2$: Reads and writes exclusively from new column.
- Verify zero active queries read the old column.
- Drop old column in non-blocking off-peak migration:
  ```sql
  ALTER TABLE orders DROP COLUMN status;
  ```

---

## 3. Rollback Protocol
- **Phase 1 Rollback**: Drop new column if application release fails. Old column was never modified.
- **Phase 2 Rollback**: Stop backfill background worker.
- **Phase 3 Rollback**: Revert application release back to $v1.1$ reading from old column before dropping it.
