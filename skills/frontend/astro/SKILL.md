---
name: astro
description: Production Astro 5.x engineering guide. Covers Islands architecture, Server Islands, Content Collections, Astro Actions, View Transitions, SSR/Hybrid routing, and Zero-JS baseline.
version: 5.x
last-verified: 2026-11-17
compatibility: Astro 4, Astro 5, React, Vue, Svelte, Tailwind CSS v4, TypeScript 5+
slash-commands:
  - command: /astro-production
    description: Full Astro production architecture audit, Core Web Vitals, and build verification
    argument-hint: "[--mode=static|server|hybrid]"
  - command: /astro-island
    description: Islands architecture design and client hydration directive optimization
    argument-hint: "[--directive=load|idle|visible|media|only]"
  - command: /astro-server-island
    description: Deferred dynamic content with Server Islands and fallback states
    argument-hint: "[--component=Name]"
  - command: /astro-content
    description: Type-safe Content Collections schema definition with zod
    argument-hint: "[--collection=Name]"
  - command: /astro-action
    description: Type-safe Astro Action RPC mutation implementation
    argument-hint: "[--action=Name]"
---

# Astro 5.x Production Engineering Guide

Astro is an all-in-one web framework designed for content-focused and high-performance websites. It pioneers the **Islands Architecture** and **Server Islands**, delivering zero client-side JavaScript by default while enabling surgical interactive hydration and dynamic deferred rendering.

> [!IMPORTANT]
> **Zero-Hallucination Protocol**: Always consult local offline documentation in [`assets/`](assets/README.md) for official API specifications, configuration reference, and module exports before authoring Astro code.

---

## 1. Core Architectural Principles

```
┌─────────────────────────────────────────────────────────────┐
│                      Astro Document                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Pure Static HTML & CSS (0kb Client JS)                │  │
│  │                                                       │  │
│  │   ┌────────────────────┐     ┌─────────────────────┐  │  │
│  │   │ Client Island      │     │ Server Island       │  │  │
│  │   │ React / Vue / Svelte│    │ `server:defer`      │  │  │
│  │   │ `client:visible`   │     │ Instant Fallback    │  │  │
│  │   └────────────────────┘     └─────────────────────┘  │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

1. **Zero Client JS by Default**: Astro components (`.astro`) render exclusively on the server to static HTML and CSS. No runtime framework code is sent to the client unless explicitly instructed via client directives.
2. **Component Islands**: Interactive UI elements (React, Preact, Svelte, Vue, Solid) are isolated islands floating in a sea of static HTML. Each island hydrates independently without blocking the rest of the page.
3. **Server Islands (`server:defer`)**: Astro 5 feature allowing heavy or personalized server components to be deferred and loaded asynchronously after initial static HTML delivery, providing instant TTFB with personalized content.
4. **Type-Safe Content Layer**: Content Collections validate Markdown, MDX, and external CMS data using Zod schemas at build time.
5. **Type-Safe Actions (`astro:actions`)**: First-class RPC backend mutations with end-to-end type safety, input validation, and automatic progressive enhancement.

---

## 2. Client Hydration Directives Matrix

Never ship unnecessary JavaScript. Choose the least aggressive directive matching the component's UX needs:

| Directive | Execution Trigger | Best Use Case | Performance Impact |
| :--- | :--- | :--- | :--- |
| **None** (Default) | Rendered to static HTML | Badges, cards, static headers, footers | **Zero JS** (0 KB) |
| `client:load` | Immediately on page load | Critical interactive elements (search modal, sticky cart button) | Blocks main thread if overused |
| `client:idle` | Once page finishes initial load (`requestIdleCallback`) | Lower priority widgets (analytics widget, chat launcher) | Minimal impact on LCP |
| `client:visible` | When component enters viewport (`IntersectionObserver`) | Heavy carousels, comments sections, reviews, media players | Zero JS until scrolled into view |
| `client:media="(query)"` | When CSS media query matches | Desktop-only megamenu, mobile-only hamburger drawer | Hydrates only on targeted devices |
| `client:only="react"` | Client-side only; skips SSR | Components relying strictly on browser APIs (`window`, WebGL, canvas) | Eliminates SSR hydration mismatches |

```astro
---
// src/pages/index.astro
import Header from '../components/Header.astro'; // Pure HTML
import CartFlyout from '../components/CartFlyout.tsx'; // React Island
import ReviewsCarousel from '../components/ReviewsCarousel.svelte'; // Svelte Island
---

