# Response Standards Reference (Success & RFC 9457 Errors)

Enterprise API response formatting rules conforming to RFC 9110 and RFC 9457.

---

## 1. Success Response Envelope

All single resource and collection responses wrap data in a top-level envelope:

### Single Resource Representation
```http
HTTP/1.1 200 OK
Content-Type: application/json
```
```json
{
  "data": {
    "id": "usr_01HX9J5Y8K...",
    "email": "user@example.com",
    "name": "Jane Doe",
    "status": "active",
    "createdAt": "2026-11-16T12:00:00Z",
    "updatedAt": "2026-11-16T12:00:00Z"
  }
}
```

### Paginated Collection Representation
```http
HTTP/1.1 200 OK
Content-Type: application/json
```
```json
{
  "data": [
    {
      "id": "inv_01HX9...",
      "amount": 4900,
      "currency": "USD",
      "status": "paid"
    }
  ],
  "meta": {
    "cursor": "ZXhwaXJ5OjE3MzE3NTg0MDA=",
    "hasNextPage": true,
    "limit": 20,
    "totalCount": 142
  }
}
```

---

## 2. Error Response Standards (RFC 9457 Problem Details)

All 4xx and 5xx responses MUST use the `application/problem+json` media type.

### Standard Problem Details Structure
| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | URI string | Stable identifier URI categorizing the problem type (e.g. `https://api.example.com/problems/validation-error`). |
| `title` | string | Short human-readable summary of problem type. Should not change between occurrences. |
| `status` | integer | HTTP status code matching the response header. |
| `detail` | string | Specific human-readable explanation of this particular occurrence. |
| `instance` | URI string | Relative URI identifying the specific request path that generated the error. |
| `errors` | array | (Extension) Granular field-level validation errors. |

### Field Validation Error Example (422)
```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json
```
```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "One or more fields failed validation checks.",
  "instance": "/v1/users",
  "errors": [
    {
      "field": "email",
      "code": "invalid_format",
      "message": "Must be an RFC 5322 compliant email address."
    },
    {
      "field": "age",
      "code": "out_of_range",
      "message": "Must be greater than or equal to 18."
    }
  ]
}
```
