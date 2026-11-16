# Discriminated Unions & Type Narrowing in TypeScript

## Why Discriminated Unions Are Essential
A discriminated union uses a common literal property (the "discriminant", e.g., `status`, `kind`, `type`) across multiple variants.

## Exhaustive Compile-Time Validation
When adding new variants to a union, TypeScript must fail compilation if a `switch` statement forgets to handle the new variant:

```typescript
export function assertNever(value: never): never {
  throw new Error(`Unhandled union member: ${JSON.stringify(value)}`);
}

type Notification =
  | { type: "email"; email: string }
  | { type: "sms"; phoneNumber: string }
  | { type: "push"; deviceToken: string };

function sendNotification(n: Notification) {
  switch (n.type) {
    case "email":
      return dispatchEmail(n.email);
    case "sms":
      return dispatchSms(n.phoneNumber);
    case "push":
      return dispatchPush(n.deviceToken);
    default:
      return assertNever(n); // Compiler error if a 4th variant is added without a case!
  }
}
```
