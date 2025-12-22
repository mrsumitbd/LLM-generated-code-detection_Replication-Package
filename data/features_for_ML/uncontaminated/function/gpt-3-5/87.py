def pad_dataproto_to_divisor(data: 'DataProto', size_divisor: int):
    pad_size = size_divisor - (len(data) % size_divisor)
    if pad_size != size_divisor:
        padding = b'\x00' * pad_size
        data += padding
    return data, pad_size