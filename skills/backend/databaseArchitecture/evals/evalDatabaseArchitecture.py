#!/usr/bin/env python3
"""
evalDatabaseArchitecture.py
Evaluates the diagnostic and analysis scripts in databaseArchitecture:
- auditDatabaseSchema.py
- analyzeMigration.py
- inspectDatabaseIndexes.py
"""

import subprocess
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "..", "scripts")
FIXTURES_DIR = os.path.join(BASE_DIR, "fixtures")

def test_audit_valid_schema():
    script = os.path.join(SCRIPTS_DIR, "auditDatabaseSchema.py")
    fixture = os.path.join(FIXTURES_DIR, "validSchema.sql")
    res = subprocess.run([sys.executable, script, "--schema", fixture], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 0, f"Expected 0 for valid schema, got {res.returncode}: {res.stderr}"
    data = json.loads(res.stdout)
    assert data["isCompliant"] is True
    print(" test_audit_valid_schema passed")

def test_audit_invalid_schema():
    script = os.path.join(SCRIPTS_DIR, "auditDatabaseSchema.py")
    fixture = os.path.join(FIXTURES_DIR, "invalidSchema.sql")
    res = subprocess.run([sys.executable, script, "--schema", fixture], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 1, "Expected 1 for invalid schema"
    data = json.loads(res.stdout)
    assert data["isCompliant"] is False
    rules = [f["rule"] for f in data["findings"]]
    assert "PRIMARY_KEY_REQUIRED" in rules
    assert "TABLE_NAMING_HUNGARIAN_PREFIX" in rules
    assert "SPECULATIVE_CATCHALL_COLUMN" in rules
    assert "INCOMPLETE_RLS_POLICY" in rules
    assert "CROSS_TENANT_FK_VULNERABILITY" in rules
    assert "MISSING_EXCLUSION_CONSTRAINT" in rules
    print(" test_audit_invalid_schema passed")

def test_analyze_safe_migration():
    script = os.path.join(SCRIPTS_DIR, "analyzeMigration.py")
    fixture = os.path.join(FIXTURES_DIR, "safeMigration.sql")
    res = subprocess.run([sys.executable, script, "--migration", fixture], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 0, f"Expected 0 for safe migration, got {res.returncode}: {res.stderr}"
    data = json.loads(res.stdout)
    assert data["isSafeForZeroDowntime"] is True
    print(" test_analyze_safe_migration passed")

def test_analyze_dangerous_migration():
    script = os.path.join(SCRIPTS_DIR, "analyzeMigration.py")
    fixture = os.path.join(FIXTURES_DIR, "dangerousMigration.sql")
    res = subprocess.run([sys.executable, script, "--migration", fixture], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 1, "Expected 1 for dangerous migration"
    data = json.loads(res.stdout)
    assert data["isSafeForZeroDowntime"] is False
    ops = [f["operation"] for f in data["findings"]]
    assert "DROP_COLUMN" in ops
    assert "RENAME_COLUMN" in ops
    assert "BLOCKING_INDEX_CREATION" in ops
    print(" test_analyze_dangerous_migration passed")

def test_inspect_indexes():
    script = os.path.join(SCRIPTS_DIR, "inspectDatabaseIndexes.py")
    valid_fixture = os.path.join(FIXTURES_DIR, "validSchema.sql")
    res_valid = subprocess.run([sys.executable, script, "--schema", valid_fixture], stdout=subprocess.PIPE, text=True, check=True)
    data_valid = json.loads(res_valid.stdout)
    assert data_valid["unindexedFkCount"] == 0

    invalid_fixture = os.path.join(FIXTURES_DIR, "invalidSchema.sql")
    res_invalid = subprocess.run([sys.executable, script, "--schema", invalid_fixture], stdout=subprocess.PIPE, text=True, check=True)
    data_invalid = json.loads(res_invalid.stdout)
    assert data_invalid["unindexedFkCount"] > 0
    print(" test_inspect_indexes passed")

if __name__ == "__main__":
    test_audit_valid_schema()
    test_audit_invalid_schema()
    test_analyze_safe_migration()
    test_analyze_dangerous_migration()
    test_inspect_indexes()
    print("All databaseArchitecture evals passed successfully!")
