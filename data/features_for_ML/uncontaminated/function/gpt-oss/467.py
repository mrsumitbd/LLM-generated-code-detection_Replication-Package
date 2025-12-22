from __future__ import annotations

from typing import Tuple, Union

import jax.numpy as jnp
from pint import Quantity


def reshape(
    a: Union[jax.Array, Quantity],
    shape: Union[int, Tuple[int, ...]],
    order: str = "C",
) -> Union[jax.Array, Quantity]:
    """
    Gives a new shape to a quantity or an array without changing its data.

    Parameters
    ----------
    a : array_like, Quantity
        Array to be reshaped.
    shape : int or tuple of ints
        The new shape should be compatible with the original shape. If
        an integer, then the result will be a 1-D array of that length.
        One shape dimension can be -1. In this case, the value is
        inferred from the length of the array and remaining dimensions.
    order : {'C', 'F', 'A'}, optional
        Read the elements of `a` using this index order, and place the
        elements into the reshaped array using this index order.  'C'
        means to read / write the elements using C-like index order,
        with the last axis index changing fastest, back to the first
        axis index changing slowest. 'F' means to read / write the
        elements using Fortran-like index order, with the first index
        changing fastest, and the last index changing slowest. Note that
        the 'C' and 'F' options take no account of the memory layout of
        the underlying array, and only refer to the order of indexing.
        'A' means to read / write the elements in Fortran-like index
        order if `a` is Fortran *contiguous* in memory, C-like order
        otherwise.

    Returns
    -------
    reshaped_array : ndarray, Quantity
        This will be a new view object if possible; otherwise, it will
        be a copy.  Note there is no guarantee of the *memory layout*
        (C- or Fortran- contiguous) of the returned array.
    """
    # Normalise shape to a tuple
    if isinstance(shape, int):
        shape = (shape,)

    # If a is a pint.Quantity, reshape its magnitude and keep units
    if isinstance(a, Quantity):
        mag = a.magnitude
        reshaped_mag = jnp.reshape(mag, shape)
        return a.__class__(reshaped_mag, a.units)

    # For plain JAX arrays, just use jnp.reshape
    return jnp.reshape(a, shape)