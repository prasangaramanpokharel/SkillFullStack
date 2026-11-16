#!/usr/bin/env python3
"""
scaffoldUvProject.py
Scaffolds a production-ready Python src-layout project configured with uv, Ruff, and mypy.
"""

import os
import sys
import argparse

def scaffold_python(name: str, out_dir: str):
    src_dir = os.path.join(out_dir, "src", name)
    tests_dir = os.path.join(out_dir, "tests")
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(tests_dir, exist_ok=True)

    # pyproject.toml
    pyproject = f"""[project]
name = "{name}"
version = "0.1.0"
description = "Production service built with modern standards"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.10.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "mypy>=1.14.0",
    "ruff>=0.9.0",
]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]

[tool.mypy]
strict = true
python_version = "3.12"
"""
    with open(os.path.join(out_dir, "pyproject.toml"), "w") as f:
        f.write(pyproject)

    # __init__.py and main.py
    with open(os.path.join(src_dir, "__init__.py"), "w") as f:
        f.write('"""Service package."""\n')

    with open(os.path.join(src_dir, "main.py"), "w") as f:
        f.write("""from pydantic import BaseModel

class Status(BaseModel):
    model_config = {"frozen": True}
    healthy: bool = True

def run() -> None:
    status = Status()
    print(f"Service running: {status.healthy}")

if __name__ == "__main__":
    run()
""")

    # test file
    with open(os.path.join(tests_dir, "test_main.py"), "w") as f:
        f.write(f"from {name}.main import Status\n\ndef test_status():\n    assert Status().healthy is True\n")

    print(f" Scaffolded Python project '{name}' at {out_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--out", default=".", help="Target directory")
    args = parser.parse_args()
    scaffold_python(args.name, args.out)
