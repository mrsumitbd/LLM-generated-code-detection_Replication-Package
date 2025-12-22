import jax
import jax.numpy as jnp
from jax.experimental.sparse import COO
from typing import Union

# Assume Quantity is from a units library (e.g. pint or astropy)
try:
    from pint import Quantity  # type: ignore
except Exception:
    try:
        from astropy.units import Quantity  # type: ignore
    except Exception:
        Quantity = None  # type: ignore


def coo_matvec(
    mat: COO,
    v: Union[jax.Array, "Quantity"],
    transpose: bool = False,
) -> Union[jax.Array, "Quantity"]:
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
    # Extract COO components
    data = mat.data
    indices = mat.indices  # shape (nnz, 2)
    shape = mat.shape

    # Handle unit-aware vectors
    if Quantity is not None and isinstance(v, Quantity):
        unit = v.unit
        v_mag = v.magnitude
    else:
        unit = None
        v_mag = v

    if not transpose:
        # y[row] = sum_i data[i] * v[col]
        row_indices = indices[:, 0]
        col_indices = indices[:, 1]
        y_shape = shape[0]
        y_mag = jax.ops.segment_sum(data * v_mag[col_indices], row_indices, y_shape)
    else:
        # y[col] = sum_i data[i] * v[row]
        row_indices = indices[:, 0]
        col_indices = indices[:, 1]
        y_shape = shape[1]
        y_mag = jax.ops.segment_sum(data * v_mag[row_indices], col_indices, y_shape)

    if unit is not None:
        return y_mag * unit
    return y_mag