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



\## 📌 Executive Summary



\*\*Fijnman-GSA³ v5.1.1\*\*  

\*Architect: Natanaël van Dijk\*



\### Core Thesis



In safety-critical reasoning, admissibility must take precedence over truth.



Systems should only produce outputs when structural consistency can be guaranteed.  

Otherwise, they must refuse.



\---



\### 1. The Structural Problem



Contemporary AI systems (including LLMs) operate in a fail-open manner.



When faced with:

\- incomplete information  

\- conflicting constraints  



they attempt probabilistic completion.



This leads to:

\- \*\*Hallucinations\*\* — implicit assumptions introduced without justification  

\- \*\*Epistemic fragility\*\* — inconsistent outputs from identical inputs  



\---



\### 2. The GSA³ Approach: Fail-Closed Reasoning



Fijnman-GSA³ introduces a layered symbolic framework for admissibility-based reasoning.



\*\*Key components:\*\*



\- \*\*Invariant hierarchy (Φᵢ)\*\*  

&#x20; Φ₀ ⊆ Φ₁ ⊆ … ⊆ Φₖ  



\- \*\*Level-relative admissibility (I\\\*)\*\*  

&#x20; The system selects the highest level at which the state remains consistent  



\- \*\*Kernel-based reasoning\*\*  

&#x20; Inconsistent substates collapse; only admissible structure remains  



If no admissible level exists → \*\*REFUSAL\*\*



\---



\### 3. Mechanized Verification



GSA³ is executable and solver-backed.



\- \*\*Symbolic state space\*\* — states are logical formulas (Ψ)  

\- \*\*SMT-based validation\*\* — Z3 checks consistency and uniqueness  

\- \*\*Deterministic execution\*\* — restricted to decidable fragments  



\---



\### 4. Strategic Implications



\- \*\*Reliability by refusal\*\*  

&#x20; No output without structural justification  



\- \*\*Safety-first reasoning\*\*  

&#x20; Designed for domains where wrong answers are unacceptable  



\- \*\*Open and protected\*\*  

&#x20; Released under AGPLv3 to prevent proprietary enclosure  



\---



\*\*GSA³ reframes reasoning:\*\*



Not \*what is likely true\*  

but  

\*\*what is structurally admissible\*\*



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



Visual overview of the fail-closed reasoning pipeline:


```plaintext
State Space (Ψ)
   |
   v
Apply Constraints (Ξ)
   |
   v
Substate S'
   |
   v
Check Φᵢ-Consistency
   |
   +----------------------+
   |                      |
   v                      v
Consistent           Inconsistent
   |                      |
   v                      v
Kernel K^(i)(S')     Collapse
   |                      |
   v                      v
Select I*             REFUSAL
   |
   v
+---------+
|         |
v         v
STRICT   SAFE
(unique) (multiple)
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

python -m tests.test\_muddy\_children

python -m tests.test\_inconsistency

python -m tests.test\_unique\_model

python -m tests.test\_strict

python -m tests.test\_mode\_profile

python -m tests.test\_defeasible

python -m tests.test\_kernel\_monotonicity

```



All tests are deterministic and demonstrate the behavior of the fail-closed reasoning pipeline.



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



\## 🌐 Applications



GSA³ is designed for domains where \*\*guessing is more dangerous than refusal\*\*.



\### Possible application areas



\- \*\*LLM reasoning safety\*\*  

&#x20; As a validation layer that filters outputs and refuses structurally unsupported conclusions.



\- \*\*Agent systems\*\*  

&#x20; For workflows where actions should only be taken when the underlying state is admissible under explicit constraints.



\- \*\*Knowledge validation\*\*  

&#x20; For systems that need to distinguish between consistent, inconsistent, and underdetermined states without relying on probability.



\- \*\*Formal reasoning tools\*\*  

&#x20; As a fail-closed core for symbolic reasoning environments, theorem-oriented workflows, or constraint-based analysis.



\- \*\*Human-in-the-loop systems\*\*  

&#x20; Where the system should stop and defer rather than fabricate an answer.



\### Why this matters



Many systems are optimized to always return something.  

GSA³ is built for situations where returning the wrong thing is worse than returning nothing.



In those settings, \*\*refusal is not failure — it is a reliability condition.\*\*



\---



\## ❓ Why not probability?



Many reasoning systems rely on probabilistic models to handle uncertainty.



GSA³ takes a different approach.



Instead of asking:

> "What is most likely true?"



it asks:

> "What is structurally admissible under invariant constraints?"



\### Key difference



\- Probabilistic systems assign confidence to conclusions, even when the structure is incomplete or inconsistent.

\- GSA³ enforces structural validity first — if admissibility cannot be established, the system refuses.



\### Why this matters



Probabilities can still produce answers under:

\- incomplete information  

\- conflicting constraints  

\- underdetermined states  



GSA³ does not.



If a conclusion is not supported by the invariant structure, it is rejected.



\### Design principle



> In safety-critical or correctness-critical systems,

> a wrong answer is worse than no answer.



GSA³ is designed for those settings.



This makes GSA³ fundamentally different from systems that optimize for completion rather than correctness.



\---



\## ⚠️ Status



Research prototype / reference implementation

Not optimized for production use



\---



\## 👤 Author



Natanaël van Dijk



\---



