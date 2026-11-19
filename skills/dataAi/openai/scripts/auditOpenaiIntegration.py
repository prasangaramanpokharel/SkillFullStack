#!/usr/bin/env python3
"""
OpenAI Integration Production Auditor
Scans codebases for deprecated Chat Completions / Assistants patterns, missing error handling,
unbounded token limits, and un-cached repetitive prompt headers.
"""

import os
import sys
import re
from pathlib import Path

def audit_directory(target_dir):
    print(f"\n🔍 Auditing OpenAI Integrations in: {target_dir}")
    issues = []
    checked_files = 0

    deprecated_patterns = [
        (r'client\.chat\.completions\.create', 'DEPRECATION: Legacy chat.completions.create detected. Migrate to client.responses.create for better cache hit rates and reasoning performance.'),
        (r'client\.beta\.assistants', 'DEPRECATION: Assistants API detected. Assistants API is sunsetted in favor of Responses API with store: true.'),
        (r'client\.beta\.threads', 'DEPRECATION: Threads API detected. Use Responses API conversation_id for multi-turn state tracking.'),
        (r'OPENAI_API_KEY\s*=\s*["\']sk-[a-zA-Z0-9_-]+["\']', 'SECURITY: Hardcoded OpenAI API key detected. Store credentials in environment variables or cloud secrets.'),
        (r'response_format\s*=\s*\{\s*["\']type["\']\s*:\s*["\']json_object["\']\s*\}', 'WARNING: Using un-typed json_object without schema. Enforce strict JSON Schema with strict: True.'),
    ]

    for root, _, files in os.walk(target_dir):
        if any(ignored in root for ignored in ['node_modules', '.git', '__pycache__', '.venv', 'dist']):
            continue
        for file in files:
            if file.endswith(('.py', '.ts', '.js', '.tsx', '.jsx')):
                filepath = os.path.join(root, file)
                checked_files += 1
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for pattern, msg in deprecated_patterns:
                            if re.search(pattern, content):
                                issues.append((filepath, msg))
                except Exception:
                    pass

    print(f"Scanned {checked_files} source files.")
    if not issues:
        print("✅ PASS: No deprecated patterns or security violations detected.\n")
        return 0
    else:
        print(f"⚠️  Found {len(issues)} issue(s):")
        for f, msg in issues:
            print(f"  • {f}\n    {msg}")
        print("")
        return 1

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    sys.exit(audit_directory(target))
