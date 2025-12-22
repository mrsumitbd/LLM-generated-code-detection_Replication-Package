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
        mat = mat.T
    
    # mat is now (m, n) and v is (n,)
    # result should be (m,)
    m, n = mat.shape
    
    # Extract COO components
    row, col = mat.coords
    data = mat.data
    
    # Gather v values at column indices
    v_gathered = v[col]
    
    # Multiply data by gathered v values
    products = data * v_gathered
    
    # Sum products for each row index
    result = jnp.zeros(m, dtype=mat.dtype)
    result = result.at[row].add(products)
    
    return result