from z3 import *
from src.gsa51_core import GSA51Core


def main():
    # Variable
    x = Int("x")
    variables = [x]

    # State space: x must be >= 0
    psi = x >= 0

    # Invariants
    phi0 = []                # constitutional
    phi1 = [x >= 0]          # redundant but fine
    phis = [phi0, phi1]

    core = GSA51Core(variables, psi, phis)

    # CONTRADICTION:
    # xi says x < 0, but psi says x >= 0
    xi = x < 0

    result = core.evaluate(xi)

    print("Outcome:", result["outcome"])
    print("Level:", result["level"])
    print("Kernel:", result["kernel"])

    # Assertions
    assert result["outcome"] == "REFUSAL", "Expected REFUSAL"
    assert result["level"] is None, "Expected no admissible level"
    assert result["kernel"] is None, "Expected empty kernel"

    print("\nTest passed (REFUSAL correctly triggered).")


if __name__ == "__main__":
    main()