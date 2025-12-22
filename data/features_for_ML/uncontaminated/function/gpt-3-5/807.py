def convert_to_bytes(value, bytes, mock=False):
    if mock:
        return b'\x00' * bytes
    return value.to_bytes(bytes, byteorder='big')