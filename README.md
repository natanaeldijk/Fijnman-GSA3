# Constraint-Flow Model (CFM) + GSA Core

> A fail-closed reasoning system with a non-interfering diagnostic layer.

---

## 🧠 Overview

This repository implements a **two-layer architecture**:

- **GSA Core** → determines admissibility (existence)
- **CFM Layer** → explains outcomes (diagnostic only)

This enforces the central principle:

> **The core determines existence; CFM explains it.**

---

## 🧱 Architecture

         +----------------------+
         |   CFM (Diagnostic)   |
         |----------------------|
         | - rupture analysis   |
         | - interference       |
         | - perspective (Π)    |
         +----------↑-----------+
                    |
                    | read-only
                    |
         +----------↓-----------+
         |     GSA Core         |
         |----------------------|
         | - constraints (Ω)    |
         | - transitions (Θ)    |
         | - fail-closed logic  |
         +----------------------+


### Key Property

- CFM has **read-only access**
- CFM **cannot modify** core behavior
- Core output is **final and authoritative**

---

## 📁 Project Structure

fijnman-gsa3/
├── paper/ # Formal theory (LaTeX, PDF, figures)
├── src/
│ ├── gsa/ # Core reasoning system (existence)
│ └── cfm/ # Diagnostic layer (analysis)
├── tests/ # Verification
├── README.md
├── pytest.ini

---

## ⚙️ Components

### 🔹 GSA Core (`src/gsa/`)

Contains:

- `GSA51Core` → formal symbolic reasoning system
- `Core` → minimal 1D fail-closed prototype

Behavior:

- Returns:
  - `ADMISSIBLE`
  - `REJECT`
- No guessing
- No repair
- No implicit assumptions

---

### 🔹 CFM Layer (`src/cfm/`)

Implements:

- **Rupture detection**
- **Constraint interference**
- **Perspective distribution (Π)**

Example:

```python
is_rupture(output)
interference(x, dx, lower, upper)
update_pi(pi, x, output)
```

---

🚫 Strict Constraints (CFM)

CFM is forbidden to:

modify core state
change core output
repair invalid inputs
infer missing data

---

🧪 Tests

Run:

python -m pytest tests

Verified:

✅ fail-closed behavior
✅ boundary rejection
✅ rupture detection
✅ interference correctness
✅ non-interference guarantee

---

🧪 Prototype Model

Current simulation:

State: x ∈ ℝ
Constraints:
x ≥ -1
x ≤ 1
Transition: x → x + Δx

CFM detects:

rupture when bounds violated
dominant constraint causing failure

---

📄 Formal Model

Located in:

paper/

Defines:

Flow
Constraints
Stability
Rupture
Interference
Perspective distribution (Π)

---

🖼️ Figures
paper/figures/

Contains diagrams used in the paper:

flow visualization
constraint space
rupture examples

---

🔬 Theoretical Guarantees
Non-Interference

CFM does not affect the core:

∂(Core Output) / ∂(CFM) = 0
Fail-Closed Semantics

If constraints are violated:

→ REJECT
→ no state update

---

🚧 Status

CFM Proto v0.1

✅ executable
✅ tested
✅ structurally correct
✅ aligned with formal theory

---

🔮 Roadmap

Next steps:

HALT vs REJECT vs REFUSAL separation
structured rupture objects
flow tracking (time series)
perspective learning (Bayesian refinement)
visualization tools

---

🧠 Design Philosophy

This system is built on:

explicit constraints over implicit assumptions
fail-closed reasoning
separation of decision and interpretation

---

