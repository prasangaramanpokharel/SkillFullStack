# Dynamic Skill Rule Deconstruction

To compliance-audit any skill in the catalog, the agent dynamically parses the target skill's `SKILL.md` and reference guides into concrete verification rules.

---

## 1. Rule Extraction Sources in a Skill

1. **YAML Frontmatter**:
   - `compatibility`: Runtime and tool versions that must be adhered to.
   - `slash-commands`: Specific task commands and flags.
2. **Anti-Patterns Table**:
   - Converts the "Anti-Pattern" column into prohibited static patterns.
   - Converts the "Correct Modern Standard" column into required invariants.
3. **Core Architectural Guidelines**:
   - Boundary rules (e.g. `server-only`, Data Access Layer, parameterized queries).
   - Typing constraints (e.g. strict TypeScript, no `any`).
   - Security prerequisites (e.g. anonymous principal rejection, CSP headers).

---

## 2. Rule Deconstruction Example: `nextjs` Skill

| Extracted Rule ID | Category | Target Selector | Forbidden Pattern | Required Compliant Invariant |
| :--- | :--- | :--- | :--- | :--- |
| `NX-01` | Architecture | `app/**/*` | Top-level `"use client"` in layout or data fetchers | Server Components by default; push `"use client"` to leaves |
| `NX-02` | Security | `app/api/**/*`, `dal/**/*` | Direct DB queries without DAL or `server-only` | Enforce `import 'server-only'` in data access files |
| `NX-03` | Caching | `app/**/*` | Legacy `unstable_cache` or unkeyed cache | Modern `"use cache"` directive with cacheLife/cacheTag |
| `NX-04` | Navigation | `components/**/*.tsx` | Standard `<a href="...">` | Next.js `<Link href="...">` |
