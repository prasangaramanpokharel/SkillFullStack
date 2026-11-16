# API Versioning & Compatibility Policies

All API modifications must preserve consumer stability and backward compatibility.

---

## 1. The Additive Law of API Changes

The following changes are **NON-BREAKING** (Allowed on existing major versions):
- Adding new optional request query parameters or request body fields.
- Adding new fields to response representations.
- Adding a new endpoint or HTTP method to an existing resource.
- Adding new error codes within the existing RFC 9457 structure.

The following changes are **BREAKING** (Forbidden on existing major versions):
- Removing an existing endpoint or HTTP method.
- Renaming or removing existing fields in response payloads.
- Changing the data type of an existing field (e.g. integer to string).
- Adding new required request headers, query parameters, or body properties.
- Changing semantic meaning or status code of an existing response.

---

## 2. Deprecation Signaling Protocol

When an endpoint or field is deprecated, it must signal deprecation using exact standards:
- **`Deprecation` Header (RFC 9745)**:
  Uses an RFC 9651 Structured Field Date:
  ```http
  Deprecation: @1794787200
  ```
- **`Sunset` Header (RFC 8594)**:
  Uses an HTTP-date format specifying when the endpoint will be turned off:
  ```http
  Sunset: Tue, 17 Nov 2026 00:00:00 GMT
  ```
- **`Link` Header**:
  Points to migration documentation:
  ```http
  Link: <https://api.example.com/docs/migrations/v2>; rel="deprecation"
  ```
- **Minimum Notice Window**: Deprecated endpoints must remain operational for a minimum of 180 days before removal.
