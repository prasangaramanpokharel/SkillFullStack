# Distributed Systems Reliability & Fault Tolerance Reference

---

## 1. Resilience Patterns

### Circuit Breakers (Martin Fowler Pattern)
- **Closed**: Requests flow normally. Failures are tracked.
- **Open**: When failure rate exceeds threshold (e.g. 50% over 10s), instantly fail fast without executing outbound calls. Return `503 Service Unavailable`.
- **Half-Open**: After a cooling period (e.g. 30s), allow canary requests through to probe dependency health.

### Jittered Exponential Backoff
When retrying transient network errors:
$$\text{delay} = \min(\text{cap}, \text{base} \cdot 2^{\text{attempt}}) \pm \text{random\_jitter}$$
*Law*: Never retry non-idempotent operations without an `Idempotency-Key`.

### Bulkheads
Isolate thread pools and connection pools per downstream service so a degradation in Payment Gateway does not exhaust threads for Authentication.

---

## 2. Load Shedding & Backpressure

When CPU or connection pools reach critical thresholds ($\ge 85\%$):
- Immediately reject lower-priority traffic (background reports, non-essential webhooks) with `429 Too Many Requests` or `503 Service Unavailable`.
- Protect core checkout and authentication flows.
