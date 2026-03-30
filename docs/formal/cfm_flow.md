# CFM Flow

## Purpose

The CFM (Counterfactual Monitor) flow composes diagnostic functions into a single evaluation pipeline.

It observes the behavior of the core system without modifying it.

The CFM layer is **read-only** and exists purely for analysis, interpretation, and monitoring.

---

## Structure

A single step consists of:

```text
core → rupture → interference → update_pi

Each component operates independently and contributes diagnostic information.

---

## Definition

Given:
- a core system Core
- a current state x
- a proposed step dx
- a perspective parameter π

the flow computes:
(result, x_new) = core.step(x, dx)
rupture         = is_rupture(result)
interference    = interference(x, dx, lower, upper)
π'              = update_pi(π, dx, accepted)

and returns:
{
    result,
    x_new,
    rupture,
    interference,
    π'
}

---

## Output Semantics

result
The authoritative decision of the core.

Possible values:
- ADMISSIBLE
- REJECT
- REFUSAL
- HALT_SPEC_REQUIRED

---

## x_new

The updated state returned by the core.

If a rupture occurs, this may remain unchanged.

---

## rupture

A boolean indicator of constraint violation.
True  → transition rejected by the core
False → transition accepted

---

## interference

A diagnostic structure describing constraint pressure.
{
    "values": {
        "upper": float | None,
        "lower": float | None
    },
    "severity": "LOW" | "MEDIUM" | "HIGH"
}

- values quantify proximity to constraint boundaries
- severity provides a qualitative classification

---

## π' (updated perspective)

The updated perspective parameter.

Interpretation:
- If the step is accepted → π shifts in the direction of dx
- If rejected → π remains unchanged

---

## Interference Severity

Interference values are mapped to qualitative levels:
LOW
MEDIUM
HIGH

This classification is:
- diagnostic only
- independent of the core decision
- used for interpretation, not control

---

## Interpretation

The CFM flow provides a layered explanation of a core step:
- result → what happened
- rupture → whether constraints were violated
- interference → how close the system is to violation
- π' → how perspective evolves over time

---

## Design Principles

The CFM flow must:
- never modify the core
- operate in read-only mode
- remain compositional
- remain fully testable
- separate existence (core) from interpretation (CFM)

---

## Invariants

The following must always hold:
- Core output is unchanged by CFM
- No state mutation occurs inside CFM
- Diagnostics do not affect admissibility
- The flow is deterministic given (core, x, dx, π)

---

## Conceptual Summary

Core defines reality.
CFM explains it.

