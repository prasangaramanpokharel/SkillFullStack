---
name: webEngineering
description: Complete web engineering and pre-flight production checklist skill. Covers exhaustive launch readiness (Legal, GDPR cookie consent, security headers, observability), modern technical SEO and AI agent discovery (llms.txt, AI crawler robots.txt, JSON-LD, Open Graph), Core Web Vitals optimization (LCP <= 2.5s, INP <= 200ms, CLS <= 0.1, caching hierarchies), automated testing (WCAG 2.2 AA accessibility, Playwright E2E), and production API latency/contract standards (RFC 9457 Problem Details, p95/p99 latency budgets, idempotency keys).
version: 2026.x
last-verified: 2026-11-19
compatibility: Framework-agnostic (Next.js, Astro, Remix/React Router, SvelteKit, Nuxt, Vite SPAs, static web), HTML5, WCAG 2.2 AA, RFC 9457, RFC 9309, llms.txt standard
slash-commands:
  - command: /web-checklist
    description: Execute exhaustive pre-production launch verification across Legal, Security, Observability, and QA gates.
    argument-hint: "[--gate=all|legal|security|observability]"
  - command: /web-seo
    description: Audit and generate technical SEO assets, AI agent discovery files (llms.txt), robots.txt, and JSON-LD schemas.
    argument-hint: "[--generate=llms|robots|schema]"
  - command: /web-performance
    description: Optimize Core Web Vitals (LCP <= 2.5s, INP <= 200ms, CLS <= 0.1), caching hierarchies, and asset payloads.
    argument-hint: "[--metric=lcp|inp|cls]"
  - command: /web-testing
    description: Enforce WCAG 2.2 AA accessibility compliance, keyboard navigation, and Playwright E2E smoke suites.
    argument-hint: "[--suite=a11y|e2e]"
  - command: /web-api
    description: Enforce RFC 9457 Problem Details error envelopes, p50/p95/p99 latency budgets, and idempotency keys.
    argument-hint: "[--slo=p95]"
  - command: /web-audit
    description: Run the automated CLI diagnostic scanner and generate web-readiness-report.md scorecard.
    argument-hint: "[--path=<dir>]"
---

# Web Engineering & Pre-Flight Production Master Guide

This skill governs the end-to-end engineering, optimization, security, and launch readiness of modern web applications. It serves as the ultimate pre-flight checklist before any website is exposed to production traffic.

---

## ⚡ Zero-Hallucination Offline Assets Notice
Before configuring web infrastructure, SEO metadata, or performance budgets, agents **MUST** consult the bundled official specifications in [`assets/`](assets/README.md):
- `llms.txt` Standard Specification: [`assets/seo/llms-txt-specification.md`](assets/seo/llms-txt-specification.md)
- AI Crawlers & RFC 9309 `robots.txt`: [`assets/seo/ai-crawlers-and-robots-txt.md`](assets/seo/ai-crawlers-and-robots-txt.md)
- Core Web Vitals (LCP, INP, CLS): [`assets/cwv/core-web-vitals-inp-lcp.md`](assets/cwv/core-web-vitals-inp-lcp.md)
- RFC 9457 Problem Details for HTTP APIs: [`assets/api/rfc-9457-problem-details.md`](assets/api/rfc-9457-problem-details.md)
- Web Security Headers & CSP Level 3: [`assets/legal-security/web-security-headers-csp.md`](assets/legal-security/web-security-headers-csp.md)

---

## 1. Pre-Production Master Checklist (`/web-checklist`)

Every web release must clear the 6 critical launch gates:

```
┌────────────────────────────────────────────────────────┐
│           PRE-PRODUCTION WEB LAUNCH GATES              │
├────────────────────────────────────────────────────────┤
│ 1. LEGAL & PRIVACY: Privacy Policy, Terms, Cookie opt-in│
│ 2. SECURITY HEADERS: CSP Level 3, HSTS, X-Content-Type │
│ 3. TECHNICAL & AGENT SEO: llms.txt, robots.txt, JSON-LD│
│ 4. CORE WEB VITALS: LCP <= 2.5s, INP <= 200ms, CLS<=0.1│
│ 5. ACCESSIBILITY: WCAG 2.2 AA, touch targets, contrast │
│ 6. PRODUCTION APIS: RFC 9457, p95 <= 150ms, Idempotency│
└────────────────────────────────────────────────────────┘
```

- **Deep Reference**: [`references/preProductionLaunchChecklist.md`](references/preProductionLaunchChecklist.md)
- **Launch Template**: [`templates/webReadinessReport.template.md`](templates/webReadinessReport.template.md)

