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

---

## 4. Mandatory Production Slugs & Route Mapping

Every production web application must expose and route these standard URL slugs:

| Required Slug | Standard Aliases | Requirement | Compliance & Standard Anchor | Purpose & Expected Content |
| :--- | :--- | :---: | :--- | :--- |
| **`/privacy-policy`** | `/privacy` | **MANDATORY** | GDPR Art. 13, CCPA/CPRA, CalOPPA | Data collection disclosure, third-party processors, user data deletion rights, contact email. |
| **`/terms-of-service`**| `/terms`, `/tos` | **MANDATORY** | Contract Law & Consumer Protection | Acceptable use policy, liability limitations, dispute resolution, governing law. |
| **`/cookie-policy`** | `/cookies` | **MANDATORY** | EU ePrivacy Directive (Directive 2002/58/EC) | Detailed inventory of strictly necessary, performance, functional, and marketing cookies with opt-out mechanisms. |
| **`/.well-known/security.txt`** | `/security` | **MANDATORY** | RFC 9116 | Cryptographic vulnerability disclosure policy, security team PGP key, and report email. |
| **`/accessibility`** | `/accessibility-statement` | **MANDATORY** | ADA Title III, Section 508, EAA | Declaration of WCAG 2.2 AA conformity, known limitations, and contact method for accessibility feedback. |
| **`/impressum`** | `/legal-notice` | **MANDATORY (EU/DE/AT/CH)** | Telemediengesetz (TMG § 5) / DSA | Company registration number, registered office address, VAT ID, authorized representatives. |
| **`/contact`** | `/support` | **MANDATORY** | Consumer Protection Regulations | Direct communication channel (contact form, verified email, physical corporate address). |
| **`/robots.txt`** | None | **MANDATORY** | RFC 9309 | Crawl boundaries for search engines and AI agents; points to `/sitemap.xml` and `/llms.txt`. |
| **`/sitemap.xml`** | `/sitemap-index.xml` | **MANDATORY** | Sitemaps.org Protocol | XML catalog of all public, canonical, indexable URLs with `<lastmod>` timestamps. |
| **`/llms.txt`** | None | **MANDATORY** | Answer.AI Specification | Curated markdown index of documentation and capabilities for LLMs and AI coding agents. |
| **`/llms-full.txt`** | None | **RECOMMENDED** | Answer.AI Specification | Complete un-truncated markdown documentation bundle for single-pass agent context ingestion. |
| **`/404`** | None | **MANDATORY** | HTTP/1.1 Standard | Custom branded "Not Found" error page with search bar and navigational links back to home. |
| **`/api/health`** | `/healthz`, `/health` | **MANDATORY** | SRE & Cloud Uptime Probes | Returns `200 OK` `{ "status": "healthy", "timestamp": "..." }` for load balancers and synthetic monitoring. |
