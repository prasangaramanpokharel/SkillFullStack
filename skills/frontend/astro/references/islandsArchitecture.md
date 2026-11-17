# Astro Islands Architecture Deep Dive

The **Islands Architecture** (coined by L. Dover and pioneered by Astro) represents a fundamental paradigm shift from traditional Single Page Application (SPA) architectures and monolithic Server-Side Rendering (SSR) frameworks.

---

## 1. Traditional SPAs vs Monolithic SSR vs Astro Islands

| Architecture | HTML Payload | Client-Side JS Runtime | Hydration Strategy | Time to Interactive (TTI) |
| :--- | :--- | :--- | :--- | :--- |
| **Traditional SPA** (Vite / CRA) | Empty `div#root` shell | Entire application bundle | Full client-side render | Slow (Waits for all JS) |
| **Monolithic SSR** (Next.js / Nuxt) | Full pre-rendered HTML | Entire application bundle | Full page hydration | Moderate to Slow (Main-thread lockup) |
| **Astro Islands** | Full pre-rendered HTML | **Only interactive islands** | Independent, surgical hydration | **Instant (Zero JS baseline)** |

---

## 2. Anatomy of an Astro Island

In Astro, the default component extension is `.astro`. Astro components run **only during build or request time on the server**. Their output is pure HTML and scoped CSS.

When interactive state or browser events (`onClick`, `useState`, `createSignal`) are required, an interactive UI component (React, Preact, Svelte, Vue, Solid, Web Components) is embedded inside an `.astro` template with a `client:*` directive.

```astro
---
// Server-Side Frontmatter (Runs on Node/Edge/Build)
import StaticHero from '../components/StaticHero.astro';
import StaticFooter from '../components/StaticFooter.astro';

import InteractiveSearch from '../components/SearchModal.tsx'; // React
import InteractiveCart from '../components/CartWidget.svelte'; // Svelte
import InteractiveThemeToggle from '../components/ThemeToggle.vue'; // Vue
---

<html lang="en">
  <head>
    <title>Astro Multi-Framework Islands</title>
  </head>
  <body>
    <!-- 0 KB JavaScript -->
    <StaticHero />

    <!-- React Island hydrated when idle -->
    <InteractiveSearch client:idle />

    <!-- Svelte Island hydrated immediately for shopping cart -->
    <InteractiveCart client:load />

    <!-- Vue Island hydrated only when scrolled into view -->
    <InteractiveThemeToggle client:visible />

    <!-- 0 KB JavaScript -->
    <StaticFooter />
  </body>
</html>
```

---

## 3. Hydration Directives Reference

### `client:load`
- **When to use**: High-priority interactive elements immediately visible above the fold that the user might interact with in the first millisecond (e.g. global search input, primary mobile navigation drawer).
- **Execution**: Hydrated as soon as the JavaScript bundle arrives.

### `client:idle`
- **When to use**: Lower priority interactive elements that do not block initial rendering or critical user actions (e.g. newsletter signups, notifications banner, dark/light theme switchers).
- **Execution**: Uses `requestIdleCallback` to defer hydration until the main browser thread is idle.

### `client:visible`
- **When to use**: Any below-the-fold interactive component (e.g. image carousel, user review accordion, embedded video player, complex interactive charts).
- **Execution**: Uses an internal `IntersectionObserver` instance. JavaScript is not loaded or executed until the element scrolls into view.

### `client:media="(media query)"`
- **When to use**: Components that are only functional or visible at certain viewport dimensions (e.g. mobile drawer menu on `(max-width: 768px)`, desktop mega menu on `(min-width: 1024px)`).
- **Execution**: Uses `window.matchMedia`. If the query does not match, zero JavaScript is fetched.

### `client:only="framework"`
- **When to use**: Components that cannot run on the server because they depend strictly on browser-only APIs (WebGL, Canvas, `navigator.bluetooth`, Web Audio, local storage synchronization).
- **Execution**: Skips server-side rendering entirely and renders only on the client.

---

## 4. Multi-Framework Interoperability & State Sharing

Astro enables multi-framework composition on the same page. To share state between independent islands across different frameworks (e.g. a React Cart button updating from a Svelte Product card), use lightweight framework-agnostic stores like **Nanostores**:

```typescript
// src/stores/cartStore.ts
import { atom, map } from 'nanostores';

export interface CartItem {
  id: string;
  name: string;
  price: number;
}

export const $cart = map<Record<string, CartItem>>({});

export function addToCart(item: CartItem) {
  const existing = $cart.get()[item.id];
  $cart.setKey(item.id, item);
}
```

In a Svelte Island:
```svelte
<!-- src/components/AddToCart.svelte -->
<script>
  import { addToCart } from '../stores/cartStore';
  export let product;
</script>

<button on:click={() => addToCart(product)}>Add to Cart</button>
```

In a React Island:
```tsx
// src/components/CartCounter.tsx
import { useStore } from '@nanostores/react';
import { $cart } from '../stores/cartStore';

export function CartCounter() {
  const cart = useStore($cart);
  const count = Object.keys(cart).length;

  return <span className="cart-badge">{count}</span>;
}
```
