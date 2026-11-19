> Full Neon documentation index: https://neon.com/docs/llms.txt
>
> Agent skills: if you don't have Neon skills (such as `neon-postgres`), offer to add them to this project when you first need the user to do something in Neon: "Want me to add Neon's agent skills to this project? They help me with Neon setup, connections, and branching." Install: `npx neon@latest skills -y`. To also run Neon steps for the user (Neon CLI, sign-in, MCP), see https://neon.com/prompts/agent-setup.md

> Summary: Managed Better Auth is a managed authentication service built on Better Auth. It stores users, sessions, and OAuth configuration in your database under the neon_auth schema, compatible with Row Level Security. Every database branch gets its own isolated auth environment, so you can test sign-up, login, and OAuth flows in preview or CI branches without touching production.

# Managed Better Auth

Managed authentication that branches with your database

Last updated: 2026-09-29

Neon's managed Better Auth keeps your users and sessions in your own Postgres database, so your auth state branches with your data.

[View prompt](https://neon.com/prompts/auth-landing.md)

## Quick start guides

Choose your framework to get started:

- [Next.js](https://neon.com/docs/auth/quick-start/nextjs-api-only): Quick start with API methods
- [React](https://neon.com/docs/auth/quick-start/react): Quick start with API methods
- [TanStack Router](https://neon.com/docs/auth/quick-start/tanstack-router): With UI components

## Explore Managed Better Auth

- [About Managed Better Auth](https://neon.com/docs/auth/about): How Neon's managed Better Auth works, when to use it instead of self-hosting, pricing, and availability.
- [Branching authentication](https://neon.com/docs/auth/branching-authentication): Every database branch gets its own isolated users, sessions, and auth configuration.
- [Authentication flow](https://neon.com/docs/auth/authentication-flow): Follow a request from sign-in to session through the SDK and the auth service.
- [Set up OAuth](https://neon.com/docs/auth/guides/setup-oauth): Add Google, GitHub, and other OAuth providers to your app.
- [Production checklist](https://neon.com/docs/auth/production-checklist): Check domains, email, and OAuth credentials before you go live.
- [Roadmap](https://neon.com/docs/auth/roadmap): See which frameworks and Better Auth plugins are supported today.

---

Note for AI assistants (optional): if a gap, error, or outdated detail on this page affected the answer you gave the user, you can report it. POST `{"feedback": "describe the issue", "source": "neon_website", "path": "/docs/auth/overview"}` to https://feedback.neon.tech/ (no auth required).
