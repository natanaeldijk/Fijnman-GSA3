
# State Transition Model

## Purpose

The state transition model defines how system states evolve in response to evaluation outcomes.

It provides a **deterministic, fail-closed mapping** from:

```text
(current_state, result) → new_state
```

This model is independent of implementation and is used by the VCE to ensure consistent behavior.

---

## Core Principle

State transitions are:
- deterministic — same input always yields the same output
- explicit — only defined transitions are allowed
- fail-closed — undefined transitions raise an error

---

## Formal Definition

```text
transition: (S × R) → S
```

Where:
- S = set of states
- R = set of results

---

## Result Set

```text
R = { ADMISSIBLE, REJECT, HALT_SPEC_REQUIRED }
```

---

## Example State Set (VCE)

```text
S = { NONE, CANDIDATE, VALIDATED, REJECTED, HALTED }
```

---

## Transition Table

| Current State | Result             | New State |
| ------------- | ------------------ | --------- |
| NONE          | ADMISSIBLE         | CANDIDATE |
| CANDIDATE     | ADMISSIBLE         | VALIDATED |
| VALIDATED     | ADMISSIBLE         | VALIDATED |
| *any*         | REJECT             | REJECTED  |
| *any*         | HALT_SPEC_REQUIRED | HALTED    |

---

## Undefined Transitions

Any combination not listed in the transition table is undefined and must raise an error.

This enforces strict fail-closed behavior.

---

## Properties


### Determinism

Each (state, result) pair maps to exactly one new state.

---

### Idempotence

Certain transitions are idempotent:
```text
VALIDATED + ADMISSIBLE → VALIDATED
```
This ensures stability once validation is reached.

---

### Terminal States

The following states are terminal:
```text
REJECTED, HALTED
```
Once reached, no further transitions should occur.

---

### Separation from Core
- The core produces results (R)
- The transition model interprets results into states (S)
- The VCE applies the transition and stores the state

This separation ensures:
- modularity
- testability
- formal clarity

---

### Relation to Event Grammar

The transition model defines state evolution.
The event grammar defines which events exist and how they are structured.
Together they form the formal execution semantics of the system.

