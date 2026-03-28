from z3 import *
from src.gsa51_core import GSA51Core


def collect_models(formula, variables):
    """Return all models satisfying the given formula."""
    s = Solver()
    s.add(formula)

    models = []
    while s.check() == sat:
        m = s.model()

        snapshot = {str(v): m.eval(v, model_completion=True) for v in variables}
        models.append(snapshot)

        # Block current model
        block = [v != m.eval(v, model_completion=True) for v in variables]
        s.add(Or(block))

    return models


def main():
    # Variables: muddy status of child 1 and child 2
    m1, m2 = Bools("m1 m2")
    variables = [m1, m2]

    # State space: all four combinations are allowed
    psi = BoolVal(True)

    # Invariant hierarchy:
    # Φ0 = constitutional layer (empty => vacuously consistent)
    # Φ1 = epistemic refinement: "at least one child is muddy"
    phi0 = []
    phi1 = [Or(m1, m2)]
    phis = [phi0, phi1]

    core = GSA51Core(variables, psi, phis)

    # Public announcement: at least one child is muddy
    xi = Or(m1, m2)

    result = core.evaluate(xi)

    print("Outcome:", result["outcome"])
    print("Level:", result["level"])

    assert result["outcome"] == "ADMISSIBLE_LEVEL", "Expected admissible outcome"
    assert result["level"] == 1, "Expected highest admissible level to be 1"
    assert result["kernel"] is not None, "Expected a non-empty kernel"

    kernel_formula = simplify(result["kernel"])
    print("Kernel formula:", kernel_formula)

    models = collect_models(kernel_formula, variables)

    print("Models:")
    for model in models:
        print(model)

    # Expected surviving models after the announcement:
    # (m1=True,  m2=False)
    # (m1=False, m2=True)
    # (m1=True,  m2=True)
    assert len(models) == 3, f"Expected 3 models, got {len(models)}"

    normalized = {
        (bool(is_true(model["m1"])), bool(is_true(model["m2"])))
        for model in models
    }

    expected = {
        (True, False),
        (False, True),
        (True, True),
    }

    assert normalized == expected, f"Unexpected model set: {normalized}"

    unique = core.is_unique(xi)
    print("Unique model:", unique)
    assert unique is False, "Expected substate not to be unique"

    print("\nTest passed.")


if __name__ == "__main__":
    main()