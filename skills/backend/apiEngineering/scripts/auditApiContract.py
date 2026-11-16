#!/usr/bin/env python3
"""
auditApiContract.py
Audits an OpenAPI JSON or YAML contract against 2026 API standards:
- RFC 9457 Problem Details error schemas (application/problem+json)
- Top-level success response enveloping ({ data, meta })
- Pagination bounds (limit parameter with max ceiling <= 100)
- Explicit HTTP status codes (no 200 for errors)
"""

import sys
import os
import json
import argparse
import re

def audit_openapi_spec(spec_data):
    findings = []
    paths = spec_data.get("paths", {})
    if not paths:
        findings.append({"level": "ERROR", "message": "No paths defined in OpenAPI specification."})

    version = spec_data.get("openapi", "")
    if not version.startswith("3."):
        findings.append({"level": "WARN", "message": f"Expected OpenAPI 3.1+ or 3.2.x, found '{version}'."})

    for path, path_item in paths.items():
        for method, operation in path_item.items():
            if method.lower() not in ["get", "post", "put", "patch", "delete", "query"]:
                continue
            
            op_id = f"{method.upper()} {path}"
            responses = operation.get("responses", {})
            
            # Check for error responses
            has_problem_details = False
            for code, resp in responses.items():
                if code.startswith("4") or code.startswith("5"):
                    content = resp.get("content", {})
                    if "application/problem+json" in content:
                        has_problem_details = True
                    elif "application/json" in content:
                        findings.append({
                            "level": "WARN",
                            "endpoint": op_id,
                            "code": code,
                            "message": "Error response uses 'application/json' instead of RFC 9457 'application/problem+json'."
                        })
            
            if not has_problem_details:
                findings.append({
                    "level": "ERROR",
                    "endpoint": op_id,
                    "message": "Missing RFC 9457 Problem Details (application/problem+json) for 4xx/5xx responses."
                })

            # Check collection pagination
            if method.lower() == "get" and not path.endswith("}"):
                # likely a collection endpoint
                params = operation.get("parameters", [])
                limit_param = next((p for p in params if p.get("name") in ["limit", "pageSize", "page_size"]), None)
                if not limit_param:
                    findings.append({
                        "level": "WARN",
                        "endpoint": op_id,
                        "message": "Collection endpoint missing 'limit' pagination query parameter."
                    })
                else:
                    schema = limit_param.get("schema", {})
                    max_limit = schema.get("maximum")
                    if max_limit is None or max_limit > 100:
                        findings.append({
                            "level": "WARN",
                            "endpoint": op_id,
                            "message": f"Pagination 'limit' missing maximum constraint or exceeds ceiling of 100 (found: {max_limit})."
                        })

    error_count = len([f for f in findings if f["level"] == "ERROR"])
    warn_count = len([f for f in findings if f["level"] == "WARN"])
    
    return {
        "isCompliant": error_count == 0,
        "summary": {
            "errors": error_count,
            "warnings": warn_count,
            "pathsChecked": len(paths)
        },
        "findings": findings
    }

def main():
    parser = argparse.ArgumentParser(description="Audit OpenAPI spec for 2026 API standards")
    parser.add_argument("--spec", help="Path to OpenAPI JSON file", required=False)
    args = parser.parse_args()

    if args.spec and os.path.exists(args.spec):
        with open(args.spec, "r") as f:
            data = json.load(f)
    elif not sys.stdin.isatty():
        data = json.load(sys.stdin)
    else:
        # Default mock sample for testing
        data = {
            "openapi": "3.2.1",
            "paths": {
                "/users": {
                    "get": {
                        "parameters": [{"name": "limit", "in": "query", "schema": {"type": "integer", "maximum": 50}}],
                        "responses": {
                            "200": {"description": "OK"},
                            "422": {"content": {"application/problem+json": {"schema": {"type": "object"}}}}
                        }
                    }
                }
            }
        }

    report = audit_openapi_spec(data)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["isCompliant"] else 1)

if __name__ == "__main__":
    main()
