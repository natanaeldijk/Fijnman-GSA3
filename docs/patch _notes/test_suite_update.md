# Patch Notes — Test Suite Update

## Added
- Dedicated `tests/gsa/` suite for `GSA51Core`
- Formal pytest conversion of legacy script-based tests:
  - `test_defeasible.py`
  - `test_inconsistency.py`
  - `test_kernel_monotonicity.py`
  - `test_mode_profile.py`
  - `test_modes.py`
  - `test_muddy_children.py`
  - `test_unique_model.py`

## Changed
- Replaced legacy imports:
  - `from src.gsa51_core import GSA51Core`
  with:
  - `from gsa.core import GSA51Core`
- Converted all tests from `main()` script style to pytest function style
- Standardized test location:
  - `tests/gsa/` for formal core tests
  - `tests/` for toy core + CFM tests

## Fixed
- Resolved import path issues via `pytest.ini`
- Corrected strict mode expectation in `test_modes.py`
- Verified compatibility of `GSA51Core` with all migrated tests

## Verified
- `python -m pytest tests/gsa`
- Result: `9 passed`