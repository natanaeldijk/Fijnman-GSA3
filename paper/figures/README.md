# Figures

This directory contains the figures used in the paper.

The figures illustrate the core architecture of the reasoning system, including:
- admissibility-based state transitions
- constraint enforcement and rupture behavior
- separation between core decision logic and diagnostic interpretation

---

## Figure 1 — Integrated Architecture

**Title:**  
Admissibility-Based Reasoning Architecture with Constraint Enforcement and Diagnostic Interpretation

**Description:**  
This figure presents the full system architecture.

The system is divided into two layers:

- **Core (Existence Layer)**  
  Determines whether transitions are admissible.  
  Uses constraints (Ω), transitions (Θ), and fail-closed logic.  
  The core is authoritative and its output is final.

- **Diagnostic Layer (CFM)**  
  Observes the core in read-only mode.  
  Performs rupture detection, interference analysis, and perspective updates.  
  It does not modify the core state.

The figure also shows the interaction between:
- admissibility decisions  
- constraint enforcement  
- diagnostic interpretation  

---

## Figure 2 — Constraint Space and Rupture

**Description:**  
This figure illustrates constraint enforcement in a simple 1D state space.

- The feasible region Ω is defined as an interval.
- A transition that remains within Ω is allowed.
- A transition that leaves Ω causes a rupture.

When a rupture occurs:
- the core returns **REJECT**
- the state is not updated

This demonstrates fail-closed behavior:
invalid transitions do not modify the system.

---

## Figure 3 — Diagnostic Perspective Update

**Description:**  
This figure shows how the diagnostic layer updates interpretative beliefs.

- A prior distribution Π represents possible interpretations.
- The core produces an output (e.g., REJECT due to rupture).
- The diagnostic layer updates Π → Π′ based on the observation.

Important:
- The core result does not change.
- Only the interpretation is updated.

This illustrates strict separation between:
- decision (core)
- interpretation (diagnostic layer)

---

## Notes

- All figures follow the same principle:  
  **no implicit state mutation**

- The core determines admissibility.  
- The diagnostic layer explains outcomes without altering them.

- The architecture is fail-closed:
  undefined or invalid transitions result in rejection or halt.