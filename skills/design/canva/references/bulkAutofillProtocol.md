# Canva Bulk Autofill Protocol (One Design Per Row)

**Last verified:** 2026-11-20  
**Scope:** Automated batch generation of unique Canva designs from tabular datasets using Brand Templates.

---

## 1. Prerequisites & Architectural Constraints

- **Subscription Requirement**: Canva Autofill API features require an active Canva Enterprise account.
- **Sequential Execution**: All row iterations **MUST be executed sequentially**, never in concurrent unthrottled batches. Unthrottled calls risk HTTP 429 rate limits and make error tracking opaque.
- **No Undo Mechanism**: Creating designs produces permanent documents in the user's workspace. Always require pre-flight verification on batches $> 10$ rows.

---

## 2. Ingestion & Pre-flight Inspection

### Supported Input Modalities
1. **Local Files**: `.csv`, `.tsv`, `.json` uploaded or located in the workspace.
2. **Pasted Data**: Markdown tables, tab-delimited text, or raw JSON arrays pasted directly into chat.
3. **Remote URLs**: HTTP/HTTPS endpoints delivering CSV or JSON payloads.

### Normalization Step
Parse rows into an array of uniform dictionary objects:
```json
[
  { "sku": "PROD-001", "name": "Titanium Wireless Earbuds", "price": "$129.00", "image_url": "https://cdn.example.com/earbuds.jpg" },
  { "sku": "PROD-002", "name": "Noise-Cancelling Headphones", "price": "$299.00", "image_url": "https://cdn.example.com/headphones.jpg" }
]
```

---

## 3. Brand Template Schema Inspection

Query the target brand template to inspect its expected data tags:

```
Canva:get-brand-template-dataset  template_id="DABxxx_template"
```

The response exposes expected fields and types (`text`, `image`, `chart`):

```json
{
  "dataset": {
    "product_name": { "type": "text" },
    "unit_price": { "type": "text" },
    "hero_photo": { "type": "image" }
  }
}
```

---

## 4. Column-to-Field Mapping Matrix

Perform case-insensitive, fuzzy matching between parsed input columns and template fields:

| Template Field | Field Type | Matched Column | Mapping Status | Action / Notes |
| :--- | :--- | :--- | :--- | :--- |
| `product_name` | `text` | `name` | ✅ Auto-matched | Direct text insertion |
| `unit_price` | `text` | `price` | ✅ Auto-matched | Currency string preservation |
| `hero_photo` | `image` | `image_url` | 🔄 Pattern B (URL) | Requires pre-upload to Canva Asset Library |
| `disclaimer` | `text` | *(none)* | ⚠️ Unmatched | Omitted; template default text retained |

---

## 5. Image Field Resolution Patterns

Image fields cannot directly accept external URLs in the `autofill-design` payload. Apply one of three patterns:

### Pattern A: Direct Canva Asset ID
When the dataset column already contains Canva asset identifiers (e.g. `asset_98765`):
```json
{
  "hero_photo": {
    "type": "image",
    "asset_id": "asset_98765"
  }
}
```

### Pattern B: Remote Image URL Pre-Upload
When the dataset provides external image URLs:
1. Immediately before creating that row's design, invoke:
   ```
   Canva:upload-asset-from-url  url="https://cdn.example.com/photo.jpg"  name="autofill_hero_PROD-001"
   ```
2. Extract the returned `asset_id`.
3. Pass `asset_id` into the `autofill-design` call.
*Benefit: If one image URL fails to download, only that specific row fails; the rest of the batch continues.*

### Pattern C: Missing or Null Image Column
If no image column exists in the dataset:
- Prompt user whether to keep the default template placeholder or abort.
- If keeping default, cleanly omit the image key from the `data` payload.

---

## 6. Sequential Batch Generation Loop

```python
results = []
for index, row in enumerate(dataset_rows, start=1):
    # 1. Skip completely empty rows
    if not any(row.values()):
        results.append({"row": index, "status": "skipped", "reason": "empty_row"})
        continue

    # 2. Upload remote images if Pattern B
    asset_id = None
    if row.get("image_url"):
        upload_job = upload_asset_from_url(url=row["image_url"], name=f"batch_img_{index}")
        asset_id = upload_job.asset_id

    # 3. Assemble autofill payload
    payload = {
        "product_name": {"type": "text", "text": str(row["name"])},
        "unit_price": {"type": "text", "text": str(row["price"])}
    }
    if asset_id:
        payload["hero_photo"] = {"type": "image", "asset_id": asset_id}

    # 4. Trigger single autofill creation
    title = f"Campaign Variant - Row {index} - {row.get('name', 'Item')}"
    response = autofill_design(template_id=template_id, title=title, data=payload)

    # 5. Record result
    results.append({
        "row": index,
        "status": "success" if response.ok else "failed",
        "design_id": response.design_id,
        "edit_url": response.edit_url,
        "error": response.error
    })
```

---

## 7. Batch Completion Summary Report

Summarize the batch execution in tabular format:

```markdown
## Bulk Generation Summary

- **Total Rows Processed:** 24
- **Successfully Created:** 23
- **Failed / Skipped:** 1

| Row | Identifier | Status | Generated Design | Notes / Error |
| :---: | :--- | :--- | :--- | :--- |
| 1 | PROD-001 | ✅ Success | [Edit in Canva](https://www.canva.com/design/DAG.../edit) | Hero photo uploaded |
| 2 | PROD-002 | ✅ Success | [Edit in Canva](https://www.canva.com/design/DAG.../edit) | Hero photo uploaded |
| 3 | PROD-003 | ❌ Failed | — | Image URL returned HTTP 404 |
```
