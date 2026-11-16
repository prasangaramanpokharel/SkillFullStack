# Database Schema Migration Policies

Policies governing zero-downtime schema evolution and rollback procedures.

---

## 1. Zero-Downtime Expand-and-Contract Protocol

Directly modifying or dropping live columns causes downtime because running application pods expect the old schema. All breaking changes must follow the **Expand-and-Contract** methodology:

1. **Expand**: Add the new column as nullable (`ALTER TABLE users ADD COLUMN full_name VARCHAR(255) NULL`). Deploy application code that writes to both old and new columns.
2. **Backfill**: Run asynchronous background jobs in small batches to populate the new column for historical rows.
3. **Contract**: Update application code to read exclusively from the new column. Once verified, deprecate and drop the old column in a subsequent release.

---

## 2. Forbidden Migration Patterns in Production

- **`ALTER TABLE ... ADD COLUMN ... DEFAULT <value>` without fast-default support**: Avoid full table rewrites and table locks.
- **`ALTER TABLE ... DROP COLUMN ...` without deprecation cycle**: Must have zero active queries referencing the column before drop.
- **`CREATE INDEX` without `CONCURRENTLY`**: Never take an exclusive table lock during index creation on active production tables.
- **Renaming Columns**: Never rename columns directly (`ALTER TABLE ... RENAME COLUMN ...`). Use expand-and-contract with dual-writing.
