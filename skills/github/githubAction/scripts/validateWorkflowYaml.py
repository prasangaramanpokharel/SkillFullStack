#!/usr/bin/env python3
"""
validateWorkflowYaml.py
Lints GitHub Actions workflow files for security best practices and anti-patterns.
"""

import os
import re
import sys
import argparse

def validate_workflow(file_path: str) -> list[str]:
    issues = []
    if not os.path.exists(file_path):
        return [f"File not found: {file_path}"]

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check permissions block
    if "permissions:" not in content:
        issues.append("Security Warning: No top-level or job-level 'permissions:' block defined (defaults to write-all in some configurations).")

    # 2. Check for missing timeout-minutes
    if "timeout-minutes:" not in content:
        issues.append("Reliability Warning: No 'timeout-minutes:' defined. Stuck jobs could consume full billing quotas.")

    # 3. Check for floating @v tags in uses:
    lines = content.splitlines()
    for idx, line in enumerate(lines, 1):
        if "uses:" in line and not line.strip().startswith("#"):
            # Check if it uses actions/ but doesn't have SHA-256 (40 hex chars)
            match = re.search(r"uses:\s*([a-zA-Z0-9_\-\./]+)@([a-zA-Z0-9_\-\.]+)", line)
            if match:
                action, ref = match.group(1), match.group(2)
                if not re.match(r"^[0-9a-f]{40}$", ref):
                    issues.append(f"Line {idx}: Action '{action}' uses mutable ref '@{ref}'. Pin to a 40-character commit SHA for supply-chain integrity.")

    return issues

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lint GitHub Actions workflows")
    parser.add_argument("--file", required=True, help="Path to workflow YAML")
    args = parser.parse_args()

    results = validate_workflow(args.file)
    if results:
        print(f"⚠️ Validation warnings for {args.file}:")
        for r in results:
            print(f"  • {r}")
        sys.exit(1)
    else:
        print(f" Workflow {args.file} passed all security and reliability checks!")
