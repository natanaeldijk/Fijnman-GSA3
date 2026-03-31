# Event Grammar

## Purpose

The event grammar defines the structure and types of events that occur during execution.

It provides a formal specification of **what can happen** in the system, independent of how state transitions are applied.

---

## Core Principle

Events are:

- **explicit** — every meaningful action is represented as an event  
- **typed** — each event has a defined structure  
- **append-only** — events are never modified or deleted  
- **observable** — events can be consumed by external systems (e.g. CFM)  

---

## Formal Definition

```text
Event = (type: EventType, object_id: str, payload: dict)
```

Where:
- EventType defines the kind of event
- object_id identifies the target KnowledgeObject
- payload contains event-specific data

---

## Event Types

```text
EventType = {
    PROPOSAL_RECEIVED,
    CORE_EVALUATED,
    TRANSITION_APPLIED
}
```

---

## Event Definitions

### PROPOSAL_RECEIVED

Represents the arrival of a new proposal.
```text
payload = {
    x: float,
    dx: float | None,
    state_before: KOState
}
```

---

### CORE_EVALUATED

Represents the result of evaluating a proposal by the core.
```text
payload = {
    result: str,
    x_old: float,
    x_new: float
}
```

Where:
```text
result ∈ { ADMISSIBLE, REJECT, HALT_SPEC_REQUIRED }
```

---

### TRANSITION_APPLIED

Represents a state transition applied by the VCE.
```text
payload = {
    state_before: KOState,
    state_after: KOState,
    result: str
}
```

---

### Event Stream

Events form an ordered sequence:
```text
E = [e₁, e₂, e₃, ...]
```

The sequence is:
- append-only
- time-ordered
- complete
This ensures full reproducibility of execution.

---

## Properties


### Completeness

Every execution step produces a fixed sequence of events:
```text
PROPOSAL_RECEIVED
→ CORE_EVALUATED
→ TRANSITION_APPLIED
```

---

### Determinism

Given the same input sequence, the same event sequence is produced.

---

### Observability

The event stream can be consumed by external systems:
- CFM (diagnostics)
- logging systems
- replay engines
These systems must treat events as read-only.

---

### Relation to State Transition Model
- The event grammar defines what happens
- The state transition model defines how state changes
Together they define the execution semantics of the system.

---

### Design Constraints
- Events must be serializable
- Events must be immutable once created
- Event types must be finite and explicitly defined

---

### Future Extensions

Possible extensions include:
- additional event types (e.g. OBJECT_CREATED, SESSION_STARTED)
- richer payload schemas
- versioned event formats

All extensions must preserve:
- backward compatibility
- append-only semantics