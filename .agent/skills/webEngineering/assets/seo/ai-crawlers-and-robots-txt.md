# AI Crawlers & RFC 9309 `robots.txt` Specification

Modern web properties must govern search engine indexers and AI agents using differentiated user-agent directives in `robots.txt`.

---

## 1. Classification of Modern Web Bots

| Bot Category | User-Agent Tokens | Purpose | Recommended Policy |
| :--- | :--- | :--- | :--- |
| **Search Engine Indexers** | `Googlebot`, `Bingbot`, `DuckDuckBot`, `YandexBot` | Organic search results indexing | Allow content; Disallow internal API/admin |
| **AI Search & Retrieval Bots** | `PerplexityBot`, `ChatGPT-User`, `Claude-Web` | Real-time user prompt synthesis & citation | Allow indexable pages; provides referral traffic |
| **Foundation Model Training Scrapers** | `GPTBot`, `ClaudeBot`, `Google-Extended`, `CCBot` | Training dataset harvesting | Disallow if opting out of model training |

---

## 2. Best Practice Directives
```
User-agent: Googlebot
Disallow: /api/
Disallow: /admin/
Allow: /

User-agent: PerplexityBot
Disallow: /api/
Allow: /

User-agent: GPTBot
Disallow: /

Sitemap: https://example.com/sitemap.xml
```