<Header />
<main>
  <!-- Hydrates immediately for instant interaction -->
  <CartFlyout client:load />

  <!-- Zero JS until user scrolls down to reviews -->
  <ReviewsCarousel client:visible />
</main>
```

---

## 3. Server Islands (`server:defer`) in Astro 5

Server Islands combine static caching with dynamic personalization. The static shell is served instantly from CDN cache, while personalized components render asynchronously on the server:

```astro
---
// src/pages/dashboard.astro
import UserGreeting from '../components/UserGreeting.astro';
import StaticSkeleton from '../components/StaticSkeleton.astro';

export const prerender = true; // Prerender static page shell
---

<nav>...</nav>
<main>
  <h1>Welcome to the Platform</h1>

  <!-- Server Island deferred rendering -->
  <UserGreeting server:defer>
    <!-- Fallback slot rendered immediately in static HTML -->
    <StaticSkeleton slot="fallback" />
  </UserGreeting>
</main>
```

Inside `UserGreeting.astro`:
```astro
---
// src/components/UserGreeting.astro
const session = await Astro.session?.get('user');
const user = session ? await db.getUser(session.id) : null;
---

<div>
  {user ? <p>Welcome back, {user.name}!</p> : <a href="/login">Sign In</a>}
</div>
```

---

## 4. Type-Safe Content Collections

Define schemas in `src/content.config.ts` (Astro 5+) or `src/content/config.ts` (Astro 4):

```typescript
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: ({ image }) =>
    z.object({
      title: z.string().max(80),
      description: z.string(),
      pubDate: z.coerce.date(),
      draft: z.boolean().default(false),
      coverImage: image(),
      tags: z.array(z.string()).default([]),
      author: z.string().default('Anonymous'),
    }),
});

export const collections = { blog };
```

Querying collections in pages:
```astro
---
// src/pages/blog/index.astro
import { getCollection } from 'astro:content';
import { Image } from 'astro:assets';

