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

    kernels = [core.kernel(xi, i)[0] for i in range(len(phis))]

    print("Kernel non-emptiness:", kernels)

    assert kernels == [True, True, False]

    print("\nTest passed.")


if __name__ == "__main__":
    main()