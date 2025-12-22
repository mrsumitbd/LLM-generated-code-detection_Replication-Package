def chunk_to_complete_utf8(byte_blocks):
    for s in chunk_bytes_to_strings(byte_blocks):
        yield s.encode("utf-8")