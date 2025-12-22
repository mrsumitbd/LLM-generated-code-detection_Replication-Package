from __future__ import annotations

from typing import Sequence, Union

import jax.numpy as jnp
from jax import numpy as jnp_np

from .quantity import Quantity  # assumed to be the saiunit Quantity implementation
from .unit import unit  # assumed to provide unit('second') etc.


def ifftn(
    a: Union[Quantity, jax.typing.ArrayLike],
    s: Sequence[int] | None = None,
    axes: Sequence[int] | None = None,
    norm: str | None = None,
) -> Union[Quantity, jax.typing.ArrayLike]:
    """
    Compute a multidimensional inverse discrete Fourier transform.

    Parameters
    ----------
    a : Quantity or array
        Input array or quantity.
    s : Sequence[int] or None, optional
        Shape of the output along the specified axes. If None, the shape of ``a``
        along those axes is used.
    axes : Sequence[int] or None, optional
        Axes along which to compute the transform. If None, all axes are used.
    norm : str or None, optional
        Normalization mode. One of ``'backward'``, ``'ortho'``, or ``'forward'``.

    Returns
    -------
    Quantity or array
        The inverse FFT of ``a``. If ``a`` was a quantity, the returned quantity
        has units divided by ``second**len(axes)``.
    """
    # Extract magnitude and unit if a is a Quantity
    if isinstance(a, Quantity):
        mag = a.magnitude
        unit_a = a.unit
    else:
        mag = jnp.asarray(a)
        unit_a = None

    # Determine axes
    if axes is None:
        axes = tuple(range(mag.ndim))
    else:
        axes = tuple(axes)

    # Determine shape
    if s is None:
        s = tuple(mag.shape[ax] for ax in axes)
    else:
        if len(s) != len(axes):
            raise ValueError("Length of s must match length of axes")
        s = tuple(s)

    # Perform the inverse FFT
    result = jnp_np.fft.ifftn(mag, s=s, axes=axes, norm=norm)

    # Attach units if necessary
    if unit_a is not None:
        # Divide by second**len(axes)
        new_unit = unit_a / (unit("second") ** len(axes))
        return Quantity(result, new_unit)
    else:
        return result