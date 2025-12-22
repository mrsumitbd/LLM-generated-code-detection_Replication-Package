import numbers
import numpy as np

class Dimension:
    """
    Stores the indices of the 7 basic SI unit dimension (length, mass, etc.).

    Provides a subset of arithmetic operations appropriate to dimensions:
    multiplication, division and powers, and equality testing.

    Parameters
    ----------
    dims : sequence of `float`
        The dimension indices of the 7 basic SI unit dimensions.

    Notes
    -----
    Users shouldn't use this class directly, it is used internally in Array
    and Unit. Even internally, never use ``Dimension(...)`` to create a new
    instance, use `get_or_create_dimension` instead. This function makes
    sure that only one Dimension instance exists for every combination of
    indices, allowing for a very fast dimensionality check with ``is``.
    """

    _SI_NAMES = ("m", "kg", "s", "A", "K", "mol", "cd")

    def __init__(self, dims):
        # Store as immutable tuple of floats (or ints)
        self._dims = tuple(float(d) for d in dims)
        # Precompute hash
        self._hash = hash(self._dims)

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, value):
        self._hash = value

    def get_dimension(self, d):
        """Return the exponent for the d‑th SI base dimension."""
        return self._dims[d]

    @property
    def is_dimensionless(self):
        """True if all exponents are zero."""
        return all(d == 0 for d in self._dims)

    @property
    def dim(self):
        """Return the tuple of exponents."""
        return self._dims

    def _str_representation(self, python_code: bool = False):
        if python_code:
            return f"Dimension({self._dims})"
        # Human readable form
        parts = []
        for name, exp in zip(self._SI_NAMES, self._dims):
            if exp != 0:
                if exp == 1:
                    parts.append(name)
                else:
                    parts.append(f"{name}^{exp:g}")
        if not parts:
            return "dimensionless"
        return " ".join(parts)

    def __repr__(self):
        return self._str_representation(python_code=True)

    def __str__(self):
        return self._str_representation(python_code=False)

    def __mul__(self, value: 'Dimension'):
        if not isinstance(value, Dimension):
            return NotImplemented
        new_dims = tuple(a + b for a, b in zip(self._dims, value._dims))
        return Dimension(new_dims)

    def __div__(self, value: 'Dimension'):
        if not isinstance(value, Dimension):
            return NotImplemented
        new_dims = tuple(a - b for a, b in zip(self._dims, value._dims))
        return Dimension(new_dims)

    __truediv__ = __div__

    def __pow__(self, value: numbers.Number | np.ndarray):
        if isinstance(value, np.ndarray):
            # For array exponents, return an array of Dimensions
            # (not typically used, but we support it)
            return np.array([Dimension(tuple(d * v for d in self._dims)) for v in value])
        if not isinstance(value, numbers.Number):
            return NotImplemented
        new_dims = tuple(d * value for d in self._dims)
        return Dimension(new_dims)

    def __imul__(self, value):
        if not isinstance(value, Dimension):
            return NotImplemented
        self._dims = tuple(a + b for a, b in zip(self._dims, value._dims))
        self._hash = hash(self._dims)
        return self

    def __idiv__(self, value):
        if not isinstance(value, Dimension):
            return NotImplemented
        self._dims = tuple(a - b for a, b in zip(self._dims, value._dims))
        self._hash = hash(self._dims)
        return self

    __itruediv__ = __idiv__

    def __ipow__(self, value):
        if not isinstance(value, numbers.Number):
            return NotImplemented
        self._dims = tuple(d * value for d in self._dims)
        self._hash = hash(self._dims)
        return self

    def __eq__(self, value: 'Dimension') -> bool:
        if not isinstance(value, Dimension):
            return False
        return self._dims == value._dims

    def __ne__(self, value):
        return not self.__eq__(value)

    def __getstate__(self):
        return {"dims": self._dims, "hash": self._hash}

    def __setstate__(self, state):
        self._dims = state["dims"]
        self._hash = state["hash"]

    def __reduce__(self):
        return (Dimension, (self._dims,))

    def __deepcopy__(self, memodict):
        return Dimension(self._dims)

    def __hash__(self):
        return self._hash