# Accessibility (WCAG 2.2 AA) & Web Testing (`/web-testing`)

Production web applications must ensure barrier-free access and robust end-to-end automated verification.

---

## 1. WCAG 2.2 Level AA Accessibility Standards

1. **Color Contrast**:
   - Normal text ($<18\text{pt}$ / $24\text{px}$): Minimum **4.5:1** contrast ratio against background.
   - Large text ($\ge 18\text{pt}$ / $24\text{px}$ bold): Minimum **3:1** contrast ratio.
2. **Keyboard Operability**:
   - Every interactive control must receive tab focus.
   - Visible `:focus-visible` focus ring (never `outline: none` without replacement).
   - No keyboard traps.
3. **Form Fields & Labels**:
   - Every `<input>`, `<select>`, `<textarea>` must have an associated `<label for="...">` or `aria-label`.
   - Error messages must be programmatically linked via `aria-describedby` and `aria-invalid="true"`.
4. **Target Size (Minimum)**:
   - Touch targets must measure at least **24x24 CSS pixels** to prevent accidental clicks on mobile.

---

## 2. Automated Testing Pyramid

### 2.1 Static Accessibility Auditing
Integrate `@axe-core/playwright` into continuous integration tests to catch 50%+ of common WCAG failures automatically before deployment:
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('homepage accessibility audit', async ({ page }) => {
  await page.goto('/');
  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
  expect(accessibilityScanResults.violations).toEqual([]);
});
```

### 2.2 Critical Path E2E Testing
- Smoke test: Homepage loads and renders header, hero, and footer without console errors.
- Auth flow: User login, session persistence, and logout.
- Core conversion: Checkout, form submission, or primary business transaction.
