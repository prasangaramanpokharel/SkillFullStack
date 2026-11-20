# Brand Kit Verification & Governance Rubric

**Last verified:** 2026-11-20  
**Scope:** Automated & visual auditing of Canva designs against organizational brand kits and style guidelines.

---

## 1. The Brand-Kit Data Gap Architecture

When querying brand kits via `Canva:list-brand-kits`, the response typically provides **kit IDs, names, and visual thumbnails**, but machine-readable hex values and font family manifests may be omitted depending on organization permission scopes.

Similarly, `Canva:get-design-content` extracts raw strings (`richtexts`), while transactional inspection exposes bounding boxes and sizes, but frequently omits explicit font faces and fill colors.

### The Hybrid Verification Protocol

```
                        ┌───────────────────────────────┐
                        │   Canva:list-brand-kits       │
                        └──────────────┬────────────────┘
                                       │
                      Does kit payload contain hex/fonts?
                                      / \
                                Yes  /   \  No (Data Gap)
                                    /     \
                                   ▼       ▼
┌──────────────────────────────────────┐ ┌──────────────────────────────────────┐
│        Deterministic Mode            │ │          Visual Hybrid Mode          │
│ Exact hex code & font family matching│ │ 1. Design thumbnail vs. Kit preview │
│ via parsed attributes                │ │ 2. Prompt user for primary palette   │
│                                      │ │    and font families                 │
└──────────────────────────────────────┘ └──────────────────────────────────────┘
```

> [!IMPORTANT]
> Never invent or hallucinate brand colors or font names. If hex codes or font families are not returned in the payload or provided by the user, mark that attribute as **Can't verify** with an explicit request for developer input.

---

## 2. Five-Dimension Evaluation Rubric

Every design is audited across five core dimensions with a three-tier status: **On brand**, **Off brand**, or **Can't verify**.

### 1. Color Palette Governance
- **Primary & Secondary Fills**: Are background, card, and shape fills restricted to approved brand tokens?
- **Text & Accent Contrast**: Are headings, links, and CTAs utilizing approved accent hues?
- **Deviation Flagging**: Identify offending hex codes (e.g., `#1A73E8`) and calculate the nearest valid brand alternative (e.g., `#0B5CD7`).

### 2. Typography Hierarchy
- **Typeface Families**: Do heading, subheading, and body elements match the brand typography guidelines (e.g., *Inter*, *Cabinet Grotesk*, *Space Grotesk*)?
- **Hierarchy & Scale**: Are font sizes, weights, and line-heights applied consistently across slides/pages?

### 3. Logo Placement & Integrity
- **Presence & Lockup**: Is the official logo present on title, closing, or campaign hero placements?
- **Aspect Ratio & Clearspace**: Verify via thumbnail inspection that the logo is not horizontally stretched, vertically squished, recolored into non-brand tints, or crowded by adjacent text.

### 4. Tone of Voice & Copy Standards
- **Messaging Alignment**: Does the written copy match the brand tone (e.g., concise, authoritative, engineering-focused, playful)?
- **Vocabulary & Jargon**: Flag banned terms, outdated product naming, or grammatical typos.

### 5. Multi-Page Visual Consistency
- **Cross-Slide Cohesion**: Are margins, gutters, header positions, and badge styles identical across all pages?
- **Component Uniformity**: Are buttons and visual motifs styled identically throughout the presentation?

---

## 3. Standardized Audit Report Format

When delivering audit results, use the standardized format:

```markdown
## Brand Check — "<Design Title>" vs "<Brand Kit Name>"

**Overall Verdict:** ⚠️ Mostly on brand (3 issues detected)

### 🚨 Off brand (Action Required)
- **[Color - High]** Page 2 heading uses `#1A73E8` — not present in brand palette.
  *Remediation:* Replace with primary brand blue `#0B5CD7`.
- **[Typography - Med]** Page 4 body paragraph appears in *Arial*; brand guideline mandates *Inter*.
  *Remediation:* Requires manual font update in Canva editor (API cannot mutate typeface).
- **[Logo - High]** Page 1 logo clearspace is infringed by subtitle text box.
  *Remediation:* Shift subtitle down 24px via `/canva-edit`.

### ❓ Can't verify (User Input Needed)
- Brand kit API did not expose secondary accent hex codes. Please provide hex codes for verification.

### ✅ On brand
- Primary logo mark matches official SVG vector lockup.
- Margin padding (48px) and grid structure are consistent across pages 1–6.
- Copy tone conforms to technical developer documentation standards.
```

---

## 4. Remediation Dispatch

Following the audit report:
1. **API-Fixable Issues**: Offer to resolve immediately via `/canva-edit` (text color, sizing, position, media swap).
2. **Manual Canva UI Actions**: List issues that require manual editor action (font family replacement, canvas background colors).
