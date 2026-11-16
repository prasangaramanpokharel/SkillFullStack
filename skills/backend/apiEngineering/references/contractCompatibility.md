# API Contract Compatibility & Breaking Change Detection Reference

---

## 1. Classification of API Changes

| Change Type | Classification | CI Action |
| :--- | :--- | :--- |
| **Add optional query parameter** | Non-Breaking | PASS |
| **Add field to response object** | Non-Breaking | PASS |
| **Add new endpoint** | Non-Breaking | PASS |
| **Remove endpoint** | **Breaking** | **FAIL CI** |
| **Remove response field** | **Breaking** | **FAIL CI** |
| **Rename response field** | **Breaking** | **FAIL CI** |
| **Change field type (string $\rightarrow$ integer)** | **Breaking** | **FAIL CI** |
| **Add required request parameter** | **Breaking** | **FAIL CI** |
| **Change response HTTP status code** | **Breaking** | **FAIL CI** |

---

## 2. Breaking Change Detection in CI

Use `python3 scripts/checkBreakingChanges.py --old=spec-v1.json --new=spec-v2.json` in your pull request pipeline. Any detected breaking change requires:
1. Incrementing the API major version (e.g. `/v1` $\rightarrow$ `/v2`).
2. Setting `Deprecation` and `Sunset` headers on the previous version.
3. Updating migration guides.
