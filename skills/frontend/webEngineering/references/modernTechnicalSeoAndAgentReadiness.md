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
- `WebSite` with `SearchAction` for site-search box.
- `Organization` with logo, social links, and contact points.
- `SoftwareApplication` or `Article` on specific pages.
