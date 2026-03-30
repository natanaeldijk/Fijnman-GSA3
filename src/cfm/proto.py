"""
CFM (Counterfactual Monitor)

This module observes the core system without modifying it.

Responsibilities:
- Detect rupture (constraint violations)
- Analyze interference (how close to boundaries)
- Update perspective (π)

Design principle:
CFM NEVER changes the core result.
"""


from __future__ import annotations

from dataclasses import dataclass
from gsa.core import GSA51Core
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
import argparse
import json
import math

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


ADMISSIBLE = "ADMISSIBLE"
REJECT = "REJECT"
REFUSAL = "REFUSAL"
HALT_SPEC_REQUIRED = "HALT_SPEC_REQUIRED"


@dataclass
class CoreResult:
    output: str
    attempted_state: float
    actual_state: float
    reason: Optional[str] = None


class GSA51Core:
    """
    Minimal fail-closed toy core for CFM testing.

    State: x in R
    Constraints:
        lower <= x <= upper

    Semantics:
        - ADMISSIBLE: proposed new state is inside bounds
        - REJECT: proposed new state violates bounds
        - HALT_SPEC_REQUIRED: proposal is malformed / undefined

    The core does not update its state on failure.
    """

    def __init__(self, lower: float = -1.0, upper: float = 1.0) -> None:
        if lower >= upper:
            raise ValueError("lower must be smaller than upper")
        self.lower = lower
        self.upper = upper

    def step(self, x: float, dx: Optional[float]) -> CoreResult:
        if dx is None or not isinstance(dx, (int, float)) or math.isnan(dx):
            return CoreResult(
                output=HALT_SPEC_REQUIRED,
                attempted_state=x,
                actual_state=x,
                reason="Missing or invalid step specification",
            )

        x_new = x + float(dx)

        if x_new < self.lower:
            return CoreResult(
                output=REJECT,
                attempted_state=x_new,
                actual_state=x,
                reason=f"Lower constraint violated: x_new={x_new:.6f} < {self.lower:.6f}",
            )
        if x_new > self.upper:
            return CoreResult(
                output=REJECT,
                attempted_state=x_new,
                actual_state=x,
                reason=f"Upper constraint violated: x_new={x_new:.6f} > {self.upper:.6f}",
            )

        return CoreResult(
            output=ADMISSIBLE,
            attempted_state=x_new,
            actual_state=x_new,
            reason="State remained in admissible region",
        )


@dataclass
class FlowState:
    history: List[float] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    proposals: List[Optional[float]] = field(default_factory=list)
    attempted_states: List[float] = field(default_factory=list)


@dataclass
class Event:
    step: int
    event_type: str
    data: Dict[str, Any]


