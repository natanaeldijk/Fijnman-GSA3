# Event Grammar

## Rule

No implicit state mutation  
Undefined transition → HALT_SPEC_REQUIRED  

---

## Event Structure

Event e = (
  event_id,
  event_type,
  entity_id,
  payload,
  timestamp,
  proposal_status,
  validator_status
)

---

## Event Types

reasoning_unit_extracted  
reasoning_unit_typed  
relation_detected  
conflict_detected  
boundary_detected  
convergence_detected  

relation_proposed  
knowledge_object_proposed  
knowledge_object_promoted  

validator_fail  
halt_spec_required  
refusal_triggered  

archive_requested  
supersession_requested  
projection_requested  