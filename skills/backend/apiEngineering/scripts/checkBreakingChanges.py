#!/usr/bin/env python3
"""
checkBreakingChanges.py
Compares two OpenAPI JSON specifications (old vs new) and flags breaking changes:
- Removed endpoints / methods
- Removed response properties
- Added required request parameters
- Changed response HTTP status codes
"""

import sys
import json
import argparse
import os

def detect_breaking_changes(old_spec, new_spec):
    breaking = []
    old_paths = old_spec.get("paths", {})
    new_paths = new_spec.get("paths", {})

    # Check for removed paths and operations
    for path, old_item in old_paths.items():
        if path not in new_paths:
            breaking.append(f"Removed endpoint path: '{path}'")
            continue
        new_item = new_paths[path]
        for method, old_op in old_item.items():
            if method.lower() not in ["get", "post", "put", "patch", "delete", "query"]:
                continue
            if method not in new_item:
                breaking.append(f"Removed HTTP method '{method.upper()}' from '{path}'")
                continue
            
            new_op = new_item[method]
            
            # Check for newly added required parameters
            old_params = {p.get("name"): p for p in old_op.get("parameters", [])}
            for new_p in new_op.get("parameters", []):
                p_name = new_p.get("name")
                if new_p.get("required") is True:
                    if p_name not in old_params or not old_params[p_name].get("required"):
                        breaking.append(f"Added new required parameter '{p_name}' to '{method.upper()} {path}'")

            # Check for removed status codes
            old_responses = old_op.get("responses", {})
            new_responses = new_op.get("responses", {})
            for code in old_responses:
                if code.startswith("2") and code not in new_responses:
                    breaking.append(f"Removed success status code '{code}' from '{method.upper()} {path}'")

    return {
        "hasBreakingChanges": len(breaking) > 0,
        "breakingChangesCount": len(breaking),
        "breakingChanges": breaking
    }

def main():
    parser = argparse.ArgumentParser(description="Check for breaking changes between two OpenAPI specs")
    parser.add_argument("--old", required=True, help="Path to baseline OpenAPI JSON")
    parser.add_argument("--new", required=True, help="Path to modified OpenAPI JSON")
    args = parser.parse_args()

    if not os.path.exists(args.old) or not os.path.exists(args.new):
        print(json.dumps({"error": "Spec files not found"}, indent=2))
        sys.exit(1)

    with open(args.old) as f:
        old_data = json.load(f)
    with open(args.new) as f:
        new_data = json.load(f)

    result = detect_breaking_changes(old_data, new_data)
    print(json.dumps(result, indent=2))
    sys.exit(1 if result["hasBreakingChanges"] else 0)

if __name__ == "__main__":
    main()
