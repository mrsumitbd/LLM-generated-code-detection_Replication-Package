def is_valid_numpy_dtype_string(dtype_str: str) -> bool:
    try:
        import numpy as np
        np.dtype(dtype_str)
        return True
    except:
        return False