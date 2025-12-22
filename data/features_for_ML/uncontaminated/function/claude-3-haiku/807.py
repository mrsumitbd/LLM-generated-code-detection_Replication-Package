def convert_to_bytes(value, bytes, mock=False):
    if mock:
        return value
    else:
        return value * bytes