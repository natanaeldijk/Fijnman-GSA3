# Interference

## Purpose

Interference measures which active constraint boundary is most affected by a proposed state transition.

It is a diagnostic quantity.
It does not alter the core decision.

---

## Definition

Given:

- current state `x`
- proposed step `dx`
- lower boundary `lower`
- upper boundary `upper`

the interference function returns a boundary-sensitivity map.

```text
interference(x, dx, lower, upper) → boundary ↦ score

---

Interpretation
if dx > 0, the proposed motion is evaluated relative to the upper boundary
if dx < 0, the proposed motion is evaluated relative to the lower boundary
if dx = 0, there is no interference

The score increases when:

the proposed step becomes larger
the available distance to the relevant boundary becomes smaller

---

Minimal Rule

For positive motion:
Int_upper = |dx / (upper - x)|

For negative motion:
Int_lower = |dx / (x - lower)|

If the relevant distance is zero, interference is treated as infinite.

---

Role in CFM

Interference is used to:

identify which boundary is most responsible for rupture
explain why a proposed transition fails
support diagnostic interpretation without modifying the core

It is therefore explanatory, not generative.
