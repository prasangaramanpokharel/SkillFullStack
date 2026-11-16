#!/usr/bin/env python3
"""
auditTestPyramid.py
Scans the current project directory for test files, classifying them into Unit, Integration,
and End-to-End tiers to evaluate alignment with the test pyramid.
"""

import os
import re
import json

def classify_test_file(path):
    lower = path.lower()
    if any(k in lower for k in ["e2e", "cypress", "playwright", "integration", "spec.integ"]):
        if any(k in lower for k in ["e2e", "cypress", "playwright"]):
            return "e2e"
        return "integration"
    return "unit"

def scan_project(root_dir="."):
    test_files = {"unit": [], "integration": [], "e2e": []}
    
    test_patterns = [
        re.compile(r".*\.(test|spec)\.(ts|tsx|js|jsx)$"),
        re.compile(r"test_.*\.py$"),
        re.compile(r".*_test\.py$"),
        re.compile(r".*_test\.go$")
    ]
    
    ignore_dirs = {".git", "node_modules", ".venv", "venv", "dist", "build", ".next", ".research"}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if any(p.match(f) for p in test_patterns):
                rel_path = os.path.relpath(os.path.join(root, f), root_dir)
                category = classify_test_file(rel_path)
                test_files[category].append(rel_path)

    total = sum(len(v) for v in test_files.values())
    ratios = {
        k: (round(len(v) / total * 100, 1) if total > 0 else 0)
        for k, v in test_files.items()
    }

    healthy = ratios["unit"] >= 60 and ratios["e2e"] <= 20 if total > 0 else True

    return {
        "totalTestFiles": total,
        "counts": {k: len(v) for k, v in test_files.items()},
        "ratiosPercent": ratios,
        "isPyramidHealthy": healthy,
        "files": test_files
    }

if __name__ == "__main__":
    report = scan_project(".")
    print(json.dumps(report, indent=2))
