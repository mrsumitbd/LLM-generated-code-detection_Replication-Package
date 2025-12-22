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
        self.dims = tuple(float(d) for d in dims)
        self._hash = None

    @property
    def hash(self):
        if self._hash is None:
            self._hash = hash(self.dims)
        return self._hash

    @hash.setter
    def hash(self, value):
        self._hash = value

    def get_dimension(self, d):
        return self.dims[d]

    @property
    def is_dimensionless(self):
        return all(d == 0 for d in self.dims)

    @property
    def dim(self):
        return self.dims

    def _str_representation(self, python_code: bool = False):
        dim_names = ['length', 'mass', 'time', 'current', 'temperature', 'amount', 'luminosity']
        parts = []
        for i, (name, exp) in enumerate(zip(dim_names, self.dims)):
            if exp != 0:
                if exp == 1:
                    parts.append(name)
                else:
                    parts.append(f"{name}^{exp}")
        
        if not parts:
            return "dimensionless"
        return " * ".join(parts)

    def __repr__(self):
        return f"Dimension({list(self.dims)})"

    def __str__(self):
        return self._str_representation()

    def __mul__(self, value: 'Dimension'):
        if not isinstance(value, Dimension):
            return NotImplemented
        new_dims = tuple(a + b for a, b in zip(self.dims, value.dims))
        from . import get_or_create_dimension
        return get_or_create_dimension(new_dims)

    def __div__(self, value: 'Dimension'):
        if not isinstance(value, Dimension):
            return NotImplemented
        new_dims = tuple(a - b for a, b in zip(self.dims, value.dims))
        from . import get_or_create_dimension
        return get_or_create_dimension(new_dims)

    def __truediv__(self, value: 'Dimension'):
        return self.__div__(value)

    def __pow__(self, value: numbers.Number | np.ndarray):
        new_dims = tuple(d * value for d in self.dims)
        from . import get_or_create_dimension
        return get_or_create_dimension(new_dims)

    def __imul__(self, value):
        result = self.__mul__(value)
        self.dims = result.dims
        self._hash = None
        return self

    def __idiv__(self, value):
        result = self.__div__(value)
        self.dims = result.dims
        self._hash = None
        return self

    def __itruediv__(self, value):
        return self.__idiv__(value)

    def __ipow__(self, value):
        result = self.__pow__(value)
        self.dims = result.dims
        self._hash = None
        return self

    def __eq__(self, value: 'Dimension') -> bool:
        if not isinstance(value, Dimension):
            return False
        return self.dims == value.dims

    def __ne__(self, value):
        return not self.__eq__(value)

    def __getstate__(self):
        return {'dims': self.dims, '_hash': self._hash}

    def __setstate__(self, state):
        self.dims = state['dims']
        self._hash = state.get('_hash', None)

    def __reduce__(self):
        return (self.__class__, (list(self.dims),))

    def __deepcopy__(self, memodict):
        from . import get_or_create_dimension
        return get_or_create_dimension(self.dims)

    def __hash__(self):
        return self.hash