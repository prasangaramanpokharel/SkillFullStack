# Web Production Launch Readiness Report

- **Evaluation Date**: {TIMESTAMP}
- **Target Application**: `{APP_NAME}` (`{APP_URL_OR_PATH}`)
- **Framework / Runtime**: {FRAMEWORK_RUNTIME}
- **Overall Readiness Score**: {SCORE}% ({PASSED_CHECKS}/{TOTAL_CHECKS} Checks Passed)
- **Launch Status**: {PRODUCTION_READY | LAUNCH_BLOCKED_CRITICAL_ISSUES}

---

## 1. Domain Health Scorecards

| Audit Category | Status | Passed | Total | Key Blocker |
| :--- | :---: | :---: | :---: | :--- |
| **Legal & Privacy (GDPR/CCPA/Cookies)** | {PASS_FAIL} | {P_LEGAL} | {T_LEGAL} | {BLOCKER_LEGAL} |
| **Security Headers & Defense (CSP/HSTS)** | {PASS_FAIL} | {P_SEC} | {T_SEC} | {BLOCKER_SEC} |
| **Technical SEO & Agent Discovery (llms.txt)** | {PASS_FAIL} | {P_SEO} | {T_SEO} | {BLOCKER_SEO} |
| **Core Web Vitals & Caching (LCP/INP/CLS)** | {PASS_FAIL} | {P_CWV} | {T_CWV} | {BLOCKER_CWV} |
| **Accessibility (WCAG 2.2 AA) & Testing** | {PASS_FAIL} | {P_A11Y} | {T_A11Y} | {BLOCKER_A11Y} |
| **Production API (RFC 9457 & Latency SLOs)** | {PASS_FAIL} | {P_API} | {T_API} | {BLOCKER_API} |

---

## 2. Detailed Pre-Flight Checklist Breakdown

### 2.1 Legal & Compliance
- [ ] **Privacy Policy & Terms**: Accessible in footer with last-updated date.
- [ ] **Cookie Consent Banner**: Opt-in required before loading non-essential analytics/trackers (GDPR compliant).
- [ ] **Accessibility Statement**: Accessible link documenting WCAG adherence and contact for reporting barriers.

### 2.2 Security & Headers
- [ ] **Strict-Transport-Security (HSTS)**: `max-age=63072000; includeSubDomains; preload`
- [ ] **Content-Security-Policy (CSP)**: Nonce-based or strict hash-based CSP Level 3.
- [ ] **X-Content-Type-Options**: `nosniff`
- [ ] **Referrer-Policy**: `strict-origin-when-cross-origin`
- [ ] **Permissions-Policy**: Restricted camera, microphone, and geolocation.

### 2.3 Technical SEO & Agent Readiness
- [ ] **`robots.txt`**: Present with differentiated rules for search vs AI crawlers.
- [ ] **`llms.txt` & `llms-full.txt`**: Present at root with clean markdown documentation links.
- [ ] **Sitemap & Canonical URLs**: `sitemap.xml` registered; canonical tags on every indexable page.
- [ ] **Structured Data (JSON-LD)**: Schema.org markup (Organization, WebSite, Article, Product).
- [ ] **Open Graph & Twitter Cards**: Valid `og:image`, `og:title`, `og:description`, `twitter:card`.

### 2.4 Core Web Vitals & Performance
- [ ] **LCP (Largest Contentful Paint)**: $\le 2.5\text{s}$ at 75th percentile (Hero asset preloaded, `fetchpriority="high"`).
- [ ] **INP (Interaction to Next Paint)**: $\le 200\text{ms}$ (No long-running tasks blocking main thread).
- [ ] **CLS (Cumulative Layout Shift)**: $\le 0.1$ (Explicit image width/height or CSS aspect-ratio).
- [ ] **Caching Headers**: `Cache-Control: public, max-age=31536000, immutable` on hashed static assets.

### 2.5 Accessibility & Testing
- [ ] **Color Contrast**: $\ge 4.5:1$ for normal text, $\ge 3:1$ for large text (WCAG 2.2 AA).
- [ ] **Keyboard Navigation**: All interactive elements reachable via Tab; visible `:focus-visible` ring.
- [ ] **Screen Reader Compatibility**: Semantic landmarks (`<main>`, `<nav>`, `<header>`), valid ARIA roles.
- [ ] **E2E Test Coverage**: Automated smoke and critical user-path tests running in CI/CD.

### 2.6 Production API & Observability
- [ ] **Standardized Error Responses**: RFC 9457 Problem Details JSON format.
- [ ] **Latency Budgets**: p95 $\le 150\text{ms}$, p99 $\le 300\text{ms}$.
- [ ] **Idempotency Protection**: Mutating endpoints support `Idempotency-Key` headers.
- [ ] **Error Monitoring & Healthchecks**: Sentry / OpenTelemetry active; `/api/health` probe operational.

---

## 3. Remediation Diffs & Fixes
{REMEDIATION_CODE_DIFFS}
