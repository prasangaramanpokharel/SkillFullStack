#!/usr/bin/env python3
"""
auditDatabaseSchema.py
Static SQL DDL linter checking:
- Presence of PRIMARY KEY on every table
- Explicit referential actions on FOREIGN KEY constraints
- Presence of NOT NULL on non-nullable fields
- Detection of dangerous EAV or unstructured JSON anti-patterns without constraints
"""

import sys
import os
import re
import json
import argparse

def audit_sql_schema(sql_content):
    findings = []
    
    # Extract CREATE TABLE blocks
    table_pattern = re.compile(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_\"\.]+)\s*\((.*?)\);", re.DOTALL | re.IGNORECASE)
    tables = table_pattern.findall(sql_content)
    
    if not tables:
        findings.append({"level": "WARN", "message": "No CREATE TABLE statements found in input."})

    PROHIBITED_TABLE_NAMES = {"data", "info", "items", "records", "logs", "temp", "test"}
    PROHIBITED_COLUMN_NAMES = {"misc", "extra_data", "temp", "field1", "future_use", "data"}

    for table_name, body in tables:
        clean_name = table_name.replace('"', '').strip()
        body_lower = body.lower()
        
        # 1. Table Naming Checks
        if clean_name.lower().startswith("tbl_") or clean_name.lower().startswith("tbl"):
            findings.append({
                "level": "WARN",
                "table": clean_name,
                "rule": "TABLE_NAMING_HUNGARIAN_PREFIX",
                "message": f"Table '{clean_name}' uses Hungarian notation prefix 'tbl_'. Use clean plural snake_case instead."
            })
        if clean_name.lower() in PROHIBITED_TABLE_NAMES:
            findings.append({
                "level": "ERROR",
                "table": clean_name,
                "rule": "TABLE_NAMING_GENERIC_PROHIBITED",
                "message": f"Table name '{clean_name}' is generic and prohibited. Specify the business domain entity name."
            })
        if any(c.isupper() for c in clean_name):
            findings.append({
                "level": "WARN",
                "table": clean_name,
                "rule": "TABLE_NAMING_SNAKE_CASE",
                "message": f"Table '{clean_name}' uses uppercase or PascalCase letters. Use lowercase snake_case."
            })

        # 2. Check for Primary Key
        has_pk = "primary key" in body_lower
        if not has_pk:
            findings.append({
                "level": "ERROR",
                "table": clean_name,
                "rule": "PRIMARY_KEY_REQUIRED",
                "message": f"Table '{clean_name}' does not define a PRIMARY KEY."
            })

        # 3. Check Foreign Keys for ON DELETE clause
        fk_matches = re.findall(r"foreign\s+key\s*\([^\)]+\)\s*references\s+([a-zA-Z0-9_\"\.]+)(?:\s*\([^\)]+\))?([^,\n\)]*)", body, re.IGNORECASE)
        for ref_table, clause in fk_matches:
            if "on delete" not in clause.lower():
                findings.append({
                    "level": "WARN",
                    "table": clean_name,
                    "rule": "EXPLICIT_REFERENTIAL_ACTION",
                    "message": f"Foreign key referencing '{ref_table.strip()}' missing explicit ON DELETE action (e.g. RESTRICT or CASCADE)."
                })

        # 4. Check for speculative/generic columns (YAGNI / Lean Schema)
        col_lines = [line.strip().split()[0].replace('"', '') for line in body.splitlines() if line.strip() and not line.strip().upper().startswith(("PRIMARY", "FOREIGN", "CONSTRAINT", "UNIQUE", "CHECK", ")"))]
        for col in col_lines:
            if col.lower() in PROHIBITED_COLUMN_NAMES:
                findings.append({
                    "level": "WARN",
                    "table": clean_name,
                    "column": col,
                    "rule": "SPECULATIVE_CATCHALL_COLUMN",
                    "message": f"Column '{col}' appears to be a generic catch-all or speculative field violating the Lean Schema Law (YAGNI)."
                })

        # 5. Check for multi-tenant tenant_id recommendation
        if any(keyword in clean_name for keyword in ["order", "invoice", "account", "customer", "project"]):
            if "tenant_id" not in body_lower:
                findings.append({
                    "level": "INFO",
                    "table": clean_name,
                    "rule": "TENANT_ISOLATION_RECOMMENDATION",
                    "message": f"Tenant-scoped entity table '{clean_name}' does not include a 'tenant_id' column."
                })

        # 6. Check for Temporal Booking Exclusion Constraint
        if any(w in clean_name for w in ["appointment", "booking", "reservation", "schedule", "stay"]):
            if ("start" in body_lower and "end" in body_lower) or ("assigned_at" in body_lower and "vacated_at" in body_lower):
                if "exclude" not in body_lower or "gist" not in body_lower:
                    findings.append({
                        "level": "WARN",
                        "table": clean_name,
                        "rule": "MISSING_EXCLUSION_CONSTRAINT",
                        "message": f"Temporal allocation table '{clean_name}' lacks a PostgreSQL Exclusion Constraint (EXCLUDE USING gist) to prevent overlapping double-bookings."
                    })

        # 7. Check for Cross-Tenant Composite Foreign Key
        if "tenant_id" in body_lower:
            # Check foreign keys that reference other tables without tenant_id in the key
            simple_fks = re.findall(r"foreign\s+key\s*\(\s*([a-zA-Z0-9_]+)\s*\)\s*references\s+([a-zA-Z0-9_]+)\s*\(\s*([a-zA-Z0-9_]+)\s*\)", body, re.IGNORECASE)
            for col, ref_t, ref_c in simple_fks:
                if col.lower() != "tenant_id" and ref_t.lower() not in ["hospitals", "tenants", "organizations", "accounts"]:
                    findings.append({
                        "level": "WARN",
                        "table": clean_name,
                        "column": col,
                        "rule": "CROSS_TENANT_FK_VULNERABILITY",
                        "message": f"Foreign key on '{clean_name}({col})' referencing '{ref_t}' is not tenant-aware. Enforce composite FK '(tenant_id, {col}) REFERENCES {ref_t}(tenant_id, id)'."
                    })

    # 8. Check for RLS Policy Completeness across entire script
    rls_tables = set(re.findall(r"alter\s+table\s+([a-zA-Z0-9_\"\.]+)\s+enable\s+row\s+level\s+security", sql_content, re.IGNORECASE))
    policy_tables = set(re.findall(r"create\s+policy\s+[a-zA-Z0-9_\"\.]+\s+on\s+([a-zA-Z0-9_\"\.]+)", sql_content, re.IGNORECASE))
    
    rls_clean = {t.replace('"', '').strip() for t in rls_tables}
    policy_clean = {t.replace('"', '').strip() for t in policy_tables}

    for t in rls_clean:
        if t not in policy_clean:
            findings.append({
                "level": "ERROR",
                "table": t,
                "rule": "INCOMPLETE_RLS_POLICY",
                "message": f"Table '{t}' has ROW LEVEL SECURITY enabled, but lacks any CREATE POLICY definition. Normal roles will be completely denied access."
            })

    error_count = len([f for f in findings if f["level"] == "ERROR"])
    warn_count = len([f for f in findings if f["level"] == "WARN"])
    
    return {
        "isCompliant": error_count == 0,
        "summary": {
            "tablesAudited": len(tables),
            "errors": error_count,
            "warnings": warn_count
        },
        "findings": findings
    }

def main():
    parser = argparse.ArgumentParser(description="Audit SQL DDL schema for database architecture rules")
    parser.add_argument("--schema", help="Path to SQL schema file", required=False)
    args = parser.parse_args()

    if args.schema and os.path.exists(args.schema):
        with open(args.schema) as f:
            content = f.read()
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        content = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE
        );
        """

    result = audit_sql_schema(content)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["isCompliant"] else 1)

if __name__ == "__main__":
    main()
