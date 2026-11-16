# Modern `pyproject.toml` Production Specification

A standardized blueprint combining dependencies, dev tools, Ruff, and strict Mypy:

```toml
[project]
name = "production-service"
version = "0.1.0"
description = "Production service built with modern Python standards"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
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
ignore_missing_imports = true
warn_unused_ignores = true
disallow_untyped_defs = true
```
