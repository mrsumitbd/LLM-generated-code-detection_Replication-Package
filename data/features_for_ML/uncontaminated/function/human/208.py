import jax
from saiunit._base import Quantity, split_mantissa_unit, maybe_decimal, get_mantissa, get_unit

def coo_matvec(
    mat: COO,
    v: jax.Array | Quantity,
    transpose: bool = False
) -> jax.Array | Quantity:
    """Product of COO sparse matrix and a dense vector.

    Args:
      mat : COO matrix
      v : one-dimensional array of size ``(shape[0] if transpose else shape[1],)`` and
        dtype ``mat.dtype``
      transpose : boolean specifying whether to transpose the sparse matrix
        before computing.

    Returns:
      y : array of shape ``(mat.shape[1] if transpose else mat.shape[0],)`` representing
        the matrix vector product.
    """
    data, row, col = mat._bufs
    return _coo_matvec(data, row, col, v, spinfo=mat._info, transpose=transpose)