# Social Media Channel Formats & Creative Resize Matrix

**Last verified:** 2026-11-20  
**Review Cadence:** Every 90 days or upon social platform advertising spec updates.  
**Scope:** Automated cross-platform canvas resizing and dimension resolution from master creative assets.

---

## 1. Automated Dimension Resolution Hierarchy

When a user requests resizing for social media, determine the target dimensions using this deterministic 5-step hierarchy:

1. **Exact Pixels Provided**: If user specifies exact dimensions (e.g. `1080x1080`), use only those dimensions.
2. **Platform + Placement Named**: If user specifies a platform and placement (e.g. "Instagram Story" or "Pinterest Pin"), lookup the exact canvas in **Section 4 (Platform & Placement Lookup)**.
3. **Aspect Ratio Named**: If user specifies an aspect ratio without pixels (e.g. `9:16`, `4:5`, `1:1`, `16:9`), lookup the canvas in **Section 3 (Aspect-Ratio Set)**.
4. **Generic "All Channels / Platform-Ready"**: If user asks for "each channel", "all platforms", or "social media variants" without naming specific placements, use **Section 2 (Default Channel Set)**. Do not prompt for placement clarification.
5. **Generic "Common Formats / Social Versions"**: If user asks for "social versions" or "common aspect ratios", use **Section 3 (Aspect-Ratio Set)**.

> [!NOTE]
> When one single platform is named without a placement (e.g. *"Resize this for Facebook"*), ask which specific placement is required (Feed portrait vs Story vs Link landscape). When all platforms are requested, apply Rule 4 directly.

---

## 2. Default Channel Set

Preferred canonical placements covering all major networks. Exact duplicate and near-duplicate canvases are consolidated:
- LinkedIn landscape (1200 × 627), X landscape (1200 × 628), and Facebook link image (1200 × 630) are consolidated into **1200 × 627** on generic requests, labeled for all three platforms.

| Target Placements Covered | Canvas Dimensions | Aspect Ratio | Primary Use Case |
| :--- | :---: | :---: | :--- |
| **TikTok vertical, Instagram Story / Reel, Facebook Story / Reel, YouTube Short** | `1080 × 1920` | 9:16 | Fullscreen mobile vertical video / carousel |
| **Instagram Feed portrait, Facebook Feed portrait** | `1080 × 1350` | 4:5 | High-engagement mobile feed card |
| **LinkedIn single-image landscape, X image landscape, Facebook link image** | `1200 × 627` | ~1.91:1 | Desktop & mobile desktop feed link banners |
| **YouTube standard video** | `1920 × 1080` | 16:9 | Horizontal video, presentation screens, web hero |

---

## 3. Aspect-Ratio Set

Standardized ratio configurations used when requests specify ratios rather than networks:

| Ratio | Canvas Dimensions | Orientation | Typical Placement |
| :---: | :---: | :---: | :--- |
| **9:16** | `1080 × 1920` | Vertical | Stories, Reels, TikTok, Shorts |
| **4:5** | `1080 × 1350` | Portrait | Instagram & Facebook Feed Posts |
| **1:1** | `1080 × 1080` | Square | Universal Feed Post, Carousel Cards |
| **16:9** | `1920 × 1080` | Landscape | YouTube, LinkedIn banners, Presentation decks |

---

## 4. Platform and Placement Lookup Table

Authoritative specifications when specific platforms and placements are requested:

| Platform | Specific Placement | Canvas Dimensions | Aspect Ratio |
| :--- | :--- | :---: | :---: |
| **Instagram** | Feed Portrait | `1080 × 1350` | 4:5 |
| **Instagram** | Feed Square | `1080 × 1080` | 1:1 |
| **Instagram** | Story / Reel | `1080 × 1920` | 9:16 |
| **TikTok** | Vertical Video / Ad | `1080 × 1920` | 9:16 |
| **LinkedIn** | Single-image Landscape | `1200 × 627` | 1.91:1 |
| **LinkedIn** | Single-image Square | `1200 × 1200` | 1:1 |
| **X (Twitter)** | Image Landscape | `1200 × 628` | 1.91:1 |
| **X (Twitter)** | Image Square | `1200 × 1200` | 1:1 |
| **Pinterest** | Standard Pin | `1000 × 1500` | 2:3 |
| **YouTube** | Short | `1080 × 1920` | 9:16 |
| **YouTube** | Standard Video Thumbnail / Video | `1920 × 1080` | 16:9 |
| **Facebook** | Feed Portrait | `1080 × 1350` | 4:5 |
| **Facebook** | Feed Square | `1080 × 1080` | 1:1 |
| **Facebook** | Story / Reel | `1080 × 1920` | 9:16 |
| **Facebook** | Link Image / Ad Landscape | `1200 × 630` | 1.91:1 |

---

## 5. Resize Invocation & Parallel Execution

Call `Canva:resize-design` for each unique width × height canvas:

```json
{
  "design_id": "DAGfA-xxxxxx",
  "design_type": {
    "type": "custom",
    "width": 1080,
    "height": 1920
  },
  "user_intent": "Resize master flyer to vertical 9:16 story variant"
}
```

### Response Parsing & Output Presentation
Consolidate results into a clean markdown summary table:

| Requested Placement(s) | Canvas | Status | Thumbnail | Direct Canva Edit Link |
| :--- | :---: | :---: | :---: | :--- |
| **Instagram Story, TikTok, YouTube Short** | `1080 × 1920` | ✅ Created | ![Preview](https://...) | [Open in Canva Editor](https://www.canva.com/design/DAG.../edit) |
| **Instagram Feed Portrait** | `1080 × 1350` | ✅ Created | ![Preview](https://...) | [Open in Canva Editor](https://www.canva.com/design/DAG.../edit) |
| **LinkedIn / X Landscape Banner** | `1200 × 627` | ✅ Created | ![Preview](https://...) | [Open in Canva Editor](https://www.canva.com/design/DAG.../edit) |
| **YouTube Standard Video** | `1920 × 1080` | ✅ Created | ![Preview](https://...) | [Open in Canva Editor](https://www.canva.com/design/DAG.../edit) |
