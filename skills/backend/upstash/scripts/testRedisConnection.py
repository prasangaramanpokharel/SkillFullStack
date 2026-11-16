#!/usr/bin/env python3
"""
testRedisConnection.py
Verifies Upstash Redis REST connectivity and latency.
"""

import os
import sys
import json
import time
import urllib.request

def test_connection():
    url = os.environ.get("UPSTASH_REDIS_REST_URL")
    token = os.environ.get("UPSTASH_REDIS_REST_TOKEN")

    if not url or not token:
        print("Error: Missing UPSTASH_REDIS_REST_URL or UPSTASH_REDIS_REST_TOKEN in environment.")
        print("Usage: UPSTASH_REDIS_REST_URL=... UPSTASH_REDIS_REST_TOKEN=... python3 testRedisConnection.py")
        sys.exit(1)

    endpoint = f"{url.rstrip('/')}/ping"
    start_time = time.time()

    req = urllib.request.Request(endpoint, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            elapsed_ms = (time.time() - start_time) * 1000
            data = json.loads(resp.read().decode("utf-8"))
            print(f" Upstash Redis Connected! Response: {data.get('result', 'OK')} ({elapsed_ms:.1f}ms)")
    except Exception as e:
        print(f" Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()
