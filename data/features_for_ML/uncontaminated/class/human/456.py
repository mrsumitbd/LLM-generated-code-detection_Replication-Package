import numbers
import jax
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

    __module__ = "saiunit"
    __slots__ = ["_dims", "_hash"]
    __array_priority__ = 1000

    # ---- INITIALISATION ---- #

    def __init__(self, dims):
        self._dims: np.ndarray = np.asarray(dims)
        self._hash = None

    @property
    def hash(self):
        """
        Calculate and return the hash value of the dimension.

        This property memoizes the hash value for efficiency. Once calculated,
        the hash value is stored in the `_hash` attribute for future access.
        The hash is based on the binary representation of the dimensions array.

        Returns
        -------
        int
            The hash value of the dimensions array.

        Notes
        -----
        The hash is only calculated once and then cached. This allows Dimension
        objects with the same dimensional values to have the same hash, supporting
        their use as dictionary keys and in sets.
        """
        if self._hash is None:
            self._hash = hash(self._dims.tobytes())
        return self._hash

    @hash.setter
    def hash(self, value):
        """
        Prevent external modification of the hash value.

        The hash value is derived from the dimensions and should not be
        externally modifiable to maintain integrity of the hashing system.

        Parameters
        ----------
        value : Any
            The attempted new value (ignored).

        Raises
        ------
        ValueError
            Always raised to prevent setting the hash value.
        """
        raise ValueError("Cannot set hash value")

    # ---- METHODS ---- #
    def get_dimension(self, d):
        """
        Return a specific dimension.

        Parameters
        ----------
        d : `str`
            A string identifying the SI basic unit dimension. Can be either a
            description like "length" or a basic unit like "m" or "metre".

        Returns
        -------
        dim : `float`
            The dimensionality of the dimension `d`.
        """
        return self._dims[_dim2index[d]]

    @property
    def is_dimensionless(self):
        """
        Whether this Dimension is dimensionless.

        Notes
        -----
        Normally, instead one should check dimension for being identical to
        `DIMENSIONLESS`.
        """
        return np.allclose(self._dims, 0)
        # return all([x == 0 for x in self._dims])

    @property
    def dim(self):
        """
        Returns the `Dimension` object itself. This can be useful, because it
        allows to check for the dimension of an object by checking its ``dim``
        attribute -- this will return a `Dimension` object for `Array`,
        `Unit` and `Dimension`.
        """
        return self

    # ---- REPRESENTATION ---- #
    def _str_representation(self, python_code: bool = False):
        """
        String representation in basic SI units, or ``"1"`` for dimensionless.
        Use ``python_code=False`` for display purposes and ``True`` for valid
        Python code.
        """

        if python_code:
            power_operator = " ** "
        else:
            power_operator = "^"

        parts = []
        for i in range(len(self._dims)):
            if self._dims[i]:
                if python_code:
                    s = _iclass_label[i]
                else:
                    s = _ilabel[i]
                if self._dims[i] != 1:
                    s += power_operator + str(self._dims[i])
                parts.append(s)
        if python_code:
            s = " * ".join(parts)
            if not len(s):
                return f"{self.__class__.__name__}()"
        else:
            s = " ".join(parts)
            if not len(s):
                return "1"
        return s.strip()

    def __repr__(self):
        """
        Return a string representation of the Dimension object suitable for Python code.

        This method returns a representation that can be used to recreate the
        Dimension object through evaluation, using the full class and method names.

        Returns
        -------
        str
            A string representing the dimension in a format suitable for Python code,
            including the class name and dimension values.
        """
        return self._str_representation(python_code=True)

    def __str__(self):
        """
        Return a human-readable string representation of the Dimension object.

        This method returns a string representation designed for display purposes,
        showing the basic SI units with appropriate exponents (e.g., "m kg s^-2" for force).
        For dimensionless quantities, it returns "1".

        Returns
        -------
        str
            A concise string representation of the dimension using standard unit symbols.
        """
        return self._str_representation(python_code=False)

    # ---- ARITHMETIC ---- #
    # Note that none of the dimension arithmetic objects do sanity checking
    # on their inputs, although most will throw an exception if you pass the
    # wrong sort of input
    def __mul__(self, value: 'Dimension'):
        """
        Multiply this Dimension object with another Dimension object.

        This method implements the multiplication operation for Dimension objects,
        combining their dimensional exponents by adding them together. For example,
        multiplying length by length results in area (length²).

        Parameters
        ----------
        value : Dimension
            The Dimension object to multiply with this one.

        Returns
        -------
        Dimension
            A new Dimension object representing the product of the two dimensions.

        Raises
        ------
        AssertionError
            If the provided value is not a Dimension object.

        Examples
        --------
        >>> length = get_or_create_dimension([1, 0, 0, 0, 0, 0, 0])  # meter
        >>> area = length * length  # meter²
        """
        assert isinstance(value, Dimension), "Can only divide by a Dimension object"
        return get_or_create_dimension(self._dims + value._dims)

    def __div__(self, value: 'Dimension'):
        """
        Divide this Dimension object by another Dimension object.

        This method implements the division operation for Dimension objects,
        combining their dimensional exponents by subtracting them. For example,
        dividing velocity (length/time) by time results in acceleration (length/time²).

        Parameters
        ----------
        value : Dimension
            The Dimension object to divide this one by.

        Returns
        -------
        Dimension
            A new Dimension object representing the quotient of the two dimensions.

        Raises
        ------
        AssertionError
            If the provided value is not a Dimension object.

        Examples
        --------
        >>> length_time = get_or_create_dimension([1, 0, -1, 0, 0, 0, 0])  # velocity
        >>> time = get_or_create_dimension([0, 0, 1, 0, 0, 0, 0])  # second
        >>> acceleration = length_time / time  # meter/second²
        """
        assert isinstance(value, Dimension), "Can only divide by a Dimension object"
        return get_or_create_dimension(self._dims - value._dims)

    def __truediv__(self, value: 'Dimension'):
        """
        True division implementation for Dimension objects.

        This method provides the same functionality as __div__ but for Python 3's
        true division operator (/).

        Parameters
        ----------
        value : Dimension
            The Dimension object to divide this one by.

        Returns
        -------
        Dimension
            A new Dimension object representing the quotient of the two dimensions.

        See Also
        --------
        __div__ : Division implementation that is called by this method.
        """
        return self.__div__(value)

    def __pow__(self, value: numbers.Number | np.ndarray):
        """
        Raise this Dimension object to a power.

        This method implements the power operation for Dimension objects,
        multiplying each dimensional exponent by the given value. For example,
        squaring a length dimension results in an area dimension.

        Parameters
        ----------
        value : numbers.Number or np.ndarray
            The exponent to raise the dimension to. Must be a scalar value.

        Returns
        -------
        Dimension
            A new Dimension object representing the original dimension raised to the power.

        Raises
        ------
        TypeError
            If the provided value is a tracer object or if multiple exponents are provided.

        Examples
        --------
        >>> length = get_or_create_dimension([1, 0, 0, 0, 0, 0, 0])  # meter
        >>> area = length ** 2  # meter²
        >>> volume = length ** 3  # meter³
        """
        if _is_tracer(value):
            raise TypeError(f"Cannot use a tracer {value} as an exponent, please use a constant.")
        value = np.array(value)
        if value.size > 1:
            raise TypeError("Too many exponents")
        return get_or_create_dimension(self._dims * value)

    def __imul__(self, value):
        """
        In-place multiplication operation for Dimension objects.

        This method would theoretically implement the in-place multiplication
        operation (e.g., a *= b) for Dimension objects, but since Dimension
        objects are designed to be immutable, this operation is not supported.

        Parameters
        ----------
        value : Any
            The value to multiply with (not used).

        Raises
        ------
        NotImplementedError
            Always raised because Dimension objects are immutable.
        """
        raise NotImplementedError("Dimension object is immutable")

    def __idiv__(self, value):
        """
        In-place division operation for Dimension objects.

        This method would theoretically implement the in-place division
        operation (e.g., a /= b) for Dimension objects, but since Dimension
        objects are designed to be immutable, this operation is not supported.

        Parameters
        ----------
        value : Any
            The value to divide by (not used).

        Raises
        ------
        NotImplementedError
            Always raised because Dimension objects are immutable.
        """
        raise NotImplementedError("Dimension object is immutable")

    def __itruediv__(self, value):
        """
        In-place true division operation for Dimension objects.

        This method would theoretically implement the in-place true division
        operation (e.g., a /= b) for Dimension objects in Python 3, but since
        Dimension objects are designed to be immutable, this operation is not supported.

        Parameters
        ----------
        value : Any
            The value to divide by (not used).

        Raises
        ------
        NotImplementedError
            Always raised because Dimension objects are immutable.
        """
        raise NotImplementedError("Dimension object is immutable")

    def __ipow__(self, value):
        """
        In-place power operation for Dimension objects.

        This method would theoretically implement the in-place power
        operation (e.g., a **= b) for Dimension objects, but since Dimension
        objects are designed to be immutable, this operation is not supported.

        Parameters
        ----------
        value : Any
            The exponent to raise to (not used).

        Raises
        ------
        NotImplementedError
            Always raised because Dimension objects are immutable.
        """
        raise NotImplementedError("Dimension object is immutable")

    # ---- COMPARISON ---- #
    def __eq__(self, value: 'Dimension') -> bool:
        """
        Compare this Dimension object with another for equality.

        This method implements the equality comparison (==) for Dimension objects.
        Two Dimension objects are considered equal if they have the same dimensional
        exponents (within a small numerical tolerance).

        Parameters
        ----------
        value : Dimension
            The Dimension object to compare with this one.

        Returns
        -------
        bool
            True if the dimensions are equal (have the same exponents),
            False otherwise or if the provided value is not a Dimension object.

        Notes
        -----
        The comparison uses numpy's allclose() function to handle potential
        floating-point precision issues in the dimension exponents.
        If value is not a Dimension object, returns False without attempting comparison.
        """
        if not isinstance(value, Dimension):
            return False
        try:
            return np.allclose(self._dims, value._dims)
        except (AttributeError, jax.errors.TracerArrayConversionError):
            # Only compare equal to another Dimensions object
            return False

    def __ne__(self, value):
        """
        Implement the not-equal comparison operator (!=) for Dimension objects.

        This method implements inequality by negating the result of the equality
        comparison method.

        Parameters
        ----------
        value : Any
            The value to compare with this Dimension object.

        Returns
        -------
        bool
            True if the dimensions are not equal, False otherwise.
        """
        return not self.__eq__(value)

    # MAKE DIMENSION PICKABLE #
    def __getstate__(self):
        """
        Support for pickling Dimension objects.

        Returns the internal dimensional exponents array which is sufficient
        to reconstruct the Dimension object.

        Returns
        -------
        numpy.ndarray
            The array of dimensional exponents.
        """
        return self._dims

    def __setstate__(self, state):
        """
        Support for unpickling Dimension objects.

        Sets the internal dimensional exponents from the pickled state.

        Parameters
        ----------
        state : numpy.ndarray
            The array of dimensional exponents.
        """
        self._dims = state

    def __reduce__(self):
        """
        Support for pickling with singleton pattern preservation.

        This method ensures that when unpickling a Dimension object,
        the singleton system (using get_or_create_dimension) is used
        rather than creating a duplicate Dimension object with the same values.

        Returns
        -------
        tuple
            A tuple of (callable, args) where callable is get_or_create_dimension
            and args is a tuple containing the dimensional exponents.
        """
        # Make sure that unpickling Dimension objects does not bypass the singleton system
        return get_or_create_dimension, (self._dims,)

    def __deepcopy__(self, memodict):
        """
        Support for deepcopy while maintaining the singleton pattern.

        Since Dimension objects are designed to be singletons (only one instance
        should exist for each unique set of dimensions), this method returns
        the object itself rather than creating a new copy.

        Parameters
        ----------
        memodict : dict
            Dictionary of id-to-object mapping to keep track of objects
            that have already been copied.

        Returns
        -------
        Dimension
            The Dimension object itself (not a copy).
        """
        return self

    def __hash__(self):
        """
        Calculate a hash value for the Dimension object.

        This method is required for Dimension objects to be usable as
        dictionary keys or in sets. It returns the hash value computed
        and cached by the hash property.

        Returns
        -------
        int
            The hash value of the Dimension object.
        """
        return self.hash