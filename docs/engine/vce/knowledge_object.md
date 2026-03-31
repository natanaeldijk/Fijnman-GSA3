# Knowledge Object

## Purpose

The `KnowledgeObject` is the fundamental unit of state within the Vault Continuity Engine (VCE). It represents a discrete piece of knowledge that evolves through a well‑defined, fail‑closed lifecycle. The object’s state is the single source of truth for its admissibility and progression.

---

## Definition

A `KnowledgeObject` is defined by:

- **object_id** — unique identifier  
- **state** — one of the lifecycle states  
- **value** — an optional numeric value (from the core’s state space)  

Formally:
KnowledgeObject = (id: str, state: KOState, value: float | None)

### Lifecycle States

| State       | Meaning                                                                 |
|-------------|-------------------------------------------------------------------------|
| `NONE`      | Initial state; no core evaluation has occurred yet.                    |
| `CANDIDATE` | Proposed and admissible at least once; not yet fully validated.        |
| `VALIDATED` | Survived repeated admissibility checks; stable knowledge.              |
| `REJECTED`  | A proposal was rejected by the core; terminal state.                   |
| `HALTED`    | A proposal caused a `HALT_SPEC_REQUIRED`; terminal state.              |

---

## Transition Rules

Transitions are governed exclusively by the core’s decision (`ADMISSIBLE`, `REJECT`, or `HALT_SPEC_REQUIRED`) and the current state. The transition function `transition_knowledge_object(state, result)` is deterministic and fail‑closed.

### Transition Table

| Current State | Core Result       | New State   | Notes                                  |
|---------------|-------------------|-------------|----------------------------------------|
| `NONE`        | `ADMISSIBLE`      | `CANDIDATE` | First admissible step.                 |
| `CANDIDATE`   | `ADMISSIBLE`      | `VALIDATED` | Second admissible step confirms.       |
| `VALIDATED`   | `ADMISSIBLE`      | `VALIDATED` | Idempotent; remains validated.         |
| *any*         | `REJECT`          | `REJECTED`  | Terminal – no further transitions.     |
| *any*         | `HALT_SPEC_REQUIRED` | `HALTED` | Terminal – specification missing.      |

All other combinations are **undefined** and raise an `UndefinedTransition` exception.

---

## Fail‑Closed Semantics

- If a transition is not explicitly defined, the system **halts** by raising an exception.  
- No implicit fallback, no guesswork.  
- The core result is authoritative; VCE only interprets it through the strict transition table.
- **A KnowledgeObject can never transition out of a terminal state (`REJECTED`, `HALTED`).**

---

## Idempotence

The transition for `VALIDATED` with `ADMISSIBLE` is idempotent:  
`VALIDATED → ADMISSIBLE → VALIDATED`.  

This guarantees that a stable knowledge object does not oscillate or degrade when presented with further admissible proposals.

---

## Value Attribute

The `value` attribute holds the numeric state from the core after the last transition. It is set by the runner and is not used in transition logic. It may be used by diagnostics (CFM) or for external projection.

---

## Canonical Principle

**The state of a KnowledgeObject is authoritative.**  
External representations (e.g., markdown exports) are derived from this internal state and never modify it directly.

---

## Example Lifecycle

```text
NONE → (ADMISSIBLE) → CANDIDATE → (ADMISSIBLE) → VALIDATED → (REJECT) → REJECTED

or

NONE → (REJECT) → REJECTED

or

NONE → (HALT_SPEC_REQUIRED) → HALTED
```

---

## Relation to Core

The `KnowledgeObject` is the bridge between the core (which evaluates proposals) and the VCE (which manages state continuity). Each proposal targets a specific object by `object_id`. The core sees only the numeric `value`; the VCE maintains the lifecycle state separately.

This separation ensures that:
- The core remains stateless and pure.
- The VCE provides continuity across sessions.