import numpy as np

def is_valid_numpy_dtype_string(dtype_str: str) -> bool:
    """
    Return True if a given string can be converted to a numpy dtype.
    """
    try:
        np.dtype(dtype_str)
        return True
    except (TypeError, ValueError):
        return False