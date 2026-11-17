#!/usr/bin/env python3
"""
Cloudflare Production Architecture & Security Auditor
Audits Cloudflare projects for:
- Secret leakage in configuration files
- Modern compatibility date pinning
- Deprecated Cloudflare Pages configurations
- Unsafe SQL concatenation in D1 database queries
- Modern Workers Static Assets compliance
"""

import sys
import os
import re
import json
from pathlib import Path

def audit_config_file(filepath: Path):
    issues = []
    content = filepath.read_text(encoding="utf-8", errors="ignore")
    rel_path = filepath.name

    # Check for hardcoded secrets in vars block
    secret_patterns = [r'["\']?[A-Z0-9_]*(?:SECRET|PASSWORD|PRIVATE_KEY|TOKEN)["\']?\s*:\s*["\'][^"\']+["\']',
                       r'[A-Z0-9_]*(?:SECRET|PASSWORD|PRIVATE_KEY|TOKEN)\s*=\s*["\'][^"\']+["\']']
    for pat in secret_patterns:
        if re.search(pat, content, re.IGNORECASE):
            issues.append(f"[{rel_path}] Sensitive secret pattern detected in configuration. Secrets should be provisioned via `wrangler secret put <NAME>` or Cloudflare Secrets Store, never plain text.")

    # Check compatibility date
    comp_match = re.search(r'["\']?compatibility_date["\']?\s*[:=]\s*["\'](\d{4}-\d{2}-\d{2})["\']', content)
    if not comp_match:
        issues.append(f"[{rel_path}] Missing `compatibility_date`. Pin to a current date (e.g. '2026-11-01') to prevent unexpected runtime behavioral shifts.")
    else:
        year = int(comp_match.group(1).split("-")[0])
        if year < 2025:
            issues.append(f"[{rel_path}] Outdated `compatibility_date` ({comp_match.group(1)}). Consider upgrading to a modern 2025/2026 compatibility date.")

    # Check for deprecated Pages syntax
    if "pages_build_output_dir" in content:
        issues.append(f"[{rel_path}] Deprecated `pages_build_output_dir` detected. Cloudflare recommends migrating to Workers Static Assets (`\"assets\": {{ \"directory\": \"./dist\" }}`).")

    return issues

def audit_source_code(filepath: Path):
    issues = []
    content = filepath.read_text(encoding="utf-8", errors="ignore")
    rel_path = filepath.name

    # Check for D1 SQL string concatenation
    if re.search(r'\.(?:prepare|exec)\s*\(\s*`[^`]*\$\{', content):
        issues.append(f"[{rel_path}] Potential SQL injection detected in D1 query. Avoid template literals in `prepare()`. Use parameterized queries (`?`) and `.bind(...)`.")

    # Check for long timeouts without abort signals
    if "fetch(" in content and "AbortSignal.timeout" not in content and "signal:" not in content:
        # Informational check
        pass

    return issues

def audit_project(root_dir: str):
    root = Path(root_dir)
    print(f"🚀 Scanning Cloudflare project at: {root.resolve()}")
    all_issues = []

    # 1. Audit configs
    for cfg in ["wrangler.jsonc", "wrangler.json", "wrangler.toml", "cloudflare.config.ts"]:
        for cfg_file in root.rglob(cfg):
            if "node_modules" not in str(cfg_file):
                all_issues.extend(audit_config_file(cfg_file))

    # 2. Audit source code
    src_dir = root / "src"
    target_dir = src_dir if src_dir.exists() else root
    for ext in ["*.ts", "*.js", "*.tsx", "*.jsx"]:
        for code_file in target_dir.rglob(ext):
            if "node_modules" not in str(code_file) and ".git" not in str(code_file):
                all_issues.extend(audit_source_code(code_file))

    print("\n" + "=" * 60)
    print("📋 CLOUDFLARE PRODUCTION AUDIT REPORT")
    print("=" * 60)
    if not all_issues:
        print("✅ No Cloudflare architectural or security issues detected! Production ready.")
        return 0
    else:
        print(f"⚠️  Found {len(all_issues)} architectural suggestion(s):")
        for idx, issue in enumerate(all_issues, 1):
            print(f"  {idx}. {issue}")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(audit_project(target))
