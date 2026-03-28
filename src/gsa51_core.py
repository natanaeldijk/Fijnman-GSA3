"""
GSA³ v5.1.1 – Constitutional Core
Reference implementation using Z3.

Key fail-closed semantics:
- unsat  -> empty / no admissible state
- sat    -> constructible state exists
- unknown -> refusal
"""

from z3 import *


class RefusalError(Exception):
    """Raised when the solver cannot decide and the framework must refuse."""
    pass


class GSA51Core:
    def __init__(self, variables, psi, phis):
        """
        variables: list of Z3 variables (e.g., [x, y, ...])
        psi: Z3 formula defining state space S = {σ | ψ(σ)}
        phis: list of lists of Z3 formulas, where:
              phis[0] = constitutional invariants Φ₀
              phis[1..] = epistemic refinements Φ₁, Φ₂, ...
        """
        if not variables:
            raise ValueError("variables must be explicitly provided and non-empty")
        if not phis:
            raise ValueError("phis must be a non-empty invariant hierarchy")

        self.vars = variables
        self.psi = psi
        self.phis = phis
        self.k = len(phis) - 1

    def _copy_vars(self, suffix):
        """Create fresh copies of variables with given suffix."""
        return [Const(v.decl().name() + suffix, v.sort()) for v in self.vars]

    def _subst(self, formula, old_vars, new_vars):
        """Substitute variables in a formula."""
        return substitute(formula, *zip(old_vars, new_vars))

    def _sat_status(self, formula):
        """
        Return solver status for a formula:
        - sat
        - unsat
        - raises RefusalError on unknown
        """
        s = Solver()
        s.add(formula)
        result = s.check()

        if result == unknown:
            raise RefusalError("solver returned unknown")
        return result

    def _has_model(self, xi):
        """
        Return True iff ψ ∧ ξ has at least one model.
        Raises RefusalError if solver returns unknown.
        """
        return self._sat_status(And(self.psi, xi)) == sat

    def _check_consistency(self, xi, level):
        """
        Return True iff S' = {σ | ψ(σ) ∧ ξ(σ)} is Φ_level-consistent.

        IMPORTANT:
        - This checks consistency only; emptiness is handled separately.
        - If the solver returns unknown, we refuse.
        """
        if level < 0 or level > self.k:
            raise IndexError(f"level {level} out of bounds")

        # Empty invariant layer is vacuously consistent
        if not self.phis[level]:
            return True

        vars1 = self._copy_vars("_1")
        vars2 = self._copy_vars("_2")

        psi1 = self._subst(self.psi, self.vars, vars1)
        psi2 = self._subst(self.psi, self.vars, vars2)
        xi1 = self._subst(xi, self.vars, vars1)
        xi2 = self._subst(xi, self.vars, vars2)

        s = Solver()
        s.add(psi1, xi1, psi2, xi2)

        # Look for two admissible states with differing Φ-values
        disjuncts = []
        for phi in self.phis[level]:
            phi1 = self._subst(phi, self.vars, vars1)
            phi2 = self._subst(phi, self.vars, vars2)
            disjuncts.append(phi1 != phi2)

        s.add(Or(disjuncts))
        result = s.check()

        if result == unknown:
            raise RefusalError("solver returned unknown during consistency check")

        # If no differing pair exists, S' is Φ-consistent
        return result == unsat

    def kernel(self, xi, level):
        """
        Return (nonempty, formula) where:
        - nonempty = True iff K^(level)(S') is non-empty
        - formula = And(ψ, ξ) when non-empty, else None

        By v5.0+ semantics:
        - If S' is empty, kernel is empty
        - If S' is non-empty and Φ-consistent, kernel is S'
        - Otherwise kernel is empty
        """
        # First: does S' exist at all?
        if not self._has_model(xi):
            return (False, None)

        # Then: is S' Φ-consistent at this level?
        if self._check_consistency(xi, level):
            return (True, And(self.psi, xi))
        else:
            return (False, None)

    def admissibility_level(self, xi):
        """
        Return (I*, kernel_formula) or (None, None) if no admissible level exists.

        Raises RefusalError if a solver call returns unknown.
        """
        for level in range(self.k, -1, -1):
            nonempty, rep = self.kernel(xi, level)
            if nonempty:
                return level, rep
        return None, None

    def evaluate(self, xi):
        """
        High-level fail-closed evaluation.

        Returns a dict:
        - {"outcome": "ADMISSIBLE_LEVEL", "level": i, "kernel": formula}
        - {"outcome": "REFUSAL", "level": None, "kernel": None}
        """
        try:
            level, kernel_formula = self.admissibility_level(xi)
            if level is None:
                return {
                    "outcome": "REFUSAL",
                    "level": None,
                    "kernel": None,
                }
            return {
                "outcome": "ADMISSIBLE_LEVEL",
                "level": level,
                "kernel": kernel_formula,
            }
        except RefusalError:
            return {
                "outcome": "REFUSAL",
                "level": None,
                "kernel": None,
            }

    def invariant_signature(self, model, level):
        """Return tuple of Φ_level values for a given model."""
        if level < 0 or level > self.k:
            raise IndexError(f"level {level} out of bounds")
        return tuple(model.eval(phi, model_completion=True) for phi in self.phis[level])

    def is_unique(self, xi):
        """
        Return True iff ψ ∧ ξ has exactly one model.

        Fail-closed:
        - if no model exists -> False
        - if unknown -> raises RefusalError
        """
        # First check existence of at least one model
        if not self._has_model(xi):
            return False

        vars1 = self._copy_vars("_1")
        vars2 = self._copy_vars("_2")

        psi1 = self._subst(self.psi, self.vars, vars1)
        psi2 = self._subst(self.psi, self.vars, vars2)
        xi1 = self._subst(xi, self.vars, vars1)
        xi2 = self._subst(xi, self.vars, vars2)

        s = Solver()
        s.add(psi1, xi1, psi2, xi2)

        # Require two distinct models
        neq = [v1 != v2 for v1, v2 in zip(vars1, vars2)]
        s.add(Or(neq))

        result = s.check()
        if result == unknown:
            raise RefusalError("solver returned unknown during uniqueness check")

        # If no two distinct models exist, the model is unique
        return result == unsat

    def mode_at_level(self, xi, level):
        """
        Determine mode at a given level:
        STRICT / SAFE / DEFEASIBLE
        """
        # First: check if any model exists
        if not self._has_model(xi):
            return "REFUSAL"

        # STRICT: exactly one model
        if self.is_unique(xi):
            return "STRICT"

        # SAFE: multiple models but Φ-consistent
        if self._check_consistency(xi, level):
            return "SAFE"

        # Otherwise
        return "DEFEASIBLE"

    def mode_profile(self, xi):
        """
        Return ModeProfile(S') = (m0, m1, ..., mk)
        """
        profile = []
        for level in range(self.k + 1):
            mode = self.mode_at_level(xi, level)
            profile.append(mode)
        return tuple(profile)