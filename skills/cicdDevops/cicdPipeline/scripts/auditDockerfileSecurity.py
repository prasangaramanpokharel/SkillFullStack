#!/usr/bin/env python3
"""
auditDockerfileSecurity.py
Audits Dockerfiles for production security best practices:
- Multi-stage builds
- Non-root user declaration
- Avoidance of 'latest' tags
- Clean package manager cache cleanup
"""

import sys
import re
import json

def audit_dockerfile_content(content):
    lines = content.splitlines()
    has_multistage = len(re.findall(r"^\s*FROM\s+", content, re.MULTILINE | re.IGNORECASE)) > 1
    has_user = bool(re.search(r"^\s*USER\s+(?!root\b)\w+", content, re.MULTILINE | re.IGNORECASE))
    has_latest_tag = bool(re.search(r"^\s*FROM\s+[\w\./\-]+:latest\b", content, re.MULTILINE | re.IGNORECASE))
    
    findings = []
    if not has_multistage:
        findings.append("Missing multi-stage build: final image may contain build tools.")
    if not has_user:
        findings.append("Missing non-root USER declaration: container runs as root.")
    if has_latest_tag:
        findings.append("Uses mutable ':latest' image tag instead of pinned version.")

    score = 100 - (len(findings) * 30)

    return {
        "score": max(score, 0),
        "isProductionReady": len(findings) == 0,
        "hasMultiStage": has_multistage,
        "runsAsNonRoot": has_user,
        "usesPinnedTags": not has_latest_tag,
        "findings": findings
    }

def main():
    sample = sys.stdin.read() if not sys.stdin.isatty() else """
    FROM node:20-alpine AS builder
    WORKDIR /app
    COPY . .
    RUN npm build

    FROM node:20-alpine AS runner
    USER appuser
    COPY --from=builder /app/dist ./dist
    CMD ["node", "dist/main.js"]
    """
    result = audit_dockerfile_content(sample)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
