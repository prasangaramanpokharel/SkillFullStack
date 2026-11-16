#!/usr/bin/env python3
"""
evalTdd.py
Evaluates the testDrivenDevelopment skill scripts and pyramid auditing logic.
"""

import subprocess
import json
import os
import sys

def test_audit_test_pyramid():
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "auditTestPyramid.py")
    res = subprocess.run([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 0, f"Script failed: {res.stderr}"
    data = json.loads(res.stdout)
    assert "totalTestFiles" in data
    assert "counts" in data
    assert "ratiosPercent" in data
    assert "isPyramidHealthy" in data
    print(" test_audit_test_pyramid passed")

if __name__ == "__main__":
    test_audit_test_pyramid()
    print("All testDrivenDevelopment evals passed.")
