# Stability and Knowledge Objects

## Reasoning Flow

S₀ → S₁ → S₂ → ... → Sₙ

---

## Knowledge Object

K ⊆ S

∀ s ∈ K:
  ∀ admissible t:
    t(s) ∈ K

---

## Structural Stability

stable_struct(k) ⇔

∀ admissible t:
  ΔΦ(t(k), k) = 0

---

## Convergence

σ₀ → σ₁ → ...

σ converges ⇔

∃ σ*:
  ∀ n ≥ N:
    ΔΦ(σₙ, σ*) = 0

---

## Empirical Stability

stable_emp_n(k) ⇔

∀ i in window(n):
  ΔΦ_i(k) = 0