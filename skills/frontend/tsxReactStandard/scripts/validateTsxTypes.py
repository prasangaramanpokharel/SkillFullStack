#!/usr/bin/env python3
"""
validateTsxTypes.py
Lints TSX files for deprecated or anti-patterns (React.FC, forwardRef, TypeScript enum).
"""

import os
import re
import sys

ANTI_PATTERNS = [
    (r"React\.FC\b|React\.FunctionComponent\b", "Deprecated: Avoid React.FC. Use standard function declarations with explicit prop interfaces."),
    (r"forwardRef\s*<", "React 19+: Avoid forwardRef. Pass ref directly as a standard prop."),
    (r"\benum\s+[A-Z]", "Avoid TypeScript enums. Prefer union string literals (e.g. type Status = 'active' | 'inactive')."),
    (r"as\s+unknown\s+as\b", "Unsafe double-casting detected. Write a proper type guard instead of 'as unknown as'."),
]

def check_file(path: str) -> list[str]:
    issues = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f, 1):
            for pattern, msg in ANTI_PATTERNS:
                if re.search(pattern, line):
                    issues.append(f"{path}:{idx} - {msg}")
    return issues

def scan_directory(dir_path: str):
    total_issues = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith((".ts", ".tsx")):
                total_issues.extend(check_file(os.path.join(root, file)))

    if total_issues:
        print(f" Found {len(total_issues)} TSX anti-patterns:")
        for issue in total_issues:
            print(f"  • {issue}")
        sys.exit(1)
    else:
        print(" All scanned TS/TSX files adhere to modern React 19 / TypeScript standards.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_directory(target)
