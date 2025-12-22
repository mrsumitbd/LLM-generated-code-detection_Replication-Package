import numpy as np

def is_valid_numpy_dtype_string(dtype_str: str) -> bool:
    """
    Return True if a given string can be converted to a numpy dtype.
    """
    if not isinstance(dtype_str, str):
        return False
    dtype_str = dtype_str.strip()
    if not dtype_str:
        return False
    try:
        np.dtype(dtype_str)
        return True
    except Exception:
        return False