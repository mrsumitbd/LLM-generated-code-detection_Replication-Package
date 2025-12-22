from typing import Union, Optional, Tuple
import jax.numpy as jnp
from jax import Array
from astropy.units import Quantity


def nanpercentile(
    a: Union[jax.Array, Quantity],
    q: jax.typing.ArrayLike,
    axis: Optional[Union[int, Tuple[int]]] = None,
    method: str = 'linear',
    keepdims: Optional[bool] = False,
) -> jax.Array:
    """
    Compute the q‑th percentile of the data along the specified axis, while ignoring nan values.

    Parameters
    ----------
    a : array_like, Quantity
        Input array or Quantity.
    q : array_like, Quantity
        Percentile or sequence of percentiles to compute, which must be between 0 and 100 inclusive.
    axis : int or tuple of ints, optional
        Axis or axes along which to compute the percentile. If None, the flattened array is used.
    method : str, optional
        Method used to compute the percentile.  See the NumPy documentation for details.
    keepdims : bool, optional
        If True, the reduced axes are left in the result as dimensions with size one.

    Returns
    -------
    out : jax.Array
        The computed percentile(s).
    """
    # Extract raw values if Quantity is provided
    if isinstance(a, Quantity):
        a_val = a.value
    else:
        a_val = a

    if isinstance(q, Quantity):
        q_val = q.value
    else:
        q_val = q

    # Ensure keepdims is a boolean
    keepdims = bool(keepdims)

    # Delegate to JAX's nanpercentile implementation
    return jnp.nanpercentile(a_val, q_val, axis=axis, method=method, keepdims=keepdims)