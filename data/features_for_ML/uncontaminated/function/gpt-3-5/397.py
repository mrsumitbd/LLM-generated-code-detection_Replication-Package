def python_to_array(val: Any, expected_shape: ShapeType, expected_dtype: Optional[str]) -> ArrayLike:
    import numpy as np

    if expected_dtype is not None:
        return np.array(val, dtype=expected_dtype).reshape(expected_shape)
    else:
        return np.array(val).reshape(expected_shape)