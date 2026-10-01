import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const targetUrl = process.env.TARGET_URL || process.env.PLAYWRIGHT_TEST_BASE_URL || '/';

test.describe('Automated WCAG 2.2 AA Conformance Sweep', () => {
  test('verify zero detectable violations on initial render', async ({ page }) => {
    await page.goto(targetUrl, { waitUntil: 'networkidle' });

    const scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    expect(scanResults.violations).toEqual([]);
  });

  test('enforce focus visibility against sticky overlays (SC 2.4.11)', async ({ page }) => {
    await page.goto(targetUrl);
    const interactives = await page.locator('button:visible, a:visible, input:visible').all();

    for (const control of interactives) {
      await control.focus();
      const isVisibleInViewport = await page.evaluate((el) => {
        const rect = el.getBoundingClientRect();
        const hitElement = document.elementFromPoint(
          rect.left + rect.width / 2,
          rect.top + rect.height / 2
        );
        return hitElement === el || el.contains(hitElement);
      }, await control.elementHandle());

      expect(isVisibleInViewport).toBeTruthy();
    }
  });

  test('enforce target size minimum (SC 2.5.8)', async ({ page }) => {
    await page.goto(targetUrl);
    const pointerControls = await page.locator(
      'button:visible, a:visible, input[type="button"]:visible, input[type="submit"]:visible, [role="button"]:visible'
    ).all();

    // Collect non-inline interactive targets and their bounding geometry
    const targets: {
      handle: typeof pointerControls[0];
      box: { x: number; y: number; width: number; height: number; cx: number; cy: number };
    }[] = [];

    for (const control of pointerControls) {
      // SC 2.5.8 Exemption: Inline targets constrained by line-height of prose/sentence text
      const isInline = await control.evaluate((el) => {
        if (el.tagName.toLowerCase() !== 'a') return false;
        const style = window.getComputedStyle(el);
        if (style.display === 'inline') return true;
        const parent = el.closest('p, span, li, blockquote, dd');
        return Boolean(parent && style.display.includes('inline'));
      });

      if (isInline) {
        continue;
      }

      const box = await control.boundingBox();
      if (box && box.width > 0 && box.height > 0) {
        targets.push({
          handle: control,
          box: {
            ...box,
            cx: box.x + box.width / 2,
            cy: box.y + box.height / 2,
          },
        });
      }
    }

    // Verify each target satisfies either dimension >= 24x24 px OR spacing exception
    for (let i = 0; i < targets.length; i++) {
      const current = targets[i];
      const meetsMinDimension = current.box.width >= 24 && current.box.height >= 24;

      if (meetsMinDimension) {
        continue;
      }

      // SC 2.5.8 Spacing Exception:
      // A 24px diameter circle (radius 12px) centered on this target must not intersect
      // another target or the 24px circle for another undersized target.
      let spacingViolation = false;
      const radius = 12;

      for (let j = 0; j < targets.length; j++) {
        if (i === j) continue;
        const other = targets[j];
        const otherUndersized = other.box.width < 24 || other.box.height < 24;

        if (otherUndersized) {
          const dist = Math.hypot(other.box.cx - current.box.cx, other.box.cy - current.box.cy);
          if (dist < 24) {
            spacingViolation = true;
            break;
          }
        } else {
          // Circle around undersized target vs rectangle of adjacent target
          const closestX = Math.max(other.box.x, Math.min(current.box.cx, other.box.x + other.box.width));
          const closestY = Math.max(other.box.y, Math.min(current.box.cy, other.box.y + other.box.height));
          const dist = Math.hypot(current.box.cx - closestX, current.box.cy - closestY);
          if (dist < radius) {
            spacingViolation = true;
            break;
          }
        }
      }

      expect(
        spacingViolation,
        `Target [${await current.handle.evaluate((el) => el.outerHTML.slice(0, 80))}] is undersized (${Math.round(current.box.width)}x${Math.round(current.box.height)}px) and violates the 24px spacing exception.`
      ).toBeFalsy();
    }
  });

  test('enforce accessible authentication without paste blocking (SC 3.3.8)', async ({ page }) => {
    await page.goto(targetUrl);
    const inputs = await page.locator('input[type="password"], input[autocomplete*="password"], input[type="text"]').all();

    for (const input of inputs) {
      const pasteBlocked = await input.evaluate((el) => {
        let defaultPrevented = false;
        const event = new Event('paste', { bubbles: true, cancelable: true });
        el.dispatchEvent(event);
        return event.defaultPrevented;
      });
      expect(pasteBlocked).toBeFalsy();
    }
  });
});
