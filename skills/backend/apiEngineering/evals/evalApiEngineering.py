#!/usr/bin/env python3
"""
evalApiEngineering.py
Evaluates the scripts and compliance checkers in apiEngineering:
- auditApiContract.py (valid & invalid fixtures)
- generateResponseEnvelope.py (TS & Python generation)
- checkBreakingChanges.py (breaking change detection)
"""

import subprocess
import json
import os
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "..", "scripts")
FIXTURES_DIR = os.path.join(BASE_DIR, "fixtures")

def test_audit_valid_fixture():
    valid_spec = os.path.join(FIXTURES_DIR, "valid", "sampleValidOpenApi.json")
    script = os.path.join(SCRIPTS_DIR, "auditApiContract.py")
    res = subprocess.run([sys.executable, script, "--spec", valid_spec], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 0, f"Expected 0 for valid fixture, got {res.returncode}: {res.stderr}"
    data = json.loads(res.stdout)
    assert data["isCompliant"] is True
    print(" test_audit_valid_fixture passed")

def test_audit_invalid_fixture():
    invalid_spec = os.path.join(FIXTURES_DIR, "invalid", "sampleInvalidOpenApi.json")
    script = os.path.join(SCRIPTS_DIR, "auditApiContract.py")
    res = subprocess.run([sys.executable, script, "--spec", invalid_spec], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 1, "Expected 1 for invalid fixture"
    data = json.loads(res.stdout)
    assert data["isCompliant"] is False
    assert any("application/problem+json" in f["message"] for f in data["findings"])
    print(" test_audit_invalid_fixture passed")

def test_generate_envelope():
    script = os.path.join(SCRIPTS_DIR, "generateResponseEnvelope.py")
    
    # Test TypeScript
    res_ts = subprocess.run([sys.executable, script, "--lang", "ts"], stdout=subprocess.PIPE, text=True, check=True)
    assert "export interface ApiResponse<T>" in res_ts.stdout
    assert "export interface ProblemDetails" in res_ts.stdout

    # Test Python
    res_py = subprocess.run([sys.executable, script, "--lang", "py"], stdout=subprocess.PIPE, text=True, check=True)
    assert "class ApiResponse(BaseModel, Generic[T]):" in res_py.stdout
    assert "class ProblemDetails(BaseModel):" in res_py.stdout
    print(" test_generate_envelope passed")

def test_check_breaking_changes():
    script = os.path.join(SCRIPTS_DIR, "checkBreakingChanges.py")
    valid_spec = os.path.join(FIXTURES_DIR, "valid", "sampleValidOpenApi.json")
    
    # Identical specs -> no breaking changes
    res_same = subprocess.run([sys.executable, script, "--old", valid_spec, "--new", valid_spec], stdout=subprocess.PIPE, text=True)
    assert res_same.returncode == 0
    data_same = json.loads(res_same.stdout)
    assert data_same["hasBreakingChanges"] is False

    # Modified spec removing an endpoint
    with tempfile.NamedTemporaryFile("w+", suffix=".json") as tmp:
        modified = {"openapi": "3.2.1", "paths": {}}
        json.dump(modified, tmp)
        tmp.flush()
        res_diff = subprocess.run([sys.executable, script, "--old", valid_spec, "--new", tmp.name], stdout=subprocess.PIPE, text=True)
        assert res_diff.returncode == 1
        data_diff = json.loads(res_diff.stdout)
        assert data_diff["hasBreakingChanges"] is True
        assert any("Removed endpoint" in b for b in data_diff["breakingChanges"])

    print(" test_check_breaking_changes passed")

if __name__ == "__main__":
    test_audit_valid_fixture()
    test_audit_invalid_fixture()
    test_generate_envelope()
    test_check_breaking_changes()
    print("All apiEngineering evals passed successfully!")