### Mandatory Production Slugs & Route Mapping
Every web production deployment must map and serve standard technical, legal, and operational routes:

| Category | Recommended Slug | Permitted Aliases | Purpose & Compliance Reference |
| :--- | :--- | :--- | :--- |
| **Privacy Policy** | `/privacy-policy` | `/privacy` | GDPR Art. 13/14, CCPA/CPRA, CalOPPA mandatory privacy notice |
| **Terms of Service** | `/terms-of-service` | `/terms`, `/tos` | User contract, legal terms of use, dispute resolution |
| **Cookie Policy** | `/cookie-policy` | `/cookies` | EU ePrivacy Directive (Directive 2002/58/EC), tracking consent |
| **Accessibility Statement** | `/accessibility` | `/a11y` | WCAG 2.2 Level AA, Section 508, European Accessibility Act (EAA) |
| **Company Impressum** | `/impressum` | `/imprint`, `/legal-notice` | German TMG §5, EU e-Commerce legal business disclosure |
| **Contact / Support** | `/contact` | `/support`, `/help` | Mandatory customer communication channel and legal entity contact |
| **Security Disclosure** | `/.well-known/security.txt` | `/security.txt` | RFC 9116 Vulnerability disclosure program contact |
| **Search Engine Robots** | `/robots.txt` | — | RFC 9309 Search engine & AI crawler directive file |
| **XML Sitemap** | `/sitemap.xml` | — | Search engine indexation manifest |
| **AI LLM Index** | `/llms.txt` | — | Clean markdown catalog for AI coding and search agents |
| **AI LLM Full Corpus** | `/llms-full.txt` | — | Complete raw markdown corpus for AI agent synthesis |
| **404 Not Found Page** | `/404` | `/not-found` | Branded user-friendly error page with return navigation |
| **API Health Probe** | `/api/health` | `/healthz`, `/api/healthz` | Synthetic monitoring, container readiness, and uptime probes |

---

## 2. Technical SEO & AI Agent Discovery (`/web-seo`)

Modern websites must be accessible to both search engine crawlers and autonomous AI agents:

### 2.1 The `llms.txt` and `llms-full.txt` Standard
Provide a clean Markdown summary for LLMs at `/llms.txt`:
```markdown
# My Web Platform
> High-performance platform for full-stack engineering.

## Documentation
- [Quickstart](https://example.com/docs/quickstart.md): Setup in 5 minutes.
- [API Reference](https://example.com/docs/api.md): REST endpoints and error codes.
```
Template: [`templates/llms.template.txt`](templates/llms.template.txt).

### 2.2 Differentiated `robots.txt` (RFC 9309)
Differentiate search crawlers from AI synthesis and bulk scrapers:
- **Allow**: Search engines (`Googlebot`, `Bingbot`) and AI search agents (`PerplexityBot`, `ChatGPT-User`).
- **Disallow / Manage**: Bulk training harvesters (`GPTBot`, `ClaudeBot`, `Google-Extended`, `CCBot`).
Template: [`templates/robots.template.txt`](templates/robots.template.txt).

### 2.3 Metadata, Canonical & JSON-LD
- Explicit `<link rel="canonical" href="...">` on all pages.
- Social cards: `og:title`, `og:image` (1200x630), `twitter:card="summary_large_image"`.
- Schema.org structured data via `<script type="application/ld+json">` (`WebSite`, `Organization`, `BreadcrumbList`, `FAQPage`).
- App Icons & Web Manifest: `<link rel="icon" href="/favicon.ico">`, `apple-touch-icon.png` (180x180), and `manifest.webmanifest`.
- Multilingual SEO: `<link rel="alternate" hreflang="x" href="...">` and `<link rel="alternate" hreflang="x-default" href="...">`.
- XML Sitemap indexation: `sitemap.xml` linked in `robots.txt` and verified against HTTP 200 responses.
- Deep Reference: [`references/modernTechnicalSeoAndAgentReadiness.md`](references/modernTechnicalSeoAndAgentReadiness.md).

---

## 3. Core Web Vitals & Caching (`/web-performance`)

Enforce strict performance budgets evaluated at the 75th percentile of real-world user sessions (CrUX):

