import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Automated WCAG 2.2 AA Conformance Sweep', () => {
  test('verify zero detectable violations on initial render', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });

    const scanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    expect(scanResults.violations).toEqual([]);
  });

  test('enforce focus visibility against sticky overlays (SC 2.4.11)', async ({ page }) => {
    await page.goto('/');
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
    await page.goto('/');
    const pointerControls = await page.locator('button:visible, a:visible, input[type="button"]:visible, input[type="submit"]:visible').all();

    for (const control of pointerControls) {
      const box = await control.boundingBox();
      if (box) {
        // Target size must be at least 24x24 px or sufficiently spaced
        const meetsMinDimension = box.width >= 24 && box.height >= 24;
        expect(meetsMinDimension).toBeTruthy();
      }
    }
  });

  test('enforce accessible authentication without paste blocking (SC 3.3.8)', async ({ page }) => {
    await page.goto('/');
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
