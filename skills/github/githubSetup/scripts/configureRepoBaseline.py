#!/usr/bin/env python3
"""
configureRepoBaseline.py
Configures repository baseline settings and imports the production ruleset via gh CLI.
"""

import sys
import json
import argparse
import subprocess

def configure_repo(repo: str, ruleset_file: str = None):
    print(f" Configuring repository baseline for: {repo}")

    # 1. Apply repo settings
    cmd_settings = [
        "gh", "repo", "edit", repo,
        "--enable-squash-merge=true",
        "--enable-merge-commit=false",
        "--enable-rebase-merge=false",
        "--delete-branch-on-merge=true",
        "--enable-auto-merge=true"
    ]
    try:
        subprocess.run(cmd_settings, check=True)
        print(" Successfully configured squash-merge and auto-deletion settings.")
    except Exception as e:
        print(f" Failed setting repository flags: {e}")

    # 2. Apply ruleset if file provided
    if ruleset_file:
        print(f" Importing ruleset from {ruleset_file}...")
        cmd_ruleset = ["gh", "api", "-X", "POST", f"/repos/{repo}/rulesets", "--input", ruleset_file]
        try:
            res = subprocess.run(cmd_ruleset, capture_output=True, text=True, check=True)
            print(" Production Ruleset active on default branch!")
        except subprocess.CalledProcessError as err:
            print(f" Failed importing ruleset: {err.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure GitHub repository baseline")
    parser.add_argument("--repo", required=True, help="Repository in format owner/repo")
    parser.add_argument("--ruleset", help="Optional path to ruleset JSON template")
    args = parser.parse_args()

    configure_repo(args.repo, args.ruleset)
