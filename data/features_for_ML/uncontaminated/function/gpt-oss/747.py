from __future__ import annotations

from typing import Optional, Union

import jax
import jax.numpy as jnp
from jax.typing import ArrayLike

# Assume the library provides these classes
try:
    from .quantity import Quantity
    from .unit import Unit
except Exception:
    # Fallback stubs for type checking / documentation purposes
    class Quantity:
        def __init__(self, magnitude, unit):
            self.magnitude = magnitude
            self.unit = unit

        def to(self, unit):
            # Very naive conversion: assume unit is compatible and magnitude stays the same
            return Quantity(self.magnitude, unit)

    class Unit:
        pass


def atan(
    x: Union[Quantity, ArrayLike],
    unit_to_scale: Optional[Unit] = None,
) -> jax.Array:
    """
    Elementwise arc tangent: :math:`\mathrm{atan}(x)`.

    Parameters
    ----------
    x : Union[Quantity, jax.typing.ArrayLike]
        Input array or quantity. If a Quantity is provided, it must be
        dimensionless or convertible to a dimensionless quantity via
        ``unit_to_scale``.
    unit_to_scale : Optional[Unit], default None
        Unit to which the quantity should be converted before applying
        the arctangent. If ``None`` and ``x`` is a Quantity, the
        quantity's own unit is used for conversion.

    Returns
    -------
    jax.Array
        The elementwise arctangent of the input.
    """
    # If x is a Quantity, convert it to a dimensionless magnitude
    if isinstance(x, Quantity):
        # Determine the unit to scale to
        if unit_to_scale is None:
            # Use the quantity's own unit for conversion
            unit_to_scale = x.unit
        # Convert the quantity to the target unit
        try:
            scaled = x.to(unit_to_scale)
        except Exception as exc:
            raise ValueError(
                f"Cannot convert quantity with unit {x.unit} to {unit_to_scale}"
            ) from exc
        # Extract the magnitude (dimensionless after conversion)
        mag = scaled.magnitude
    else:
        # Assume x is array-like; convert to a JAX array
        mag = jnp.asarray(x)

    # Compute the arctangent elementwise
    return jnp.arctan(mag)