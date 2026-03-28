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



🧍 Simple Explanation (Non-Technical)



Most systems today try to give an answer, even when they are unsure.



That’s why you get:



wrong answers

contradictions

made-up explanations (“hallucinations”)

What GSA³ does differently



GSA³ does not try to always answer.



Instead, it asks:



“Do I have enough consistent information to justify an answer?”



If the answer is yes → it responds

If the answer is no → it refuses



Example



Imagine someone asks:



“Is this statement correct?”



A typical system might guess or give a confident answer.



GSA³ will instead:



check whether the information is consistent

check whether the constraints are satisfied

only answer if everything aligns



Otherwise:



REFUSAL



Why this is important



It means:



No guessing

No hidden assumptions

No confident nonsense



Only answers that are structurally justified.



In one sentence



GSA³ would rather say “I don’t know” than give a wrong answer.



\---



\## 🔄 Pipeline Overview



1\. \*\*State space (Ψ)\*\*  

2\. \*\*Apply constraints (Ξ)\*\*  

3\. \*\*Substate S'\*\*  

4\. \*\*Check Φᵢ-consistency\*\*  

5\. \*\*Compute kernel K⁽ⁱ⁾(S')\*\*  

6\. \*\*Select I\*\*\*  



\*\*Outcome:\*\*

\- \*\*STRICT / SAFE\*\*  

\- \*\*REFUSAL\*\*



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



