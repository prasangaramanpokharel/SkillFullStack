# Canva Transactional Editing Engine

**Last verified:** 2026-11-20  
**Scope:** Programmatic mutation of existing Canva designs with atomic transaction guarantees.

---

## 1. The Atomic Transaction Lifecycle

Mutating a Canva design is strictly transactional. Draft mutations live in an isolated buffer and **never affect the production design** until committed. If an operation fails, the session is cancelled, or the user rejects the preview, the draft is cleanly discarded.

```
                    ┌──────────────────────────────┐
                    │ Canva:resolve-shortlink / ID │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ Canva:start-editing-transaction
                    │ (captures transaction_id &  │
                    │  pages array)                │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ Canva:perform-editing-operations
                    │ (batched JSON operations)    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                      [User Visual Approval Gate]
                                  / \
                        Approved /   \ Rejected / Failed
                                /     \
                               ▼       ▼
    ┌─────────────────────────────┐  ┌─────────────────────────────┐
    │ Canva:commit-editing-trans. │  │ Canva:cancel-editing-trans. │
    │ (draft merged to design)    │  │ (draft cleanly discarded)   │
    └─────────────────────────────┘  └─────────────────────────────┘
```

---

## 2. Supported vs Unsupported Operations (CAN vs CANNOT)

The Canva Editing API has strict deterministic boundaries. Violating these boundaries causes request rejections.

### ✅ Supported Operations (`perform-editing-operations`)

| Domain | Operation Name | Description & Parameters |
| :--- | :--- | :--- |
| **Text Content** | `replace_text` | Replaces full text string inside target element (`element_id`, `text`) |
| | `find_and_replace_text` | Substring substitution across element or page (`find_text`, `replace_text`) |
| **Text Styling** | `format_text` | Mutates font size, font weight (`bold`/`normal`), font style (`italic`/`normal`), color (hex), text alignment (`left`/`center`/`right`/`justify`), line height, text decoration (`underline`/`none`), strikethrough, lists (`bullet`/`ordered`), and hyperlink URLs |
| **Media Elements**| `update_fill` | Swaps an existing image or video fill with a new asset (`asset_id`) |
| | `insert_fill` | Places a new image/video element into a target bounding box |
| | `delete_element` | Removes an element from the canvas by `element_id` |
| **Layout & Sizing**| `position_element` | Adjusts `x` and `y` coordinates relative to page origin |
| | `resize_element` | Adjusts `width` and `height` dimensions |
| **Metadata** | `update_title` | Updates the document title in Canva |
| **Autofill Keys** | `update_autofill_field`| Updates field dataset mappings (fixed-layout pages only) |

### ❌ Unsupported Operations (Strict CANNOT List)

1. **Font Family / Typeface**: The API cannot change font families (e.g. from *Arial* to *Montserrat* or *Inter*). Only size, weight, and style can be edited.
2. **New Text Elements**: The API cannot create brand-new text boxes from scratch (only media fills can be inserted). To modify text, you must target an existing `element_id`.
3. **Backgrounds & Gradients**: Background canvas colors, patterns, and gradients cannot be manipulated via API.
4. **Page Topology**: Pages cannot be added, deleted, cloned, or re-ordered through the editing transaction.
5. **Shape Properties**: Vector paths, shape border radii, stroke weights, and fill colors of geometric shapes cannot be modified (only text inside shapes is editable).
6. **Opacity & Animations**: Existing element opacity and canvas transition timings are immutable.

> [!TIP]
> When a user request requires an unsupported operation, never attempt fragile workarounds. Classify the item immediately as a **Manual Action** and provide step-by-step instructions for the Canva editor UI.

---

## 3. Responsive Pages Protocol (`is_responsive: true`)

Some Canva designs (especially modern presentation templates, docs, and responsive sites) contain pages with responsive reflow enabled.

### Verification Rule
Always inspect the `pages` array returned by `start-editing-transaction`:
```json
{
  "page_index": 0,
  "is_responsive": true
}
```

### Allowed Operations on Responsive Pages:
On responsive pages, **ONLY** the following 5 operations are allowed:
1. `update_title`
2. `replace_text`
3. `find_and_replace_text`
4. `update_fill`
5. `delete_element`

**Forbidden on Responsive Pages**:
- `format_text` (font size, weight, line height)
- `position_element` (x/y coordinates)
- `resize_element` (width/height)
- `insert_fill`

If an unsupported operation is attempted on a responsive page, abort that operation and inform the user that responsive reflow manages those attributes automatically.

---

## 4. Batched Execution & Payload Construction

Never issue individual operations one-by-one. Batch all operations for a transaction into a single `perform-editing-operations` request.

### Example Batched Payload

```json
{
  "transaction_id": "tx_9876543210abcdef",
  "page_index": 0,
  "pages": [
    {
      "page_index": 0,
      "is_responsive": false
    }
  ],
  "operations": [
    {
      "type": "replace_text",
      "element_id": "elem_heading_01",
      "text": "Q3 2026 Financial Strategy"
    },
    {
      "type": "format_text",
      "element_id": "elem_heading_01",
      "format": {
        "color": "#0B5CD7",
        "font_weight": "bold",
        "font_size": 48
      }
    },
    {
      "type": "update_fill",
      "element_id": "elem_hero_photo",
      "asset_id": "asset_abc12345"
    },
    {
      "type": "delete_element",
      "element_id": "elem_deprecated_badge"
    }
  ]
}
```

---

## 5. The Commit Approval Gate

Committing is permanent and cannot be undone via API:

1. **Show Preview**: Present the updated thumbnail returned by `perform-editing-operations`.
2. **Enumerate Changes**: List every modified element and the before/after values.
3. **Explicit Consent**: Require unambiguous user confirmation before invoking `commit-editing-transaction`.
4. **Link Sharing**: Upon successful commit, present the direct Canva edit link (`https://www.canva.com/design/<id>/edit`).
