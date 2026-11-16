#!/usr/bin/env python3
"""
testWorkflowDispatch.py
Dispatches a test event to an Inngest or QStash durable workflow endpoint.
"""

import sys
import json
import urllib.request

def dispatch_event(url: str, event_name: str, payload: dict):
    body = json.dumps({"name": event_name, "data": payload}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f" Event '{event_name}' dispatched successfully to {url}! Status: {resp.status}")
    except Exception as e:
        print(f" Dispatch failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 testWorkflowDispatch.py <endpoint_url> <event_name>")
        sys.exit(0)
    dispatch_event(sys.argv[1], sys.argv[2], {"test": True, "source": "cli"})
