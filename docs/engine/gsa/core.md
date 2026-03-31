# GSA Core

## Purpose

The GSA Core is the authoritative evaluation engine of the system.  
It determines admissibility under explicitly defined constraints.

The core is:
- deterministic
- stateless
- fail-closed

---

## Interface

The core exposes a single method:

```python
step(x: float, dx: float | None) -> tuple[str, float]
```

Parameters
- x — current value
- dx — proposed step (can be None)

Returns
- (result, x_new)

Where:
- result ∈ {ADMISSIBLE, REJECT, HALT_SPEC_REQUIRED}
- x_new — resulting value after evaluation

---

## Result Semantics

| Result               | Meaning                                               |
| -------------------- | ----------------------------------------------------- |
| `ADMISSIBLE`         | Step is valid; state may advance                      |
| `REJECT`             | Step violates constraints                             |
| `HALT_SPEC_REQUIRED` | Step cannot be evaluated due to missing specification |


---

## Properties

### Determinism

For the same (x, dx), the core always returns the same result.

### Statelessness

The core does not maintain internal history.
All continuity is handled by the VCE.

### Fail‑Closed

If the step cannot be evaluated, the core returns HALT_SPEC_REQUIRED.

---

## Example

```python
from gsa.core import GSA51Core

core = GSA51Core(lower=-1.0, upper=1.0)

result, x_new = core.step(0.0, 0.5)
# → ("ADMISSIBLE", 0.5)

result, x_new = core.step(0.9, 0.5)
# → ("REJECT", 0.9)

result, x_new = core.step(0.0, None)
# → ("HALT_SPEC_REQUIRED", 0.0)
```

---

## Role in the System

The core defines truth.
- VCE → manages state transitions
- CFM → interprets behavior
- GSA → decides what is valid

The core is never modified by higher layers.