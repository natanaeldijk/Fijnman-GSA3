...
## Mid Term (v0.7 – v0.9)

- **CFM Integration (Observer Mode)**  
  Attach CFM as a read‑only observer that receives events and can compute diagnostics (rupture, interference, perspective). This will be implemented without modifying the runner’s core loop.

- **Richer Transition System**  
  Extend the state machine to support more granular statuses (e.g., `ARCHIVED`, `DEPRECATED`) and more complex transition rules, while preserving fail‑closed semantics.

- **Interpretation Layer**  
  Implement the `Interpretation Layer` to map natural language proposals or structured commands into system mutations. This will be a pluggable component.

- **Session Context Selection**  
  Develop algorithms to select the most relevant knowledge objects and events to feed into a new LLM session, enabling true continuity.

- **Deterministic replay from event history**  
  Use the append‑only event log to replay a full execution, enabling reproducible debugging and validation.
...