# Core Web Vitals (CWV) Engineering Standards

Core Web Vitals represent Google's standardized metrics for user-centric web performance evaluated at the 75th percentile of field data (CrUX).

---

## 1. Metric Thresholds & Optimization

### 1.1 Largest Contentful Paint (LCP)
- **Target**: $\le 2.5\text{ seconds}$
- **Focus**: Render time of the largest visible block (hero image, heading text, video poster).
- **Hardening Rules**:
  - Preload the LCP resource: `<link rel="preload" as="image" href="..." fetchpriority="high">`.
  - Avoid client-side lazy-loading on the first above-the-fold image (never `loading="lazy"` on hero images).
  - Serve modern image formats: AVIF (preferred) or WebP.

### 1.2 Interaction to Next Paint (INP)
- **Target**: $\le 200\text{ milliseconds}$
- **Focus**: Responsiveness to user input (clicks, taps, keyboard strokes) over the entire page session.
- **Hardening Rules**:
  - Decompose long JavaScript tasks ($>50\text{ms}$) using `requestIdleCallback` or `setTimeout(..., 0)`.
  - Minimize main-thread locking from heavy third-party analytics or chat widgets.
  - Avoid synchronous layout thrashing (batching DOM reads before DOM writes).

### 1.3 Cumulative Layout Shift (CLS)
- **Target**: $\le 0.1$
- **Focus**: Visual stability during page load.
- **Hardening Rules**:
  - Explicit `width` and `height` attributes on all `<img>` and `<iframe>` elements.
  - CSS `aspect-ratio` reserving structural space before media loads.
  - Font display swapping: `font-display: swap` with matched fallback metrics.
