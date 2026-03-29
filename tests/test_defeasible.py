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

    xi = Or(x == 4, x == 6)

    profile = core.mode_profile(xi)
    level, _ = core.admissibility_level(xi)

    print("Mode profile:", profile)
    print("Level:", level)

    assert profile == ("SAFE", "SAFE", "DEFEASIBLE")
    assert level == 1

    print("\nTest passed.")


if __name__ == "__main__":
    main()