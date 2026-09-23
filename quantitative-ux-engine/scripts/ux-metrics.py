#!/usr/bin/env python3
"""
Quantitative UX Metrics & Cognitive Calculation Engine
Provides deterministic calculation functions for HCI mathematical models:
- Hick-Hyman Decision Time & Information Entropy
- Fitts's Law Index of Difficulty (ID) & Movement Time (MT)
- WCAG 2.2 SC 2.5.8 Target Centroid Distance & Circle Spacing
- INP Cooperative Task Batching Sizing
- Compounding Iterative Vulnerability Degradation
"""

import math
import sys
from typing import Dict, Any, Tuple

def calc_hick_hyman(n_choices: int, b_rate_ms: float = 200.0) -> Dict[str, float]:
    """
    Computes Hick-Hyman decision time: T = b * log2(n + 1)
    """
    if n_choices < 1:
        raise ValueError("n_choices must be at least 1")
    entropy_bits = math.log2(n_choices + 1)
    decision_time_ms = b_rate_ms * entropy_bits
    return {
        "choices": n_choices,
        "entropy_bits": round(entropy_bits, 4),
        "decision_time_ms": round(decision_time_ms, 2),
        "exceeds_threshold_5": n_choices > 5
    }

def calc_fitts_law(
    distance_px: float,
    width_px: float,
    a_intercept_ms: float = 50.0,
    b_slope_ms: float = 120.0,
    formulation: str = "fitts"
) -> Dict[str, float]:
    """
    Computes Fitts's Law Movement Time: MT = a + b * ID
    Formulations:
      - 'fitts': ID = log2(2D / W)
      - 'shannon': ID = log2(D / W + 1)
    """
    if width_px <= 0 or distance_px <= 0:
        raise ValueError("Distance and width must be positive non-zero numbers")

    if formulation.lower() == "shannon":
        id_bits = math.log2((distance_px / width_px) + 1.0)
    else:
        id_bits = math.log2((2.0 * distance_px) / width_px)

    mt_ms = a_intercept_ms + (b_slope_ms * id_bits)
    return {
        "distance_px": distance_px,
        "width_px": width_px,
        "formulation": formulation,
        "index_of_difficulty_bits": round(id_bits, 4),
        "movement_time_ms": round(mt_ms, 2)
    }

def check_wcag_target_spacing(
    target1: Tuple[float, float, float, float],
    target2: Tuple[float, float, float, float],
    min_diameter_px: float = 24.0
) -> Dict[str, Any]:
    """
    Target tuple: (x, y, width, height)
    Computes centroid Euclidean distance and tests whether min-diameter circles intersect.
    """
    x1, y1, w1, h1 = target1
    x2, y2, w2, h2 = target2

    c1_x, c1_y = x1 + (w1 / 2.0), y1 + (h1 / 2.0)
    c2_x, c2_y = x2 + (w2 / 2.0), y2 + (h2 / 2.0)

    centroid_dist = math.hypot(c2_x - c1_x, c2_y - c1_y)
    required_dist = min_diameter_px
    passes = centroid_dist >= required_dist

    return {
        "centroid_1": (round(c1_x, 2), round(c1_y, 2)),
        "centroid_2": (round(c2_x, 2), round(c2_y, 2)),
        "centroid_distance_px": round(centroid_dist, 2),
        "required_distance_px": required_dist,
        "conforms_sc_2_5_8": passes
    }

def calc_inp_batch_slice(per_item_latency_ms: float, max_slice_budget_ms: float = 50.0) -> int:
    """
    Computes maximum batch slice size before yielding to keep main thread under 50ms (avoiding Long Tasks).
    """
    if per_item_latency_ms <= 0:
        return 100
    batch_size = max(1, math.floor(max_slice_budget_ms / per_item_latency_ms))
    return batch_size

def calc_vulnerability_decay(v0: float, rate_r: float, rounds_n: int) -> float:
    """
    Computes compounding vulnerability growth across n unguided LLM refinement rounds:
    V_n = V_0 * (1 + r)^n
    """
    return round(v0 * math.pow(1.0 + rate_r, rounds_n), 4)

if __name__ == "__main__":
    print("--- Quantitative UX Metrics Engine ---")
    hick = calc_hick_hyman(5)
    print(f"Hick-Hyman (n=5 choices): {hick['entropy_bits']} bits -> {hick['decision_time_ms']} ms")

    fitts = calc_fitts_law(distance_px=240, width_px=48)
    print(f"Fitts's Law (D=240px, W=48px): ID={fitts['index_of_difficulty_bits']} bits -> MT={fitts['movement_time_ms']} ms")

    wcag = check_wcag_target_spacing((0, 0, 16, 16), (20, 0, 16, 16))
    print(f"WCAG 2.5.8 Spacing: Distance={wcag['centroid_distance_px']}px -> Passes: {wcag['conforms_sc_2_5_8']}")