class CFM1D:
    """
    Diagnostic layer only.
    It reads core results and produces explanatory metadata.
    It never writes into the core or changes its outputs.
    """

    def __init__(self) -> None:
        self.events: List[Event] = []
        self.pi: Dict[str, float] = {"normal": 0.5, "inverted": 0.5}

    def log(self, step: int, event_type: str, **data: Any) -> None:
        self.events.append(Event(step=step, event_type=event_type, data=data))

    @staticmethod
    def is_rupture(core_output: str) -> bool:
        return core_output in {REJECT, REFUSAL}

    @staticmethod
    def observe(x: float, perspective: str) -> float:
        if perspective == "normal":
            return x
        if perspective == "inverted":
            return -x
        raise ValueError(f"Unknown perspective: {perspective}")

    @staticmethod
    def rupture_direction(x_last: float, x_attempted: float) -> float:
        delta = x_attempted - x_last
        if delta == 0:
            return 0.0
        return 1.0 if delta > 0 else -1.0

    @staticmethod
    def interference(x: float, dx: float, lower: float, upper: float) -> Dict[str, float]:
        """
        Discrete sensitivity / violation-pressure score.

        For 1D interval constraints:
            omega_lower: x >= lower
            omega_upper: x <= upper

        We score how strongly the proposed step pushes toward or beyond each boundary.
        Larger means more interference with admissibility.
        """
        if dx == 0:
            return {"lower": 0.0, "upper": 0.0}

        attempted = x + dx
        eps = 1e-12

        lower_gap = max(x - lower, 0.0)
        upper_gap = max(upper - x, 0.0)

        lower_violation = max(lower - attempted, 0.0)
        upper_violation = max(attempted - upper, 0.0)

        lower_score = 0.0
        upper_score = 0.0

        if dx < 0:
            lower_score = abs(dx) / max(lower_gap, eps) + lower_violation
        if dx > 0:
            upper_score = abs(dx) / max(upper_gap, eps) + upper_violation

        return {"lower": lower_score, "upper": upper_score}

    @staticmethod
    def primary_driver(interference_scores: Dict[str, float]) -> Tuple[str, float]:
        name = max(interference_scores, key=interference_scores.get)
        return name, interference_scores[name]

    def update_perspective_distribution(
        self,
        x: float,
        core_output: str,
        lower: float,
        upper: float,
    ) -> Dict[str, float]:
        """
        Bayesian-style explanatory update.

        The perspective does not affect the core.
        It only scores how well a perspective explains the observed outcome.
        """
        new_pi: Dict[str, float] = {}

        for perspective, prior in self.pi.items():
            obs = self.observe(x, perspective)
            inside = lower <= obs <= upper

            if core_output == ADMISSIBLE:
                likelihood = 0.9 if inside else 0.1
            elif core_output in {REJECT, REFUSAL}:
                likelihood = 0.9 if not inside else 0.1
            else:  # HALT_SPEC_REQUIRED
                likelihood = 0.5

            new_pi[perspective] = prior * likelihood

        total = sum(new_pi.values())
        if total <= 0:
            # Fail-safe normalization fallback; diagnostic only.
            size = len(new_pi)
            self.pi = {k: 1.0 / size for k in new_pi}
            return self.pi

        self.pi = {k: v / total for k, v in new_pi.items()}
        return self.pi


def run_simulation(
    x0: float = 0.0,
    lower: float = -1.0,
    upper: float = 1.0,
    steps: int = 20,
    dx: float = 0.2,
    custom_dxs: Optional[List[Optional[float]]] = None,
) -> Tuple[GSA51Core, FlowState, CFM1D]:
    core = GSA51Core(lower=lower, upper=upper)
    flow = FlowState(history=[x0])
    cfm = CFM1D()

    proposals: List[Optional[float]]
    if custom_dxs is not None:
        proposals = custom_dxs
    else:
        proposals = [dx] * steps

    for step_index, proposal_dx in enumerate(proposals, start=1):
        x_current = flow.history[-1]

        cfm.log(step_index, "proposal_received", x=x_current, dx=proposal_dx)
        result = core.step(x_current, proposal_dx)

        flow.outputs.append(result.output)
        flow.proposals.append(proposal_dx)
        flow.attempted_states.append(result.attempted_state)

        cfm.log(
            step_index,
            "core_result",
            output=result.output,
            x_current=x_current,
            x_attempted=result.attempted_state,
            x_actual=result.actual_state,
            reason=result.reason,
        )

        if result.output == ADMISSIBLE:
            flow.history.append(result.actual_state)
            cfm.log(step_index, "flow_advanced", x_new=result.actual_state)

        elif result.output == HALT_SPEC_REQUIRED:
            # No rupture. Flow remains where it is.
            flow.history.append(result.actual_state)
            cfm.log(step_index, "halt_detected", reason=result.reason)

        elif cfm.is_rupture(result.output):
            flow.history.append(result.actual_state)
            direction = cfm.rupture_direction(x_current, result.attempted_state)
            cfm.log(
                step_index,
                "rupture_detected",
                direction=direction,
                x_last_admissible=x_current,
                x_attempted=result.attempted_state,
                output=result.output,
            )

            if proposal_dx is not None:
                scores = cfm.interference(x_current, float(proposal_dx), lower, upper)
                primary_name, primary_score = cfm.primary_driver(scores)
                cfm.log(
                    step_index,
                    "interference_computed",
                    scores=scores,
                    primary_driver=primary_name,
                    primary_score=primary_score,
                )

        updated_pi = cfm.update_perspective_distribution(
            x=flow.history[-1],
            core_output=result.output,
            lower=lower,
            upper=upper,
        )
        cfm.log(step_index, "perspective_updated", pi=updated_pi.copy())

    return core, flow, cfm


