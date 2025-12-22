from typing import Union, Optional

import jax
import jax.numpy as jnp
from jax.typing import ArrayLike

# Import Quantity and Unit types. Adjust the import path if your library uses a different module.
try:
    from pint import Quantity, Unit
except Exception:
    # Fallback: define minimal stubs if pint is not available.
    class Quantity:
        def __init__(self, magnitude, units):
            self.magnitude = magnitude
            self.units = units

        def to(self, unit):
            # Very naive conversion: assume unit is 'rad' or 'deg'
            if unit == "rad":
                if self.units == "deg":
                    return Quantity(self.magnitude * jnp.pi / 180.0, "rad")
                return Quantity(self.magnitude, "rad")
            if unit == "deg":
                if self.units == "rad":
                    return Quantity(self.magnitude * 180.0 / jnp.pi, "deg")
                return Quantity(self.magnitude, "deg")
            # Default: no conversion
            return Quantity(self.magnitude, unit)

    class Unit:
        pass


def sin(
    x: Union[ArrayLike, Quantity],
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
    # If x is a Quantity, handle unit conversion
    if isinstance(x, Quantity):
        # If a target unit is provided, convert to that unit
        if unit_to_scale is not None:
            x_converted = x.to(unit_to_scale)
        else:
            # Default: convert to radians if not already in radians
            if getattr(x, "units", None) != "rad":
                x_converted = x.to("rad")
            else:
                x_converted = x
        # Use the magnitude for the trigonometric calculation
        magnitude = x_converted.magnitude
    else:
        # For plain array-like input, just use the array directly
        magnitude = jnp.asarray(x)

    # Compute sine using JAX's sin
    return jnp.sin(magnitude)