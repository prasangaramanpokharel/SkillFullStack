# Astro Content Collections & Content Layer Architecture

Astro Content Collections provide a robust, build-time validated data management system for Markdown, MDX, JSON, YAML, and remote headless CMS data.

---

## 1. Content Layer Overview (Astro 5)

In Astro 5, Content Collections utilize the unified **Content Layer API**. Collections can be populated from:
1. **Local Files**: Markdown (`.md`), MDX (`.mdx`), JSON, and YAML files using the `glob()` loader.
2. **Remote Data**: Headless CMSs (Contentful, Sanity, Strapi), database queries, or REST APIs using custom or official loaders (e.g. `feedLoader`, `gitHubLoader`).

---

## 2. Defining Schemas (`src/content.config.ts`)

Schemas ensure every content entry matches strict validation rules during `astro build`.

```typescript
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

// 1. Markdown/MDX Blog Collection
const blog = defineCollection({
  loader: glob({ pattern: '**/[^_]*.{md,mdx}', base: './src/data/blog' }),
  schema: ({ image }) =>
    z.object({
      title: z.string().max(100),
      description: z.string(),
      pubDate: z.coerce.date(),
      updatedDate: z.coerce.date().optional(),
      draft: z.boolean().default(false),
      featured: z.boolean().default(false),
      author: z.string(),
      coverImage: image(), // Validates local image paths and exposes optimized dimensions
      tags: z.array(z.string()).min(1),
    }),
});

// 2. Structured JSON Documentation Collection
const docs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/data/docs' }),
  schema: z.object({
    title: z.string(),
    section: z.enum(['getting-started', 'guides', 'api-reference']),
    order: z.number().int(),
  }),
});

// Export all collections
export const collections = { blog, docs };
```

---

## 3. Querying Collections

Astro provides type-safe utility functions via `astro:content`:

### `getCollection()`
Retrieves all entries in a collection with optional filter predicates:
```astro
---
// src/pages/blog/index.astro
import { getCollection } from 'astro:content';

// Fetch non-draft posts sorted by date
const posts = await getCollection('blog', ({ data }) => !data.draft);
posts.sort((a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime());
---

<Layout title="Engineering Blog">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    {posts.map((post) => (
      <article>
        <h2>{post.data.title}</h2>
        <p>{post.data.description}</p>
        <a href={`/blog/${post.id}/`}>Read post</a>
      </article>
    ))}
  </div>
</Layout>
```

### `getEntry()`
Retrieves a single entry by its collection name and ID:
```astro
---
// src/pages/about.astro
import { getEntry } from 'astro:content';

const aboutPage = await getEntry('pages', 'about');
if (!aboutPage) {
  return Astro.redirect('/404');
}

const { Content } = await aboutPage.render();
---

<Layout title={aboutPage.data.title}>
  <Content />
</Layout>
```

---

## 4. Dynamic Routing with `getStaticPaths()`

Generate static HTML pages for all collection entries during build:

```astro
---
// src/pages/blog/[...slug].astro
import { getCollection, render } from 'astro:content';
import { Image } from 'astro:assets';
import BaseLayout from '../../layouts/BaseLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.id },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content, headings } = await render(post);
---

<BaseLayout title={post.data.title} description={post.data.description}>
  <article class="prose max-w-3xl mx-auto py-8">
    <Image src={post.data.coverImage} alt={post.data.title} width={1200} height={630} />
    <h1>{post.data.title}</h1>
    <time datetime={post.data.pubDate.toISOString()}>
      {post.data.pubDate.toLocaleDateString('en-US', { dateStyle: 'long' })}
    </time>
    
    <!-- Render compiled Markdown/MDX content -->
    <Content />
  </article>
</BaseLayout>
```

---

## 5. Local Image Optimization with Content Collections

When using `({ image }) => z.object({ coverImage: image() })`, Astro validates that the referenced image exists at compile time. It automatically derives width, height, and format, allowing seamless integration with `<Image />`:

```astro
---
import { Image } from 'astro:assets';
---
<!-- Outputs WebP/AVIF with precise intrinsic aspect ratio to prevent CLS -->
<Image
  src={post.data.coverImage}
  alt={post.data.title}
  widths={[400, 800, 1200]}
  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 800px"
  loading="lazy"
  decoding="async"
/>
```
