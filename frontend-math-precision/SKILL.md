---
name: frontend-math-precision
description: Apply CSS-native math (linear interpolation, trigonometry, stepped/sign functions, container query units, scroll-driven timelines, linear() easing) to eliminate magic numbers in fluid layout, radial geometry, scroll animation, and motion curves — with browser-support-aware fallbacks. Trigger for fluid responsive scaling, radial/circular layouts, scroll-driven reveals, spring-like easing, and coordinate transforms. Do NOT trigger for standard flex/grid layouts without mathematical interpolation.
metadata:
  version: "2026-08"
  last-verified: "2026-08-29"
  tags: [css, frontend, layout, animation, accessibility, responsive-design]
---

# Mathematical Paradigms in Frontend Architecture

**Last verified: August 2026.** Ground layout proportions, responsive scaling, motion, and coordinate transforms in explicit formulas instead of hardcoded pixel heuristics. Prefer native CSS math where reliably supported; fall back cleanly where it is not.

**Don't force every task through this skill.** Solve the plain way first. Reach for these techniques only when magic numbers, accessibility failures, or JS-driven jank appear.

---

## Decision Tree (Use This First)

1. Plain flex/grid + simple `clamp()` already solves it → **stop**.
2. Only 2–3 fixed breakpoints → prefer `@media` over fluid interpolation.
3. Standard `ease` / `cubic-bezier()` looks right → do not invent `linear()` springs.
4. No circular/radial positioning needed → do not introduce `sin()`/`cos()`/`atan2()`.
5. Animating a math-derived custom property (angle, length, number)? → register it with `@property` first (Module 10), or the transition will jump instead of tween.
6. Otherwise pick the matching module below.

## When NOT to Use This Skill
- Ordinary responsive cards that flex/grid already handle.
- Designs with only a few discrete breakpoints.
- Decorative motion that a basic easing already satisfies.
- Layouts that never need circular geometry.

---

## Module 1: Fluid Typography via Linear Interpolation (WCAG 1.4.4 Correct)

**Problem:** Pure `vw`/`cqi` clamps ignore user root font-size preferences and violate WCAG 2.2 SC 1.4.4 (Resize Text). Text must scale proportionally with user zoom up to 200%.

**Formula (Point-Slope Interpolation):**
- Slope `m = (y2 - y1) / (x2 - x1)`
- Intercept `b = y1 - (m * x1)`
- Viewport contribution `= m * 100vw`

**Implementation Rules:**
1. Min and max bounds must be in `rem` so they honor user root font preferences.
2. The preferred (middle) value must mix `rem` + viewport/container units (e.g. `0.625rem + 2.5vw`), never pure `vw`.
3. Keep max <= 2.5 × min as a practical ceiling so 200% zoom remains reachable. Verify in-browser.
4. Never declare `user-scalable=no` or `maximum-scale=1`.

```css
/*
  Target: 1.125rem (18px) at 320px viewport, 2.5rem (40px) at 1200px viewport.
  Assuming default 1rem = 16px:
    y1 = 18px, y2 = 40px, x1 = 320px, x2 = 1200px
    m = (40px - 18px) / (1200px - 320px) = 22 / 880 = 0.025 (2.5% of viewport width -> 2.5vw)
    b = 18px - (0.025 * 320px) = 18px - 8px = 10px -> 10px / 16px = 0.625rem
  Result: clamp(1.125rem, 0.625rem + 2.5vw, 2.5rem)
  Verification:
    At 320px:  0.625rem (10px) + 2.5vw (8px)  = 18px (1.125rem) -> exact match
    At 760px:  0.625rem (10px) + 2.5vw (19px) = 29px (1.8125rem) -> smoothly scales
    At 1200px: 0.625rem (10px) + 2.5vw (30px) = 40px (2.5rem)    -> exact match
*/
.fluid-heading {
  font-size: clamp(1.125rem, 0.625rem + 2.5vw, 2.5rem);
}
```

---

## Module 2: Radial Layouts via Native CSS Trigonometry

Native support for `sin()`, `cos()`, and `atan2()` is Baseline widely available.

Coordinate mapping:
- Angle step: `calc(360deg / var(--total-nodes))`
- Node angle: `calc(var(--angle-step) * var(--i))`
- Polar to Cartesian: `x = cos(angle) * radius`, `y = sin(angle) * radius`
- Tangent orientation: `rotate(atan2(y, x))` (DOM Y increases downward)

```css
.radial-container {
  --radius: 250px;
  --total-nodes: 8;
  --angle-step: calc(360deg / var(--total-nodes));
  position: relative;
  width: calc(var(--radius) * 2);
  height: calc(var(--radius) * 2);
}

.radial-node {
  /* style="--i: 0" ... "--i: 7" */
  --angle: calc(var(--angle-step) * var(--i));
  --x: calc(cos(var(--angle)) * var(--radius));
  --y: calc(sin(var(--angle)) * var(--radius));
  position: absolute;
  transform: translate(var(--x), var(--y)) rotate(atan2(var(--y), var(--x)));
}
```

---

