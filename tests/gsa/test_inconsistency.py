from z3 import Int
from gsa.core import GSA51Core


def test_inconsistency_triggers_refusal():
    x = Int("x")
    variables = [x]

    psi = x >= 0

    phi0 = []
    phi1 = [x >= 0]
    phis = [phi0, phi1]

    core = GSA51Core(variables, psi, phis)

    xi = x < 0
    result = core.evaluate(xi)

    assert result["outcome"] == "REFUSAL"
    assert result["level"] is None
    assert result["kernel"] is None