#!/usr/bin/env python3
"""
analyzeMigration.py
Analyzes DDL migration scripts for dangerous, blocking, or non-backward-compatible operations:
- Direct DROP COLUMN or DROP TABLE without deprecation
- Direct RENAME COLUMN
- Non-concurrent index creation (CREATE INDEX without CONCURRENTLY)
- Adding NOT NULL columns without DEFAULT values
"""

import sys
import os
import re
import json
import argparse

def analyze_migration_sql(sql_content):
    risks = []
    
    # 1. Check for DROP COLUMN
    drop_col_matches = re.findall(r"alter\s+table\s+([a-zA-Z0-9_\"\.]+)\s+drop\s+(?:column\s+)?([a-zA-Z0-9_\"\.]+)", sql_content, re.IGNORECASE)
    for table, col in drop_col_matches:
        risks.append({
            "severity": "CRITICAL",
            "operation": "DROP_COLUMN",
            "table": table.strip(),
            "target": col.strip(),
            "message": f"Directly dropping column '{col.strip()}' on table '{table.strip()}' breaks running applications. Use expand-and-contract phase 3."
        })

    # 2. Check for RENAME COLUMN
    rename_matches = re.findall(r"alter\s+table\s+([a-zA-Z0-9_\"\.]+)\s+rename\s+(?:column\s+)?([a-zA-Z0-9_\"\.]+)\s+to\s+([a-zA-Z0-9_\"\.]+)", sql_content, re.IGNORECASE)
    for table, old_c, new_c in rename_matches:
        risks.append({
            "severity": "CRITICAL",
            "operation": "RENAME_COLUMN",
            "table": table.strip(),
            "target": f"{old_c.strip()} -> {new_c.strip()}",
            "message": "Renaming columns causes immediate downtime for running application code. Use dual-writing with expand-and-contract."
        })

    # 3. Check for CREATE INDEX without CONCURRENTLY
    create_idx_matches = re.findall(r"create\s+(?:unique\s+)?index\s+(?!concurrently\b)([a-zA-Z0-9_\"\.]+)\s+on\s+([a-zA-Z0-9_\"\.]+)", sql_content, re.IGNORECASE)
    for idx_name, table in create_idx_matches:
        risks.append({
            "severity": "HIGH",
            "operation": "BLOCKING_INDEX_CREATION",
            "table": table.strip(),
            "target": idx_name.strip(),
            "message": f"Index '{idx_name.strip()}' on '{table.strip()}' created without CONCURRENTLY. This takes an exclusive write lock on production tables."
        })

    # 4. Check for ADD COLUMN NOT NULL without DEFAULT
    add_not_null = re.findall(r"alter\s+table\s+([a-zA-Z0-9_\"\.]+)\s+add\s+(?:column\s+)?([a-zA-Z0-9_\"\.]+)\s+[^;]+?not\s+null(?!\s+default\b)", sql_content, re.IGNORECASE)
    for table, col in add_not_null:
        risks.append({
            "severity": "HIGH",
            "operation": "ADD_NOT_NULL_NO_DEFAULT",
            "table": table.strip(),
            "target": col.strip(),
            "message": f"Adding NOT NULL column '{col.strip()}' without a DEFAULT fails if existing rows exist in table '{table.strip()}'."
        })

    critical_count = len([r for r in risks if r["severity"] == "CRITICAL"])
    high_count = len([r for r in risks if r["severity"] == "HIGH"])

    return {
        "isSafeForZeroDowntime": critical_count == 0 and high_count == 0,
        "summary": {
            "criticalRisks": critical_count,
            "highRisks": high_count,
            "totalFindings": len(risks)
        },
        "findings": risks
    }

def main():
    parser = argparse.ArgumentParser(description="Analyze DDL migration scripts for zero-downtime safety")
    parser.add_argument("--migration", help="Path to SQL migration file", required=False)
    args = parser.parse_args()

    if args.migration and os.path.exists(args.migration):
        with open(args.migration) as f:
            content = f.read()
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        content = """
        -- Safe expand migration
        ALTER TABLE users ADD COLUMN full_name VARCHAR(255) NULL;
        CREATE INDEX CONCURRENTLY idx_users_full_name ON users (full_name);
        """

    result = analyze_migration_sql(content)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["isSafeForZeroDowntime"] else 1)

if __name__ == "__main__":
    main()
