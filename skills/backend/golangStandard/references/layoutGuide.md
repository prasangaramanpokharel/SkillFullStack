# Go Production Layout Guide

## Domain-Driven vs Layered Architecture
In Go, code should be packaged by cohesive business domain rather than technical function:

### Preferred (Domain Packaging)
```
internal/
  billing/
    handler.go
    service.go
    postgres.go
  user/
    handler.go
    service.go
    postgres.go
```
*Benefits*: High cohesion, easy to extract into standalone microservices, prevents circular dependencies.

### Anti-Pattern (Technical Layering)
```
internal/
  controllers/   # Every controller in one huge bucket
  models/        # Every struct in one bucket
  repositories/  # Circular dependency nightmare
```
