def try_ensure_utf8(data: bytes) -> bytes:
    try:
        return data.decode('utf-8').encode('utf-8')
    except UnicodeDecodeError:
        return data