## Module 3: Scroll-Driven Animation (Progressive Enhancement)

*Critical rule: The `animation` shorthand resets `animation-timeline`. Always declare `animation-timeline` after the shorthand.*

```css
.reveal-card {
  opacity: 1;
  transform: translateY(0);
}

@supports (animation-timeline: view()) {
  .reveal-card {
    opacity: 0;
    transform: translateY(100px);
    animation: spatial-reveal linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 40%;
  }
}

@keyframes spatial-reveal {
  to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
  .reveal-card {
    animation: none;
    animation-timeline: none;
  }
}
```

---

## Module 4: Spring / Bounce Easing via `linear()`

`cubic-bezier()` cannot overshoot; `linear()` can by defining explicit stops.

```css
.elastic-element {
  transition: transform 0.4s ease-out; /* fallback */
  transition: transform 0.4s linear(0, 1.08 15%, 0.95 45%, 1.02 70%, 1 100%);
}
```

---

## Module 5: Transformed Geometry via `DOMMatrixReadOnly`

Extract true transformed coordinates, scale factors, and rotation angles from rendered elements without brittle regex parsing.

```javascript
/**
 * Decomposes CSS transforms and resolves true transformed geometry
 * using the standard DOMMatrixReadOnly API.
 */
function getTransformedGeometry(el) {
  const rect = el.getBoundingClientRect();
  const style = window.getComputedStyle(el);
  const transform = style.transform;

  // Parse 2D or 3D transform matrix via DOMMatrixReadOnly
  const matrix = transform && transform !== 'none'
    ? new DOMMatrixReadOnly(transform)
    : new DOMMatrixReadOnly();

  // Extract decomposed components
  const scaleX = Math.hypot(matrix.a, matrix.b);
  const scaleY = Math.hypot(matrix.c, matrix.d);
  const rotationDeg = Math.round(Math.atan2(matrix.b, matrix.a) * (180 / Math.PI));

  // Transform element center point through the matrix
  const centerPoint = new DOMPoint(rect.width / 2, rect.height / 2);
  const transformedCenter = matrix.transformPoint(centerPoint);

  return {
    rect,
    matrix,
    scaleX: Number(scaleX.toFixed(4)),
    scaleY: Number(scaleY.toFixed(4)),
    rotationDeg,
    centroidX: rect.left + window.scrollX + rect.width / 2,
    centroidY: rect.top + window.scrollY + rect.height / 2,
    transformedCenter: {
      x: rect.left + window.scrollX + transformedCenter.x,
      y: rect.top + window.scrollY + transformedCenter.y,
    },
  };
}
```

---

## Module 6: Stepped Quantization — `round()`, `mod()`, `abs()`, `sign()`

```css
.grid-node {
  /* Snap to 50px increments */
  width: round(var(--fluid-width), 50px);
  transform: translateX(calc(var(--offset) * sign(var(--offset))));
}

.list-item {
  /* Cyclic stagger animation delays (repeating 0-400ms pattern) */
  animation-delay: calc(mod(var(--index), 5) * 100ms);
}
```

---

## Module 7: Container Query Units (`cqi`, `cqw`, `cqh`)

```css
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

.card-title {
  /* Prefer cqi (logical) over cqw for writing-mode resilience */
  font-size: clamp(1.5rem, 5cqi, 2.5rem);
}
```

---

## Module 8: Exponential Functions — `hypot()`, `pow()`, `sqrt()`

```css
.radial-gradient-bg {
  /* Exact corner-to-corner diagonal distance */
  --diagonal: hypot(100%, 100%);
  background: radial-gradient(circle at center, var(--accent) 0%, transparent var(--diagonal));
}

.display-heading {
  /* Non-linear modular scale step */
  font-size: calc(1rem * pow(1.25, var(--scale-step)));
}
```

---

## Module 9: CSS Anchor Positioning

```css
.trigger-button {
  anchor-name: --my-tooltip-anchor;
}

.tooltip {
  position: fixed;
  position-anchor: --my-tooltip-anchor;
  top: anchor(bottom);
  left: anchor(center);
  position-try-fallbacks: flip-block;
}
```

---

## Module 10: `@property` Registration for Math Animation

```css
@property --angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

.rotating {
  --angle: 0deg;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  to { --angle: 360deg; }
}
```

---

## Module 11: Dynamic Viewport Units (`svh`, `lvh`, `dvh`)

```css
.hero {
  min-height: 100vh;  /* Fallback first */
  min-height: 100svh; /* Modern mobile-safe default */
}
```

---

## Module 12: Safe `calc()` with Divide-by-Zero Guards

```css
/* Safe: floors the divisor above zero to avoid silent Infinity/NaN failure */
--safe-divisor: max(var(--user-value, 0), 0.0001);
width: calc(100% / var(--safe-divisor));
```

---

## Cross-Cutting: `prefers-reduced-motion` Enforcement

Always gate animations:
```css
@media (prefers-reduced-motion: reduce) {
  :root { --spring-duration: 1ms; }
  .reveal-card {
    animation: none !important;
    animation-timeline: none !important;
  }
}
```
