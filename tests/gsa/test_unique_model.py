from z3 import And, Int, Solver, sat
from gsa.core import GSA51Core


def test_unique_model_strict_case():
    x = Int("x")
    variables = [x]

    psi = And(x >= 0, x <= 10)

    phi0 = []
    phi1 = [x >= 0]
    phis = [phi0, phi1]

    core = GSA51Core(variables, psi, phis)

    xi = x == 5
    result = core.evaluate(xi)

    assert result["outcome"] == "ADMISSIBLE_LEVEL"
    assert result["level"] == 1
    assert core.is_unique(xi) is True

    solver = Solver()
    solver.add(result["kernel"])
    assert solver.check() == sat