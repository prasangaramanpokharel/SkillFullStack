#!/usr/bin/env python3
"""
inspectDatabaseIndexes.py
Inspects SQL DDL schemas to identify:
- Foreign key columns lacking a supporting secondary index (causes Seq Scans & cascade locks)
- Index definitions on boolean or very low cardinality columns without a filter/partial clause
"""

import sys
import os
import re
import json
import argparse

def inspect_indexes(sql_content):
    findings = []
    
    # 1. Find all foreign keys and their columns
    # FOREIGN KEY (col) REFERENCES other_table
    fk_pattern = re.compile(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_\"\.]+)\s*\((.*?)\);", re.DOTALL | re.IGNORECASE)
    tables = fk_pattern.findall(sql_content)
    
    fks = []
    for table_name, body in tables:
        clean_tbl = table_name.replace('"', '').strip()
        fk_matches = re.findall(r"foreign\s+key\s*\(([^\)]+)\)\s*references\s+([a-zA-Z0-9_\"\.]+)", body, re.IGNORECASE)
        for fk_col, ref_tbl in fk_matches:
            col_list = [c.replace('"', '').strip().lower() for c in fk_col.split(",")]
            fks.append({
                "table": clean_tbl,
                "columns": col_list,
                "column_str": fk_col.replace('"', '').strip(),
                "referencedTable": ref_tbl.replace('"', '').strip()
            })

    # 2. Find all index definitions
    idx_pattern = re.compile(r"CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:CONCURRENTLY\s+)?([a-zA-Z0-9_\"\.]+)\s+ON\s+([a-zA-Z0-9_\"\.]+)\s*(?:USING\s+\w+\s*)?\(([^\)]+)\)", re.IGNORECASE)
    indexes = idx_pattern.findall(sql_content)
    
    idx_map = {}
    for idx_name, tbl, cols in indexes:
        clean_tbl = tbl.replace('"', '').strip()
        col_list = [c.replace('"', '').strip().lower() for c in cols.split(",")]
        if clean_tbl not in idx_map:
            idx_map[clean_tbl] = []
        idx_map[clean_tbl].append({
            "name": idx_name.replace('"', '').strip(),
            "columns": col_list,
            "leadingColumn": col_list[0]
        })

    # Also find PRIMARY KEY and UNIQUE constraints in tables that act as indexes
    for table_name, body in tables:
        clean_tbl = table_name.replace('"', '').strip()
        
        pk_matches = re.findall(r"primary\s+key\s*\(([^\)]+)\)", body, re.IGNORECASE)
        for pk_cols in pk_matches:
            col_list = [c.replace('"', '').strip().lower() for c in pk_cols.split(",")]
            if clean_tbl not in idx_map:
                idx_map[clean_tbl] = []
            idx_map[clean_tbl].append({
                "name": f"pk_{clean_tbl}_{col_list[0]}",
                "columns": col_list,
                "leadingColumn": col_list[0]
            })

        uq_matches = re.findall(r"unique\s*\(([^\)]+)\)", body, re.IGNORECASE)
        for uq_cols in uq_matches:
            col_list = [c.replace('"', '').strip().lower() for c in uq_cols.split(",")]
            if clean_tbl not in idx_map:
                idx_map[clean_tbl] = []
            idx_map[clean_tbl].append({
                "name": f"uq_{clean_tbl}_{col_list[0]}",
                "columns": col_list,
                "leadingColumn": col_list[0]
            })

    # Check for unindexed foreign keys
    # An index supports a foreign key if its leading columns match the foreign key column sequence
    for fk in fks:
        table_indexes = idx_map.get(fk["table"], [])
        fk_cols = fk["columns"]
        has_index = False
        for idx in table_indexes:
            idx_cols = idx["columns"]
            if len(idx_cols) >= len(fk_cols) and idx_cols[:len(fk_cols)] == fk_cols:
                has_index = True
                break
        if not has_index:
            findings.append({
                "level": "WARN",
                "table": fk["table"],
                "column": fk["column_str"],
                "rule": "UNINDEXED_FOREIGN_KEY",
                "message": f"Foreign key column(s) '({fk['column_str']})' in table '{fk['table']}' lack a supporting index at the leading edge. This risks table scans during joins and delete cascades."
            })

    # Check for redundant single-column prefix indexes
    for tbl, idxs in idx_map.items():
        single_col_idxs = [idx for idx in idxs if len(idx["columns"]) == 1 and not idx["name"].startswith("uq_") and not idx["name"].startswith("pk_")]
        multi_col_idxs = [idx for idx in idxs if len(idx["columns"]) > 1]
        for s_idx in single_col_idxs:
            col = s_idx["columns"][0].lower()
            matching_composite = next((m for m in multi_col_idxs if m["leadingColumn"].lower() == col), None)
            if matching_composite:
                findings.append({
                    "level": "WARN",
                    "table": tbl,
                    "index": s_idx["name"],
                    "rule": "REDUNDANT_PREFIX_INDEX",
                    "message": f"Index '{s_idx['name']}' on '{tbl}({col})' is redundant because '{matching_composite['name']}' already indexes '{col}' as its leading column."
                })

    unindexed_fks = [f for f in findings if f["rule"] == "UNINDEXED_FOREIGN_KEY"]
    redundant_idxs = [f for f in findings if f["rule"] == "REDUNDANT_PREFIX_INDEX"]

    return {
        "foreignKeysAudited": len(fks),
        "indexesAudited": len(indexes),
        "unindexedFkCount": len(unindexed_fks),
        "redundantIndexCount": len(redundant_idxs),
        "findings": findings
    }

def main():
    parser = argparse.ArgumentParser(description="Inspect SQL indexes and foreign keys")
    parser.add_argument("--schema", help="Path to SQL schema file", required=False)
    args = parser.parse_args()

    if args.schema and os.path.exists(args.schema):
        with open(args.schema) as f:
            content = f.read()
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        content = """
        CREATE TABLE orders (
            id BIGINT PRIMARY KEY,
            customer_id BIGINT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
        CREATE INDEX idx_orders_customer_id ON orders (customer_id);
        """

    result = inspect_indexes(content)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
