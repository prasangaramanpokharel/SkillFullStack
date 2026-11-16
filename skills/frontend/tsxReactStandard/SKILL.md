---
name: tsxReactStandard
description: Modern TypeScript and React 19 production engineering standards. Implements strict discriminated unions for state, native ref props (no forwardRef), Server Actions, strict tsconfig rules, and discards React.FC and TS enums.
version: React 19 / TS 5+
last-verified: 2026-11-16
compatibility: React 19, TypeScript 5.0+, Next.js 15, Vite
---

# Modern TypeScript & React 19 Engineering Guide

## 1. Domain Modeling via Discriminated Unions
Never use "optional spaghetti" where multiple conflicting fields are marked optional (`data?: T; error?: Error; isLoading: boolean;`). Make illegal states unrepresentable:

```typescript
// ✅ Production Standard: Discriminated Union
export type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

// Compile-time exhaustiveness check helper
export function assertExhaustive(x: never): never {
  throw new Error(`Unhandled union variant: ${JSON.stringify(x)}`);
}

// Foolproof pattern matching in component render
export function UserView({ state }: { state: AsyncState<User> }) {
  switch (state.status) {
    case "idle":
      return null;
    case "loading":
      return <SkeletonLoader />;
    case "error":
      return <ErrorMessage error={state.error} />;
    case "success":
      // TypeScript guarantees state.data is defined here
      return <div>Welcome, {state.data.name}</div>;
    default:
      return assertExhaustive(state);
  }
}
```

---

## 2. React 19 Idioms & Primitives

### A. Ref as a Standard Prop (Discard `forwardRef`)
React 19 passes `ref` directly as a regular prop:

```tsx
// ❌ Legacy: forwardRef<HTMLInputElement, Props>((props, ref) => ...)
// ✅ Modern React 19:
interface SearchInputProps {
  label: string;
  ref?: React.RefObject<HTMLInputElement | null>;
}

export function SearchInput({ label, ref }: SearchInputProps) {
  return (
    <div className="flex flex-col">
      <label>{label}</label>
      <input ref={ref} type="search" className="border rounded p-2" />
    </div>
  );
}
```

### B. Typed Server Actions & `useActionState`
```tsx
"use client";

import { useActionState } from "react";

export type FormActionState =
  | { status: "idle" }
  | { status: "error"; message: string }
  | { status: "success"; recordId: string };

const initialState: FormActionState = { status: "idle" };

export function ProfileForm({ action }: { action: (prev: FormActionState, formData: FormData) => Promise<FormActionState> }) {
  const [state, formAction, isPending] = useActionState(action, initialState);

  return (
    <form action={formAction}>
      <input name="email" type="email" required />
      <button disabled={isPending}>{isPending ? "Saving..." : "Save"}</button>
      {state.status === "error" && <p className="text-red-500">{state.message}</p>}
    </form>
  );
}
```

---

## 3. Component & Type Discipline

### A. Stop using `React.FC`
Avoid `React.FC` (or `React.FunctionComponent`). Use standard function declarations with explicit interfaces:

```tsx
// ❌ Avoid: const Card: React.FC<CardProps> = ({ title, children }) => ...
// ✅ Production standard:
interface CardProps {
  title: string;
  children: React.ReactNode; // Explicitly declare children only when intended
}

export function Card({ title, children }: CardProps) {
  return (
    <div className="p-4 border rounded">
      <h2>{title}</h2>
      {children}
    </div>
  );
}
```

### B. Replace Enums with Union String Literals
Native TypeScript `enum` generates runtime object code and causes unexpected numeric typing behaviors:

```typescript
// ❌ Avoid: enum Status { Active = "ACTIVE", Inactive = "INACTIVE" }
// ✅ Production standard:
export type Status = "active" | "inactive" | "pending";
```

---

## 4. Strict Compiler Rules (`tsconfig.json`)
Always enable strictness flags to catch runtime bugs at compile time:
- `noUncheckedIndexedAccess: true`: Forces handling of `undefined` when reading array indices or dictionary keys.
- `noImplicitReturns: true`: Ensures every branch returns an explicit value.
- `strict: true`: Enables strict null checks and function typing.

---

## 5. Anti-Patterns & Critical Pitfalls
- ❌ **Optional Spaghetti**: Never create types with multiple optional fields that conflict in runtime logic.
- ❌ **`any` or Double Casting**: Never use `as unknown as Type`. Always write custom type guards (`function isUser(x: unknown): x is User`).
- ❌ **Defensive Manual Memoization**: In React 19 projects utilizing the React Compiler, do not clutter components with premature `useMemo` and `useCallback` unless verified by benchmarks.

---

## 6. References & Bundled Utilities
- Discriminated union patterns and type narrowing: [references/discriminatedUnions.md](references/discriminatedUnions.md)
- Strict `tsconfig.json` production specification: [references/tsconfigStrict.md](references/tsconfigStrict.md)
- TSX anti-pattern validator script: [scripts/validateTsxTypes.py](scripts/validateTsxTypes.py)
