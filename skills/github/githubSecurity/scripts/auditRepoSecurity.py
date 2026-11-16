#!/usr/bin/env python3
"""
auditRepoSecurity.py
Queries GitHub API via gh to audit open Dependabot alerts and secret scanning posture.
"""

import sys
import json
import argparse
import subprocess

def audit_security(repo: str):
    print(f" Auditing GitHub Security Posture for: {repo}")

    # 1. Query Dependabot alerts
    try:
        res = subprocess.run(
            ["gh", "api", f"/repos/{repo}/dependabot/alerts", "--jq", ".[] | {number: .number, state: .state, severity: .security_advisory.severity, summary: .security_advisory.summary}"],
            capture_output=True, text=True, check=True
        )
        alerts = [json.loads(line) for line in res.stdout.strip().splitlines() if line.strip()]
        open_alerts = [a for a in alerts if a.get("state") == "open"]
        critical = [a for a in open_alerts if a.get("severity") in ["critical", "high"]]

        print(f" Dependabot: {len(open_alerts)} open alerts ({len(critical)} Critical/High)")
        for c in critical[:5]:
            print(f"  ▲ [{c.get('severity', '').upper()}] #{c.get('number')}: {c.get('summary')}")
    except subprocess.CalledProcessError as e:
        print(f" Dependabot alerts could not be queried (or are disabled): {e.stderr.strip() or 'Not enabled'}")

    # 2. Query Secret Scanning alerts
    try:
        res = subprocess.run(
            ["gh", "api", f"/repos/{repo}/secret-scanning/alerts", "--jq", "length"],
            capture_output=True, text=True, check=True
        )
        count = res.stdout.strip()
        print(f" Secret Scanning: {count} alerts detected.")
    except subprocess.CalledProcessError as e:
        print(f" Secret Scanning alerts query: {e.stderr.strip() or 'Not available/enabled'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit repository security posture")
    parser.add_argument("--repo", required=True, help="Repository owner/repo")
    args = parser.parse_args()

    audit_security(args.repo)
