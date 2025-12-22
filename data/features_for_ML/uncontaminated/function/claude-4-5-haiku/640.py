def _encode_array(arr: np.ndarray, b64: bool = True) -> dict:
    import base64
    
    # Get array properties
    dtype_str = str(arr.dtype)
    shape = tuple(arr.shape)
    
    # Flatten and convert to bytes
    flat_arr = arr.flatten()
    arr_bytes = flat_arr.tobytes()
    
    # Encode to base64 if requested
    if b64:
        data = base64.b64encode(arr_bytes).decode('ascii')
    else:
        data = arr_bytes
    
    return {
        'data': data,
        'dtype': dtype_str,
        'shape': shape,
        'b64': b64
    }