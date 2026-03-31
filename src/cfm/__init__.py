"""
CFM – Diagnostic layer for GSA core.

Public API:
    - is_rupture
    - interference
    - classify_interference
    - update_pi
    - CFMResult
    - cfm_step
"""

from .diagnostics import (
    is_rupture,
    interference,
    classify_interference,
    update_pi,
)
from .api import CFMResult, cfm_step