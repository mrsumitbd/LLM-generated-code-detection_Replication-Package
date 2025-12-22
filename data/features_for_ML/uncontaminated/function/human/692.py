import jax.numpy as jnp
import jax
from typing import (Union, Sequence, Tuple, Optional)
from .._base import (
    Quantity,
    fail_for_dimension_mismatch,
    get_unit,
    split_mantissa_unit,
    UNITLESS,
    unit_scale_align_to_first,
    maybe_decimal
)

def nanpercentile(
    a: Union[jax.Array, Quantity],
    q: jax.typing.ArrayLike,
    axis: Optional[Union[int, Tuple[int]]] = None,
    method: str = 'linear',
    keepdims: Optional[bool] = False,
) -> jax.Array:
    """
    Compute the q-th percentile of the data along the specified axis, while ignoring nan values.

    Returns the q-th percentile(s) of the array elements, while ignoring nan values.

    Parameters
    ----------
    a : array_like, Quantity
      Input array or Quantity.
    q : array_like, Quantity
      Percentile or sequence of percentiles to compute, which must be between 0 and 100 inclusive.
    method : str, optional
      This parameter specifies the method to use for estimating the
      percentile.  There are many different methods, some unique to NumPy.
      See the notes for explanation.  The options sorted by their R type
      as summarized in the H&F paper [1]_ are:

      1. 'inverted_cdf'
      2. 'averaged_inverted_cdf'
      3. 'closest_observation'
      4. 'interpolated_inverted_cdf'
      5. 'hazen'
      6. 'weibull'
      7. 'linear'  (default)
      8. 'median_unbiased'
      9. 'normal_unbiased'

      The first three methods are discontinuous.  NumPy further defines the
      following discontinuous variations of the default 'linear' (7.) option:

      * 'lower'
      * 'higher',
      * 'midpoint'
      * 'nearest'
    keepdims : bool, optional
      If this is set to True, the axes which are reduced are left in the result as dimensions with size one.

    Returns
    -------
    out : jax.Array
      Output array.
    """
    if isinstance(q, Quantity):
        assert q.is_unitless, 'Percentile should be unitless.'
        q = q.mantissa
    return _fun_keep_unit_unary(
        jnp.nanpercentile, a, q=q, axis=axis, method=method, keepdims=keepdims,
    )