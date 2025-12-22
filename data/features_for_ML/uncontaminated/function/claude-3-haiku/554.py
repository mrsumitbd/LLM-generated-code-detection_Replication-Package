def chunk_to_complete_utf8(byte_blocks):
    result = b''
    for block in byte_blocks:
        try:
            result += block.decode('utf-8')
        except UnicodeDecodeError:
            continue
    return result