def print_summary(core: GSA51Core, flow: FlowState, cfm: CFM1D) -> None:
    print("=== CFM PROTO SUMMARY ===")
    print(f"Bounds: [{core.lower}, {core.upper}]")
    print(f"Visited states: {flow.history}")
    print(f"Outputs: {flow.outputs}")
    print(f"Final perspective distribution: {cfm.pi}")
    print(f"Logged events: {len(cfm.events)}")

    rupture_events = [e for e in cfm.events if e.event_type == "rupture_detected"]
    if rupture_events:
        print("\nRuptures:")
        for e in rupture_events:
            print(f"  step {e.step}: {e.data}")

    interference_events = [e for e in cfm.events if e.event_type == "interference_computed"]
    if interference_events:
        print("\nInterference analyses:")
        for e in interference_events:
            print(f"  step {e.step}: {e.data}")


def save_event_log(cfm: CFM1D, output_path: str) -> None:
    serializable = [
        {
            "step": e.step,
            "event_type": e.event_type,
            "data": e.data,
        }
        for e in cfm.events
    ]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)


def plot_run(core: GSA51Core, flow: FlowState, cfm: CFM1D, path: Optional[str] = None) -> None:
    if plt is None:
        raise RuntimeError("matplotlib is not installed in this environment")

    xs = flow.history
    ts = list(range(len(xs)))

    plt.figure(figsize=(10, 5))
    plt.plot(ts, xs, marker="o", label="state x_t")
    plt.axhline(core.lower, linestyle="--", label="lower bound")
    plt.axhline(core.upper, linestyle="--", label="upper bound")

    for event in cfm.events:
        if event.event_type == "rupture_detected":
            plt.axvline(event.step, linestyle=":")

    plt.xlabel("Step")
    plt.ylabel("State")
    plt.title("CFM Proto Run")
    plt.legend()
    plt.tight_layout()

    if path:
        plt.savefig(path, dpi=150)
    else:
        plt.show()
    plt.close()


def parse_custom_dxs(raw: Optional[str]) -> Optional[List[Optional[float]]]:
    if raw is None:
        return None
    out: List[Optional[float]] = []
    for item in raw.split(","):
        token = item.strip().lower()
        if token in {"none", "nan", "halt"}:
            out.append(None)
        else:
            out.append(float(token))
    return out


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CFM proto v0.1 simulation")
    parser.add_argument("--x0", type=float, default=0.0, help="Initial state")
    parser.add_argument("--lower", type=float, default=-1.0, help="Lower bound")
    parser.add_argument("--upper", type=float, default=1.0, help="Upper bound")
    parser.add_argument("--steps", type=int, default=20, help="Number of steps for constant dx mode")
    parser.add_argument("--dx", type=float, default=0.2, help="Constant delta per step")
    parser.add_argument(
        "--custom-dxs",
        type=str,
        default=None,
        help="Comma-separated step proposals, e.g. '0.2,0.2,0.2,None,-0.5'",
    )
    parser.add_argument("--events-out", type=str, default=None, help="Write event log to JSON file")
    parser.add_argument("--plot-out", type=str, default=None, help="Write run plot to PNG file")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    custom_dxs = parse_custom_dxs(args.custom_dxs)
    core, flow, cfm = run_simulation(
        x0=args.x0,
        lower=args.lower,
        upper=args.upper,
        steps=args.steps,
        dx=args.dx,
        custom_dxs=custom_dxs,
    )

    print_summary(core, flow, cfm)

    if args.events_out:
        save_event_log(cfm, args.events_out)
        print(f"\nEvent log written to: {args.events_out}")

    if args.plot_out:
        plot_run(core, flow, cfm, args.plot_out)
        print(f"Plot written to: {args.plot_out}")

def is_rupture(core_output: str) -> bool:
    """
    Return True iff the core output indicates a rupture.

    A rupture means that a proposed transition leaves the admissible region.

    Rupture outputs:
    - REJECT
    - REFUSAL

    Non-rupture outputs:
    - ADMISSIBLE
    - HALT_SPEC_REQUIRED

    Notes
    -----
    HALT_SPEC_REQUIRED is not treated as rupture, because it indicates
    missing specification rather than a failed transition from an
    otherwise admissible region.
    """
    return core_output in ["REJECT", "REFUSAL"]


