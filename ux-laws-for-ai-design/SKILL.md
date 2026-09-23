---
name: ux-laws-for-ai-design
description: Translates core UX laws and cognitive psychology heuristics into concrete, parametric layout constraints and component architectures. Trigger when designing user interfaces, creating wireframes, defining checkout/onboarding user flows, or evaluating UI usability. Do NOT trigger for raw backend logic, database modeling, or standard API routing.
compatibility: Platform agnostic. Compatible with React, Vue, Svelte, and Tailwind CSS.
---

# UX Laws for AI Design Protocol

This skill operationalizes cognitive psychology into deterministic UI layouts. When prompted to generate interfaces or critique designs, implement the parametric rules below.

---

## Parametric Layout Constraint Engine

### 1. Hick-Hyman Law (Decision Latency Minimization)
- **Mathematical Formula**: $T = b \cdot \log_2(n + 1)$
- **Constraint**: Maximum allowable top-level interactive controls per viewport region: **5**.
- **Staging**: Multi-step onboarding or checkout flows containing $>5$ input controls must be partitioned into stepped stages or accordion sections.
- **Cognitive Offload**: Provide sensible, pre-selected defaults for optional configurations to absorb user decision load.

### 2. Fitts's Law & Motor Ergonomics
- **Mathematical Formula**: $MT = a + b \cdot \log_2\left(\frac{2D}{W}\right)$
- **Target Size**: Primary action buttons (CTAs) must maintain a minimum bounding box of **48×48 CSS px**.
- **Thumb Zone Anchoring**: On viewport widths $<768\text{ px}$, anchor primary action buttons within the bottom thumb zone (lower 35% of the display).
- **Accidental Click Prevention**: Secondary actions must be placed at least 12 px away from destructive actions to prevent errant selection.

### 3. Miller's Law & Perceptual Chunking
- **Working Memory Limit**: $7 \pm 2$ discrete informational units.
- **Clustering**: Input fields and data rows must be grouped into structural clusters of **3 to 7 items**.
- **Visual Boundaries**: Form sections must be enclosed in discrete visual containers (`<fieldset>`, cards, or bordered panels) with distinct headings.
- **Masking**: Format long character sequences (e.g., credit cards, phone numbers, postal codes) into auto-spaced visual sub-blocks.

### 4. Doherty Threshold (Continuous Feedback)
- **Response Limit**: Any asynchronous dispatch exceeding **150 ms** must display an active indeterminate progress indicator.
- **Mutation Guard**: Action buttons must immediately enter a disabled, spinning loading state upon dispatch to eliminate duplicate submissions.
- **Optimistic Updates**: Apply optimistic state mutations for lightweight local toggles (e.g., favorites, bookmarks, read/unread states).

### 5. Von Restorff Isolation Principle
- **Visual Salience**: Restrict high-saturation primary brand styling to **exactly one** action button per visible screen context.
- **Visual Hierarchy**: All competing secondary actions must render using ghost, outline, or low-contrast neutral fills.

### 6. Peak-End Rule & Completion Gradient
- **Progress Visibility**: Multi-stage flows must feature an explicit progress bar displaying percentage or step count (e.g., "Step 2 of 4").
- **Terminal Confirmation**: Terminate every multi-step transaction with a dedicated confirmation screen containing an explicit checkmark icon, persistent reference ID, and next-action directive.

---

## Output Structure

When executing UI generation, structure the response into three distinct sections:
1. **Applied UX Invariants**: Explicitly detail how Hick, Fitts, Miller, and Doherty thresholds were calculated and satisfied.
2. **Component Implementation**: Output the concrete, semantic component markup.
3. **Cognitive Boundary Check**: Detail intentional trade-offs made to absorb complexity onto the system rather than the user.

---

## Extended References (Tier 3)

For detailed psychological formulas, mathematical derivations, and edge cases across the complete catalog of UX laws, consult:
- [references/ux-heuristics-reference.md](references/ux-heuristics-reference.md)
