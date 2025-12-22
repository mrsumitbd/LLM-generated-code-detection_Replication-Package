import numpy as np
import base64

def _encode_array(arr: np.ndarray, b64: bool = True) -> dict:
    encoded_data = base64.b64encode(arr.tobytes()).decode('utf-8') if b64 else arr.tobytes().hex()
    return {'data': encoded_data, 'shape': arr.shape, 'dtype': str(arr.dtype)}