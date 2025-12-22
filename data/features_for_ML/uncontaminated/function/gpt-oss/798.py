import jax.numpy as jnp
from jax.typing import ArrayLike
from typing import Union, Tuple

# Assume Quantity is a pint.Quantity or similar
try:
    from pint import Quantity
except Exception:
    # If pint is not available, define a minimal stub for type checking
    class Quantity:
        pass


def rot90(
    m: Union[ArrayLike, Quantity],
    k: int = 1,
    axes: Tuple[int, int] = (0, 1)
) -> Union[
    jnp.ndarray, Quantity]:
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
    # Determine if input is a Quantity
    is_quantity = isinstance(m, Quantity)

    # Extract magnitude if Quantity, otherwise use as is
    if is_quantity:
        mag = m.magnitude
    else:
        mag = m

    # Convert to JAX array
    arr = jnp.asarray(mag)

    # Validate axes
    if len(axes) != 2:
        raise ValueError("axes must be a tuple of two integers")
    if axes[0] == axes[1]:
        raise ValueError("axes must be different")

    # Perform rotation
    rotated = jnp.rot90(arr, k=k, axes=axes)

    # Wrap back into Quantity if needed
    if is_quantity:
        return Quantity(rotated, m.units)
    else:
        return rotated