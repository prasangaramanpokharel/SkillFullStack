# Durable Step Function Execution Patterns

1. **`step.run(name, handler)`**: The atomic unit of durable execution. Caches return value. Retries on exception without re-running prior steps.
2. **`step.sleep(name, duration)`**: Halts execution for seconds, hours, or days. Costs zero compute resources while sleeping.
3. **`step.sleepUntil(name, timestamp)`**: Schedules resumption for a specific future ISO date or UNIX epoch.
4. **`step.waitForEvent(name, { event, timeout, match })`**: Suspends workflow execution until a specific external webhook arrives (e.g. `order.payment_verified` with matching `orderId`).
