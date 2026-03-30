"""
GSA³ v5.1.1 – Constitutional Core
Reference implementation using Z3.

Key fail-closed semantics:
- unsat   -> no admissible state / contradiction / empty result
- sat     -> constructible state exists
- unknown -> refusal
"""

from z3 import *


class RefusalError(Exception):
    """Raised when the solver cannot decide and the framework must refuse."""
    pass


class GSA51Core:
    def __init__(self, variables, psi, phis):
        """
        variables:
            List of Z3 variables, e.g. [x, y].

        psi:
            Z3 formula defining the symbolic state space:
                S = {σ | ψ(σ)}

        phis:
            List of lists of Z3 formulas, where:
                phis[0] = constitutional invariants Φ₀
                phis[1..] = epistemic refinements Φ₁, Φ₂, ...

            The intended reading is:
                Φ₀ ⊆ Φ₁ ⊆ ... ⊆ Φ_k
        """
        if not variables:
            raise ValueError("variables must be explicitly provided and non-empty")
        if psi is None:
            raise ValueError("psi must be provided")
        if not phis:
            raise ValueError("phis must be a non-empty invariant hierarchy")

        self.vars = variables
        self.psi = psi
        self.phis = phis
        self.k = len(phis) - 1

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _copy_vars(self, suffix):
        """Create fresh copies of variables with the given suffix."""
        return [Const(v.decl().name() + suffix, v.sort()) for v in self.vars]

    def _subst(self, formula, old_vars, new_vars):
        """Substitute variables in a formula."""
        return substitute(formula, *zip(old_vars, new_vars))

    def _solver_check(self, *constraints):
        """
        Run a solver check on the given constraints.

        Returns:
            sat / unsat

        Raises:
            RefusalError if the solver returns unknown.
        """
        s = Solver()
        s.add(*constraints)
        result = s.check()

        if result == unknown:
            raise RefusalError("solver returned unknown")

        return result

    def _sat_status(self, formula):
        """
        Return solver status for a single formula:
        - sat
        - unsat

        Raises:
            RefusalError on unknown.
        """
        return self._solver_check(formula)

    def _has_model(self, xi):
        """
        Return True iff ψ ∧ ξ has at least one model.

        Raises:
            RefusalError if solver returns unknown.
        """
        return self._sat_status(And(self.psi, xi)) == sat

    # -------------------------------------------------------------------------
    # Consistency and kernels
    # -------------------------------------------------------------------------

    def _check_consistency(self, xi, level):
        """
        Return True iff S' = {σ | ψ(σ) ∧ ξ(σ)} is Φ_level-consistent.

        Consistency means:
            there do NOT exist two admissible states in S'
            that differ on at least one invariant in Φ_level.

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

        # Look for two admissible states with differing Φ-values
        disjuncts = []
        for phi in self.phis[level]:
            phi1 = self._subst(phi, self.vars, vars1)
            phi2 = self._subst(phi, self.vars, vars2)
            disjuncts.append(phi1 != phi2)

        result = self._solver_check(psi1, xi1, psi2, xi2, Or(disjuncts))

        # If no differing pair exists, S' is Φ-consistent
        return result == unsat

    def kernel(self, xi, level):
        """
        Return (nonempty, formula) where:
        - nonempty = True iff K^(level)(S') is non-empty
        - formula   = And(ψ, ξ) when non-empty, else None

        By v5.0+ semantics:
        - If S' is empty, kernel is empty
        - If S' is non-empty and Φ-consistent, kernel is S'
        - Otherwise kernel is empty
        """
        if level < 0 or level > self.k:
            raise IndexError(f"level {level} out of bounds")

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

        I* is the highest level such that K^(i)(S') is non-empty.

        Raises:
            RefusalError if a solver call returns unknown.
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
            {
                "outcome": "ADMISSIBLE_LEVEL",
                "level": i,
                "kernel": formula
            }

        or

            {
                "outcome": "REFUSAL",
                "level": None,
                "kernel": None
            }
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

    # -------------------------------------------------------------------------
    # Signatures and uniqueness
    # -------------------------------------------------------------------------

    def invariant_signature(self, model, level):
        """
        Return tuple of Φ_level values for a given model.
        """
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

        # Require two distinct models
        neq = [v1 != v2 for v1, v2 in zip(vars1, vars2)]

        result = self._solver_check(psi1, xi1, psi2, xi2, Or(neq))

        # If no two distinct models exist, the model is unique
        return result == unsat

    # -------------------------------------------------------------------------
    # Modes
    # -------------------------------------------------------------------------

    def mode_at_level(self, xi, level):
        """
        Determine the mode at a given level.

        Returns one of:
        - "REFUSAL"    : no model exists
        - "STRICT"     : exactly one model exists
        - "SAFE"       : multiple models, but Φ_level-consistent
        - "DEFEASIBLE" : multiple models, not Φ_level-consistent

        Raises:
            RefusalError if solver returns unknown.
        """
        if level < 0 or level > self.k:
            raise IndexError(f"level {level} out of bounds")

        # No model at all
        if not self._has_model(xi):
            return "REFUSAL"

        # Exactly one model
        if self.is_unique(xi):
            return "STRICT"

        # Multiple models but still consistent at this level
        if self._check_consistency(xi, level):
            return "SAFE"

        # Multiple models and inconsistency at this level
        return "DEFEASIBLE"

    def mode_profile(self, xi):
        """
        Return ModeProfile(S') = (m0, m1, ..., mk)
        """
        return tuple(self.mode_at_level(xi, level) for level in range(self.k + 1))
    
     
class Core:
    def __init__(self, lower: float = -1.0, upper: float = 1.0):
        self.lower = lower
        self.upper = upper

    def step(self, x: float, dx: float):
        x_new = x + dx
        if x_new < self.lower or x_new > self.upper:
            return "REJECT", x
        return "ADMISSIBLE", x_new    