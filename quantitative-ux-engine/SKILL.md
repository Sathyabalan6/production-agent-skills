---
name: quantitative-ux-engine
description: Computes quantitative HCI metrics and interaction thresholds using mathematical formulations and Python CLI utilities. Calculates Hick-Hyman decision entropy, Fitts's Law Index of Difficulty (Shannon formulation) and Movement Time, WCAG 2.2 SC 2.5.8 centroid spacing geometry, and INP cooperative scheduling batch limits. Trigger when calculating quantitative UX metrics, computing latency budgets, sizing touch target geometry, or running verification scripts. Do NOT trigger for visual component layout or qualitative design heuristics (use cognitive-ui-patterns).
compatibility: Python 3.10+ or Node.js 20+.
---

# Quantitative UX & HCI Calculation Protocol

Use this protocol and bundled calculation utilities (`scripts/ux-metrics.py`) to mathematically verify interaction latency, target geometry, and cognitive entropy.

---

## 1. Information Theory & Decision Entropy (Hick-Hyman Law)

Model decision latency as transmitted cognitive entropy:

`T = b * log2(n + 1)`

- Cognitive rate parameter `b`: Typically ~150–250 ms/bit across user populations (default: 200 ms/bit).
- Cognitive Load Hierarchy: Hick's Law models logarithmic reaction time. When option sets grow large (e.g. n > 5–7), consider progressive disclosure, categorical grouping, or pre-selected sensible defaults. Avoid over-splitting flat option sets into unnecessary accordions when rapid scanning is preferred.
- Skewed Probabilities: When a single primary action accounts for the vast majority of user intent (p >= 0.8), visual salience reduces effective choice entropy toward ~1.0 bit.

Run calculation:
```python
from scripts.ux_metrics import calc_hick_hyman
metrics = calc_hick_hyman(n_choices=5)  # -> entropy_bits: 2.585, decision_time_ms: ~517ms
```

---

## 2. Motor Ergonomics & Movement Time (Fitts's Law)

Target acquisition time is governed by distance `D` and target width `W`:

- Shannon Formulation (Default; MacKenzie 1992, ISO 9241-9):
  `ID = log2(D / W + 1)`
  `MT = a + b * ID` (typical empirical values: a ≈ 50 ms, b ≈ 120 ms/bit)
  *Guarantees ID >= 0 bits even for large, close targets (where D < W).*
- Primary Touch Target Minimum: Ensure interactive targets provide at least 48×48 CSS px for primary mobile actions (WCAG AAA / iOS HIG standard).
- Mobile Reachability: On viewports < 768px, position primary CTAs in the ergonomic thumb zone (the lower 30–35% of the mobile viewport) to minimize acquisition distance D.
- Destructive Action Buffer: Maintain at least 12px spatial separation between primary and destructive controls (or require explicit modal confirmation) to absorb finger touch contact variance.

Run calculation:
```python
from scripts.ux_metrics import calc_fitts_law
# Shannon formulation default prevents negative ID for close, large targets:
fitts = calc_fitts_law(distance_px=20, width_px=48)  # -> ID: 0.5025 bits, MT: 110.3 ms
```

---

## 3. Spatial Geometry & Target Spacing (WCAG 2.2 SC 2.5.8)

When targets cannot meet the 24×24 CSS px threshold, verify the non-overlapping spacing exception:

`Distance(C1, C2) = sqrt((C2x - C1x)^2 + (C2y - C1y)^2) >= 24px`

- Centroids `C1, C2` of adjacent interactive controls must maintain at least 24px Euclidean distance.
- For an icon target measuring 16×16px, provide at least 8px transparent padding/margin so its 24px diameter bounding circle does not intersect adjacent controls.

Run verification:
```python
from scripts.ux_metrics import check_wcag_target_spacing
result = check_wcag_target_spacing(target1=(0, 0, 16, 16), target2=(24, 0, 16, 16))
# -> conforms_sc_2_5_8: True
```

---

## 4. Perceptual Latency & Task Scheduling (Doherty & INP)

Enforce temporal responsiveness based on perceptual limits:

- < 150 ms: Immediate visual feedback (active tap state, hover transitions, optimistic toggles).
- >= 150 ms: Indeterminate progress indicators (spinners, skeletons) to prevent duplicate actions.
- <= 400 ms: Doherty Threshold; target response window to sustain uninterrupted human task flow.
- > 50 ms: Long Task threshold. Segment CPU-heavy work into cooperative chunks:
  `batch_size = max(1, floor(50ms / per_item_latency_ms))`
  Yield execution every batch slice via `scheduler.yield()` or `setTimeout(..., 0)`.

---

## 5. Verification Standard

Execute the bundled metrics engine to verify quantitative parameters:

```bash
python3 quantitative-ux-engine/scripts/ux-metrics.py
```

---

## 6. Mathematical Foundations & Reference (Tier 3)

For formal proofs, Shannon information theory derivations, and historical citations:
- [references/mathematical-foundations.md](references/mathematical-foundations.md)
