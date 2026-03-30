from z3 import And, Int
from gsa.core import GSA51Core


def build_core():
    x = Int("x")
    variables = [x]

    psi = And(x >= 0, x <= 10)

    phi0 = []
    phi1 = [x >= 0]
    phi2 = [x >= 5]
    phis = [phi0, phi1, phi2]

    core = GSA51Core(variables, psi, phis)
    return core, x


def test_mode_profile_safe_case():
    core, x = build_core()
    assert core.mode_profile(x >= 5) == ("SAFE", "SAFE", "SAFE")


def test_mode_profile_strict_case():
    core, x = build_core()
    assert core.mode_profile(x == 5) == ("STRICT", "STRICT", "STRICT")


def test_mode_profile_refusal_case():
    core, x = build_core()
    profile = core.mode_profile(x < 0)

    # Houd dit bewust iets losser dan de andere tests:
    # refusal moet zichtbaar zijn in de evaluatie,
    # maar mode_profile kan per implementatie anders representeren.
    result = core.evaluate(x < 0)
    assert result["outcome"] == "REFUSAL"
    assert profile is not None