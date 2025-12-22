import jax.numpy as jnp
import jax
from typing import Callable, Union, Sequence
from jax.numpy import fft as jnpfft
from saiunit._base import Quantity, Unit, get_or_create_dimension
from saiunit._unit_common import second
from saiunit.math._fun_change_unit import _fun_change_unit_unary

def ifftn(
    a: Union[Quantity, jax.typing.ArrayLike],
    s: Shape | None = None,
    axes: Sequence[int] | None = None,
    norm: str | None = None
) -> Union[Quantity, jax.typing.ArrayLike]:
    r"""Compute a multidimensional inverse discrete Fourier transform.

    saiunit implementation of :func:`numpy.fft.ifftn`.

    Args:
        a: input quantity or array.
        s: sequence of integers. Specifies the shape of the result. If not specified,
            it will default to the shape of ``a`` along the specified ``axes``.
        axes: sequence of integers, default=None. Specifies the axes along which the
            transform is computed. If None, computes the transform along all the axes.
        norm: string. The normalization mode. "backward", "ortho" and "forward" are
            supported.

    Returns:
        A quantity containing the multidimensional inverse discrete Fourier transform
        of ``a``.

    See also:
        - :func:`saiunit.fft.fftn`: Computes a multidimensional discrete Fourier
          transform.
        - :func:`saiunit.fft.fft`: Computes a one-dimensional discrete Fourier
          transform.
        - :func:`saiunit.fft.ifft`: Computes a one-dimensional inverse discrete
          Fourier transform.

    Examples:
        ``saiunit.fft.ifftn`` computes the transform along all the axes by default when
        ``axes`` argument is ``None``.

        >>> import saiunit as u
        >>> import jax.numpy as jnp
        >>> x = jnp.array([[1, 2, 5, 3],
        ...                [4, 1, 2, 6],
        ...                [5, 3, 2, 1]]) * u.meter
        >>> with jnp.printoptions(precision=2, suppress=True):
        ...   print(u.fft.ifftn(x))
        ArrayImpl([[ 2.92+0.j  ,  0.08-0.33j,  0.25+0.j  ,  0.08+0.33j],
                   [-0.08+0.14j, -0.04-0.03j,  0.  -0.29j, -1.05-0.11j],
                   [-0.08-0.14j, -1.05+0.11j,  0.  +0.29j, -0.04+0.03j]],
                   dtype=complex64) * meter / second2

        When ``s=[3]``, dimension of the transform along ``axis -1`` will be ``3``
        and dimension along other axes will be the same as that of input.

        >>> with jnp.printoptions(precision=2, suppress=True):
        ...   print(u.fft.ifftn(x, s=[3]))
        ArrayImpl([[ 2.67+0.j  , -0.83-0.87j, -0.83+0.87j],
                   [ 2.33+0.j  ,  0.83-0.29j,  0.83+0.29j],
                   [ 3.33+0.j  ,  0.83+0.29j,  0.83-0.29j]], dtype=complex64) * meter / second2

        When ``s=[2]`` and ``axes=[0]``, dimension of the transform along ``axis 0``
        will be ``2`` and dimension along other axes will be same as that of input.

        >>> with jnp.printoptions(precision=2, suppress=True):
        ...   print(u.fft.ifftn(x, s=[2], axes=[0]))
        ArrayImpl([[ 2.5+0.j,  1.5+0.j,  3.5+0.j,  4.5+0.j],
                   [-1.5+0.j,  0.5+0.j,  1.5+0.j, -1.5+0.j]], dtype=complex64) * meter / second

        When ``s=[2, 3]``, shape of the transform will be ``(2, 3)``.

        >>> with jnp.printoptions(precision=2, suppress=True):
        ...   print(u.fft.ifftn(x, s=[2, 3]))
        ArrayImpl([[ 2.5 +0.j  ,  0.  -0.58j,  0.  +0.58j],
                   [ 0.17+0.j  , -0.83-0.29j, -0.83+0.29j]], dtype=complex64) * meter / second2
    """
    input_ndim = a.ndim if hasattr(a, 'ndim') else jnp.asarray(a).ndim
    n = _calculate_fftn_dimension(input_ndim, axes)
    _unit_change_fun = lambda u: u / (second ** n)
    # TODO: may cause computation overhead?
    ifftn._unit_change_fun = _unit_change_fun
    return _fun_change_unit_unary(jnpfft.ifftn,
                                  _unit_change_fun,
                                  a, s=s, axes=axes, norm=norm)