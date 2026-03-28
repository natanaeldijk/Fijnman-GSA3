from z3 import *
from src.gsa51_core import GSA51Core


def main():
    x = Int("x")
    variables = [x]

    psi = And(x >= 0, x <= 10)

    phi0 = []
    phi1 = [x >= 0]
    phi2 = [x >= 5]

    phis = [phi0, phi1, phi2]

    core = GSA51Core(variables, psi, phis)

    # Case 1: multiple models
    xi1 = x >= 5
    print("Case SAFE:", core.mode_profile(xi1))

    # Case 2: unique model
    xi2 = x == 5
    print("Case STRICT:", core.mode_profile(xi2))

    # Case 3: inconsistency
    xi3 = x < 0
    print("Case REFUSAL:", core.mode_profile(xi3))


if __name__ == "__main__":
    main()