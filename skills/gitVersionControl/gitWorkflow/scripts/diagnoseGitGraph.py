#!/usr/bin/env python3
"""
diagnoseGitGraph.py
Audits the current Git repository state, working tree hygiene, divergence from upstream,
and uncommitted changes. Outputs structured JSON.
"""

import subprocess
import json
import sys

def run_git(cmd):
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None

def main():
    inside_tree = run_git(["git", "rev-parse", "--is-inside-work-tree"])
    if inside_tree != "true":
        result = {
            "isGitRepo": False,
            "error": "Not inside a valid Git repository",
            "recommendation": "Run 'git init' to initialize repository or navigate to a Git-tracked workspace."
        }
        print(json.dumps(result, indent=2))
        sys.exit(0)

    branch = run_git(["git", "branch", "--show-current"]) or "DETACHED"
    head_sha = run_git(["git", "rev-parse", "--short", "HEAD"])
    status_raw = run_git(["git", "status", "--porcelain"]) or ""
    
    modified = []
    untracked = []
    for line in status_raw.splitlines():
        if line.startswith("??"):
            untracked.append(line[3:])
        else:
            modified.append(line)

    upstream = run_git(["git", "rev-parse", "--abbrev-ref", "@{upstream}"])
    ahead, behind = 0, 0
    if upstream:
        counts = run_git(["git", "rev-list", "--left-right", "--count", f"HEAD...{upstream}"])
        if counts:
            parts = counts.split()
            ahead = int(parts[0])
            behind = int(parts[1])

    result = {
        "branch": branch,
        "headSha": head_sha,
        "upstream": upstream or "none",
        "ahead": ahead,
        "behind": behind,
        "isClean": len(status_raw) == 0,
        "modifiedFilesCount": len(modified),
        "untrackedFilesCount": len(untracked),
        "recommendation": (
            "Ready for rebase/merge" if len(status_raw) == 0 else "Working tree dirty: stash or commit before rebasing"
        )
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
