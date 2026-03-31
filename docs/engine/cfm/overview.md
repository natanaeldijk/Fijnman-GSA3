# CFM — Overview

## Purpose

The Counterfactual Monitoring Layer (CFM) provides **diagnostics and interpretation** of execution behavior.

CFM does not influence execution.  
It observes and analyzes.

---

## Position in the Architecture

```text
GSA (core)
↓
VCE (execution)
↓
CFM (diagnostics)
```

---

## Core Principle

CFM is **strictly observational**.

- No write access to system state
- No influence on core decisions
- No modification of execution flow

---

## Responsibilities

CFM evaluates:

- rupture conditions
- interference patterns
- behavioral profiles
- stability metrics

---

## Inputs

CFM operates on:

- core outputs (`result`, `x`, `x_new`)
- VCE state
- event history

---

## Outputs

CFM produces:

- diagnostic signals
- classifications
- metrics (e.g. π updates)

---

## Design Constraints

### Non‑Interference

CFM must never alter:

- core logic
- VCE state
- transition outcomes

### Deterministic Analysis

Given the same inputs, CFM must produce the same diagnostics.

---

## Status

- ✅ basic diagnostics implemented
- 🔄 deeper interference modeling planned
- 🔄 integration with VCE event stream planned