const posts = await getCollection('blog', ({ data }) => !data.draft);
posts.sort((a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime());
---

<ul>
  {posts.map((post) => (
    <li>
      <a href={`/blog/${post.id}/`}>
        <Image src={post.data.coverImage} alt={post.data.title} width={400} height={225} />
        <h2>{post.data.title}</h2>
      </a>
    </li>
  ))}
</ul>
```

---

## 5. Type-Safe Astro Actions (`astro:actions`)

Astro Actions replace bespoke API routes for data mutations and forms:

```typescript
// src/actions/index.ts
import { defineAction, ActionError } from 'astro:actions';
import { z } from 'astro:schema';

export const server = {
  subscribeNewsletter: defineAction({
    accept: 'form',
    input: z.object({
      email: z.string().email('Invalid email address'),
      referrer: z.string().optional(),
    }),
    handler: async ({ email, referrer }, context) => {
      // Server-side database or newsletter API call
      try {
        await db.subscribers.insert({ email, referrer, createdAt: new Date() });
        return { success: true, message: 'Subscribed successfully!' };
      } catch (err) {
        throw new ActionError({
          code: 'CONFLICT',
          message: 'This email is already subscribed.',
        });
      }
    },
  }),
};
```

Using actions in `.astro` components (Zero-JS form with progressive enhancement):
```astro
---
// src/pages/newsletter.astro
import { actions } from 'astro:actions';

const result = Astro.getActionResult(actions.subscribeNewsletter);
---

<form method="POST" action={actions.subscribeNewsletter}>
  <input type="email" name="email" required placeholder="you@example.com" />
  <button type="submit">Subscribe</button>

  {result?.error && <p class="error">{result.error.message}</p>}
  {result?.data?.success && <p class="success">{result.data.message}</p>}
</form>
```

Calling actions from Client Islands (React/Vue/Svelte):
```tsx
import { actions } from 'astro:actions';

export function NewsletterIsland() {
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const { data, error } = await actions.subscribeNewsletter(formData);
    if (error) alert(error.message);
    else alert(data.message);
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

---

## 6. Rendering Modes & Routing

Configure rendering strategy in `astro.config.mjs`:

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import node from '@astrojs/node'; // or vercel, cloudflare, netlify

export default defineConfig({
  output: 'static', // Default: Full SSG
  // output: 'server', // Full SSR with adapter
  adapter: node({ mode: 'standalone' }),
});
```

### Hybrid Rendering (`prerender` export)
In `output: 'server'` mode, mark static pages to be prerendered:
```astro
---
// src/pages/about.astro
export const prerender = true; // Built as static HTML
---
<h1>About Us</h1>
```

In `output: 'static'` mode, mark dynamic pages for on-demand server rendering:
```astro
---
// src/pages/api/live-rates.ts
export const prerender = false; // Rendered on-demand per request

export async function GET() {
  return Response.json({ rate: await fetchExchangeRate() });
}
---
```

---

## 7. Production Checklist & Quality Standards

- [ ] **Zero Unhydrated Islands**: Do not attach `client:load` to static content. Default to `.astro` components.
- [ ] **Optimize Images with `<Image />`**: Always use `import { Image } from 'astro:assets'` with explicit `width`, `height`, and `alt`. Never use unoptimized `<img>`.
- [ ] **Content Validation**: Every content collection must have a strict Zod schema in `src/content.config.ts`.
- [ ] **Prefetch Strategy**: Enable `<ClientRouter />` with `data-astro-prefetch="hover"` or `"viewport"` for instant page navigations.
- [ ] **Font Optimization**: Use local fonts via `@font-face` or `@astrojs/font` with `font-display: swap` to prevent layout shifts (CLS).
- [ ] **Security Headers**: Configure CSP, HSTS, and CORS in `src/middleware.ts`.
- [ ] **Partytown for 3rd-Party Scripts**: Offload Google Analytics, GTM, and trackers to Web Workers using `@astrojs/partytown`.

---

## 8. Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Correct Astro 5 Pattern |
| :--- | :--- | :--- |
| Wrapping whole page in React/Vue | Bloats bundle, destroys Core Web Vitals | Use `.astro` layout with targeted component islands |
| Using `client:load` on below-fold UI | Triggers CPU contention during critical boot | Use `client:visible` or `client:idle` |
| Native `<img>` tags | Uncompressed formats, layout shifts (CLS) | `<Image src={...} alt="..." />` from `astro:assets` |
| Manual fetch API endpoints for forms | Fragile, no type validation, boilerplates | Type-safe `astro:actions` with Zod validation |
| Hardcoding external CMS URLs in pages | No build-time validation, breaks on API changes | Astro Content Loaders with collection schemas |

---

## 9. Offline Documentation & References

- [Welcome & Concepts](assets/welcome/why-astro.md)
- [Islands Architecture](assets/welcome/islands-architecture.md)
- [Start a Project](assets/start-a-new-project/project-structure.md)
- [Server Islands](assets/server-rendering/server-islands.md)
- [Astro Actions](assets/server-rendering/actions.md)
- [Content Collections](assets/add-content-to-your-site/content-collections.md)
- [Configuration Reference](assets/reference/configuration-reference.md)
- [Directives Reference](assets/reference/directives-reference.md)
- [Modules Reference](assets/reference/modules/astro-actions.md)
