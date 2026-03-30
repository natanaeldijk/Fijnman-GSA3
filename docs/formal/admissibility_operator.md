# Admissibility Operator

A(q,S) =

REFUSAL              if not WithinBoundary(q,S)  
HALT_SPEC_REQUIRED   if not Complete(q,S)  
REJECT               if not Anchored(q,S)  
REJECT               if not Consistent(q,S)  
ADMISSIBLE           otherwise  

---

## Complete_claim

σ = (C, R, X, P)

Complete_claim(σ) ⇔

PropositionSpecified(C)  
∧ ReferenceSpecified(R)  
∧ ScopeSpecified(X)  
∧ ProvenanceSpecified(P)