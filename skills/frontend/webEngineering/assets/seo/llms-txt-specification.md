# `llms.txt` Standard Specification

`llms.txt` is an open community standard proposed to provide Large Language Models and AI coding/research agents with a clean, high-signal index of web documentation without HTML boilerplate, scripts, or navigation elements.

---

## 1. File Placement & Discovery
- The file must be served at the root of the domain: `/llms.txt` (MIME type: `text/plain` or `text/markdown`).
- An optional companion file `/llms-full.txt` may be provided containing the complete concatenated markdown corpus.

---

## 2. Syntax & Structural Requirements

1. **H1 Header**: The exact human-readable name of the project or organization.
   ```markdown
   # Project Name
   ```
2. **Blockquote (`>`) Summary**: A single concise paragraph summarizing what the project does and its core value proposition.
   ```markdown
   > High-performance edge runtime for serverless agents.
   ```
3. **H2 Section Headers**: Curated categories grouping links.
   ```markdown
   ## Documentation
   - [Quickstart](https://example.com/docs/quickstart.md): Getting started in under 5 minutes.
   - [API Reference](https://example.com/docs/api.md): REST endpoints and技术 API specs.
   ```
4. **Markdown Link Convention**: Links should point directly to `.md` endpoints or clean text representations rather than client-rendered JS pages.
