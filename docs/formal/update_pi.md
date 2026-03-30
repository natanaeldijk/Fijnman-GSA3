## Purpose

The perspective parameter π tracks how the system evolves relative to accepted transitions.

It is a diagnostic construct used by the CFM layer.

It does not affect the core state.

---

## Definition

Given:

- current perspective `π`
- proposed step `dx`
- acceptance flag `accepted`

the update rule is:

```text
π' = π + dx    if accepted
π' = π         otherwise

---

Interpretation
- accepted motion updates the perspective
- rejected motion does not affect perspective
- perspective reflects realized, not attempted transitions

---

## Role in CFM

π is used to:
- track accumulated accepted motion
- provide a reference for future diagnostic evaluation
- separate attempted change from realized change

---

## Design Principle

The perspective update must not:

- modify the core state
- influence admissibility decisions

It is purely observational.

