#!/usr/bin/env python3
"""
Neon Serverless Postgres Configuration Auditor
Audits database connection strings, ORM configurations, and driver selections:
- Verifies migration scripts use Direct Connection instead of Pooled Connection
- Verifies serverless route handlers use @neondatabase/serverless or pooled connections
- Detects un-pooled raw pg connections in serverless/edge environments
"""

import os
import sys
import re

def audit_neon_config(target_dir):
    print(f"\n🔍 Auditing Neon Postgres Configuration in: {target_dir}")
    issues = []
    scanned = 0

    for root, _, files in os.walk(target_dir):
        if any(ignored in root for ignored in ['node_modules', '.git', 'dist', '.next']):
            continue
        for file in files:
            if file.endswith(('.ts', '.js', '.tsx', '.jsx', '.env', '.env.example', '.prisma')):
                scanned += 1
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # Check for migrations using pooler
                        if 'migrate' in file.lower() and '-pooler' in content:
                            issues.append((filepath, "CRITICAL: Schema migrations must use the Direct connection string (without -pooler), as PgBouncer does not support advisory locks and DDL."))

                        # Check for raw pg Client in serverless
                        if ('api/' in filepath or 'routes/' in filepath) and 'new Client(' in content and 'neon' not in content:
                            issues.append((filepath, "WARNING: Detected raw pg.Client in route handler. Use @neondatabase/serverless or pooled connection to prevent socket exhaustion."))
                except Exception:
                    pass

    print(f"Scanned {scanned} configuration & source files.")
    if not issues:
        print("✅ PASS: Neon connection architecture adheres to best practices.\n")
        return 0
    else:
        print(f"⚠️  Found {len(issues)} issue(s):")
        for f, msg in issues:
            print(f"  • {f}\n    {msg}")
        print("")
        return 1

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    sys.exit(audit_neon_config(target))
