"""
CFM public API: combined diagnostic step.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .diagnostics import (
    is_rupture,
    interference,
    classify_interference,
    update_pi,
)


@dataclass
class CFMResult:
    """Result of a single CFM diagnostic step."""

    result: str                   # core output (ADMISSIBLE, REJECT, ...)
    x_new: float                  # new state (same as old if rejected)
    rupture: bool                 # whether a rupture occurred
    interference: Dict[str, Any]  # {"values": dict, "severity": str}
    pi: float                     # updated perspective


def cfm_step(core: Any, x: float, dx: Optional[float], pi: float) -> CFMResult:
    """
    Execute one core step and return enriched CFM diagnostics.

    Parameters
    ----------
    core : Any
        A core instance exposing:
            - lower
            - upper
            - step(x, dx) -> (result, x_new)
    x : float
        Current state.
    dx : float or None
        Proposed step (may be None for HALT_SPEC_REQUIRED).
    pi : float
        Current perspective parameter.

    Returns
    -------
    CFMResult
        Diagnostic information (read-only, does not alter core).
    """
    if dx is None:
        result = "HALT_SPEC_REQUIRED"
        x_new = x
    else:
        result, x_new = core.step(x, dx)

    rupture = is_rupture(result)

    inter = interference(x, dx, core.lower, core.upper)

    if "upper" in inter:
        severity = classify_interference(inter["upper"])
    elif "lower" in inter:
        severity = classify_interference(inter["lower"])
    else:
        severity = "LOW"

    accepted = (result == "ADMISSIBLE")
    pi_new = update_pi(pi, dx if dx is not None else 0.0, accepted)

    return CFMResult(
        result=result,
        x_new=x_new,
        rupture=rupture,
        interference={
            "values": inter,
            "severity": severity,
        },
        pi=pi_new,
    )