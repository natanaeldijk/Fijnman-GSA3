# Execution Loop

## Purpose

The execution loop is the heart of the VCE. It takes proposals, invokes the core, updates the system state according to the fail‑closed transition rules, and logs every event. The loop is minimal by design, establishing a correct foundation for future extensions (e.g., CFM diagnostics, persistence, export).

---

## Runner

The `MinimalVCERunner` orchestrates the execution. It holds a reference to the core (which must implement `step(x, dx) → (result, x_new)`) and the system state container.

**Invariant**: The runner never modifies the core’s behavior; it only consumes its outputs.

---

## Execution Flow

A single step consists of:

1. **Receive a `Proposal`**  
   A proposal targets a `KnowledgeObject` by `object_id` and contains the current value `x` and a proposed step `dx`.

2. **Retrieve or create the `KnowledgeObject`**  
   The runner looks up the object in the system state registry. If it does not exist, a new `KnowledgeObject` with state `NONE` is created.  
   **The runner is responsible for initializing objects lazily. No object exists without being explicitly referenced by a proposal.**

3. **Log `PROPOSAL_RECEIVED` event**  
   The event records the proposal details and the object’s state before evaluation.

4. **Call `core.step(x, dx)`**  
   The core evaluates the proposal and returns a `result` and the new value `x_new`.

5. **Log `CORE_EVALUATED` event**  
   The event records the core’s decision and the resulting `x_new`.

6. **Apply transition**  
   The runner calls `transition_knowledge_object(old_state, result)` to determine the new state. If the transition is undefined, an `UndefinedTransition` exception is raised, halting execution.

7. **Update the `KnowledgeObject`**  
   The object’s `state` and `value` are updated accordingly.

8. **Log `TRANSITION_APPLIED` event**  
   The event records the state change and the core result.

9. **Return a `RunnerResult`**  
   The result contains all relevant information for the step.

---

## Event Model

Events are append‑only and stored in the system state’s history. They provide a complete audit trail.

| Event Type              | Payload                                                      |
|-------------------------|--------------------------------------------------------------|
| `PROPOSAL_RECEIVED`     | `x`, `dx`, `old_state`                                       |
| `CORE_EVALUATED`        | `result`, `x_old`, `x_new`                                   |
| `TRANSITION_APPLIED`    | `old_state`, `new_state`, `result`                           |

Events are immutable once recorded. They form an append‑only log and must never be modified or deleted.

Events are used for:
- Debugging
- Reproducing runs
- Later integration with CFM (as an observer)

---

## System State

The `SystemState` container holds:

- `objects`: a dictionary mapping `object_id` to `KnowledgeObject`
- `history`: an append‑only list of events

The state is the **single source of truth** for the current execution. All external representations (export, diagnostics) are derived from it.

---

## Fail‑Closed Guarantees

- If `core.step` returns an unexpected result (outside `ADMISSIBLE`, `REJECT`, `HALT_SPEC_REQUIRED`), the runner will treat it as undefined (but the core itself is trusted to return only these).
- If `transition_knowledge_object` does not define the combination, an exception is raised.
- No fallback logic is executed; the system halts on any undefined situation.

---

## Example

```python
from gsa.toy_core import Core
from vce.minimal import MinimalVCERunner, Proposal

core = Core(lower=-1.0, upper=1.0)
runner = MinimalVCERunner(core)

# First admissible step
result = runner.run_once(Proposal(object_id="ko_1", x=0.0, dx=0.2))
print(result)   # RunnerResult with old_state=NONE, new_state=CANDIDATE, result=ADMISSIBLE, x_new=0.2

# Second admissible step → becomes VALIDATED
result = runner.run_once(Proposal(object_id="ko_1", x=0.2, dx=0.2))
print(result)   # new_state=VALIDATED

# Rejected step → becomes REJECTED
result = runner.run_once(Proposal(object_id="ko_2", x=0.9, dx=0.2))
print(result)   # new_state=REJECTED