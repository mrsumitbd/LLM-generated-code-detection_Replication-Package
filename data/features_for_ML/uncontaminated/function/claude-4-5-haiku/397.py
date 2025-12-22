def python_to_array(
    val: Any, expected_shape: ShapeType, expected_dtype: Optional[str]
) -> ArrayLike:
    """Convert a Python object to a NumPy array."""
    import numpy as np
    
    # Convert to numpy array
    arr = np.asarray(val)
    
    # Handle dtype conversion if specified
    if expected_dtype is not None:
        arr = arr.astype(expected_dtype)
    
    # Handle shape conversion if specified
    if expected_shape is not None:
        # If expected_shape is a tuple/list of ints, reshape
        if isinstance(expected_shape, (tuple, list)):
            arr = arr.reshape(expected_shape)
        # If it's a single int, flatten and ensure that length
        elif isinstance(expected_shape, int):
            arr = arr.flatten()
            if arr.size != expected_shape:
                raise ValueError(
                    f"Cannot reshape array of size {arr.size} to shape {expected_shape}"
                )
    
    return arr