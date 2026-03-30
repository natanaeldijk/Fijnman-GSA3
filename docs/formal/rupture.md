# Rupture

## Purpose

Rupture marks the point at which a proposed transition leaves the admissible region.

It is a diagnostic concept used by the CFM layer.

It does not alter the core outcome.

---

## Definition

A rupture occurs iff the core output is:

```text
REJECT
or
REFUSAL

Formally:
is_rupture(output) = True  iff  output ∈ {REJECT, REFUSAL}

---

Non-Rupture Case

The output:
HALT_SPEC_REQUIRED

is not a rupture.

Reason:
- it indicates missing specification
- it does not represent a transition that failed after entering the admissible region
- it is an epistemic stop, not a boundary rupture

---

Interpretation
REJECT means the proposal was fully evaluable but not admissible
REFUSAL means the proposal crossed or violated a system boundary
HALT_SPEC_REQUIRED means evaluation could not be completed

Therefore:
rupture = failed admissible motion
not
underspecified motion

---

Role in CFM

Rupture is used to:

detect boundary failure
trigger interference analysis
separate structural failure from underspecification

It is diagnostic, not generative.


---

## 3. Tests in `tests/test_cfm.py`

Zorg dat deze test erin staat:

```python
from cfm.proto import is_rupture


def test_cfm_detects_rupture_on_reject():
    assert is_rupture("REJECT") is True
    assert is_rupture("REFUSAL") is True
    assert is_rupture("ADMISSIBLE") is False
    assert is_rupture("HALT_SPEC_REQUIRED") is False
