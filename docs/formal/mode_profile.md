# Mode Profile

## Purpose

The mode profile describes how a proposal or constraint behaves across the invariant hierarchy of the core.

It provides a layer‑wise characterization of admissibility behavior.

A mode profile does **not** replace the core outcome.  
It is a structural diagnostic summary of how a formula behaves at each invariant level.

---

## Definition

Given:

- a state space constraint `ψ`
- an invariant hierarchy `Φ = (Φ₀, Φ₁, ..., Φₙ)`
- a proposal or formula `ξ`


the mode profile of `ξ` is the tuple:

mode_profile(ξ) = (m₀, m₁, ..., mₙ)

where each `mᵢ` describes the behavior of `ξ` at invariant level `Φᵢ`.

---

## Mode Values

The mode values are:

- **SAFE**
- **STRICT**
- **DEFEASIBLE**

### SAFE

A level is **SAFE** when the formula is admissible and preserves multiple valid models within the constrained state space.

**Interpretation**:
- the formula is allowed
- the kernel is non‑empty
- the result is not uniquely fixed at that level

**Informally**: admissible, but not uniquely determined.

---

### STRICT

A level is **STRICT** when the formula is admissible and determines a unique surviving model or uniquely fixed structure at that level.

**Interpretation**:
- the formula is allowed
- the kernel is non‑empty
- the remaining admissible structure is unique

**Informally**: admissible and uniquely fixed.

---

### DEFEASIBLE

A level is **DEFEASIBLE** when the formula no longer survives as admissible at that level, even though it may survive at lower levels.

**Interpretation**:
- admissibility breaks at this refinement level
- the kernel becomes empty or unstable
- stronger invariants exclude the proposal

**Informally**: previously tolerated, but defeated by stronger constraints.

---

## Structural Reading

The mode profile should be read as a trajectory across invariant depth.

**Example**:

(SAFE, SAFE, DEFEASIBLE)

means:
- the proposal survives at lower levels
- the proposal remains admissible across intermediate refinement
- the proposal fails under stronger invariants

**Example**:

(STRICT, STRICT, STRICT)

means:
- the proposal is uniquely fixed at every level
- no ambiguity remains across the hierarchy

**Example**:

(SAFE, SAFE, SAFE)

means:
- the proposal remains admissible at every level
- but does not collapse to a unique model

---

## Relation to Admissibility Level

The **admissibility level** of `ξ` is the highest invariant level at which `ξ` remains admissible:

admissibility_level(ξ) = max { i | mᵢ ∈ {SAFE, STRICT} }


if such a level exists.

If no admissible level exists, the result is *undefined* or *refusal‑level* depending on the outer evaluation rule.

---

## Relation to Kernel

The mode profile is closely tied to kernel behavior.

At each level `Φᵢ`:

- **SAFE** implies kernel non‑empty and non‑unique
- **STRICT** implies kernel non‑empty and unique
- **DEFEASIBLE** implies kernel collapse or failure at that level

So the profile is a compact observable summary of kernel evolution through the invariant hierarchy.

---

## Role in the System

The mode profile is used to:

- diagnose how a proposal behaves under refinement
- distinguish stable admissibility from fragile admissibility
- identify where defeasibility begins
- support analysis **without** modifying the core decision

It is therefore **diagnostic**, not generative.

---

## Canonical Principle

The mode profile does **not** decide admissibility by itself.

The core remains authoritative.  
The mode profile only records how admissibility behaves across levels.
