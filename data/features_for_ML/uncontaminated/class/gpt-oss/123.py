import multiprocessing
from functools import wraps


class PotentialOps:
    """Mixin providing operations for potential functions:

    1. Product (`*`): Take the product of two potentials.
    2. Coercion (`coerce`): Coerce the potential to operate on another potential's vocabulary.
    3. Auto-batching (`to_autobatched`): Create a version that automatically batches concurrent requests to the instance methods.
    4. Parallelization (`to_multiprocess`): Create a version that parallelizes operations over multiple processes.
    """

    # ------------------------------------------------------------------
    # 1. Product
    # ------------------------------------------------------------------
    def __mul__(self, other):
        """
        Return a new potential that represents the product of ``self`` and ``other``.
        The resulting potential has a vocabulary that is the union of the two operands.
        """
        if not hasattr(self, "vocab") or not hasattr(other, "vocab"):
            raise AttributeError("Both operands must have a 'vocab' attribute")

        # The new vocabulary is the union of the two vocabularies
        new_vocab = self.vocab | other.vocab

        @wraps(self)
        def product_potential(assignment):
            # The assignment is expected to contain at least the variables in the new_vocab
            return self(assignment) * other(assignment)

        # Attach the vocabulary to the new potential
        product_potential.vocab = new_vocab
        return product_potential

    # ------------------------------------------------------------------
    # 2. Coercion
    # ------------------------------------------------------------------
    def coerce(self, other, f, prune=True):
        """
        Return a new potential that coerces ``self`` to operate on ``other``'s vocabulary.
        ``f`` is a function that maps an assignment for ``other`` to an assignment for ``self``.
        If ``prune`` is True, variables not present in ``other``'s vocabulary are ignored.
        """
        if not hasattr(other, "vocab"):
            raise AttributeError("The other potential must have a 'vocab' attribute")

        @wraps(self)
        def coerced_potential(assignment):
            # ``assignment`` is for ``other``'s vocabulary
            mapped_assignment = f(assignment)
            return self(mapped_assignment)

        coerced_potential.vocab = other.vocab
        return coerced_potential

    # ------------------------------------------------------------------
    # 3. Auto-batching
    # ------------------------------------------------------------------
    def to_autobatched(self):
        """
        Return a wrapper that accepts either a single assignment (dict) or a list/tuple of assignments.
        For a list/tuple, the underlying potential is applied to each assignment in a single call.
        """
        if not hasattr(self, "vocab"):
            raise AttributeError("The potential must have a 'vocab' attribute")

        class AutoBatchedPotential:
            def __init__(self, pot):
                self._pot = pot
                self.vocab = pot.vocab

            def __call__(self, assignments):
                if isinstance(assignments, dict):
                    return self._pot(assignments)
                if isinstance(assignments, (list, tuple)):
                    return [self._pot(a) for a in assignments]
                raise TypeError("Expected a dict or a list/tuple of dicts")

        return AutoBatchedPotential(self)

    # ------------------------------------------------------------------
    # 4. Parallelization
    # ------------------------------------------------------------------
    def to_multiprocess(self, num_workers=2, spawn_args=None):
        """
        Return a wrapper that parallelizes calls to the potential over multiple processes.
        ``num_workers`` specifies the number of worker processes.
        ``spawn_args`` can be used to pass arguments to ``multiprocessing.Pool``.
        """
        if not hasattr(self, "vocab"):
            raise AttributeError("The potential must have a 'vocab' attribute")

        pool = multiprocessing.Pool(processes=num_workers, **(spawn_args or {}))

        class MultiProcessedPotential:
            def __init__(self, pot, pool):
                self._pot = pot
                self._pool = pool
                self.vocab = pot.vocab

            def __call__(self, assignments):
                if isinstance(assignments, dict):
                    return self._pot(assignments)
                if isinstance(assignments, (list, tuple)):
                    return self._pool.map(self._pot, assignments)
                raise TypeError("Expected a dict or a list/tuple of dicts")

            def __del__(self):
                # Ensure the pool is closed when the wrapper is garbage‑collected
                try:
                    self._pool.close()
                    self._pool.join()
                except Exception:
                    pass

        return MultiProcessedPotential(self, pool)