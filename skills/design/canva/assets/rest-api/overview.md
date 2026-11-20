# Canva REST API Architecture Overview

The Canva REST API provides programmable HTTP endpoints to create, read, update, export, and autofill Canva designs, folders, and creative assets.

## Base URL & Protocols
- **API Base URL**: `https://api.canva.com/rest/v1`
- **Transport**: HTTPS with TLS 1.3
- **Content Type**: `application/json`
- **Authentication**: Bearer token via `Authorization: Bearer <access_token>`

## Resource Topology
- `/v1/users/me` — Current authenticated user profile
- `/v1/designs` — Design search, retrieval, metadata inspection, and creation
- `/v1/designs/{designId}/pages` — Page hierarchy and responsive layout metadata
- `/v1/designs/{designId}/comments` — Comment threads and review discussions
- `/v1/editing-sessions` — Transactional editing buffers for atomic design modifications
- `/v1/brand-templates` — Master templates configured with autofill datasets
- `/v1/autofills` — Batch generation jobs from tabular records
- `/v1/asset-uploads` — Media upload staging and job tracking
- `/v1/resizes` — Multi-channel canvas aspect-ratio transformation jobs

## Rate Limits & Concurrency
- Standard Rate Limit: 10 requests per second per access token.
- Mutating batch calls (e.g. bulk autofill or media uploads) must be executed sequentially with exponential backoff on HTTP 429 status codes.
