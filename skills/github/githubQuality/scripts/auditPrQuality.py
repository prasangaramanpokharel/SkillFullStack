#!/usr/bin/env python3
"""
auditPrQuality.py
Audits a GitHub pull request for conventional commit title format and checklist compliance.
"""

import sys
import re
import argparse
import subprocess

CONVENTIONAL_REGEX = r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-zA-Z0-9_\-]+\))?:\s+.+"

def audit_pr(pr_number: str):
    print(f" Auditing Pull Request #{pr_number}...")
    try:
        res = subprocess.run(
            ["gh", "pr", "view", pr_number, "--json", "title,body,state,author"],
            capture_output=True, text=True, check=True
        )
        import json
        data = json.loads(res.stdout)
        title = data.get("title", "")
        body = data.get("body", "")

        issues = []
        # Check conventional commit format
        if not re.match(CONVENTIONAL_REGEX, title):
            issues.append(f"Title '{title}' does not follow Conventional Commits (e.g., 'feat(scope): message')")

        # Check for uncompleted checkboxes
        uncompleted = len(re.findall(r"-\s*\[\s*\]", body))
        if uncompleted > 0:
            issues.append(f"PR contains {uncompleted} uncompleted checklist item(s) in the description.")

        if issues:
            print("❌ PR Quality Audit Failed:")
            for i in issues:
                print(f"  • {i}")
            sys.exit(1)
        else:
            print(f" PR #{pr_number} complies with conventional commit and quality standards!")

    except subprocess.CalledProcessError as e:
        print(f" Failed querying PR: {e.stderr.strip() or e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", required=True, help="PR number")
    args = parser.parse_args()
    audit_pr(args.pr)
