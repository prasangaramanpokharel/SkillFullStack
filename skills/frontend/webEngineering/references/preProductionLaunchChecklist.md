# Pre-Production Launch Checklist (`/web-checklist`)

This document establishes the exhaustive verification gate that every web application must pass before traffic is routed to production.

---

## 1. Legal, Privacy & Compliance Gate
- [ ] **Privacy Policy**: Accessible from all pages (typically footer), details data collection, cookies, third-party processors, and user rights.
- [ ] **Terms of Service**: Clearly defines acceptable use, intellectual property, warranties, and liability limitations.
- [ ] **Cookie Consent (GDPR / ePrivacy)**: Non-essential tracking scripts (Google Analytics, Meta Pixel) must **not** fire before affirmative user opt-in.
- [ ] **Impressum / Corporate Disclosure**: Mandatory for EU jurisdictions; contains registered business address, registration number, and VAT ID.
- [ ] **Accessibility Statement**: Declares target standard (WCAG 2.2 AA) and provides feedback mechanism for users with disabilities.

---

## 2. Security & Header Hardening Gate
- [ ] **HSTS Active**: `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
- [ ] **CSP Level 3**: Nonce or strict hash-based Content-Security-Policy blocking unauthorized inline scripts and object injections.
- [ ] **MIME Sniffing Blocked**: `X-Content-Type-Options: nosniff`
- [ ] **Clickjacking Defense**: `X-Frame-Options: DENY` or `frame-ancestors 'none'` in CSP.
- [ ] **Referrer Policy**: `strict-origin-when-cross-origin` preventing leaking query tokens in HTTP referrers.
- [ ] **Permissions Policy**: Disable unneeded hardware sensors (`camera=(), microphone=(), geolocation=()`).

---

## 3. Observability & Operational Health Gate
- [ ] **Centralized Error Tracking**: Sentry, Datadog, or OpenTelemetry active with source maps uploaded securely.
- [ ] **Synthetic Uptime Probes**: Automated checks pinging `/api/health` or root route every 60 seconds with PagerDuty alerts.
- [ ] **Logging Hygiene**: Ensure no PII, session tokens, passwords, or credit card numbers are logged.
- [ ] **Graceful 404 & 500 Pages**: Custom branded error pages with navigational paths back to the application.
