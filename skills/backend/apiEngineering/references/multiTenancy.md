# Multi-Tenancy Architecture & Tenant Isolation Reference

---

## 1. Multi-Tenant Data Isolation Strategies

| Strategy | Architecture | Cost | Isolation | Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Shared DB, Shared Schema (Row-Level)** | `tenant_id` column on all tables. | Lowest | Logical (Code/RLS) | High discipline needed |
| **Shared DB, Separate Schemas** | PostgreSQL schema per tenant (`tenant_acme.invoices`). | Moderate | Schema namespace | Schema migrations overhead |
| **Database per Tenant** | Completely independent database instance or cluster. | Highest | Complete physical | High infrastructure cost |

---

## 2. Row-Level Security (PostgreSQL RLS)

To prevent BOLA leaks even if application code omits a `WHERE tenant_id = ...` filter, enforce database-level RLS:
```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON invoices
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```
Set session variable upon acquiring connection:
```sql
SET LOCAL app.current_tenant_id = '01HX9...';
```
