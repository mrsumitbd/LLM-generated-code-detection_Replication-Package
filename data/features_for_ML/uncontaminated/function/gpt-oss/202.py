from __future__ import annotations

from typing import Union

import jax
import jax.numpy as jnp
from jax.scipy.linalg import solve_triangular
from pint import Quantity

def triangular_solve(
    a: Union[Quantity, jax.typing.ArrayLike],
    b: Union[Quantity, jax.typing.ArrayLike],
    left_side: bool = False,
    lower: bool = False,
    transpose_a: bool = False,
    conjugate_a: bool = False,
    unit_diagonal: bool = False,
) -> Quantity | jax.Array:
    """
    Solve a triangular linear system.

    Parameters
    ----------
    a
        A batch of triangular matrices of shape ``[..., m, m]``.
    b
        Right‑hand side matrices of shape ``[..., m, n]`` if ``left_side`` is
        ``True`` or ``[..., n, m]`` otherwise.
    left_side
        If ``True`` solve ``op(A) X = B``; otherwise solve ``X op(A) = B``.
    lower
        If ``True`` use the lower triangle of ``A``; otherwise use the upper
        triangle.
    transpose_a
        If ``True`` use the transpose of ``A``.
    conjugate_a
        If ``True`` use the complex conjugate of ``A``.
    unit_diagonal
        If ``True`` assume the diagonal of ``A`` is all ones.

    Returns
    -------
    Quantity or jax.Array
        The solution matrix with the same shape and dtype as ``b``.
    """
    # Extract magnitudes if quantities
    a_mag = a.magnitude if isinstance(a, Quantity) else a
    b_mag = b.magnitude if isinstance(b, Quantity) else b

    # Determine transpose flag for solve_triangular
    if transpose_a and conjugate_a:
        trans = "C"
    elif transpose_a:
        trans = "T"
    elif conjugate_a:
        trans = "C"
    else:
        trans = "N"

    # Solve the system
    if left_side:
        # op(A) X = B  ->  X = solve_triangular(A, B)
        x_mag = solve_triangular(
            a_mag,
            b_mag,
            lower=lower,
            unit_diagonal=unit_diagonal,
            trans=trans,
        )
    else:
        # X op(A) = B  ->  X = solve_triangular(A, B.T).T
        x_mag = solve_triangular(
            a_mag,
            b_mag.T,
            lower=lower,
            unit_diagonal=unit_diagonal,
            trans=trans,
        ).T

    # Attach units if b was a Quantity
    if isinstance(b, Quantity):
        return Quantity(x_mag, b.units)
    return x_mag