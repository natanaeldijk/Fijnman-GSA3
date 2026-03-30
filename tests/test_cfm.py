from gsa.core import Core
from cfm.proto import is_rupture, interference, update_pi


def test_cfm_detects_rupture_on_reject():
    assert is_rupture("REJECT") is True
    assert is_rupture("REFUSAL") is True
    assert is_rupture("ADMISSIBLE") is False
    assert is_rupture("HALT_SPEC_REQUIRED") is False


def test_interference_points_to_upper_boundary():
    result = interference(x=0.9, dx=0.2, lower=-1.0, upper=1.0)

    assert "upper" in result
    assert result["upper"] > 0


def test_cfm_does_not_modify_core_result():
    core = Core(lower=-1.0, upper=1.0)

    result_before, x_before = core.step(0.0, 0.2)

    _ = is_rupture(result_before)
    _ = update_pi({"normal": 0.5, "inverted": 0.5}, 0.0, result_before)

    result_after, x_after = core.step(0.0, 0.2)

    assert result_before == result_after
    assert x_before == x_after