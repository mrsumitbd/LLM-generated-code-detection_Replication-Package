import jax
from jax import jit
from jax.numpy import arctan
from pint import Quantity, Unit

@jit
def atan(
    x: Union[Quantity, jax.typing.ArrayLike],
    unit_to_scale: Optional[Unit] = None,
) -> jax.Array:
    r"""Elementwise arc tangent: :math:`\mathrm{atan}(x)`."""
    if isinstance(x, Quantity):
        if unit_to_scale is None:
            return x.to_base_units().magnitude.astype(float)
        else:
            return x.to(unit_to_scale).magnitude.astype(float)
    else:
        return arctan(x)