# Astro 5 Server Islands & Type-Safe Actions

Astro 5 introduces two transformative features for dynamic full-stack web applications:
1. **Server Islands (`server:defer`)**: Deferred dynamic rendering with static CDN caching.
2. **Astro Actions (`astro:actions`)**: End-to-end type-safe RPC endpoints for backend mutations.

---

## 1. Server Islands (`server:defer`)

### The Problem with Traditional SSR vs SSG
- **Static Site Generation (SSG)**: Blazing fast TTFB from edge CDN, but cannot personalize content (e.g. user avatar, cart count, personalized recommendations).
- **Server-Side Rendering (SSR)**: Personalized content, but TTFB is bottlenecked by the slowest database or 3rd-party API call.

### How Server Islands Solve This
Server Islands decouple static page generation from dynamic personalization. The static shell is served instantly with an empty placeholder or skeleton fallback. The server island is fetched in the background and injected into the DOM as HTML, with zero client-side React/Vue runtime required.

```astro
---
// src/pages/product/[id].astro
import ProductDetails from '../../components/ProductDetails.astro';
import DynamicPricing from '../../components/DynamicPricing.astro';
import PriceSkeleton from '../../components/PriceSkeleton.astro';

export const prerender = true; // Static CDN Cache
const { id } = Astro.params;
---

<Layout>
  <!-- Rendered statically at build time -->
  <ProductDetails productId={id} />

  <!-- Deferred server-rendered dynamic island -->
  <DynamicPricing productId={id} server:defer>
    <PriceSkeleton slot="fallback" />
  </DynamicPricing>
</Layout>
```

### Component Implementation
Inside `DynamicPricing.astro`:
```astro
---
// src/components/DynamicPricing.astro
interface Props {
  productId: string;
}

const { productId } = Astro.props;

// Access request headers, cookies, or database per-request
const currency = Astro.cookies.get('user_currency')?.value ?? 'USD';
const price = await db.fetchPrice(productId, currency);
---

<div class="pricing-badge">
  <span>{price.formatted}</span>
  <small>Includes localized tax for {currency}</small>
</div>
```

---

## 2. Astro Actions (`astro:actions`)

Astro Actions provide RPC-style type-safe server mutations without manually configuring REST or GraphQL endpoints.

### Defining Actions
Create action handlers inside `src/actions/index.ts`:

```typescript
// src/actions/index.ts
import { defineAction, ActionError } from 'astro:actions';
import { z } from 'astro:schema';

export const server = {
  createPost: defineAction({
    accept: 'form', // Accepts FormData or 'json'
    input: z.object({
      title: z.string().min(5).max(120),
      content: z.string().min(20),
      published: z.boolean().default(false),
    }),
    handler: async (input, context) => {
      // Access context.cookies, context.session, context.request
      const session = await context.session?.get('user');
      if (!session) {
        throw new ActionError({
          code: 'UNAUTHORIZED',
          message: 'You must be logged in to create a post.',
        });
      }

      try {
        const post = await db.posts.insert({
          ...input,
          authorId: session.id,
          createdAt: new Date(),
        });
        return { success: true, post };
      } catch (err) {
        throw new ActionError({
          code: 'INTERNAL_SERVER_ERROR',
          message: 'Failed to persist post to database.',
        });
      }
    },
  }),
};
```

### Consuming Actions in Pure Astro (Progressive Enhancement)
Zero client-side JavaScript required:
```astro
---
// src/pages/posts/new.astro
import { actions } from 'astro:actions';

const result = Astro.getActionResult(actions.createPost);
if (result?.data?.success) {
  return Astro.redirect(`/posts/${result.data.post.id}`);
}
---

<form method="POST" action={actions.createPost}>
  <label>
    Title
    <input type="text" name="title" required />
  </label>
  <label>
    Content
    <textarea name="content" required></textarea>
  </label>
  <button type="submit">Publish</button>

  {result?.error && (
    <div class="alert-error">
      <p>{result.error.message}</p>
      {result.error.fields && (
        <ul>
          {Object.entries(result.error.fields).map(([field, issues]) => (
            <li>{field}: {issues?.join(', ')}</li>
          ))}
        </ul>
      )}
    </div>
  )}
</form>
```

### Consuming Actions in Interactive Client Islands
Directly invoke actions with end-to-end type safety:
```tsx
// src/components/NewPostForm.tsx
import React, { useState } from 'react';
import { actions } from 'astro:actions';

export function NewPostForm() {
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg(null);

    const formData = new FormData(e.currentTarget);
    const { data, error } = await actions.createPost(formData);

    setLoading(false);
    if (error) {
      setErrorMsg(error.message);
    } else {
      window.location.href = `/posts/${data.post.id}`;
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {errorMsg && <p className="error">{errorMsg}</p>}
      <button type="submit" disabled={loading}>
        {loading ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```
