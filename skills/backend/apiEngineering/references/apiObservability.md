# API Observability: Logs, Metrics & Distributed Tracing Reference

---

## 1. Structured JSON Logging

Every API log entry must be structured JSON and include standard correlation keys:
```json
{
  "timestamp": "2026-11-16T12:00:00.123Z",
  "level": "INFO",
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
  "spanId": "00f067aa0ba902b7",
  "http": {
    "method": "POST",
    "route": "/v1/invoices",
    "status": 201,
    "durationMs": 42
  },
  "tenantId": "ten_01HX9...",
  "userId": "usr_01HX9..."
}
```
*Law*: Never log sensitive credentials, passwords, raw authorization headers, or full credit card numbers.

---

## 2. The RED Method for API Metrics

Track three golden signals on every endpoint:
- **Rate**: Invocations per second (`requests_total{route="/v1/users", status="200"}`).
- **Errors**: Number of 5xx server errors and unhandled exceptions.
- **Duration**: Latency histogram distribution (track p50, p95, p99).

---

## 3. Distributed Tracing (OpenTelemetry)

Propagate `traceparent` headers across microservices according to W3C Trace Context specifications (`traceparent: 00-4bf9...-00f0...-01`).
