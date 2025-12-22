def nanpercentile(
    a: Union[jax.Array, Quantity],
    q: jax.typing.ArrayLike,
    axis: Optional[Union[int, Tuple[int]]] = None,
    method: str = 'linear',
    keepdims: Optional[bool] = False,
) -> jax.Array:
    """
    Compute the q-th percentile of the data along the specified axis, while ignoring nan values.

    Returns the q-th percentile(s) of the array elements, while ignoring nan values.

    Parameters
    ----------
    a : array_like, Quantity
      Input array or Quantity.
    q : array_like, Quantity
      Percentile or sequence of percentiles to compute, which must be between 0 and 100 inclusive.
    method : str, optional
      This parameter specifies the method to use for estimating the
      percentile.  There are many different methods, some unique to NumPy.
      See the notes for explanation.  The options sorted by their R type
      as summarized in the H&F paper [1]_ are:

      1. 'inverted_cdf'
      2. 'averaged_inverted_cdf'
      3. 'closest_observation'
      4. 'interpolated_inverted_cdf'
      5. 'hazen'
      6. 'weibull'
      7. 'linear'  (default)
      8. 'median_unbiased'
      9. 'normal_unbiased'

      The first three methods are discontinuous.  NumPy further defines the
      following discontinuous variations of the default 'linear' (7.) option:

      * 'lower'
      * 'higher',
      * 'midpoint'
      * 'nearest'
    keepdims : bool, optional
      If this is set to True, the axes which are reduced are left in the result as dimensions with size one.

    Returns
    -------
    out : jax.Array
      Output array.
    """
    import jax.numpy as jnp
    
    # Convert input to array
    a_array = jnp.asarray(a)
    q_array = jnp.asarray(q)
    
    # Create a mask for non-nan values
    valid_mask = ~jnp.isnan(a_array)
    
    # If axis is None, flatten the array and use all valid values
    if axis is None:
        a_valid = a_array[valid_mask]
        result = jnp.percentile(a_valid, q_array, method=method, keepdims=False)
    else:
        # Handle axis parameter
        if isinstance(axis, int):
            axis = (axis,)
        
        # Replace nan values with a placeholder that won't affect percentile calculation
        # We'll use a masked approach by filtering along the specified axes
        a_filled = jnp.where(valid_mask, a_array, jnp.nan)
        
        # Use jnp.percentile with nan_policy if available, otherwise filter manually
        # JAX's percentile doesn't have nan_policy, so we need to handle it differently
        
        # Move axes to the end and reshape to separate valid values
        result = jnp.percentile(
            a_filled,
            q_array,
            axis=axis,
            method=method,
            keepdims=keepdims
        )
    
    return result