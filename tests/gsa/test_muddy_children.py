from z3 import BoolVal, Bools, Or, Solver, is_true, sat
from gsa.core import GSA51Core


def collect_models(formula, variables):
    solver = Solver()
    solver.add(formula)

    models = []
    while solver.check() == sat:
        model = solver.model()
        snapshot = {str(v): model.eval(v, model_completion=True) for v in variables}
        models.append(snapshot)

        block = [v != model.eval(v, model_completion=True) for v in variables]
        solver.add(Or(block))

    return models


def test_muddy_children_public_announcement():
    m1, m2 = Bools("m1 m2")
    variables = [m1, m2]

    psi = BoolVal(True)

    phi0 = []
    phi1 = [Or(m1, m2)]
    phis = [phi0, phi1]

    core = GSA51Core(variables, psi, phis)

    xi = Or(m1, m2)
    result = core.evaluate(xi)

    assert result["outcome"] == "ADMISSIBLE_LEVEL"
    assert result["level"] == 1
    assert result["kernel"] is not None

    kernel_formula = result["kernel"]
    models = collect_models(kernel_formula, variables)

    assert len(models) == 3

    normalized = {
        (bool(is_true(model["m1"])), bool(is_true(model["m2"])))
        for model in models
    }

    expected = {
        (True, False),
        (False, True),
        (True, True),
    }

    assert normalized == expected
    assert core.is_unique(xi) is False