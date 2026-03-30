# Fijnman-GSA3

A formal constraint-based reasoning system combining a minimal core (GSA) with a diagnostic extension layer (CFM).

---

## Overview

Fijnman-GSA3 is a structured reasoning framework built around:

* A **minimal admissibility core (GSA)**
* A **mode-based evaluation system (SAFE / STRICT)**
* A **constraint-flow diagnostic layer (CFM)**

The system is designed to study:

* consistency
* defeasible reasoning
* constraint interaction
* model stability

---

## Architecture

```
gsa/      → formal core (GSA51Core)
cfm/      → constraint-flow diagnostics (CFM prototype)
tests/    → verification suite (pytest)
docs/     → formal specifications and theory
paper/    → figures and publication material
```

---

## Core Concepts

### Constraint Admissibility

Determines whether a step is valid within given bounds and constraints.

### Mode Profiles

Each evaluation produces a triple:

```
(SAFE | STRICT, STRICT, STRICT)
```

* **SAFE**: non-critical acceptance
* **STRICT**: logically enforced constraint

---

### Kernel Monotonicity

Ensures that adding constraints does not introduce invalid previously valid states.

---

### Defeasible Reasoning

Supports reasoning under conflicting constraints while maintaining consistency.

---

### Unique Model Convergence

The system converges toward a stable admissible model under repeated updates.

---

## Modules

### GSA Core (`gsa/`)

Implements the formal reasoning system:

* admissibility checking
* mode evaluation
* constraint propagation

---

### CFM Layer (`cfm/`)

Provides diagnostics on top of the core:

* rupture detection
* constraint interference
* update behavior tracking

---

## Testing

All functionality is verified using `pytest`.

### Run all tests

```bash
python -m pytest tests
```

### Run only formal core tests

```bash
python -m pytest tests/gsa
```

---

## Project Structure

```
fijnman-gsa3/
│
├── gsa/
├── cfm/
├── tests/
│   └── gsa/
├── docs/
│   ├── core/
│   ├── formal/
│   ├── engine/
│   └── patch_notes/
├── paper/
│   └── figures/
├── README.md
├── pytest.ini
└── requirements.txt
```

---

## Documentation

Formal definitions and system design are located in:

```
docs/formal/
```

Key topics include:

* admissibility operators
* constraint systems (Φ)
* equivalence and canonical forms
* stability and knowledge dynamics

---

## Figures

All figures used for explanation and publication are stored in:

```
paper/figures/
```

Each figure should have:

* a descriptive filename
* a caption in `paper/figures/README.md`

---

## Status

* Core implementation: **stable**
* Test suite: **passing**
* CFM layer: **prototype**
* Documentation: **in progress**

---

## Purpose

This project explores a structured approach to reasoning systems where:

* constraints define admissibility
* modes define interpretation
* diagnostics reveal structural behavior

---

## Future Work

* Extend CFM diagnostics
* Formalize event grammar
* Expand model semantics
* Prepare full publication

---

## License

To be defined.
