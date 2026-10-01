---
name: cognitive-ui-patterns
description: Translates cognitive psychology heuristics and interaction design principles into concrete UI layout architectures and component structures. Trigger when designing UI components, organizing form layouts, applying Miller's chunking, establishing visual hierarchy (Von Restorff), or designing onboarding/checkout flows. Do NOT trigger for quantitative mathematical calculation or numeric latency benchmarking (use quantitative-ux-engine).
compatibility: Platform agnostic. Compatible with React, Vue, Svelte, and modern CSS/Tailwind.
---

# Cognitive UI Layout Patterns Protocol

Apply this protocol when designing, structuring, or reviewing component layouts to minimize cognitive load, streamline motor interaction, and enforce clean visual hierarchy.

---

## Component Layout & Cognitive Invariants

### 1. Decision Load & Hierarchy (Hick-Hyman Principle)
- **Logarithmic Scanning**: Choice reaction time increases logarithmically with the number of alternatives.
- **Hierarchical Structuring**: When option sets grow large (e.g. > 5–7 items), organize into logical categorical groups or progressive disclosure panels. Avoid arbitrarily forcing clean, scannable lists into nested accordions or excessive wizard steps when direct visual scanning is more efficient.
- **Sensible Defaults**: Pre-select common default choices for non-critical options to absorb user decision overhead.

### 2. Motor Ergonomics & Touch Targets (Fitts's Principle)
- **Primary CTA Sizing**: Ensure primary interactive actions maintain at least **48×48 CSS px** bounding box dimensions to guarantee reliable finger/pointer acquisition.
- **Mobile Thumb Zone**: On viewports < 768px, anchor primary navigation and action buttons within the ergonomic thumb reach zone (the lower 30–35% of the mobile display).
- **Destructive Separation**: Separate destructive actions (Delete, Remove, Reset) from primary actions by at least **12px** spatial buffer or require an explicit confirmation modal to prevent accidental activation.

### 3. Perceptual Chunking (Miller's Law)
- **Information Chunking**: Structure dense forms, tables, and dashboards into cohesive clusters of **3 to 7 items**.
- **Visual Enclosures**: Enclose related field groups within clear visual boundaries (`<fieldset>`, card containers, or distinct section dividers) with semantic headings.
- **Formatted Inputs**: Provide masked or spaced formatting for structured data (phone numbers, payment cards, verification codes) to match user working memory spans.

### 4. Continuous Feedback (Doherty Threshold)
- **Progress Feedback**: Any action with processing time > 150 ms must immediately render an indeterminate loading spinner, skeleton placeholder, or progress indicator.
- **Dispatch Guards**: Disable action buttons immediately upon click/submit and display a loading state to eliminate duplicate requests.
- **Optimistic UI**: Apply immediate optimistic mutations for low-risk client interactions (toggles, bookmarks, favorites).

### 5. Visual Salience (Von Restorff Isolation Principle)
- **Primary Distinctiveness**: Reserve high-contrast, filled primary styling for **exactly one** primary action button per active view context.
- **Secondary De-emphasis**: Render all competing secondary actions using ghost, outline, or neutral tones to prevent visual competition.

### 6. Transaction Closure (Peak-End Rule)
- **Progress Orientation**: Multi-step flows must display persistent progress indicators (e.g. "Step 2 of 4" or a visual step tracker).
- **Explicit Completion**: Conclude multi-step flows with an unambiguous completion view featuring a status confirmation icon, summary details, reference identifier, and next-step actions.

---

## Output Structure

When generating or refining component markup, structure the response into:
1. **Applied Cognitive Patterns**: Detail specific heuristics applied (chunking, thumb reach, visual salience).
2. **Component Implementation**: Output accessible, semantic component markup and styling.
3. **Ergonomic Trade-offs**: Note any deliberate design decisions balancing direct scanning against progressive disclosure.

---

## Extended References (Tier 3)

For detailed psychological foundations and edge cases across cognitive UX heuristics:
- [references/ux-heuristics-reference.md](references/ux-heuristics-reference.md)
