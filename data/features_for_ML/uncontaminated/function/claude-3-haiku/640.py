import numpy as np
import base64

def _encode_array(arr: np.ndarray, b64: bool = True) -> dict:
    """
    Encodes a NumPy array into a dictionary.

    Args:
        arr (np.ndarray): The input NumPy array to be encoded.
        b64 (bool, optional): Whether to encode the array using base64. Defaults to True.

    Returns:
        dict: A dictionary containing the encoded array data and metadata.
    """
    data = arr.tobytes()
    if b64:
        data = base64.b64encode(data).decode('utf-8')

    return {
        'dtype': str(arr.dtype),
        'shape': arr.shape,
        'data': data
    }