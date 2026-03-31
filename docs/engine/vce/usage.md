# VCE — Usage

This guide shows how to use the `MinimalVCERunner` to execute proposals, observe state transitions, and work with the event log.

---

## Basic Example

```python
from gsa.toy_core import Core
from vce.minimal import MinimalVCERunner, Proposal

# Create core (bounds -1..1)
core = Core(lower=-1.0, upper=1.0)

# Create runner
runner = MinimalVCERunner(core)

# First proposal for object "ko_1"
p1 = Proposal(object_id="ko_1", x=0.0, dx=0.2)
result1 = runner.run_once(p1)

print(result1)