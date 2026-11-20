# Feedback Triage & Comment Resolution Protocol

**Last verified:** 2026-11-20  
**Scope:** Automated extraction, categorization, batch resolution, and comment replies for stakeholder review threads on Canva designs.

---

## 1. Core Operating Philosophy: "Feedback to Finished"

When stakeholders leave comments across slides in a Canva design, the goal is to drive the design to completion with minimal developer friction:
1. Extract all comment threads and replies.
2. Triage every comment into **Actionable**, **Requires Manual Action**, or **Resolved**.
3. Formulate a unified execution plan and obtain user approval **EXACTLY ONCE**.
4. Execute mutations in a single batched transaction and auto-commit immediately.
5. Post polite status replies to comment threads to close the review loop.
6. Present a clean manual action checklist for any unsupported operations.

---

## 2. Three-Tier Feedback Triage Matrix

```
                          ┌───────────────────────────┐
                          │   Canva:list-comments     │
                          │   Canva:list-replies      │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                         Does comment request changes?
                                       / \
                                  No  /   \  Yes
                                     /     \
                                    ▼       ▼
                       ┌────────────────┐  Is request supported by
                       │    Resolved    │  Canva Editing API?
                       │ (LGTM, thumbs) │            / \
                       └────────────────┘     Yes   /   \  No
                                                   /     \
                                                  ▼       ▼
                                        ┌────────────┐ ┌────────────────────┐
                                        │ Actionable │ │ Requires Manual    │
                                        │ (Mutate)   │ │ Action (Checklist) │
                                        └────────────┘ └────────────────────┘
```

### 1. Actionable (API-Supported Mutations)
Comments requesting modifications that map to valid Canva operations:
- Text string replacements, copy rewrites, punchier phrasing, typo fixes (`replace_text`, `find_and_replace_text`).
- Font sizing, bold/italic weighting, color swaps, line spacing, text alignment (`format_text`).
- Replacing existing placeholder images with new assets (`update_fill`).
- Repositioning or resizing existing elements (`position_element`, `resize_element`).
- Deleting obsolete elements or badges (`delete_element`).

*Rule of thumb:* Be helpful and proactive. If a reviewer writes "make the subtitle punchier", draft a punchy rewrite and include it in the plan rather than asking the user for clarification.

### 2. Requires Manual Action (API-Unsupported)
Comments requesting changes beyond API capabilities:
- Changing font families (e.g. from *Arial* to *Montserrat*).
- Creating brand-new text boxes or badges from scratch.
- Modifying canvas background colors or gradients.
- Re-ordering, cloning, or deleting whole pages/slides.
- Tweaking geometric vector shape fills or animations.

*Rule of thumb:* Do not apologize or over-explain API limits. Categorize them directly as manual actions and save them for the post-commit checklist.

### 3. Resolved (No Action Required)
Comments that acknowledge completed work or express approval (e.g., "Looks great!", "LGTM", "Resolved in v2"). Acknowledge and skip without mutating the canvas.

---

## 3. Resolving Conflicting Reviewer Opinions

When two stakeholders give contradictory feedback (e.g., Reviewer A: *"Make headline dark blue"*, Reviewer B: *"Keep headline white for contrast"*):
- Do NOT pick a winner arbitrarily.
- Highlight the collision in the pre-flight plan:
  ```markdown
  ⚠️ Contradiction on Slide 3:
  - @Sarah: "Use dark blue headline"
  - @David: "Keep headline white"
  Recommended resolution: Dark blue on light background card (achieves both contrast and palette).
  Confirm preferred direction?
  ```

---

## 4. The Single Approval Gate

**Crucial Protocol Rule:** You MUST present the unified plan to the user and request confirmation **ONE TIME ONLY**.

Once the user approves:
- **IMMEDIATELY** execute `start-editing-transaction`.
- Apply all approved operations in a single batched `perform-editing-operations` call.
- **IMMEDIATELY** execute `commit-editing-transaction`.
- **NEVER** ask "Shall I commit?", "Are you ready to save?", or pause for a second confirmation. The initial plan approval authorizes the entire transaction.

---

## 5. Comment Thread Auto-Reply

After committing changes to the design, post automated resolution replies via `Canva:reply-to-comment`:

- **For Actionable Threads**:
  > *"Applied requested change via automation: updated heading copy and bumped font size to 36pt bold."*
- **For Manual Threads**:
  > *"Note: Font family change to Montserrat requires manual selection in the Canva editor toolbar (API restriction)."*

---

## 6. Post-Execution Manual Checklist Format

Present any remaining manual changes clearly at the conclusion:

```markdown
## Manual Actions Required in Canva Editor

1. **Slide 2 — Update Heading Font to Montserrat**
   - *Reviewer:* @Marcus | *Constraint:* API cannot change typeface
   - *Action:* Select slide 2 title -> Open font dropdown -> Select Montserrat Bold.

2. **Slide 5 — Insert Legal Disclaimer Box**
   - *Reviewer:* @Legal | *Constraint:* API cannot create new text elements
   - *Action:* Press 'T' to add text box at bottom: "Confidential - For Internal Use Only".
```
