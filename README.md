# Fijnman-GSA3

![Status](https://img.shields.io/badge/status-research--prototype-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Architecture](https://img.shields.io/badge/architecture-GSA%20%2B%20CFM-purple)
![Docs](https://img.shields.io/badge/docs-in%20progress-orange)
![License](https://img.shields.io/badge/license-AGPL--3.0-red)

A formal constraint-based reasoning system combining a minimal core (GSA) with a non-invasive diagnostic layer (CFM).

---

## 👤 Author

**Natanael van Dijk**

---

## Overview

Fijnman-GSA3 is a structured reasoning framework built around:

- a **minimal admissibility core (GSA)**
- a **mode-based evaluation system**
- a **constraint-flow diagnostic layer (CFM)**

The project is aimed at reasoning under explicit constraints, with a strong focus on:
- admissibility
- consistency
- defeasible reasoning
- model stability
- non-interfering diagnostics

---

## Architecture

```text
gsa/      → formal reasoning core
cfm/      → diagnostic layer
tests/    → verification suite
docs/     → formal specifications
paper/    → figures and publication material
```

The core determines admissibility; the diagnostic layer explains outcomes.

---

## Repository Structure

```text
Fijnman-GSA3/
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

## Core Concepts


### GSA Core

Responsible for:
- admissibility evaluation
- constraint handling
- mode profiling
- kernel behavior
- unique model checks


### CFM Layer

Responsible for:
- rupture detection
- interference analysis
- perspective updates
- explanation without modifying the core

---

## Testing

Run all tests:
```bash
python -m pytest tests


En:

```md
Run GSA-only tests:
```bash
python -m pytest tests/gsa

---

## Documentation

Located in:

- `docs/core/` → minimal definitions  
- `docs/formal/` → theoretical framework  
- `docs/engine/` → system behavior  
- `docs/patch_notes/` → updates  

---

## Paper Material

Located in:
paper/figures/
Contains figures and captions for publication.

---

## Current Status

- Core: stable  
- Tests: passing  
- CFM: prototype  
- Docs: in progress  

---

## Design Goals

- constraint-driven reasoning
- explicit admissibility
- non-invasive diagnostics
- testable formal behavior

---

## Roadmap

- extend CFM diagnostics
- formalize event grammar
- expand documentation
- prepare publication

---

## 🔄 Recent Changes

### 🚀 CFM Flow Implementation

### Added
- Full CFM evaluation pipeline (`cfm_step`)
- `CFMResult` dataclass for structured output
- Interference severity classification (LOW / MEDIUM / HIGH)
- Diagnostic composition:
  - rupture detection
  - interference analysis
  - perspective update (π)

### Updated
- `cfm_step` now returns a structured object instead of dict
- Interference output now includes:
  - raw boundary values
  - qualitative severity classification
- Test suite updated to reflect dataclass-based interface

### Fixed
- Resolved mismatch between dict vs dataclass return type
- Removed duplicate `cfm_step` definitions in tests
- Fixed import issues (`PYTHONPATH=src`)
- Fixed `update_pi` type inconsistency (dict → float bug)

### Tests
- Added tests for:
  - CFM step structure
  - Non-modification of core
  - Interference severity classification
- All tests passing:
 - GSA tests ✅  
 - CFM tests ✅  
 - Integration tests ✅   

### Documentation
- Added formal specification:
  - `docs/formal/cfm_flow.md`
- Defined:
  - pipeline structure
  - output semantics
  - invariants
  - design principles

### Design
- Enforced strict separation:
  - Core = existence (authoritative)
  - CFM = interpretation (read-only)
- Ensured compositional and testable architecture

---

## Conceptual Summary

Core defines reality.  
CFM explains it.

---
## License

### This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

This means:
- You can use, modify, and distribute the code
- If you run it as a service, you must also share your modifications
- The project remains fully open-source

### See the LICENSE file for full details.