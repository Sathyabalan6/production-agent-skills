# Mathematical Foundations of HCI & Quantitative UX (Tier 3 Reference)

This reference outlines the analytical derivations, information theory formulations, and statistical frameworks governing quantitative human-computer interaction and agent evaluation.

---

## 1. Information Theory & Hick-Hyman Law

### Formal Formulation
The Hick-Hyman Law relates reaction time ($T$) to the transmitted information entropy ($H$) of a categorical decision:

$$T = b \cdot H$$

For $n$ equiprobable stimuli where the probability of selecting any alternative is $p_i = \frac{1}{n}$, Shannon's entropy $H = -\sum_{i=1}^n p_i \log_2(p_i) = \log_2(n)$.

Accounting for the baseline temporal cost of non-response / stimulus presence uncertainty:

$$T = b \cdot \log_2(n + 1)$$

Where:
- $b \in [150, 250]\text{ ms/bit}$ is the cognitive processing rate constant across human populations.
- When options have unequal selection probabilities $p_i$:
  $$H = \sum_{i=1}^n p_i \log_2\left(\frac{1}{p_i} + 1\right)$$
  Highlighting a primary choice ($p_{\text{primary}} \approx 0.8$) dramatically reduces transmitted entropy compared to uniform distributions.

---

## 2. Motor Ergonomics & Fitts's Law

### Formulations
1. **Fitts's Original (1954)**:
   $$MT = a + b \cdot \log_2\left(\frac{2D}{W}\right)$$
2. **Shannon Formulation (MacKenzie 1992, ISO 9241-9 Standard)**:
   $$MT = a + b \cdot \log_2\left(\frac{D}{W} + 1\right)$$
   *Advantage*: Prevents negative Index of Difficulty ($ID < 0$) when targets are larger than distance ($W > 2D$).

### Thumb Zone Radial Geometry
The ergonomic thumb arc on handheld touchscreens is modeled in polar coordinates $(r, \theta)$:
- Center of rotation: Metacarpophalangeal joint at bottom right $(W_v, H_v)$ for right-handed grip.
- Functional reach radius: $r_{\min} \approx 35\text{ mm}$, $r_{\max} \approx 75\text{ mm}$.
- In viewport CSS coordinates:
  $$\text{Zone}_{\text{natural}} = \left\{ (x, y) \mid y \ge 0.65 \cdot H_v \land \sqrt{(x - W_v)^2 + (y - H_v)^2} \le r_{\max} \right\}$$
  Anchor controls within the bottom $120\text{ px}$ to eliminate reach displacement ($D \to 0$).

---

## 3. Spatial Geometry & Target Spacing (WCAG 2.2 SC 2.5.8)

### Centroid Distance Theorem
Let two rectangular target bounding boxes $B_1 = [x_1, y_1, w_1, h_1]$ and $B_2 = [x_2, y_2, w_2, h_2]$ have geometric centers:
$$C_1 = \left(x_1 + \frac{w_1}{2}, y_1 + \frac{h_1}{2}\right), \quad C_2 = \left(x_2 + \frac{w_2}{2}, y_2 + \frac{h_2}{2}\right)$$

Each target is circumscribed with an imaginary circle of diameter $D_{\text{spec}} = 24\text{ px}$ (radius $r = 12\text{ px}$). The circles do not intersect if and only if:
$$\|C_1 - C_2\|_2 = \sqrt{(C_{2x} - C_{1x})^2 + (C_{2y} - C_{1y})^2} \ge 2r = 24\text{ px}$$

---

## 4. Psychophysics & Temporal Latency Thresholds

1. **Weber-Fechner Law**:
   $$\Delta I / I = k$$
   Perceived change in sensory stimulus is proportional to baseline magnitude. Latency jumps from $50\text{ ms}$ to $150\text{ ms}$ are readily apparent ($\Delta I / I = 2.0$), while changes from $1000\text{ ms}$ to $1100\text{ ms}$ are negligible ($\Delta I / I = 0.1$).
2. **Doherty Threshold ($400\text{ ms}$)**:
   Empirical limit established at IBM (1982) where computer response delays exceed human short-term working memory persistence, triggering task disruption and secondary thought branching.
3. **Core Web Vitals INP Threshold ($200\text{ ms}$)**:
   Measures discrete event handling + processing + presentation delay. Batching chunking threshold:
   $$k = \left\lfloor \frac{50\text{ ms}}{\tau_{\text{item}}} \right\rfloor$$

---

## 5. Statistical Agent Benchmarking & Vulnerability Decay

### Compounding Degradation Dynamics
Given per-round vulnerability regression rate $r$:
$$V_n = V_0 \cdot (1 + r)^n$$
When $n = 5$ iterations yield $V_5 = 1.376 \cdot V_0$:
$$r = 1.376^{1/5} - 1 \approx 0.0659\text{ (6.59% compounding decay per round)}$$

### Cohen's Kappa ($\kappa$) Inter-Rater Reliability
$$\kappa = \frac{P_o - P_e}{1 - P_e}$$
Where:
- $P_o$: Observed proportional agreement between LLM evaluator and human ground truth.
- $P_e$: Chance agreement calculated from marginal probabilities.
- $\kappa \ge 0.85$ defines production calibration for automated judging pipelines.
