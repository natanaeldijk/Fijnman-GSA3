from unittest import result

from gsa.core import Core
from cfm import (
    is_rupture,
    interference,
    update_pi,
    cfm_step,
    classify_interference,
)


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
    _ = update_pi(0.0, 0.0, result_before == "ADMISSIBLE")

    result_after, x_after = core.step(0.0, 0.2)

    assert result_before == result_after
    assert x_before == x_after


def test_interference_points_to_upper_boundary():
    result = interference(x=0.9, dx=0.2, lower=-1.0, upper=1.0)

    assert "upper" in result
    assert result["upper"] > 0


def test_interference_points_to_lower_boundary():
    result = interference(x=-0.9, dx=-0.2, lower=-1.0, upper=1.0)

    assert "lower" in result
    assert result["lower"] > 0


def test_interference_zero_motion():
    result = interference(x=0.0, dx=0.0, lower=-1.0, upper=1.0)

    assert result == {"none": 0.0}


def test_update_pi_accepts_step():
    assert update_pi(0.0, 0.5, True) == 0.5


def test_update_pi_rejects_step():
    assert update_pi(0.0, 0.5, False) == 0.0


def test_cfm_step_runs_and_returns_structure():
    core = Core(lower=-1.0, upper=1.0)

    result = cfm_step(core, x=0.0, dx=0.2, pi=0.0)

    assert result.result is not None
    assert result.x_new is not None
    assert hasattr(result, "rupture")
    assert hasattr(result, "interference")
    assert hasattr(result, "pi")


def test_cfm_step_does_not_modify_core():
    core = Core(lower=-1.0, upper=1.0)

    result1 = cfm_step(core, 0.0, 0.2, 0.0)
    result2 = cfm_step(core, 0.0, 0.2, 0.0)

    assert result1.result == result2.result


def test_classify_interference_low():
    assert classify_interference(0.2) == "LOW"


def test_classify_interference_medium():
    assert classify_interference(0.7) == "MEDIUM"


def test_classify_interference_high():
    assert classify_interference(1.5) == "HIGH"


def test_cfm_result_structure():
    core = Core(lower=-1.0, upper=1.0)
    res = cfm_step(core, 0.0, 0.2, 0.0)

    assert isinstance(res.result, str)
    assert isinstance(res.rupture, bool)
    assert isinstance(res.pi, float)