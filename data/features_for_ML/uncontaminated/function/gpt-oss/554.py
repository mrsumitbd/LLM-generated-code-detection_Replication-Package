def chunk_to_complete_utf8(byte_blocks):
    """
    Yield byte strings that contain only complete UTF‑8 encoded characters.
    Any incomplete multibyte character at the end of a block is buffered
    and prepended to the next block.

    Parameters
    ----------
    byte_blocks : iterable of bytes
        Iterable yielding chunks of bytes that may split UTF‑8 characters.

    Yields
    ------
    bytes
        Chunks that end on a UTF‑8 character boundary.
    """
    buffer = b""

    for block in byte_blocks:
        data = buffer + block
        pos = 0  # start of the remaining data to process

        while pos < len(data):
            # Find the start byte of the last character in the remaining data
            # Scan backwards from the end of the remaining data
            i = len(data) - 1
            while i >= pos and (data[i] & 0b11000000) == 0b10000000:
                i -= 1

            if i < pos:
                # No start byte found; all remaining bytes are continuation bytes
                # This should not happen in valid UTF‑8, but we treat it as incomplete
                break

            # Determine the expected length of the UTF‑8 sequence
            byte = data[i]
            if (byte & 0b11110000) == 0b11110000:
                exp_len = 4
            elif (byte & 0b11100000) == 0b11100000:
                exp_len = 3
            elif (byte & 0b11000000) == 0b11000000:
                exp_len = 2
            else:
                exp_len = 1

            # Check if the sequence is complete within the data
            if i + exp_len <= len(data):
                # Yield the complete part up to the end of this character
                yield data[pos : i + exp_len]
                pos = i + exp_len
            else:
                # Incomplete sequence at the end; buffer it for the next block
                break

        # Any remaining bytes that were not yielded are buffered
        buffer = data[pos:]

    # After processing all blocks, if there's any buffered data left,
    # it must be an incomplete sequence. We discard it because it cannot
    # form a complete UTF‑8 character.