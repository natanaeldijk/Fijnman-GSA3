# CFM Result

## Purpose

CFMResult provides a structured representation of a CFM evaluation step.

---

## Fields

- result: core decision
- x_new: resulting state
- rupture: whether a rupture occurred
- interference: constraint pressure analysis
- pi: updated perspective

---

## Design Principle

CFMResult is a container.

It does not affect core computation.
It only organizes diagnostic output.