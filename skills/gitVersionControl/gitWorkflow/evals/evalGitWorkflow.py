#!/usr/bin/env python3
"""
evalGitWorkflow.py
Validates the diagnostic script and ensures that gitWorkflow executes cleanly.
"""

import subprocess
import json
import os
import sys

def test_diagnose_script():
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "diagnoseGitGraph.py")
    res = subprocess.run([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 0, f"Script failed: {res.stderr}"
    data = json.loads(res.stdout)
    assert "recommendation" in data
    print(" test_diagnose_script default workspace check passed")

def test_diagnose_script_in_repo():
    import tempfile
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "diagnoseGitGraph.py"))
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(["git", "init"], cwd=tmpdir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("hello")
        subprocess.run(["git", "add", "."], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=tmpdir, check=True)
        
        res = subprocess.run([sys.executable, script_path], cwd=tmpdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert res.returncode == 0, f"Failed in git repo: {res.stderr}"
        data = json.loads(res.stdout)
        assert data.get("isClean") is True
        assert data.get("branch") in ["main", "master"]
        print(" test_diagnose_script_in_repo passed")

if __name__ == "__main__":
    test_diagnose_script()
    test_diagnose_script_in_repo()
    print("All gitWorkflow evals passed.")
