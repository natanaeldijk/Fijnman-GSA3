"""
Minimal VCE runner v0.1

Purpose:
- Single entity machine: KnowledgeObject
- Single execution loop
- Fail-closed transition system
- No CFM in execution path (CFM is strictly diagnostic)

This runner is intentionally minimal to establish a correct execution foundation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


# ============================================================
# Exceptions
# ============================================================

class UndefinedTransition(Exception):
    """
    Raised when a transition is not explicitly defined.

    This enforces fail-closed semantics:
    if a transition is not defined, execution must stop.
    """
    pass


# ============================================================
# Core entity state machine
# ============================================================

class KOState(Enum):
    """
    States for the KnowledgeObject lifecycle.
    """
    NONE = "none"
    CANDIDATE = "candidate"
    VALIDATED = "validated"
    REJECTED = "rejected"
    HALTED = "halted"


@dataclass
class KnowledgeObject:
    """
    Minimal representation of a knowledge object.

    Attributes:
        object_id: Unique identifier
        state: Current lifecycle state
        value: Current numeric state (from core)
    """
    object_id: str
    state: KOState = KOState.NONE
    value: Optional[float] = None


# ============================================================
# Event model
# ============================================================

class EventType(Enum):
    """
    Event types for the minimal execution model.
    """
    PROPOSAL_RECEIVED = "proposal_received"
    CORE_EVALUATED = "core_evaluated"
    TRANSITION_APPLIED = "transition_applied"


@dataclass
class Proposal:
    """
    Minimal proposal structure.

    Attributes:
        object_id: Target KnowledgeObject
        x: Current state value
        dx: Proposed step
    """
    object_id: str
    x: float
    dx: float


@dataclass
class Event:
    """
    Event log entry.

    Attributes:
        event_type: Type of event
        object_id: Associated KnowledgeObject
        payload: Arbitrary structured data
    """
    event_type: EventType
    object_id: str
    payload: Dict[str, Any]


# ============================================================
# System state
# ============================================================

@dataclass
class SystemState:
    """
    Minimal system state container.

    Attributes:
        objects: Registry of KnowledgeObjects
        history: Append-only event log
    """
    objects: Dict[str, KnowledgeObject] = field(default_factory=dict)
    history: List[Event] = field(default_factory=list)

    def get_or_create_object(self, object_id: str) -> KnowledgeObject:
        """
        Retrieve an existing object or create a new one.
        """
        if object_id not in self.objects:
            self.objects[object_id] = KnowledgeObject(object_id=object_id)
        return self.objects[object_id]

    def log(self, event: Event) -> None:
        """
        Append an event to the system history.
        """
        self.history.append(event)


# ============================================================
# Transition logic
# ============================================================

def transition_knowledge_object(state: KOState, result: str) -> KOState:
    """
    Fail-closed transition function for KnowledgeObject.

    Rules:
    - REJECT → REJECTED
    - HALT_SPEC_REQUIRED → HALTED
    - ADMISSIBLE:
        NONE → CANDIDATE
        CANDIDATE → VALIDATED
        VALIDATED → VALIDATED (idempotent)

    Any undefined transition raises an error.
    """
    if result == "REJECT":
        return KOState.REJECTED

    if result == "HALT_SPEC_REQUIRED":
        return KOState.HALTED

    if result == "ADMISSIBLE":
        if state == KOState.NONE:
            return KOState.CANDIDATE
        if state == KOState.CANDIDATE:
            return KOState.VALIDATED
        if state == KOState.VALIDATED:
            return KOState.VALIDATED

    raise UndefinedTransition(
        f"Undefined transition for state={state.value!r}, result={result!r}"
    )


# ============================================================
# Runner result
# ============================================================

@dataclass
class RunnerResult:
    """
    Result of a single execution step.

    Attributes:
        object_id: Target object
        old_state: Previous state
        new_state: Resulting state
        result: Core decision
        x_old: Previous value
        x_new: New value
    """
    object_id: str
    old_state: KOState
    new_state: KOState
    result: str
    x_old: float
    x_new: float


# ============================================================
# Minimal VCE runner
# ============================================================

class MinimalVCERunner:
    """
    Minimal VCE execution engine.

    Execution flow:
        Proposal
        → core.step(x, dx)
        → state transition
        → history logging

    Design constraints:
    - Uses only core.step() (no diagnostics layer)
    - Strict fail-closed behavior
    - No implicit transitions or fallbacks
    """

    def __init__(self, core: Any):
        """
        Parameters:
            core: Object exposing .step(x, dx) → (result, x_new)
        """
        self.core = core
        self.system_state = SystemState()

    def run_once(self, proposal: Proposal) -> RunnerResult:
        """
        Execute a single proposal.

        Raises:
            UndefinedTransition if transition is not defined.
        """
        ko = self.system_state.get_or_create_object(proposal.object_id)
        old_state = ko.state

        # Log proposal reception
        self.system_state.log(
            Event(
                event_type=EventType.PROPOSAL_RECEIVED,
                object_id=proposal.object_id,
                payload={
                    "x": proposal.x,
                    "dx": proposal.dx,
                    "old_state": old_state.value,
                },
            )
        )

        # Core evaluation (authoritative)
        result, x_new = self.core.step(proposal.x, proposal.dx)

        self.system_state.log(
            Event(
                event_type=EventType.CORE_EVALUATED,
                object_id=proposal.object_id,
                payload={
                    "result": result,
                    "x_old": proposal.x,
                    "x_new": x_new,
                },
            )
        )

        # Apply state transition
        new_state = transition_knowledge_object(old_state, result)

        ko.state = new_state
        ko.value = x_new

        self.system_state.log(
            Event(
                event_type=EventType.TRANSITION_APPLIED,
                object_id=proposal.object_id,
                payload={
                    "old_state": old_state.value,
                    "new_state": new_state.value,
                    "result": result,
                },
            )
        )

        return RunnerResult(
            object_id=proposal.object_id,
            old_state=old_state,
            new_state=new_state,
            result=result,
            x_old=proposal.x,
            x_new=x_new,
        )


# ============================================================
# Demo usage
# ============================================================

if __name__ == "__main__":
    from gsa.toy_core import Core

    core = Core(lower=-1.0, upper=1.0)
    runner = MinimalVCERunner(core)

    # First admissible step
    r1 = runner.run_once(Proposal(object_id="ko_1", x=0.0, dx=0.2))
    print(r1)

    # Second admissible step
    r2 = runner.run_once(Proposal(object_id="ko_1", x=r1.x_new, dx=0.2))
    print(r2)

    # Rejected step
    r3 = runner.run_once(Proposal(object_id="ko_2", x=0.9, dx=0.2))
    print(r3)

    print("\nEvent history:")
    for event in runner.system_state.history:
        print(event)