# UX Heuristics & Mathematical Foundations (Tier 3 Reference)

This reference catalogs cognitive psychology principles, mathematical formulas, and algorithmic design constraints for human-computer interaction.

## 1. Decision & Time Heuristics
- **Hick-Hyman Law**: $T = b \cdot \log_2(n + 1)$
  - Decision time grows logarithmically with the number and complexity of choices.
  - Limit choices per view region $\le 5$. Use category drill-downs or wizard steps when items exceed this threshold.
- **Fitts's Law**: $MT = a + b \cdot \log_2\left(\frac{2D}{W}\right)$
  - Movement time is determined by distance ($D$) to target and target width ($W$).
  - Maximize primary CTA hit areas ($\ge 48\times 48\text{ px}$) and minimize travel distance by anchoring to screen edges or thumb zones.
- **Parkinson's Law**:
  - Tasks expand to fill allocated time. Provide clear, minimal workflows with default options and auto-fill to abbreviate task durations.
- **Doherty Threshold**:
  - Human-computer feedback loop must operate $\le 400\text{ ms}$ to maintain continuous cognitive focus. Provide instantaneous visual feedback ($\le 150\text{ ms}$) on touch/click events.

## 2. Memory & Cognitive Load
- **Miller's Law**:
  - Working memory span accommodates $7 \pm 2$ chunks. Group complex inputs into clusters of 3 to 7 items using cards, fieldsets, and whitespace boundaries.
- **Serial Position Effect**:
  - Items at the beginning (Primacy) and end (Recency) of a sequence are recalled best. Place critical actions, navigation anchors, or core information at the start and finish of lists.
- **Von Restorff Effect (Isolation Principle)**:
  - When multiple homogeneous items are present, the one differing visually is remembered. Reserve high-contrast primary styles for the singular primary conversion action.
- **Zeigarnik Effect**:
  - Incomplete tasks generate cognitive tension. Utilize visual progress bars and incomplete checklist indicators to motivate task completion.
- **Goal-Gradient Effect**:
  - Motivation accelerates as users approach the target goal. Multi-step flows should display remaining steps and visually accelerate completion proximity.

## 3. Gestalt Principles & Visual Hierarchy
- **Law of Proximity**:
  - Elements close together are perceived as a group. Form labels must have tighter vertical margins to their inputs than the distance between adjacent form groups.
- **Law of Similarity**:
  - Visually similar elements share functional properties. Maintain consistent button shapes, typography scales, and interactive cues.
- **Uniform Connectedness**:
  - Visually connected elements (via enclosing borders, connecting lines, or shared container backgrounds) are perceived as strongly related.
- **Law of Prägnanz (Simplicity)**:
  - The human brain processes ambiguous or complex images in the simplest possible form. Avoid visual clutter, unnecessary borders, and stacked shadows.

## 4. Operational Invariants
- **Tesler's Law (Conservation of Complexity)**:
  - Every system has an irreducible amount of complexity. The engineering responsibility is to absorb this complexity in code rather than offloading it onto the user.
- **Postel's Law (Robustness Principle)**:
  - Be conservative in what you send, liberal in what you accept. Form inputs should accept diverse input formats (phone numbers with/without dashes, country codes, dates) and normalize them server-side.
- **Jakob's Law**:
  - Users spend most of their time on other sites. Adopt platform-standard mental models for navigation, form interactions, and search controls.
- **Occam's Razor**:
  - When multiple designs accomplish an objective, select the one with the fewest assumptions and components.
- **Pareto Principle (80/20 Rule)**:
  - 80% of value comes from 20% of features. Prioritize primary user paths and eliminate low-utility secondary chrome.
