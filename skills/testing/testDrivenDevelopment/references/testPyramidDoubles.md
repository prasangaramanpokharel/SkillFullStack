# Test Engineering & Test Double Deep Reference

## 1. Test Pyramid Breakdown (SE Curriculum Chapter 10)

```
       /\
      /  \       10% End-to-End (E2E) - System level, full environment, UI/API
     /----\
    /      \     20% Integration - Component wiring, database repositories, HTTP boundaries
   /--------\
  /          \   70% Unit Tests - Domain logic, algorithmic isolation, <10ms execution
 /------------\
```

- **Unit Tests**: Test pure business logic in isolation. Mocks or fakes replace slow dependencies.
- **Integration Tests**: Verify that separate units work together correctly (e.g., ORM mappings, serialization).
- **End-to-End (E2E)**: Verify critical path user journeys from entry point to persistence.

---

## 2. Test Doubles Classification (Meszaros Taxonomy)

1. **Dummy Objects**: Passed to satisfy parameters (e.g. `null`, empty string, empty object), never queried.
2. **Test Stubs**: Provide pre-canned responses to queries made during the test.
3. **Test Spies**: Record information about calls (method invoked, arguments, frequency) for post-execution assertions.
4. **Mock Objects**: Expectations are defined upfront; verify that interactions occurred in the exact expected order.
5. **Fake Objects**: Implement complete functionality with shortcuts not suitable for production (e.g., `InMemoryUserRepository`).

---

## 3. Boundary Value Analysis (BVA) Heuristic

For any integer input range $[MIN, MAX]$:
- Test 5 key points: $MIN - 1$, $MIN$, $NOMINAL$, $MAX$, $MAX + 1$.
- Special cases: $0$, empty string `""`, null / undefined, maximum memory buffer limits.
