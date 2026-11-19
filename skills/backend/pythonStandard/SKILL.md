---
name: pythonStandard
description: Modern production Python engineering standards with Astral uv toolchain, Ruff linter/formatter, Pydantic v2 core models, strict mypy type checking, and asyncio.TaskGroup structured concurrency.
version: 3.12+
last-verified: 2026-11-16
compatibility: Python 3.11, Python 3.12, Python 3.13, uv, ruff, pydantic 2.x
slash-commands:
  - command: /python-standard
    description: Enforce modern Python standards with uv, Ruff, and Pydantic v2
    argument-hint: "[--strict=true]"
  - command: /python-uv
    description: Manage virtual environments and dependency locking with Astral uv
    argument-hint: "[--add=package]"
  - command: /python-typing
    description: Apply strict PEP 585/604 type hints and TaskGroup concurrency
    argument-hint: "[--async=true]"

---

# Modern Production Python Engineering Guide

## 1. Toolchain & Package Management (`uv`)
Replace legacy `pip`, `virtualenv`, `poetry`, and `pyenv` entirely with **`uv`**:

```bash
# Initialize a production application with src layout
uv init --app my_service
cd my_service

# Pin target Python version (auto-installs if missing)
uv python pin 3.12

# Add dependencies (updates pyproject.toml and creates uv.lock)
uv add fastapi pydantic

# Add development tools
uv add --dev ruff mypy pytest

# Execute scripts in the locked environment (never activate venvs manually)
uv run pytest
```

---

## 2. Formatting & Linting (`Ruff`)
Ruff replaces Black, Flake8, isort, and pyupgrade in a single high-performance binary:

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort (clean automatic imports)
    "UP",  # pyupgrade (enforce modern Python 3.12+ idioms)
    "B",   # flake8-bugbear (common runtime traps)
    "SIM", # flake8-simplify
]
```

Run checks:
```bash
uv run ruff format .       # Format files
uv run ruff check --fix .  # Autofix lint errors
```

---

## 3. Modern Static Typing (PEP 585 & PEP 604)
Never import `List`, `Dict`, `Tuple`, or `Optional` from `typing`:

```python
# ❌ Legacy Anti-Pattern:
from typing import List, Optional, Dict
def process(items: Optional[List[str]] = None) -> Dict[str, int]: ...

# ✅ Modern Production Standard (Built-ins & Union Pipes):
def process(items: list[str] | None = None) -> dict[str, int]:
    if items is None:
        items = []
    return {item: len(item) for item in items}
```

---

## 4. Runtime Validation & Settings (`Pydantic V2`)
Use Pydantic v2's Rust-powered core for configuration, serialization, and boundary validations:

```python
from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Literal

class UserProfile(BaseModel):
    model_config = {"frozen": True, "str_strip_whitespace": True}

    username: str = Field(min_length=3, max_length=50)
    email: str
    role: Literal["admin", "member", "guest"] = "member"

    @field_validator("username")
    @classmethod
    def normalize_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()

    @computed_field
    @property
    def display_tag(self) -> str:
        return f"@{self.username} ({self.role})"
```

---

## 5. Structured Concurrency (`asyncio.TaskGroup`)
Never use unmanaged `asyncio.create_task()` in loops without lifecycle safety. Use `asyncio.TaskGroup`:

```python
import asyncio

async def fetch_all(urls: list[str]) -> list[str]:
    results: list[str] = []
    
    # TaskGroup cancels all remaining child tasks automatically if any task raises an exception
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            tg.create_task(fetch_url(url, results))
            
    return results
```

---

## 6. Anti-Patterns & Critical Pitfalls
- ❌ **`requirements.txt` / Manual Venvs**: Do not use unpinned `requirements.txt`. Always commit `uv.lock` and run with `uv run`.
- ❌ **Mutable Default Arguments**: Never write `def func(items: list = []):`; use `items: list[str] | None = None`.
- ❌ **Catching Bare Exceptions**: Never write `except Exception: pass`. Always log structured errors or catch specific exceptions.
- ❌ **`typing.Optional` & `typing.List`**: Avoid legacy imports; use `str | None` and `list[str]`.

---

## 7. References & Bundled Utilities
- Production `pyproject.toml` specification: [references/pyprojectSpecs.md](references/pyprojectSpecs.md)
- Pydantic v2 deep patterns: [references/pydanticPatterns.md](references/pydanticPatterns.md)
- Project scaffolding script: [scripts/scaffoldUvProject.py](scripts/scaffoldUvProject.py)
