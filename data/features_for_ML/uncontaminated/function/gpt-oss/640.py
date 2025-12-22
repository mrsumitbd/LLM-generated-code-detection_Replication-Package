import numpy as np
import base64

def _encode_array(arr: np.ndarray, b64: bool = True) -> dict:
    """
    Encode a NumPy array into a serializable dictionary.

    Parameters
    ----------
    arr : np.ndarray
        The array to encode.
    b64 : bool, default True
        If True, the array data is encoded as a base64 string.
        If False, the raw bytes of the array are stored directly.

    Returns
    -------
    dict
        A dictionary containing the array's dtype, shape, and data.
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError(f"_encode_array expects a np.ndarray, got {type(arr).__name__}")

    # Convert the array to raw bytes
    raw_bytes = arr.tobytes()

    if b64:
        # Encode bytes to base64 string
        data = base64.b64encode(raw_bytes).decode("ascii")
    else:
        # Store raw bytes directly (may not be JSON serializable)
        data = raw_bytes

    return {
        "dtype": str(arr.dtype),
        "shape": arr.shape,
        "data": data,
    }