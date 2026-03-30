from gsa.core import Core


def test_core_accepts_valid_step():
    core = Core(lower=-1.0, upper=1.0)

    result, x_new = core.step(0.0, 0.2)

    assert result == "ADMISSIBLE"
    assert x_new == 0.2


def test_core_rejects_out_of_bounds_step():
    core = Core(lower=-1.0, upper=1.0)

    result, x_new = core.step(0.9, 0.2)

    assert result == "REJECT"
    assert x_new == 0.9