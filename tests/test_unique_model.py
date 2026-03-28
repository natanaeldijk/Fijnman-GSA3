from z3 import *
from src.gsa51_core import GSA51Core


def main():
    # Variable
    x = Int("x")
    variables = [x]

    # State space
    psi = And(x >= 0, x <= 10)

    # Invariants
    phi0 = []              # constitutional
    phi1 = [x >= 0]        # trivial refinement
    phis = [phi0, phi1]

    core = GSA51Core(variables, psi, phis)

    # Constraint: exactly one value
    xi = (x == 5)

    result = core.evaluate(xi)

    print("Outcome:", result["outcome"])
    print("Level:", result["level"])
    print("Kernel:", result["kernel"])

    assert result["outcome"] == "ADMISSIBLE_LEVEL"
    assert result["level"] == 1

    # Check uniqueness
    unique = core.is_unique(xi)
    print("Unique model:", unique)

    assert unique is True, "Expected exactly one model"

    # Show model
    s = Solver()
    s.add(result["kernel"])

    if s.check() == sat:
        print("Model:", s.model())
    else:
        print("Unexpected: no model found")

    print("\nTest passed (STRICT case achieved).")


if __name__ == "__main__":
    main()