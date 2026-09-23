---
name: quantitative-ux-engine
description: Applies formal mathematical models, information theory, psychophysics, and empirical benchmarking to UI/UX layouts and agent evaluation. Computes Hick-Hyman decision entropy, Fitts's Law Index of Difficulty (ID) and movement time, WCAG 2.2 target spacing geometry, Doherty/INP cooperative scheduling batch thresholds, and compound iteration vulnerability degradation. Trigger when mathematically sizing targets, calculating cognitive load, modeling interaction latency, or setting quantitative UX/agent benchmarks. Do NOT trigger for subjective aesthetic reviews or raw CSS styling.
compatibility: Python 3.10+ or Node.js 20+.
---

# Quantitative UX & HCI Mathematical Protocol

Execute this protocol when designing, auditing, or mathematically constraining user interfaces, interaction loops, or agent benchmarking pipelines.

---

## 1. Information Theory & Decision Entropy (Hick-Hyman Law)

Calculate transmitted cognitive entropy before rendering menus, option sets, or form controls:

$$T = b \cdot \log_2(n + 1)$$

- **Decision Budget**: Hard cap of **5 top-level interactive options** per viewport region ($H \le 2.585\text{ bits}$, $T \approx 517\text{ ms}$ at $b = 200\text{ ms/bit}$).
- **Entropy Partitioning**: If options exceed 5, partition into progressive stages, accordion clusters, or hierarchical sub-trees to prevent exponential decision latency.
- **Biased Distribution**: When one primary action accounts for $\ge 80\%$ of intent, apply high-saturation styling to reduce entropy towards $1.0\text{ bit}$.

---

## 2. Motor Ergonomics & Movement Time (Fitts's Law)

Compute Target Acquisition Difficulty and Movement Time ($MT$):

$$ID = \log_2\left(\frac{2D}{W}\right) \quad \text{or} \quad ID_{\text{Shannon}} = \log_2\left(\frac{D}{W} + 1\right)$$
$$MT = a + b \cdot ID \quad (a \approx 50\text{ ms}, b \approx 120\text{ ms/bit})$$

- **Primary Action Minimum**: Primary CTAs must maintain a bounding box of at least **$48 \times 48\text{ CSS px}$** ($W \ge 48\text{ px}$).
- **Target Difficulty Cap**: Keep $ID \le 3.5\text{ bits}$ for primary actions.
- **Mobile Ergonomic Zone**: On viewports $<768\text{ px}$, anchor primary CTAs within the bottom $120\text{ px}$ (lower $35\%$ thumb reach zone, $D \to 0 \implies MT \to a$).
- **Destructive Separation**: Destructive controls must be separated from primary actions by at least **$12\text{ px}$** buffer to eliminate target overlap error ($P(\text{error}) < 0.01$).

---

## 3. Spatial Geometry & Target Spacing (WCAG 2.2 SC 2.5.8)

When targets cannot meet $24 \times 24\text{ px}$, enforce non-overlapping circular spacing:

$$\|C_1 - C_2\| = \sqrt{(C_{2x} - C_{1x})^2 + (C_{2y} - C_{1y})^2} \ge 24\text{ px}$$

- Centroids $C_1, C_2$ of adjacent interactive bounding boxes must maintain a minimum Euclidean distance of **$24\text{ px}$**.
- For an icon target measuring $16 \times 16\text{ px}$, inject at least **$8\text{ px}$** of transparent padding or margin around the target.

---

## 4. Psychophysics & Latency Limits (Doherty & INP)

Enforce temporal responsiveness based on perceptual thresholds:

- **$t < 150\text{ ms}$**: Local state transitions, active tap highlights, and optimistic toggles.
- **$t \ge 150\text{ ms}$**: Indeterminate spinners or skeleton loaders to preserve human working memory and prevent duplicate clicks.
- **$t \le 400\text{ ms}$**: Doherty Threshold; maximum permissible end-to-end round trip for uninterrupted human cognitive flow.
- **$t > 50\text{ ms}$**: Long Task threshold. Slice large computational operations into batches using cooperative scheduling:
  $$k = \max\left(1, \left\lfloor \frac{50\text{ ms}}{\tau_{\text{item}}} \right\rfloor\right)$$
  Yield main thread execution every $k$ items via `scheduler.yield()`.

---

## 5. Agent Iteration & Benchmarking Statistics

- **Vulnerability Compounding Decay**: Unconstrained agent iterations compound defect probability:
  $$V_n = V_0 \cdot (1 + r)^n \quad (r \approx 6.59\%\text{ per prompt iteration})$$
  Enforce **Plan-Validate-Patch** to truncate iteration degradation.
- **Skill Lift**:
  $$\text{Skill Lift} = \text{Score}_{\text{with-skill}} - \text{Score}_{\text{without-skill}} \quad (\text{Target: } \ge +15\text{ percentage points})$$
- **Grader Calibration**:
  $$\kappa = \frac{P_o - P_e}{1 - P_e} \ge 0.85 \quad (\text{Cohen's Kappa for automated LLM judging})$$

---

## 6. Deterministic Calculation Standard

Before outputting layout recommendations or state chunking logic, verify metrics using the calculation script:

```bash
python3 scripts/ux-metrics.py
```

---

## 7. Deep Analytical References (Tier 3)

For complete mathematical proofs, Shannon entropy derivations, and empirical benchmark evaluations:
- [references/mathematical-foundations.md](references/mathematical-foundations.md)
