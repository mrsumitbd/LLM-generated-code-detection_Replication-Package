from typing import Union, Optional, Tuple, Any, Callable
import jax.numpy as jnp
from .._base import Quantity, Unit
import jax

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
    return _fun_accept_unitless_unary(jnp.sin, x, unit_to_scale=unit_to_scale)