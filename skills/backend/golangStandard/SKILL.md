---
name: golangStandard
description: Production-grade Go engineering standards. Implements log/slog structured logging, context propagation, explicit error wrapping with %w, errgroup structured concurrency, and clean internal domain layouts.
version: 1.23+
last-verified: 2026-11-16
compatibility: Go 1.22+, Go 1.23+, Go 1.24+
slash-commands:
  - command: /go-standard
    description: Enforce production Go architecture, clean domain layout, and error wrapping
    argument-hint: "[--domain=order|user]"
  - command: /go-slog
    description: Configure structured logging with log/slog and context propagation
    argument-hint: "[--format=json|text]"
  - command: /go-concurrency
    description: Design structured concurrency with errgroup and context cancellation
    argument-hint: "[--workers=10]"

---

# Production Go Engineering Guide

## 1. Core Architecture & Project Layout
Avoid sprawling, deeply nested `/pkg` directory trees. Modern Go services adhere to clean domain separation or flat packages:

```
my-service/
├── cmd/
│   └── server/
│       └── main.go       # Dependency wiring, config load, graceful OS shutdown
├── internal/
│   ├── platform/       # Cross-cutting concerns (db pool, telemetry, slog setup)
│   └── order/          # Domain package (handler, domain model, repository)
│       ├── handler.go  # HTTP/gRPC transport adapters
│       ├── service.go  # Pure business logic
│       └── repo.go     # Database queries / SQL persistence
├── go.mod
└── go.sum
```

- Code inside `internal/` cannot be imported by external modules, enforcing privacy.
- Group by business domain (`internal/order`, `internal/user`) rather than technical layers (`internal/controllers`, `internal/models`).

---

## 2. Structured Logging with `log/slog`
Never use `log.Println` or `fmt.Println` in production code. Use the standard library `log/slog`:

### Initialization & Context Extraction
```go
package platform

import (
	"context"
	"log/slog"
	"os"
)

type contextKey string
const loggerKey contextKey = "slog_logger"

func InitLogger(isProduction bool) *slog.Logger {
	var handler slog.Handler
	opts := &slog.HandlerOptions{Level: slog.LevelInfo}

	if isProduction {
		handler = slog.NewJSONHandler(os.Stdout, opts) // CloudWatch / Datadog JSON
	} else {
		handler = slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelDebug})
	}

	logger := slog.New(handler)
	slog.SetDefault(logger)
	return logger
}

// Inject request-scoped trace fields
func ContextWithLogger(ctx context.Context, logger *slog.Logger) context.Context {
	return context.WithValue(ctx, loggerKey, logger)
}

func LoggerFromContext(ctx context.Context) *slog.Logger {
	if l, ok := ctx.Value(loggerKey).(*slog.Logger); ok {
		return l
	}
	return slog.Default()
}
```

---

## 3. Idiomatic Error Handling
Wrap errors contextually with `%w` so callers can inspect sentinel errors with `errors.Is` and custom error types with `errors.As`:

```go
package order

import (
	"context"
	"errors"
	"fmt"
)

var ErrOrderNotFound = errors.New("order not found")

func (s *Service) GetOrder(ctx context.Context, orderID string) (*Order, error) {
	logger := platform.LoggerFromContext(ctx)

	order, err := s.repo.FindByID(ctx, orderID)
	if err != nil {
		if errors.Is(err, ErrOrderNotFound) {
			logger.WarnContext(ctx, "order lookup missed", "order_id", orderID)
			return nil, fmt.Errorf("get order [%s]: %w", orderID, ErrOrderNotFound)
		}

		// Log structured error attribute "err", err (never fmt.Sprintf)
		logger.ErrorContext(ctx, "database query failed", "order_id", orderID, "err", err)
		return nil, fmt.Errorf("get order [%s]: %w", orderID, err)
	}

	return order, nil
}
```

---

## 4. Structured Concurrency with `errgroup`
Avoid raw `go func()` without lifecycle management. Use `golang.org/x/sync/errgroup` with a cancellable context:

```go
import (
	"context"
	"golang.org/x/sync/errgroup"
)

func ProcessBatch(ctx context.Context, items []string) error {
	g, ctx := errgroup.WithContext(ctx)
	g.SetLimit(10) // Bound concurrency to avoid resource exhaustion

	for _, item := range items {
		item := item // Capture variable
		g.Go(func() error {
			if err := ctx.Err(); err != nil {
				return err // Context cancelled early by another failure
			}
			return processItem(ctx, item)
		})
	}

	return g.Wait() // Returns first encountered error and cancels sibling tasks
}
```

---

## 5. Anti-Patterns & Critical Pitfalls
- ❌ **Ignoring Context**: Never execute SQL queries or HTTP calls using `context.Background()` inside handlers; always pass down the request's `r.Context()`.
- ❌ **Unstructured Log Formatting**: Never format errors into log strings like `logger.Error(fmt.Sprintf("failed: %v", err))`. Always use key-value structured pairs: `"err", err`.
- ❌ **Panic for Flow Control**: Do not use `panic()` for operational errors; return explicit error values. Reserve panic only for unrecoverable startup assertions.
- ❌ **Goroutine Leaks**: Never start goroutines that listen to unbuffered channels without a `select` block listening to `ctx.Done()`.

---

## 6. References & Bundled Utilities
- Structured logging patterns: [references/slogPatterns.md](references/slogPatterns.md)
- Domain project layout guidelines: [references/layoutGuide.md](references/layoutGuide.md)
- Go module scaffolding tool: [scripts/scaffoldGoModule.py](scripts/scaffoldGoModule.py)
