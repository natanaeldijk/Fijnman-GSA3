# Minimal Core — VCE / GSA³

## State

S = (N, R, C, H)

N = nodes  
R = relations  
C = constraints  
H = history  

---

## Proposal

q = (kind, payload, anchors, provenance, context)

kind ∈ {
  claim,
  relation_assertion,
  reasoning_step,
  boundary_assertion,
  promotion_request
}

---

## Admissibility

A : Q × S → Ω

Ω = {
  ADMISSIBLE,
  REJECT,
  HALT_SPEC_REQUIRED,
  REFUSAL
}

---

## Structural Guard

G : S × Q → {0,1}

---

## Execution Rule

execute(q,S) iff:

A(q,S) = ADMISSIBLE  
∧ G(S,q) = 1