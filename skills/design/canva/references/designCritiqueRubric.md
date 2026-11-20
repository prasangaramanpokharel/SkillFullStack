# Canva Design Critique & Visual Feedback Rubric

**Last verified:** 2026-11-20  
**Scope:** Read-only visual, typographical, structural, and accessibility evaluation of Canva designs.

---

## 1. Inspection Philosophy & Data Sources

Critiquing a design requires evaluating both programmatic content and visual rendering:

1. **Visual Grounding (`Canva:get-design-thumbnail`)**: Primary source for assessing color contrast, balance, whitespace, and graphical hierarchy.
2. **Text Copy Grounding (`Canva:get-design-content`)**: Extracts exact string contents for proofreading, brevity, and tone evaluation.
3. **Geometry Grounding (Read-Only Transaction)**: Open a transaction with `Canva:start-editing-transaction`, extract element coordinates and bounding boxes, and **always call `Canva:cancel-editing-transaction` immediately**. Never leave a transaction dangling or commit inspect-only transactions.

---

## 2. The Seven Evaluative Lenses

Assess every design systematically against these seven pillars:

### 1. Visual Hierarchy
- **Focal Point**: Does the primary element (headline, hero visual, key metric) immediately capture user attention?
- **Scale Contrast**: Is there a clear size progression (e.g. Title $36\text{pt} \rightarrow$ Subheading $24\text{pt} \rightarrow$ Body $14\text{pt}$)? Flag elements where headlines compete with subheadings.

### 2. Layout & Spacing
- **Grid Alignment**: Are text boxes, cards, and images aligned along common vertical and horizontal axes?
- **Whitespace / Breathing Room**: Are page borders crowded? Flag content encroaching within 32px of page edges.
- **Negative Space Balance**: Is visual weight distributed evenly, avoiding awkward voids or bottom-heavy clustering?

### 3. Copy & Messaging
- **Single Core Takeaway**: Does each slide or canvas convey one primary idea?
- **Conciseness & Scannability**: Can the text be skimmed in under 5 seconds? Replace dense paragraphs with bulleted takeaways.
- **Tone & Accuracy**: Identify spelling errors, awkward line wraps, orphaned words, and inconsistent grammatical voice.

### 4. Cross-Page Consistency
- **Design Tokens**: Are identical colors, font families, and corner radii maintained across multiple slides?
- **Header & Footer Anchors**: Do page titles or logos shift position from slide to slide?

### 5. Readability & Contrast
- **Text over Photography**: Never place un-scrimmed light text directly over detailed photo backgrounds. Recommend semi-transparent overlays or solid background cards.
- **Type Scale vs Medium**: For presentations, body text must be $\ge 16\text{pt}$. For mobile social posts, headlines must remain legible on 5-inch screens.

### 6. Accessibility (WCAG 2.2 AA Standards)
- **Contrast Ratios**: Normal text must achieve $\ge 4.5:1$ against backgrounds; large text ($\ge 18\text{pt}$ or bold $\ge 14\text{pt}$) must achieve $\ge 3:1$.
- **Color Independence**: Ensure information is not communicated exclusively through color (e.g. green/red indicators must have accompanied text or icons).

### 7. Fit for Purpose
- **Medium Context**: A pitch deck slide requires high scannability; an Instagram Story requires vertical 9:16 thumb-stopping focus; a technical whitepaper flyer requires dense, structured data tables.

---

## 3. Severity Categorization

Rank every observation into one of three unambiguous priority tiers:

- **🚨 [High]**: Blatant legibility failures, unreadable text-on-image, severe clipping, broken visual hierarchy, or missing CTA.
- **⚠️ [Med]**: Inconsistent spacing, competing secondary headings, repetitive phrasing, or suboptimal contrast.
- **💡 [Low]**: Minor polish items, subtle padding adjustments, trailing punctuation consistency, or optional stylistic refinements.

---

## 4. Structured Output Format

Always pair each detected flaw with an explicit, actionable remedy:

```markdown
## Design Critique — "<Design Title>" (4 Pages)

### 🎯 Top Priorities (Highest Impact)
1. **[High] Page 2 — Text Contrast Breakdown**
   *Problem:* White body text placed directly over an un-scrimmed gradient photo background.
   *Fix:* Add a 40% black background scrim or place text inside a solid `#FFFFFF` card with `#111827` text.
2. **[High] Page 1 — Competing Headlines**
   *Problem:* The subtitle is rendered in the same font size (32pt) and bold weight as the main title.
   *Fix:* Increase title to 44pt bold and drop subtitle to 20pt regular weight.

### 📄 Page-by-Page Breakdown
- **Page 1 (Cover)**:
  - [Med] Logo is placed 10px from the top edge. Increase margin to 40px for breathing room.
  - [Low] Typo: "Inovation" -> "Innovation".
- **Page 2 (Market Analysis)**:
  - [Med] 5 bullets are grouped in one massive text block. Break into 2 distinct columns.

### ✨ What's Working Well
- Strong, cohesive brand blue palette across all slides.
- Excellent high-resolution hero imagery.
```
