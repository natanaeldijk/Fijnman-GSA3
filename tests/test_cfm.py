"""
Tests for CFM diagnostic layer.
"""

import pytest
from gsa.toy_core import Core
from cfm import (
    is_rupture,
    interference,
    classify_interference,
    update_pi,
    cfm_step,
    CFMResult,
)


def test_is_rupture():
    assert is_rupture("REJECT") is True
    assert is_rupture("REFUSAL") is True
    assert is_rupture("ADMISSIBLE") is False
    assert is_rupture("HALT_SPEC_REQUIRED") is False


def test_interference_upper():
    result = interference(0.9, 0.2, -1.0, 1.0)
    assert "upper" in result
    assert result["upper"] == pytest.approx(0.2 / 0.1)


def test_interference_lower():
    result = interference(-0.9, -0.2, -1.0, 1.0)
    assert "lower" in result
    assert result["lower"] == pytest.approx(0.2 / 0.1)


def test_interference_zero():
    result = interference(0.0, 0.0, -1.0, 1.0)
    assert result == {"none": 0.0}


def test_interference_boundary_hit():
    result = interference(1.0, 0.2, -1.0, 1.0)
    assert "upper" in result
    assert result["upper"] == float("inf")


def test_interference_none():
    result = interference(0.5, None, -1.0, 1.0)
    assert result == {"none": 0.0}


def test_interference_nan():
    result = interference(0.5, float("nan"), -1.0, 1.0)
    assert result == {"none": 0.0}


def test_classify_interference():
    assert classify_interference(0.2) == "LOW"
    assert classify_interference(0.7) == "MEDIUM"
    assert classify_interference(1.5) == "HIGH"


def test_update_pi():
    assert update_pi(0.0, 0.5, True) == pytest.approx(0.05)
    assert update_pi(0.0, 0.5, False) == pytest.approx(0.0)
    assert update_pi(0.9, 0.5, True) == pytest.approx(0.95)
    assert update_pi(-0.9, -0.5, True) == pytest.approx(-0.95)


def test_update_pi_custom_learning_rate():
    assert update_pi(0.0, 0.5, True, learning_rate=1.0) == pytest.approx(0.5)


def test_cfm_step_structure():
    core = Core(lower=-1.0, upper=1.0)
    result = cfm_step(core, 0.0, 0.2, 0.0)
    assert isinstance(result, CFMResult)
    assert isinstance(result.result, str)
    assert isinstance(result.x_new, float)
    assert isinstance(result.rupture, bool)
    assert isinstance(result.interference, dict)
    assert "values" in result.interference
    assert "severity" in result.interference
    assert isinstance(result.pi, float)


def test_cfm_step_does_not_modify_core():
    core = Core(lower=-1.0, upper=1.0)
    result1 = cfm_step(core, 0.0, 0.2, 0.0)
    result2 = cfm_step(core, 0.0, 0.2, 0.0)
    assert result1.result == result2.result
    assert result1.x_new == result2.x_new


def test_cfm_step_rupture_on_reject():
    core = Core(lower=-1.0, upper=1.0)
    result = cfm_step(core, 0.9, 0.2, 0.0)
    assert result.result == "REJECT"
    assert result.rupture is True
    assert result.x_new == 0.9
    assert "upper" in result.interference["values"]
    assert result.interference["severity"] == "HIGH"


def test_cfm_step_admissible():
    core = Core(lower=-1.0, upper=1.0)
    result = cfm_step(core, 0.0, 0.2, 0.0)
    assert result.result == "ADMISSIBLE"
    assert result.rupture is False
    assert result.x_new == 0.2
    assert "upper" in result.interference["values"]
    assert result.interference["severity"] in {"LOW", "MEDIUM", "HIGH"}


def test_cfm_step_pi_update_on_accept():
    core = Core(lower=-1.0, upper=1.0)
    result = cfm_step(core, 0.0, 0.2, 0.0)
    assert result.pi == pytest.approx(0.02)


def test_cfm_step_handles_none_dx():
    core = Core(lower=-1.0, upper=1.0)
    result = cfm_step(core, 0.0, None, 0.0)
    assert result.result == "HALT_SPEC_REQUIRED"
    assert result.rupture is False
    assert result.x_new == 0.0
    assert result.interference["values"] == {"none": 0.0}
    assert result.interference["severity"] == "LOW"
    assert result.pi == pytest.approx(0.0)