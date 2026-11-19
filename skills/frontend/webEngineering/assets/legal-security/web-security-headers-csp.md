# Web Security Headers & Content Security Policy (CSP)

Production web applications must enforce browser-level security boundaries through standardized HTTP response headers.

---

## 1. Mandatory Production Headers

```http
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
X-Frame-Options: DENY
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
Cross-Origin-Opener-Policy: same-origin
```

---

## 2. Content Security Policy (CSP Level 3)

A modern strict CSP eliminates Cross-Site Scripting (XSS) by using cryptographic nonces or hashes rather than brittle domain allowlists:

```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{RANDOM_BASE64}' 'strict-dynamic'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://api.example.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self';
```
