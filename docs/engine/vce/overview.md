# Vault Continuity Engine — Overview

## Purpose

The Vault Continuity Engine (VCE) is an execution layer that provides **continuity of state** across multiple steps and sessions. It maintains a persistent internal state of knowledge objects, enforces fail‑closed transitions, and optionally projects that state into human‑readable formats.

The VCE does not replace the core (GSA); it sits **above** it, using the core as the authoritative evaluator of proposals.

---

## Core Principles

### Execution is Authoritative

Only proposals that pass the core’s admissibility check can change the system state. The core’s output (`ADMISSIBLE`, `REJECT`, `HALT_SPEC_REQUIRED`) is final and non‑negotiable.

### Fail‑Closed Behavior

Any undefined transition (a combination of state and core result not explicitly defined) raises an exception and halts execution. No implicit fallback, no guesswork.

### Internal State as Source of Truth

The VCE’s internal `SystemState` (objects and event history) is the single authoritative representation. External representations (e.g., markdown exports, JSON dumps) are derived projections and must never be used to modify the state directly.

### Separation of Concerns

- **Core** – evaluates proposals (stateless, pure)
- **VCE** – manages state continuity and execution flow
- **CFM** – (optional) reads state for diagnostics; never writes

---

## Six‑Layer Architecture

The VCE is structured into six logical layers, each with a clear responsibility. This separation ensures modularity and testability.

| Layer               | Responsibility                                                                                      | Status           |
|---------------------|-----------------------------------------------------------------------------------------------------|------------------|
| **Source Layer**    | Incoming proposals (from user, LLM, script).                                                        | Implemented      |
| **Interpretation Layer** | Maps source inputs to system mutatations (e.g., `create`, `revise`, `promote`).                  | Placeholder      |
| **State Layer**     | Holds `SystemState`: `KnowledgeObject` registry and event history.                                 | Implemented      |
| **Update Engine**   | Applies transitions (`transition_knowledge_object`) based on core result.                          | Implemented      |
| **Export Layer**    | Projects internal state to external formats (markdown, JSON).                                      | Planned          |
| **Session Context** | Selects relevant state for the next session (e.g., for LLM context injection).                     | Future           |

The **Interpretation Layer** and **Session Context** are intentionally minimal in v0.1; they will be expanded as the system matures.

---

## Relation to Other Components


- The **core** is stateless and authoritative.
- The **VCE** maintains state and uses the core as a pure function.
- **CFM** can observe the VCE’s state and events to produce diagnostics, but never modifies the core or VCE state.  
  CFM is strictly observational and has no write access to the system state.

---

## Design Decisions

### No External Tool Dependency

The VCE does not rely on Obsidian, Notion, or any external tool. Internal state is kept in memory (or later in a simple persistence layer). Export to markdown is optional and decoupled.

### Idempotence

Transitions are idempotent where appropriate (e.g., `VALIDATED` stays `VALIDATED` on further `ADMISSIBLE`). This prevents state churn.

### Append‑Only History

All events are logged in an append‑only history, enabling replay, debugging, and later analysis (e.g., by CFM).

---

## Current Status

- ✅ `KnowledgeObject` lifecycle and transition logic  
- ✅ `MinimalVCERunner` with event logging  
- ✅ Integration with `gsa.toy_core.Core`  
- 🔄 Export layer (planned)  
- 🔄 Interpretation layer (placeholder)  
- 🔄 CFM observer integration (planned)

---

## Getting Started

See [`usage.md`](./usage.md) for practical examples and [`execution_loop.md`](./execution_loop.md) for a detailed walkthrough of the runner.