#!/usr/bin/env python3
"""
evalCicd.py
Validates the auditDockerfileSecurity script.
"""

import subprocess
import json
import os
import sys

def test_audit_dockerfile():
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "auditDockerfileSecurity.py")
    sample_dockerfile = """
    FROM golang:1.22-alpine AS builder
    WORKDIR /src
    COPY . .
    RUN go build -o /app/server

    FROM alpine:3.19 AS runner
    RUN adduser -D -u 10001 appuser
    USER appuser
    COPY --from=builder /app/server /app/server
    CMD ["/app/server"]
    """
    res = subprocess.run([sys.executable, script_path], input=sample_dockerfile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 0, f"Script failed: {res.stderr}"
    data = json.loads(res.stdout)
    assert data["isProductionReady"] is True
    assert data["hasMultiStage"] is True
    assert data["runsAsNonRoot"] is True
    assert data["score"] == 100
    print(" test_audit_dockerfile passed")

if __name__ == "__main__":
    test_audit_dockerfile()
    print("All cicdPipeline evals passed.")
