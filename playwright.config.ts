import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for production-agent-skills automated audit suites.
 * Uses TARGET_URL or PLAYWRIGHT_TEST_BASE_URL (defaults to http://127.0.0.1:3000).
 */
export default defineConfig({
  testDir: './ai-website-polish/scripts',
  timeout: 30000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'list',
  use: {
    baseURL: process.env.TARGET_URL || process.env.PLAYWRIGHT_TEST_BASE_URL || 'http://127.0.0.1:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
