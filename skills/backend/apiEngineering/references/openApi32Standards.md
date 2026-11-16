# OpenAPI 3.2.1 Specifications Guide

Reference guide for OpenAPI 3.2.1 (released September 10, 2026), building upon OpenAPI 3.1 and JSON Schema 2020-12.

---

## 1. Key Capabilities in OpenAPI 3.2.1

### A. Root `$self` Identification
Allows specifications to explicitly identify their canonical URI at the root, resolving `$ref` ambiguity during local authoring and multi-file bundling:
```yaml
openapi: 3.2.1
$self: https://api.example.com/openapi/v1.yaml
info:
  title: Enterprise Order Service
  version: 1.0.0
```

### B. First-Class Real-Time Streaming Support
Native support for Server-Sent Events (`text/event-stream`), JSON Lines, and JSON Sequences via `itemSchema`:
```yaml
responses:
  '200':
    description: Real-time order status stream
    content:
      text/event-stream:
        itemSchema:
          $ref: '#/components/schemas/OrderStatusEvent'
```

### C. The HTTP `QUERY` Method
Native contract support for safe, idempotent read queries with complex request bodies (RFC 9110 / draft):
```yaml
paths:
  /v1/analytics/query:
    query:
      summary: Complex analytical aggregation query
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AnalyticsFilterQuery'
      responses:
        '200':
          description: Query results
```

### D. Hierarchical Tags Taxonomies
Native support for grouping and categorizing operations without non-standard vendor extensions:
```yaml
tags:
  - name: Invoicing
    summary: Customer billing and invoices
    kind: domain
  - name: Payments
    parent: Invoicing
    summary: Payment processing and refunds
```
