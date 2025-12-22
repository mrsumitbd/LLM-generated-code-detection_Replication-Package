def pad_dataproto_to_divisor(data: 'DataProto', size_divisor: int):
    """Pad a DataProto to size divisible by size_divisor

    Args:
        size_divisor (int): size divisor

    Returns:
        data: (DataProto): the padded DataProto
        pad_size (int)
    """
    current_size = len(data)
    remainder = current_size % size_divisor
    
    if remainder == 0:
        pad_size = 0
    else:
        pad_size = size_divisor - remainder
    
    if pad_size > 0:
        data = data + b'\x00' * pad_size
    
    return data, pad_size