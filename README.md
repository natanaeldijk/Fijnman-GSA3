\# Fijnman-GSA³ v5.1.1



\*\*A Fail-Closed Framework for Structural Reasoning\*\*



> A formal, fail-closed alternative to truth-based reasoning systems.



A layered symbolic framework for admissibility-based reasoning systems.

GSA³ eliminates hallucinations by enforcing \*\*fail-closed semantics\*\*, replacing truth with \*\*structural invariance\*\* as the criterion for admissibility.



\---



\## 🔑 Core Idea



Instead of asking whether a statement is \*true\*, GSA³ asks:



> \*\*Is this state structurally admissible under invariant constraints?\*\*



If not → \*\*REFUSAL\*\*



\---



\## 🧩 Intuition



Traditional reasoning systems try to determine whether statements are \*\*true\*\*.



GSA³ takes a different approach:



> A state is not accepted because it is true,

> but because it is \*\*structurally admissible\*\*.



\---



\### What goes wrong in standard systems?



Most AI systems fail \*\*open\*\*:



\* If information is missing → they guess

\* If inconsistent → they still produce output

\* If ambiguous → they hallucinate



\---



\### What GSA³ does instead



GSA³ enforces a \*\*fail-closed pipeline\*\*:



1\. Start with a symbolic state space

2\. Apply constraints (Ξ) → obtain a substate

3\. Check consistency relative to invariants (Φᵢ)

4\. Compute the \*\*kernel\*\* (maximal consistent substate)

5\. Select the highest admissible level (I\*)



If no level is consistent → \*\*REFUSAL\*\*



\---



\### Why this matters



\* No hallucinations

\* No silent contradictions

\* No unjustified conclusions



Every output is \*\*structurally justified\*\*.



\---



\### One-line summary



> GSA³ replaces truth with \*\*consistency under invariants\*\*,

> and replaces guessing with \*\*refusal\*\*.



\---



\## 🔄 Pipeline Overview



```text

State space (Ψ)

&#x20;     ↓

Apply constraints (Ξ)

&#x20;     ↓

Substate S'

&#x20;     ↓

Check Φᵢ-consistency

&#x20;     ↓

Kernel K⁽ⁱ⁾(S')

&#x20;     ↓

Select I\*

&#x20;     ↓

Outcome:

&#x20; → STRICT / SAFE

&#x20; → REFUSAL

```



\---



\## 🧠 Key Concepts



\* \*\*Fail-closed semantics\*\*: no guessing, no fallback heuristics

\* \*\*Invariant hierarchy\*\*: Φ₀ ⊆ Φ₁ ⊆ … ⊆ Φₖ

\* \*\*Kernel-based admissibility\*\*: inconsistent substates collapse

\* \*\*I\*\*\*: highest admissible level of knowledge



\*\*Modes:\*\*



\* \*\*STRICT\*\* → unique model

\* \*\*SAFE\*\* → multiple consistent models

\* \*\*DEFEASIBLE\*\* → inconsistency → collapse



\---



\## 📄 Paper



Full formal specification:



\[paper/fijnman\_gsa3\_v5.1.1.pdf](paper/fijnman\_gsa3\_v5.1.1.pdf)



Includes:



\* Constitutional core

\* Relational admissibility (RGR / RCR)

\* Execution semantics

\* Formal properties and proofs



\---



\## ⚙️ Implementation



Minimal reference implementation using Z3:



```

src/gsa51\_core.py

```



\### Requirements



```bash

pip install z3-solver

```



\---



\## 🧪 Tests



Run from repository root:



```bash

python tests/test\_muddy\_children.py

python tests/test\_inconsistency.py

python tests/test\_unique\_model.py

python tests/test\_strict.py

python tests/test\_mode\_profile.py

```



All tests are deterministic and demonstrate different admissibility modes (SAFE, STRICT, REFUSAL).



\---



\## 📊 Example Output



```

Outcome: ADMISSIBLE\_LEVEL

Level: 1

Kernel formula: Or(m1, m2)



Models:

{m1: True, m2: False}

{m1: False, m2: True}

{m1: True, m2: True}



Unique model: False

```



\---



\## 🔒 License



GNU Affero General Public License v3.0 (AGPLv3)



This ensures:



\* No closed-source forks

\* No proprietary SaaS without sharing changes

\* Full reciprocity



\---



\## 🌍 Vision



GSA³ is a step toward \*\*structurally reliable reasoning systems\*\*:



\* No hallucinations

\* No silent failures

\* No hidden assumptions



Only admissible structure survives.



\---



\## ⚠️ Status



Research prototype / reference implementation

Not optimized for production use



\---



\## 👤 Author



Natanaël van Dijk



\---



