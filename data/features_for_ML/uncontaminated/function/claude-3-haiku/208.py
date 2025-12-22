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
    if transpose:
        row, col, data = mat.T.row, mat.T.col, mat.T.data
    else:
        row, col, data = mat.row, mat.col, mat.data

    y = jax.ops.segment_sum(data * v[col], row, mat.shape[0 if transpose else 1])
    return y