# Core Web Vitals & Caching Hierarchies (`/web-performance`)

High-performance web applications optimize both client-side rendering pipelines and server/edge caching layers.

---

## 1. Core Web Vitals Engineering Budgets

| Metric | Target | Root Causes | Key Mitigation |
| :--- | :---: | :--- | :--- |
| **LCP** | $\le 2.5\text{s}$ | Slow server TTFB, render-blocking scripts, unoptimized hero images | Preload hero image with `fetchpriority="high"`, edge CDN caching |
| **INP** | $\le 200\text{ms}$ | Long tasks ($>50\text{ms}$), layout thrashing, main thread locking | Chunk execution via `requestIdleCallback`, defer non-critical JS |
| **CLS** | $\le 0.1$ | Images/embeds without dimensions, dynamically injected banners | Explicit `width`/`height` or CSS `aspect-ratio` on all elements |

---

## 2. HTTP Caching Architecture

### 2.1 Static Fingerprinted Assets (JS, CSS, Media)
```http
Cache-Control: public, max-age=31536000, immutable
```

### 2.2 Dynamic HTML Pages & API Endpoints
```http
Cache-Control: s-maxage=60, stale-while-revalidate=86400
ETag: "w/33a64df551425fcc55e4d42a148795d9f25f89d4"
```

---

## 3. Asset Compression & Modern Formats
- Images: Compress using **AVIF** (highest compression efficiency) with **WebP** fallback.
- Enforce responsive `srcset` and `sizes` attributes.
- Text Resources: Serve with **Brotli** (`br`) compression by default.
