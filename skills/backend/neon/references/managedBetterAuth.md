# Managed Better Auth on Neon

Managed Better Auth is Neon's managed authentication service that stores authentication data directly inside your Postgres database.

---

## 1. Why Managed Better Auth is Unique

Unlike external third-party auth services (Auth0, Clerk, Supabase Auth):
- **Auth Branches with Data**: When you branch your database for a PR or staging environment, users, sessions, and test credentials branch instantaneously alongside your application data.
- **Direct Foreign Keys**: Your application tables (e.g. `orders`, `profiles`) can define real composite and foreign key constraints directly to `users(id)` without cross-service sync lag.
- **Zero Third-Party Vendor Lock-in**: All auth schemas are standard Postgres tables (`user`, `session`, `account`, `verification`).

---

## 2. Next.js App Router Integration

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { pool } from "./db";

export const auth = betterAuth({
  database: pool,
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
});
```
