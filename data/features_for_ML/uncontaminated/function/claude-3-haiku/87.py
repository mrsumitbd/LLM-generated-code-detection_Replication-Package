def pad_dataproto_to_divisor(data: 'DataProto', size_divisor: int):
    """Pad a DataProto to size divisible by size_divisor

    Args:
        size_divisor (int): size divisor

    Returns:
        data: (DataProto): the padded DataProto
        pad_size (int)
    """
    data_size = len(data.SerializeToString())
    pad_size = size_divisor - (data_size % size_divisor)
    if pad_size < size_divisor:
        data.data.extend([0] * pad_size)
    return data, pad_size