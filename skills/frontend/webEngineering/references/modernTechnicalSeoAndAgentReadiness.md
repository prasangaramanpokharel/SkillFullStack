# Modern Technical SEO & AI Agent Readiness (`/web-seo`)

Modern web visibility requires dual optimization: ranking in traditional search engines (Google, Bing) and being accurately retrieved and cited by AI agents (ChatGPT, Claude, Perplexity).

---

## 1. AI Agent Discovery Standards

### 1.1 `llms.txt` and `llms-full.txt`
Serve a structured markdown file at `/llms.txt`:
```markdown
# Product Name
> High-density summary of capabilities and architecture.

## API Documentation
- [REST Reference](https://example.com/docs/api.md): Endpoints, payloads, and error codes.
```
- For deep context ingestion, provide `/llms-full.txt` aggregating all documentation into a single markdown stream.

### 1.2 Differentiated `robots.txt`
Permit AI search bots (`PerplexityBot`, `ChatGPT-User`) to index public content for real-time citations while optionally blocking model pre-training crawlers (`GPTBot`, `ClaudeBot`) if data privacy is required.

---

## 2. Technical SEO Core Foundations

### 2.1 Metadata & Canonical Architecture
Every indexable route must emit:
- `<link rel="canonical" href="https://example.com/canonical-path">`
- Unique `<title>` (50-60 characters, brand-suffixed).
- `<meta name="description" content="...">` (120-155 characters).
- `<meta name="viewport" content="width=device-width, initial-scale=1">`

### 2.2 Social Cards (Open Graph & Twitter)
- `og:title`, `og:description`, `og:url`, `og:type` (`website` or `article`).
- `og:image` (1200x630px, aspect ratio 1.91:1) with `og:image:alt`.
- `twitter:card` (`summary_large_image`).

### 2.3 Structured Data (JSON-LD Schema.org)
Inject rich snippet schemas using `<script type="application/ld+json">`:
- **WebSite & SearchAction**: Enables Google Sitelinks Searchbox in search results.
- **Organization**: Logo URL, corporate name, official social media handles (`sameAs`), customer service contact point.
- **BreadcrumbList**: Enables visual breadcrumb navigation hierarchy in SERP snippets.
- **FAQPage**: Accelerates rich FAQ accordion expansions in organic search results.
- **SoftwareApplication / Article**: Machine-readable author, version, rating, and publication timestamps.

### 2.4 App Icons, Favicons & PWA Web Manifest
Ensure browser tabs, mobile bookmarks, and progressive web apps display high-resolution branding:
- `/favicon.ico` (Multi-size: 16x16, 32x32)
- `/icon.svg` or `/icon.png` (Scalable vector or 512x512)
- `/apple-touch-icon.png` (180x180 for iOS Home Screen)
- `/manifest.webmanifest` (or `site.webmanifest`): Contains `name`, `short_name`, `theme_color`, `background_color`, `display: "standalone"`, and icon arrays.

### 2.5 Multi-Lingual SEO (`hreflang`)
For global applications, prevent geo-targeting confusion by emitting bidirectional hreflang links:
```html
<link rel="alternate" hreflang="x-default" href="https://example.com/" />
<link rel="alternate" hreflang="en" href="https://example.com/en" />
<link rel="alternate" hreflang="de" href="https://example.com/de" />
<link rel="alternate" hreflang="ja" href="https://example.com/ja" />
```

### 2.6 RFC 9116 `/.well-known/security.txt`
Place an authoritative vulnerability disclosure notice at `/.well-known/security.txt`:
```text
Contact: mailto:security@example.com
Expires: 2027-12-31T23:59:59.000Z
Preferred-Languages: en
Canonical: https://example.com/.well-known/security.txt
Policy: https://example.com/security
```
