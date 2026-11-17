# GitHub Docs API Specification

Official programmatic interfaces provided by GitHub Docs (`https://docs.github.com`) to retrieve Markdown content, search documentation, and discover endpoints.

## 1. Article Endpoint

The Article endpoint returns the Markdown content and metadata of any GitHub Docs page.

### Getting Full Markdown Body
`GET https://docs.github.com/api/article/body` returns raw markdown content.

```shell
curl -fsSL "https://docs.github.com/api/article/body?pathname=/en/get-started/start-your-journey/what-is-github"
```

Query Parameters:
- `pathname` (required): The article path including language prefix (e.g. `/en/...`).
- `apiVersion` (optional): For REST API reference pages, specifies which version to retrieve.

### Getting Article Metadata
`GET https://docs.github.com/api/article/meta` returns title, intro, product area, and breadcrumbs in JSON.

### Getting Content and Metadata Together
`GET https://docs.github.com/api/article?pathname=/en/...` returns both metadata and the article body in a single JSON payload.

---

## 2. Pagelist Endpoint

Returns a list of every available page path for a given language and version:

```shell
curl -fsSL "https://docs.github.com/api/pagelist/en/free-pro-team@latest"
```

- Languages list: `GET https://docs.github.com/api/pagelist/languages`
- Versions list: `GET https://docs.github.com/api/pagelist/versions`

---

## 3. Search Endpoint

Full-text search across all documentation content:

```shell
curl -fsSL "https://docs.github.com/api/search/v1?query=actions&client_name=docs-api-example&version=free-pro-team&language=en"
```

Query Parameters:
- `query` (required): Search keyword
- `client_name` (required): Client identifier
- `version` (optional): `free-pro-team`, `enterprise-cloud`, etc.
- `size` (optional): Results per page (up to 50, default 10)

---

## 4. `llms.txt` for AI Agents

GitHub Docs publishes a standard `llms.txt` file at `https://docs.github.com/llms.txt`.
AI agents should use this as the primary sitemap index for discovering documentation structure.