| Core Web Vital | Budget | Key Optimization Invariant |
| :--- | :---: | :--- |
| **LCP (Largest Contentful Paint)** | $\le 2.5\text{s}$ | Preload hero image with `fetchpriority="high"`; avoid lazy-loading above-the-fold media. |
| **INP (Interaction to Next Paint)** | $\le 200\text{ms}$ | Chunk long JavaScript tasks ($>50\text{ms}$); offload computation using `requestIdleCallback`. |
| **CLS (Cumulative Layout Shift)** | $\le 0.1$ | Explicit `width`/`height` or CSS `aspect-ratio` on all images, embeds, and dynamic slots. |

### 3.1 Caching Hierarchy
- Fingerprinted static assets: `Cache-Control: public, max-age=31536000, immutable`.
- HTML and dynamic routes: `Cache-Control: s-maxage=60, stale-while-revalidate=86400` with ETags.
- Deep Reference: [`references/coreWebVitalsAndCaching.md`](references/coreWebVitalsAndCaching.md).

---

## 4. Accessibility & Web Testing (`/web-testing`)

### 4.1 WCAG 2.2 Level AA Requirements
1. **Color Contrast**: $\ge 4.5:1$ for body text, $\ge 3:1$ for large/bold text.
2. **Keyboard Operability**: Visible `:focus-visible` ring on all interactive elements; no keyboard traps.
3. **Touch Targets**: Minimum **24x24 CSS pixels** on mobile viewports.
4. **Form Labels**: Every input must link to a valid `<label>` or `aria-label`.

### 4.2 Automated Testing
- Automated accessibility scans in Playwright using `@axe-core/playwright`.
- E2E smoke tests validating critical business flows (homepage render, auth, checkout/form submission).
- Deep Reference: [`references/accessibilityAndWebTesting.md`](references/accessibilityAndWebTesting.md).

---

## 5. Production API Standards & Latency Budgets (`/web-api`)

Web application backends and edge APIs require predictable contracts and strict latency SLOs:

### 5.1 Latency Budgets (SLOs)
- **p50 (Median)**: $\le 50\text{ms}$
- **p95 (95th Percentile)**: $\le 150\text{ms}$
- **p99 (Worst Case)**: $\le 300\text{ms}$

### 5.2 RFC 9457 Problem Details Error Responses
All $4\text{xx}$ and $5\text{xx}$ responses return `Content-Type: application/problem+json`:
```json
{
  "type": "https://api.example.com/errors/invalid-parameter",
  "title": "Invalid Request Parameters",
  "status": 400,
  "detail": "Field 'email' is malformed.",
  "instance": "/api/v1/users",
  "traceId": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
}
```
Template: [`templates/problemDetails.template.json`](templates/problemDetails.template.json).

### 5.3 Idempotency Keys
State-mutating endpoints (`POST /payments`, `POST /orders`) must accept an `Idempotency-Key` header to prevent double-execution during network retries.
- Deep Reference: [`references/productionApiStandardsAndLatency.md`](references/productionApiStandardsAndLatency.md).

---

## 6. Anti-Patterns to Avoid

| Anti-Pattern | Why It Breaks Production | Correct Modern Standard |
| :--- | :--- | :--- |
| **Lazy Loading the Hero Image** | Delays Largest Contentful Paint (LCP) significantly, hurting search rankings. | Mark hero image with `loading="eager"` and `fetchpriority="high"`. |
| **Omitting Image Dimensions** | Browsers cannot reserve space before image loads, triggering high Cumulative Layout Shift (CLS). | Set explicit `width` and `height` attributes or CSS `aspect-ratio`. |
| **Firing Analytics Before Cookie Consent** | Violates GDPR / ePrivacy directives, exposing businesses to statutory fines. | Gate all non-essential trackers behind affirmative user consent. |
| **Generic 500 JSON Errors (`{ error: "failed" }`)** | Clients cannot programmatically handle errors cleanly or debug field validation issues. | Return standardized RFC 9457 Problem Details (`application/problem+json`). |
| **Blocking All AI Bots in `robots.txt`** | Completely hides site from AI search engines (Perplexity, ChatGPT Search), eliminating modern referral traffic. | Permit search synthesis agents while blocking training scrapers. |
| **Missing Canonical Tags** | Causes duplicate content penalties across query params, trailing slashes, or HTTP/HTTPS variants. | Enforce self-referential canonical tags on all indexable pages. |

---

## 7. Automated CLI Diagnostics & Execution (`/web-audit`)

Run the automated pre-flight web auditor from the project root:

```bash
# 1. Audit web project and generate web-readiness-report.md
python3 skills/frontend/webEngineering/scripts/auditWebReadiness.py --path .

# 2. Output JSON for CI/CD deployment gating
python3 skills/frontend/webEngineering/scripts/auditWebReadiness.py --path . --format json
```
