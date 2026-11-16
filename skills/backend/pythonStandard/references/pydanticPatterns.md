# Pydantic V2 Production Patterns

## 1. Immutability & Clean Configuration
Use the modern `model_config` dict instead of inner `class Config`:
```python
class AppSettings(BaseModel):
    model_config = {
        "frozen": True,              # Immutable instances (hashable)
        "str_strip_whitespace": True,# Strip input whitespace automatically
        "extra": "forbid",           # Disallow unexpected fields
    }
```

## 2. Model Validators vs Field Validators
- `@field_validator("fieldName")`: Operates on a single field before or after core validation.
- `@model_validator(mode="after")`: Evaluates cross-field dependencies (e.g. `confirmPassword == password`).
