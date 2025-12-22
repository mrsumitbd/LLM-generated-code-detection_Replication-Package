import numbers
import numpy as np

class Dimension:
    def __init__(self, dims):
        self.dims = dims

    @property
    def hash(self):
        return hash(tuple(self.dims))

    @hash.setter
    def hash(self, value):
        self.hash = value

    def get_dimension(self, d):
        return self.dims[d]

    @property
    def is_dimensionless(self):
        return all(dim == 0 for dim in self.dims)

    @property
    def dim(self):
        return self.dims

    def _str_representation(self, python_code=False):
        if python_code:
            return f"Dimension({self.dims})"
        else:
            return f"Dimension({self.dims})"

    def __repr__(self):
        return self._str_representation()

    def __str__(self):
        return self._str_representation()

    def __mul__(self, value: 'Dimension'):
        new_dims = [self.dims[i] + value.dims[i] for i in range(len(self.dims))]
        return Dimension(new_dims)

    def __div__(self, value: 'Dimension'):
        new_dims = [self.dims[i] - value.dims[i] for i in range(len(self.dims))]
        return Dimension(new_dims)

    def __truediv__(self, value: 'Dimension'):
        return self.__div__(value)

    def __pow__(self, value: numbers.Number | np.ndarray):
        if isinstance(value, (int, float)):
            new_dims = [dim * value for dim in self.dims]
            return Dimension(new_dims)
        else:
            raise TypeError("Exponent must be a number")

    def __imul__(self, value):
        self.dims = (self * value).dims
        return self

    def __idiv__(self, value):
        self.dims = (self / value).dims
        return self

    def __itruediv__(self, value):
        return self.__idiv__(value)

    def __ipow__(self, value):
        self.dims = (self ** value).dims
        return self

    def __eq__(self, value: 'Dimension') -> bool:
        return self.dims == value.dims

    def __ne__(self, value):
        return not self.__eq__(value)

    def __getstate__(self):
        return self.dims

    def __setstate__(self, state):
        self.dims = state

    def __reduce__(self):
        return (self.__class__, (self.dims,))

    def __deepcopy__(self, memodict):
        return Dimension(self.dims)

    def __hash__(self):
        return hash(tuple(self.dims))