# Canva REST API Designs & Editing Operations

## Design Retrieval
```bash
# Retrieve design metadata
canva api designs get --design-id DABcd1234ef

# Search designs by name
canva api designs list --query "Q3 Strategy Presentation"
```

## Editing Operations Specification

### 1. `replace_text`
Replaces the entire string contents of a targeted text element.
```json
{
  "type": "replace_text",
  "element_id": "elem_h1_title",
  "text": "Enterprise Cloud Architecture"
}
```

### 2. `find_and_replace_text`
Performs targeted substring replacement across text elements.
```json
{
  "type": "find_and_replace_text",
  "find_text": "2025",
  "replace_text": "2026"
}
```

### 3. `format_text`
Applies typographic and styling changes to target text.
```json
{
  "type": "format_text",
  "element_id": "elem_h1_title",
  "format": {
    "font_size": 42.0,
    "font_weight": "bold",
    "font_style": "normal",
    "color": "#0B5CD7",
    "alignment": "left",
    "line_height": 1.2
  }
}
```

### 4. `update_fill`
Replaces the asset fill of a photo or video container.
```json
{
  "type": "update_fill",
  "element_id": "elem_hero_banner",
  "asset_id": "Msd98234-asset"
}
```

### 5. `position_element` & `resize_element`
Adjusts coordinates and bounding box dimensions.
```json
{
  "type": "position_element",
  "element_id": "elem_cta_button",
  "top": 450.0,
  "left": 120.0
}
```
