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

def rot90(
    m: Union[jax.typing.ArrayLike, Quantity],
    k: int = 1,
    axes: Tuple[int, int] = (0, 1)
) -> Union[
    jax.Array, Quantity]:
    """
    Rotate an array by 90 degrees in the plane specified by axes.

    Rotation direction is from the first towards the second axis.

    Parameters
    ----------
    m : array_like, Quantity
      Array of two or more dimensions.
    k : integer
      Number of times the array is rotated by 90 degrees.
    axes : (2,) array_like
      The array is rotated in the plane defined by the axes.
      Axes must be different.

    Returns
    -------
    y : ndarray, Quantity
      A rotated view of `m`.

      This is a quantity if `m` is a quantity.
    """
    return _fun_keep_unit_unary(jnp.rot90, m, k=k, axes=axes)