#!/usr/bin/env python3
"""
runPromptEvalSuite.py
Wrapper script to run Promptfoo or Pytest evaluation suites and return standardized exit codes.
"""

import sys
import subprocess

def run_suite(framework: str):
    if framework == "promptfoo":
        cmd = ["npx", "promptfoo@latest", "eval", "--ci"]
    elif framework == "deepeval":
        cmd = ["pytest", "tests/evals/"]
    else:
        print(f"Unknown framework: {framework}. Choose 'promptfoo' or 'deepeval'.")
        sys.exit(1)

    print(f"Running evaluation suite via: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd)
        sys.exit(res.returncode)
    except FileNotFoundError:
        print(f"Command not found. Ensure {cmd[0]} is installed.")
        sys.exit(1)

if __name__ == "__main__":
    fw = sys.argv[1] if len(sys.argv) > 1 else "promptfoo"
    run_suite(fw)
