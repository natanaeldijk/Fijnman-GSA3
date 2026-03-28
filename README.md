\# Fijnman-GSA³ v5.1.1



\*\*A Fail-Closed Framework for Structural Reasoning\*\*



A layered symbolic framework for admissibility-based reasoning systems.

GSA³ eliminates hallucinations by enforcing \*\*fail-closed semantics\*\*, replacing truth with \*\*structural invariance\*\* as the criterion for admissibility.



\---



\## 🔑 Core Idea



Instead of asking whether a statement is \*true\*, GSA³ asks:



> \*\*Is this state structurally admissible under invariant constraints?\*\*



If not → \*\*REFUSAL\*\*



\---



\## 🧠 Key Concepts



\* \*\*Fail-closed semantics\*\*: no guessing, no fallback heuristics

\* \*\*Invariant hierarchy\*\*: ( \\Phi\_0 \\subseteq \\Phi\_1 \\subseteq \\dots \\subseteq \\Phi\_k )

\* \*\*Kernel-based admissibility\*\*: inconsistent substates collapse

\* \*\*I\*\*\*: highest admissible level of knowledge

\* \*\*Modes\*\*:



&#x20; \* \*\*STRICT\*\* → unique model

&#x20; \* \*\*SAFE\*\* → multiple consistent models

&#x20; \* \*\*DEFEASIBLE\*\* → inconsistency → collapse



\---



\## 📄 Paper



Full formal specification:



```

paper/fijnman\_gsa3\_v5.1.1.pdf

```



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



