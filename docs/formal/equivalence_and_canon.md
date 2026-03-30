# Equivalence and Canonicalization

## Claim Representation

σ = (C, R, X, P)

---

## Equivalence

σ₁ ~σ σ₂ iff:

Eq_C(C₁, C₂)  
∧ Eq_R(R₁, R₂)  
∧ Eq_X(X₁, X₂)  
∧ Eq_P(P₁, P₂)

---

## Equivalence Rules

Eq_* is TRUE iff:

- normalization(C) == normalization(C)
OR
- explicit registry mapping exists

otherwise:

→ HALT_SPEC_REQUIRED

---

## Canonical Form

canon : σ → σ̂

Properties:

- σ̂ ~σ σ
- σ₁ ~σ σ₂ ⇒ canon(σ₁) = canon(σ₂)
- canon(canon(σ)) = canon(σ)

---

## Nodes

N ⊆ { [σ]~σ }