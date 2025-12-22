def pad_dataproto_to_divisor(data: 'DataProto', size_divisor: int):
    """Pad a DataProto to size divisible by size_divisor

    Args:
        size_divisor (int): size divisor

    Returns:
        data: (DataProto): the padded DataProto
        pad_size (int)
    """
    if size_divisor <= 0:
        raise ValueError("size_divisor must be a positive integer")

    # Retrieve the current data bytes; assume the field is named 'data'
    current_bytes = getattr(data, "data", None)
    if current_bytes is None:
        # If the field is missing, treat as empty bytes
        current_bytes = b""
    elif not isinstance(current_bytes, (bytes, bytearray)):
        # Try to convert to bytes if possible
        try:
            current_bytes = bytes(current_bytes)
        except Exception as e:
            raise TypeError("DataProto 'data' field must be bytes-like") from e

    current_len = len(current_bytes)
    remainder = current_len % size_divisor
    pad_size = 0 if remainder == 0 else size_divisor - remainder

    if pad_size > 0:
        # Pad with zero bytes
        padded_bytes = current_bytes + b"\x00" * pad_size
        # Update the DataProto field
        setattr(data, "data", padded_bytes)

    return data, pad_size