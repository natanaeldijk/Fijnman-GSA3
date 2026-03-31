"""
Diagnostic primitives for CFM.

These functions are pure and read-only.
They do not modify any core state.
"""

import math


def is_rupture(core_output: str) -> bool:
    """Return True iff the core output indicates a rupture."""
    return core_output in {"REJECT", "REFUSAL"}


def interference(x: float, dx: float, lower: float, upper: float) -> dict[str, float]:
    """
    Compute sensitivity of a step to boundary constraints.

    Returns a dict with a single key:
        - "upper" if dx > 0
        - "lower" if dx < 0
        - "none" if dx == 0

    The value is the ratio |dx| / distance to the boundary,
    or inf if the step would exactly hit or cross the boundary.

    If dx is None or NaN, returns {"none": 0.0} as there is no meaningful motion.
    """
    if dx is None or (isinstance(dx, float) and math.isnan(dx)):
        return {"none": 0.0}

    if dx > 0:
        dist = upper - x
        return {"upper": abs(dx / dist) if dist != 0 else float("inf")}
    elif dx < 0:
        dist = x - lower
        return {"lower": abs(dx / dist) if dist != 0 else float("inf")}
    else:
        return {"none": 0.0}


def classify_interference(score: float) -> str:
    """Classify interference magnitude as LOW, MEDIUM, or HIGH."""
    if score < 0.5:
        return "LOW"
    if score < 1.0:
        return "MEDIUM"
    return "HIGH"


def update_pi(pi: float, dx: float, accepted: bool, learning_rate: float = 0.1) -> float:
    """
    Update perspective parameter π.

    When a step is accepted, π moves towards the direction of dx.
    When a step is rejected, π stays unchanged.

    Optionally, a learning_rate can be specified (default 0.1) to avoid
    excessive jumps. The result is clipped to [-1, 1] for stability.
    """
    if accepted:
        new_pi = pi + learning_rate * dx
        return max(-1.0, min(1.0, new_pi))
    return pi