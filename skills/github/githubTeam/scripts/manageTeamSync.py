#!/usr/bin/env python3
"""
manageTeamSync.py
Queries and displays GitHub organization team hierarchy and permission bindings.
"""

import sys
import json
import argparse
import subprocess

def inspect_teams(org: str):
    print(f" Querying team structure for organization: {org}...")
    try:
        res = subprocess.run(
            ["gh", "api", f"/orgs/{org}/teams", "--jq", ".[] | {name: .name, slug: .slug, privacy: .privacy, members_count: .members_count, parent: .parent.slug}"],
            capture_output=True, text=True, check=True
        )
        teams = [json.loads(line) for line in res.stdout.strip().splitlines() if line.strip()]
        print(f" Organization '{org}' contains {len(teams)} teams:")
        for t in teams:
            parent_str = f" (Child of @{t['parent']})" if t.get("parent") else " [Root]"
            print(f"  • @{t['slug']}{parent_str}: {t.get('members_count', 0)} members ({t.get('privacy')})")
    except subprocess.CalledProcessError as e:
        print(f" Failed querying organization teams: {e.stderr.strip() or e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--org", required=True, help="GitHub organization name")
    args = parser.parse_args()
    inspect_teams(args.org)
