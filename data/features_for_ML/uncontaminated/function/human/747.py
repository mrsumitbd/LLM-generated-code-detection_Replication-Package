from typing import Union, Optional, Callable, Sequence
from .._base import Quantity, Unit
from jax import lax
import jax
from ..math._fun_accept_unitless import _fun_accept_unitless_unary, _fun_accept_unitless_binary, _fun_unitless_binary

def atan(
    x: Union[Quantity, jax.typing.ArrayLike],
    unit_to_scale: Optional[Unit] = None,
) -> jax.Array:
    r"""Elementwise arc tangent: :math:`\mathrm{atan}(x)`."""
    return _fun_accept_unitless_unary(lax.atan, x, unit_to_scale=unit_to_scale)