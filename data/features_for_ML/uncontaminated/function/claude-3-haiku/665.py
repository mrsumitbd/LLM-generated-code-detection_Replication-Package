import jax
from jax.typing import ArrayLike
from pint import Quantity, Unit
from typing import Optional

def sin(
    x: Union[jax.typing.ArrayLike, Quantity],
    unit_to_scale: Optional[Unit] = None,
) -> jax.Array:
    """
    Compute the sine of the input elements.

    Parameters
    ----------
    x : array_like, Quantity
      Input array or Quantity.
    unit_to_scale : Unit, optional
      The unit to scale the ``x``.

    Returns
    -------
    out : jax.Array
      Output array.
    """
    if isinstance(x, Quantity):
        if unit_to_scale is not None:
            x = x.to(unit_to_scale).magnitude
        else:
            x = x.magnitude
    return jax.numpy.sin(x)