#!/usr/bin/env python3
"""
configureRepoBaseline.py
Configures repository baseline settings and idempotently deploys or updates
production rulesets via the GitHub CLI (gh), preventing maintainer lockouts,
schema 422 errors, and phantom status checks.
"""

import sys
import os
import json
import glob
import re
import argparse
import subprocess
from typing import Dict, Any, List, Optional, Tuple

def parse_github_error(output: str) -> Optional[Dict[str, Any]]:
    """Attempt to parse GitHub CLI JSON error output."""
    for line in output.splitlines():
        trimmed = line.strip()
        if trimmed.startswith("{") and trimmed.endswith("}"):
            try:
                data = json.loads(trimmed)
                if isinstance(data, dict) and ("message" in data or "errors" in data):
                    return data
            except json.JSONDecodeError:
                pass
    try:
        data = json.loads(output.strip())
        if isinstance(data, dict) and ("message" in data or "errors" in data):
            return data
    except Exception:
        pass
    return None

def format_error_diagnostic(err: subprocess.CalledProcessError) -> str:
    """Format an actionable diagnostic from a failed gh invocation."""
    combined = (err.stderr or "") + "\n" + (err.stdout or "")
    parsed = parse_github_error(combined)
    if parsed:
        msg = f"HTTP Error: {parsed.get('message', 'Unprocessable Entity')}"
        if "errors" in parsed and isinstance(parsed["errors"], list):
            details = "\n".join([f"    - {e.get('message', json.dumps(e)) if isinstance(e, dict) else e}" for e in parsed["errors"]])
            msg += f"\n  Validation Failures:\n{details}"
        if "documentation_url" in parsed:
            msg += f"\n  Reference: {parsed['documentation_url']}"
        return msg
    return err.stderr.strip() if err.stderr else combined.strip()

def detect_local_workflow_jobs() -> List[str]:
    """Scan .github/workflows/*.{yml,yaml} for defined job IDs."""
    job_ids = set()
    workflow_files = glob.glob(".github/workflows/*.yml") + glob.glob(".github/workflows/*.yaml")
    for wf in workflow_files:
        try:
            with open(wf, "r", encoding="utf-8") as f:
                content = f.read()
            # Simple regex search for jobs under 'jobs:' block
            in_jobs = False
            for line in content.splitlines():
                if re.match(r"^jobs:\s*$", line):
                    in_jobs = True
                    continue
                if in_jobs:
                    # Top-level job identifier under jobs: has 2 spaces indent
                    match = re.match(r"^  ([a-zA-Z0-9_\-]+):\s*$", line)
                    if match:
                        job_ids.add(match.group(1))
                    elif re.match(r"^[^\s#]", line):
                        # Exit jobs block
                        in_jobs = False
        except Exception:
            continue
    return sorted(list(job_ids))

def configure_repo_flags(repo: str, dry_run: bool = False) -> bool:
    """Apply standard repository settings: squash-merge only, auto-delete branches."""
    cmd = [
        "gh", "repo", "edit", repo,
        "--enable-squash-merge=true",
        "--enable-merge-commit=false",
        "--enable-rebase-merge=false",
        "--delete-branch-on-merge=true",
        "--enable-auto-merge=true"
    ]
    if dry_run:
        print(f" [DRY-RUN] Would configure repo flags: {' '.join(cmd)}")
        return True

    print(f" Configuring repository baseline flags for {repo}...")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("  ✓ Successfully configured squash-merge, auto-delete, and auto-merge settings.")
        return True
    except subprocess.CalledProcessError as err:
        print(f"  ✗ Failed setting repository flags: {format_error_diagnostic(err)}")
        return False

def get_existing_rulesets(repo: str) -> List[Dict[str, Any]]:
    """Fetch existing rulesets for the repository to enable idempotent PUT updates."""
    cmd = ["gh", "api", f"/repos/{repo}/rulesets"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout.strip())
    except subprocess.CalledProcessError:
        return []
    except json.JSONDecodeError:
        return []

