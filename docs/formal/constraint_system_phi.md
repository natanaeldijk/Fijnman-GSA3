# Constraint System Φ

## Execution Rule

ΔΦ = 0   → EXECUTE  
ΔΦ ≠ 0   → REFUSAL / HALT  

---

## Φ₁ — Completeness

Complete_claim(σ) = true

---

## Φ₂ — Canonical Consistency

canon(σ) is defined

---

## Φ₃ — Admissibility Preservation

A(q,S) must remain consistent after transition

---

## Φ₄ — Equivalence Stability

σ₁ ~σ σ₂ ⇒ t(σ₁) ~σ t(σ₂)

---

## Φ₅ — Closure

Transitions remain inside admissible space

---

## Φ₆ — Projection Consistency

Vault state must match engine state

---

## Φ₇ — Roundtrip Integrity

Projection → reconstruction preserves state