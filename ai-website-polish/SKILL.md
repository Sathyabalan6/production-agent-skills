---
name: ai-website-polish
description: Audits and transforms AI-generated or rapidly prototyped web applications into production-ready deployments. Applies deterministic WCAG 2.2 AA accessibility checks, Interaction to Next Paint (INP) performance remediations, responsive layout corrections, and pre-launch asset hygiene. Trigger when reviewing vibe-coded applications, auditing frontends for launch readiness, or hardening UI states. Do NOT trigger for general CSS design styling or raw backend database schema design.
compatibility: Requires Node.js 20+, Playwright test runner, and @axe-core/playwright.
---

# AI Website Polish Protocol

Execute this protocol when auditing or finalizing AI-generated web applications. The agent must operate in a strict **Plan-Validate-Patch** sequence, prioritizing accessibility and security blockers before cosmetic refinements.

## Execution Sequence

1. **Initial Audit**: Run automated accessibility and static analysis suites.
2. **Blocker Remediation**: Resolve keyboard navigation traps, contrast failures, and hidden focus indicators.
3. **Runtime Performance**: Optimize event loop responsiveness (INP) and eliminate main-thread blocking tasks.
4. **Layout Stabilization**: Enforce responsive viewport constraints and touch-target minimums.
5. **Asset & Link Hygiene**: Purge placeholder assets, mock strings, and unanchored links. Consult [references/full-checklist.md](references/full-checklist.md) for pre-launch operational verification.

---

## 1. Regulatory Accessibility Requirements (WCAG 2.2 Level AA)

The agent must enforce the following technical criteria across all generated code:

- **Focus Not Obscured (SC 2.4.11 - Level AA)**:
  Any focusable control (`a`, `button`, `input`) must remain visible upon receiving keyboard focus. When floating or sticky headers/footers exist, apply CSS scroll margins to prevent element interception:
  ```css
  :focus-visible {
    scroll-margin-top: 5rem;
    scroll-margin-bottom: 5rem;
    outline: 2px solid var(--focus-ring-color, #2563eb);
    outline-offset: 2px;
  }
  ```

- **Target Size Minimum (SC 2.5.8 - Level AA)**:
  All interactive pointer targets must measure at least **24×24 CSS px**, or provide sufficient transparent padding such that adjacent target centers remain at least 24 px apart. (Target **44×44 px** for primary mobile controls to satisfy touch ergonomics).

- **Accessible Authentication (SC 3.3.8 - Level AA)**:
  Never disable clipboard paste operations on password, MFA, or verification input fields (`onPaste={(e) => e.preventDefault()}` is strictly prohibited). Provide password manager auto-fill metadata (e.g., `autocomplete="current-password"` or `autocomplete="one-time-code"`).

- **Dragging Alternatives (SC 2.5.7 - Level AA)**:
  Any interactive drag-and-drop workflow (reorderable lists, kanban boards, sliders) must offer equivalent discrete button controls (e.g., "Move Up", "Move Down", "Transfer Item", or keyboard arrow navigation).

---

## 2. Interaction Performance & Core Web Vitals (INP Focus)

- **Interaction to Next Paint (INP)**: Identify and segment long tasks (>50 ms) in user event handlers.
- **State Transition Scheduling**: Wrap non-urgent computational state updates in `React.useTransition` or chunk execution utilizing cooperative scheduling primitives like `scheduler.yield()`:
  ```typescript
  // Cooperative execution prevents long task blocking on main thread
  async function processBatch<T>(items: T[], fn: (item: T) => void): Promise<void> {
    for (let i = 0; i < items.length; i++) {
      fn(items[i]);
      if (i % 50 === 0) {
        if ('scheduler' in window && 'yield' in (window as any).scheduler) {
          await (window as any).scheduler.yield();
        } else {
          await new Promise((resolve) => setTimeout(resolve, 0));
        }
      }
    }
  }
  ```
- **Cumulative Layout Shift (CLS)**: Eliminate layout jitter by declaring explicit `width`, `height`, and `aspect-ratio` on all image, video, and iframe elements.

---

## 3. Viewport & Mobile Responsive Invariants

- **Horizontal Scroll Elimination**: Test at 375 px and 390 px viewport widths. Ensure horizontal scrolling is entirely eliminated. `overflow-x: hidden` must **NOT** be applied to `<body>` as a band-aid; fix inner container bounding boxes and grid/flex wrapping instead.
- **Modal & Drawer Focus Trapping**: Mobile navigation drawers and dialogs must trap keyboard focus when open and return focus to the toggle trigger button upon close.

---

## 4. Deterministic Verification Standard

Before declaring task completion, execute the bundled verification test:

```bash
npx playwright test scripts/a11y-audit.spec.ts
```

Verify that zero violations are returned across `wcag2a`, `wcag2aa`, and `wcag22aa` tag suites.

---

## 5. Extended Pre-Launch Audits (Progressive Disclosure)

For comprehensive checklists spanning SEO metadata, favicon configurations, OpenGraph cards, legal consent banners, and pre-launch asset hygiene, consult:
- [references/full-checklist.md](references/full-checklist.md)
