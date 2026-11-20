# Canva MCP Server Tool Contracts (`canva_canva`)

The Canva Model Context Protocol (MCP) server allows AI agents in Antigravity, Claude Code, and Cursor to directly interact with Canva resources.

## Tool Contracts

### 1. `Canva:resolve-shortlink`
- Resolves shortened `canva.link/...` URLs into fully qualified Canva design URLs.
- **Parameters**: `url` (string, required)

### 2. `Canva:get-design`
- Fetches metadata, page count, and edit/view URLs for a design ID.
- **Parameters**: `design_id` (string, required)

### 3. `Canva:get-design-content`
- Extracts all text (`richtexts`) across slides.
- **Parameters**: `design_id` (string, required)

### 4. `Canva:get-design-thumbnail`
- Fetches pre-rendered JPEG/PNG image thumbnails of design slides.
- **Parameters**: `design_id` (string, required)

### 5. `Canva:start-editing-transaction`
- Opens an isolated drafting session for atomic design mutations.
- **Parameters**: `design_id` (string, required)
- **Returns**: `transaction_id`, `pages` array

### 6. `Canva:perform-editing-operations`
- Applies batched mutations to the draft canvas.
- **Parameters**: `transaction_id` (string), `pages` (array), `page_index` (integer), `operations` (array)

### 7. `Canva:commit-editing-transaction`
- Merges draft modifications into the live production design.
- **Parameters**: `transaction_id` (string, required)

### 8. `Canva:cancel-editing-transaction`
- Safely discards draft changes without affecting live design.
- **Parameters**: `transaction_id` (string, required)

### 9. `Canva:autofill-design`
- Batch-generates a single design by binding data to a Brand Template.
- **Parameters**: `template_id` (string), `data` (object), `title` (string)

### 10. `Canva:resize-design`
- Creates an adapted variant of an existing design at targeted pixel dimensions.
- **Parameters**: `design_id` (string), `design_type` (object with `width`, `height`), `user_intent` (string)
