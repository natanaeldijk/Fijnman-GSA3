# CFM Diagnostics

## Purpose

This module defines the diagnostic functions used by the CFM.

These functions analyze execution behavior without modifying it.

---

## Functions

### `is_rupture`

Detects whether a rupture condition has occurred.

A rupture indicates a breakdown in continuity or admissibility.

---

### `interference`

Measures interaction between competing transitions or constraints.

---

### `classify_interference`

Classifies interference into predefined categories.

Example categories may include:
- constructive
- destructive
- neutral

---

### `update_pi`

Updates the confidence parameter `π`.
```text
π_new = π_old + α * signal
```


Where:
- `α` is the learning rate
- `signal` depends on outcome

---

## Properties

### Boundedness

π is clipped to:
0 ≤ π ≤ 1

---


### Monotonicity (Conditional)

- increases on accepted steps
- stable or decreases otherwise

---

## Design Principle

Diagnostics are:

- pure functions
- side‑effect free
- independent of execution

---

## Role

CFM diagnostics provide interpretation, not control.