def prepare_ruleset_payload(
    base_file: Optional[str],
    status_checks: Optional[List[str]],
    enforcement: Optional[str]
) -> Dict[str, Any]:
    """Load and validate ruleset payload, applying safety and schema fixes."""
    if base_file and os.path.exists(base_file):
        with open(base_file, "r", encoding="utf-8") as f:
            payload = json.load(f)
    else:
        # Default fallback template path relative to script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_template = os.path.join(script_dir, "..", "references", "rulesetTemplates.json")
        if os.path.exists(default_template):
            with open(default_template, "r", encoding="utf-8") as f:
                payload = json.load(f)
        else:
            payload = {
                "name": "Standard Production Branch Governance",
                "target": "branch",
                "enforcement": "active",
                "conditions": {
                    "ref_name": {
                        "include": ["~DEFAULT_BRANCH"],
                        "exclude": []
                    }
                },
                "rules": [
                    {"type": "deletion"},
                    {"type": "non_fast_forward"},
                    {"type": "required_linear_history"},
                    {
                        "type": "pull_request",
                        "parameters": {
                            "required_approving_review_count": 1,
                            "dismiss_stale_reviews_on_push": true,
                            "require_code_owner_review": false,
                            "require_last_push_approval": false,
                            "required_review_thread_resolution": true
                        }
                    }
                ],
                "bypass_actors": [
                    {
                        "actor_id": 5,
                        "actor_type": "RepositoryRole",
                        "bypass_mode": "always"
                    }
                ]
            }

    # 1. Enforce required schema fields on pull_request rule
    for rule in payload.get("rules", []):
        if rule.get("type") == "pull_request":
            params = rule.setdefault("parameters", {})
            params.setdefault("required_review_thread_resolution", True)
            params.setdefault("require_last_push_approval", False)
            params.setdefault("require_code_owner_review", False)
            params.setdefault("dismiss_stale_reviews_on_push", True)
            params.setdefault("required_approving_review_count", 1)

    # 2. Fix Solo Maintainer Lockout: Ensure Admin bypass exists
    bypass_actors = payload.setdefault("bypass_actors", [])
    has_admin_bypass = any(
        a.get("actor_type") == "RepositoryRole" and a.get("actor_id") == 5
        for a in bypass_actors
    )
    if not has_admin_bypass:
        bypass_actors.append({
            "actor_id": 5,
            "actor_type": "RepositoryRole",
            "bypass_mode": "always"
        })

    # 3. Dynamic status checks: avoid phantom checks
    if status_checks is not None:
        if len(status_checks) == 0 or (len(status_checks) == 1 and status_checks[0].lower() in ["none", "skip", ""]):
            # Explicitly omit status check rule
            payload["rules"] = [r for r in payload.get("rules", []) if r.get("type") != "required_status_checks"]
            print("  ℹ️ Status checks set to none; omitted required_status_checks rule to prevent phantom check lockouts.")
        else:
            # Update or insert status check rule
            check_rule = None
            for r in payload.get("rules", []):
                if r.get("type") == "required_status_checks":
                    check_rule = r
                    break
            if not check_rule:
                check_rule = {
                    "type": "required_status_checks",
                    "parameters": {
                        "strict_required_status_checks_policy": True,
                        "required_status_checks": []
                    }
                }
                payload["rules"].append(check_rule)
            check_rule["parameters"]["required_status_checks"] = [{"context": c} for c in status_checks]
            print(f"  ✓ Enforcing status check contexts: {', '.join(status_checks)}")

    # 4. Enforcement level override
    if enforcement:
        payload["enforcement"] = enforcement

    return payload

def deploy_ruleset_idempotent(repo: str, payload: Dict[str, Any], dry_run: bool = False) -> bool:
    """Deploy ruleset via PUT if existing, or POST if new."""
    ruleset_name = payload.get("name", "Standard Production Branch Governance")
    print(f" Checking existing rulesets in {repo} for '{ruleset_name}'...")

    existing_rulesets = get_existing_rulesets(repo)
    matched_id = None
    for r in existing_rulesets:
        if r.get("name", "").strip().lower() == ruleset_name.strip().lower():
            matched_id = r.get("id")
            break

    payload_json = json.dumps(payload, indent=2)

    if dry_run:
        action = f"PUT /repos/{repo}/rulesets/{matched_id}" if matched_id else f"POST /repos/{repo}/rulesets"
        print(f" [DRY-RUN] Would execute {action} with payload:\n{payload_json}")
        return True

    if matched_id:
        print(f"  ↻ Found existing ruleset ID {matched_id}. Performing idempotent UPDATE (PUT)...")
        cmd = ["gh", "api", "-X", "PUT", f"/repos/{repo}/rulesets/{matched_id}", "--input", "-"]
    else:
        print(f"  + No existing ruleset named '{ruleset_name}'. Performing CREATE (POST)...")
        cmd = ["gh", "api", "-X", "POST", f"/repos/{repo}/rulesets", "--input", "-"]

    try:
        res = subprocess.run(cmd, input=payload_json, capture_output=True, text=True, check=True)
        response_data = json.loads(res.stdout) if res.stdout.strip() else {}
        active_id = response_data.get("id", matched_id or "new")
        print(f"  ✓ Ruleset '{ruleset_name}' successfully active (ID: {active_id})!")
        return True
    except subprocess.CalledProcessError as err:
        print(f"  ✗ Ruleset deployment failed:\n  {format_error_diagnostic(err)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Configure GitHub repository baseline settings and idempotent production rulesets."
    )
    parser.add_argument("--repo", required=True, help="GitHub repository in format owner/repo")
    parser.add_argument("--ruleset", help="Path to ruleset JSON template (default: references/rulesetTemplates.json)")
    parser.add_argument(
        "--checks",
        help="Comma-separated status check contexts (e.g. 'test,build'), or 'none' to omit status checks"
    )
    parser.add_argument(
        "--auto-detect-checks",
        action="store_true",
        help="Scan local .github/workflows/*.yml to discover active CI job names"
    )
    parser.add_argument(
        "--enforce",
        choices=["active", "evaluate", "disabled"],
        help="Ruleset enforcement level (default: active)"
    )
    parser.add_argument(
        "--skip-settings",
        action="store_true",
        help="Skip configuring repository flags (squash merge, auto-delete)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned operations without calling GitHub API"
    )
    args = parser.parse_args()

    print(f"═══════════════════════════════════════════════════════════════════════")
    print(f" 🚀 GITHUB REPOSITORY BASELINE CONFIGURATOR: {args.repo}")
    print(f"═══════════════════════════════════════════════════════════════════════")

    # 1. Configure repository flags
    if not args.skip_settings:
        configure_repo_flags(args.repo, dry_run=args.dry_run)

    # 2. Determine status checks
    status_checks = None
    if args.checks is not None:
        if args.checks.strip().lower() in ["none", "skip", ""]:
            status_checks = []
        else:
            status_checks = [c.strip() for c in args.checks.split(",") if c.strip()]
    elif args.auto_detect_checks:
        detected = detect_local_workflow_jobs()
        if detected:
            print(f"  🔍 Auto-detected CI jobs in .github/workflows: {', '.join(detected)}")
            status_checks = detected
        else:
            print("  ⚠️ No workflow jobs detected in .github/workflows; omitting required status checks.")
            status_checks = []

    # 3. Prepare payload and deploy
    payload = prepare_ruleset_payload(args.ruleset, status_checks, args.enforce)
    deploy_ruleset_idempotent(args.repo, payload, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