def interference(x: float, dx: float, lower: float, upper: float) -> dict[str, float]:
    result: dict[str, float] = {}

    if dx > 0:
        dist_upper = upper - x
        result["upper"] = abs(dx / dist_upper) if dist_upper != 0 else float("inf")
    elif dx < 0:
        dist_lower = x - lower
        result["lower"] = abs(dx / dist_lower) if dist_lower != 0 else float("inf")
    else:
        result["none"] = 0.0

    return result


def update_pi(pi: dict[str, float], x: float, core_output: str) -> dict[str, float]:
    def observe(value: float, perspective: str) -> float:
        if perspective == "normal":
            return value
        if perspective == "inverted":
            return -value
        return value

    new_pi: dict[str, float] = {}

    for perspective, prior in pi.items():
        obs = observe(x, perspective)

        # simpele likelihood voor proto
        likelihood = 1.0 if abs(obs) <= 1 else 0.5

        new_pi[perspective] = likelihood * prior

    total = sum(new_pi.values())
    if total == 0:
        size = len(new_pi)
        return {k: 1.0 / size for k in new_pi}

    return {k: v / total for k, v in new_pi.items()}


def interference(x: float, dx: float, lower: float, upper: float) -> dict[str, float]:
    """
    Measure which active boundary is most affected by a proposed step.

    Parameters
    ----------
    x : float
        Current state value.
    dx : float
        Proposed step.
    lower : float
        Lower admissible boundary.
    upper : float
        Upper admissible boundary.

    Returns
    -------
    dict[str, float]
        A simple boundary-sensitivity map.

        Examples:
        - {"upper": 2.0}
        - {"lower": 1.5}
        - {"none": 0.0}

    Interpretation
    --------------
    - Larger values mean stronger interference with that boundary.
    - Positive motion tests the upper boundary.
    - Negative motion tests the lower boundary.
    - Zero motion produces no interference.
    """
    result: dict[str, float] = {}

    if dx > 0:
        dist_upper = upper - x
        result["upper"] = abs(dx / dist_upper) if dist_upper != 0 else float("inf")
    elif dx < 0:
        dist_lower = x - lower
        result["lower"] = abs(dx / dist_lower) if dist_lower != 0 else float("inf")
    else:
        result["none"] = 0.0

    return result


def update_pi(pi: float, dx: float, accepted: bool) -> float:
    """
    Update the perspective parameter π based on the outcome of a proposed step.

    Parameters
    ----------
    pi : float
        Current perspective value.
    dx : float
        Proposed step.
    accepted : bool
        Whether the step was accepted by the core.

    Returns
    -------
    float
        Updated perspective.

    Interpretation
    --------------
    - If the step is accepted, π shifts in the direction of dx.
    - If the step is rejected, π remains unchanged.

    Notes
    -----
    This function does NOT modify the core state.
    It only tracks how perspective evolves relative to accepted motion.
    """
    if accepted:
        return pi + dx
    return pi


def classify_interference(score: float) -> str:
    """
    Classify interference severity.

    Parameters
    ----------
    score : float
        Interference magnitude.

    Returns
    -------
    str
        One of:
        - LOW
        - MEDIUM
        - HIGH
    """
    if score < 0.5:
        return "LOW"
    if score < 1.0:
        return "MEDIUM"
    return "HIGH"


@dataclass
class CFMResult:
    result: str
    x_new: float
    rupture: bool
    interference: dict
    pi: float


def cfm_step(core, x: float, dx: float, pi: float):
    result, x_new = core.step(x, dx)
    rupture = is_rupture(result)

    inter = interference(x, dx, core.lower, core.upper)

    if "upper" in inter:
        severity = classify_interference(inter["upper"])
    elif "lower" in inter:
        severity = classify_interference(inter["lower"])
    else:
        severity = "LOW"

    accepted = result == "ADMISSIBLE"
    pi_new = update_pi(pi, dx, accepted)

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


if __name__ == "__main__":
    main()


