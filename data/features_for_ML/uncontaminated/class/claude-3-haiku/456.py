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

    def __init__(self, dims):
        self._dims = tuple(dims)
        self._hash = None

    @property
    def hash(self):
        if self._hash is None:
            self._hash = hash(self._dims)
        return self._hash

    @hash.setter
    def hash(self, value):
        self._hash = value

    def get_dimension(self, d):
        return self._dims[d]

    @property
    def is_dimensionless(self):
        return all(dim == 0 for dim in self._dims)

    @property
    def dim(self):
        return self._dims

    def _str_representation(self, python_code: bool = False):
        if python_code:
            return f"Dimension({self._dims})"
        else:
            return "[" + ", ".join(f"{dim:+.2f}" for dim in self._dims) + "]"

    def __repr__(self):
        return self._str_representation(python_code=True)

    def __str__(self):
        return self._str_representation()

    def __mul__(self, value: 'Dimension'):
        return Dimension(a + b for a, b in zip(self._dims, value._dims))

    def __div__(self, value: 'Dimension'):
        return Dimension(a - b for a, b in zip(self._dims, value._dims))

    def __truediv__(self, value: 'Dimension'):
        return self.__div__(value)

    def __pow__(self, value: numbers.Number | np.ndarray):
        if isinstance(value, (numbers.Number, np.ndarray)):
            return Dimension(dim * value for dim in self._dims)
        else:
            raise TypeError("Exponent must be a number or numpy array")

    def __imul__(self, value):
        self._dims = tuple(a + b for a, b in zip(self._dims, value._dims))
        self._hash = None
        return self

    def __idiv__(self, value):
        self._dims = tuple(a - b for a, b in zip(self._dims, value._dims))
        self._hash = None
        return self

    def __itruediv__(self, value):
        return self.__idiv__(value)

    def __ipow__(self, value):
        if isinstance(value, (numbers.Number, np.ndarray)):
            self._dims = tuple(dim * value for dim in self._dims)
            self._hash = None
            return self
        else:
            raise TypeError("Exponent must be a number or numpy array")

    def __eq__(self, value: 'Dimension') -> bool:
        return self._dims == value._dims

    def __ne__(self, value):
        return self._dims != value._dims

    def __getstate__(self):
        return self._dims

    def __setstate__(self, state):
        self._dims = state
        self._hash = None

    def __reduce__(self):
        return (Dimension, (self._dims,))

    def __deepcopy__(self, memodict):
        return Dimension(self._dims)

    def __hash__(self):
        return self.hash