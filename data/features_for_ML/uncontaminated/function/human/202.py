from jax import lax, Array
from typing import Union, Callable, Any
import jax
from .._base import Quantity, maybe_decimal, fail_for_unit_mismatch
from .._misc import set_module_as, maybe_custom_array, maybe_custom_array_tree

def triangular_solve(
    a: Union[Quantity, jax.typing.ArrayLike],
    b: Union[Quantity, jax.typing.ArrayLike],
    left_side: bool = False, lower: bool = False,
    transpose_a: bool = False, conjugate_a: bool = False,
    unit_diagonal: bool = False,
) -> Quantity | jax.Array:
    r"""Triangular solve.

    Solves either the matrix equation

    .. math::
        \mathit{op}(A) . X = B

    if ``left_side`` is ``True`` or

    .. math::
        X . \mathit{op}(A) = B

    if ``left_side`` is ``False``.

    ``A`` must be a lower or upper triangular square matrix, and where
    :math:`\mathit{op}(A)` may either transpose :math:`A` if ``transpose_a``
    is ``True`` and/or take its complex conjugate if ``conjugate_a`` is ``True``.

    Args:
        a: A batch of matrices with shape ``[..., m, m]``.
        b: A batch of matrices with shape ``[..., m, n]`` if ``left_side`` is
            ``True`` or shape ``[..., n, m]`` otherwise.
        left_side: describes which of the two matrix equations to solve; see above.
        lower: describes which triangle of ``a`` should be used. The other triangle
            is ignored.
        transpose_a: if ``True``, the value of ``a`` is transposed.
        conjugate_a: if ``True``, the complex conjugate of ``a`` is used in the
            solve. Has no effect if ``a`` is real.
        unit_diagonal: if ``True``, the diagonal of ``a`` is assumed to be unit
            (all 1s) and not accessed.

    Returns:
    A batch of matrices the same shape and dtype as ``b``.
    """
    a = maybe_custom_array(a)
    b = maybe_custom_array(b)
    if isinstance(a, Quantity) and isinstance(b, Quantity):
        return maybe_decimal(Quantity(lax.linalg.triangular_solve(a.mantissa, b.mantissa, left_side=left_side,
                                                                  lower=lower, transpose_a=transpose_a,
                                                                  conjugate_a=conjugate_a,
                                                                  unit_diagonal=unit_diagonal), unit=b.unit))
    elif isinstance(a, Quantity):
        return lax.linalg.triangular_solve(a.mantissa, b, left_side=left_side,
                                           lower=lower, transpose_a=transpose_a, conjugate_a=conjugate_a,
                                           unit_diagonal=unit_diagonal)
    elif isinstance(b, Quantity):
        return maybe_decimal(Quantity(lax.linalg.triangular_solve(a, b.mantissa, left_side=left_side,
                                                                  lower=lower, transpose_a=transpose_a,
                                                                  conjugate_a=conjugate_a,
                                                                  unit_diagonal=unit_diagonal), unit=b.unit))
    else:
        return lax.linalg.triangular_solve(a, b, left_side=left_side,
                                           lower=lower, transpose_a=transpose_a, conjugate_a=conjugate_a,
                                           unit_diagonal=unit_diagonal)