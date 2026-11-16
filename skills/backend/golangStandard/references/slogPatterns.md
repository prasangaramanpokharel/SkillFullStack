# Go `log/slog` Production Patterns

## 1. Handlers & Performance
- **`slog.NewJSONHandler`**: Emits newline-delimited JSON objects. Standard for production containers, Kubernetes, Datadog, AWS CloudWatch.
- **`slog.NewTextHandler`**: Human-readable colored/plain text output for local development.

## 2. Using `slog.Attr` for High-Throughput Paths
In hot loops, prefer strongly-typed attribute constructors to avoid reflection allocations:
```go
slog.String("user_id", u.ID)
slog.Int("attempts", count)
slog.Duration("latency", elapsed)
slog.Any("err", err)
```

## 3. Custom ReplaceAttr Hook (Masking Sensitive Keys)
```go
opts := &slog.HandlerOptions{
    ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
        if a.Key == "password" || a.Key == "token" || a.Key == "authorization" {
            return slog.String(a.Key, "[REDACTED]")
        }
        return a
    },
}
```
