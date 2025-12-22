def chunk_to_complete_utf8(byte_blocks):
    result = []
    current_byte = 0
    for byte_block in byte_blocks:
        if current_byte == 0:
            if byte_block < 0x80:
                result.append(byte_block.to_bytes(1, 'big'))
            elif byte_block < 0xE0:
                current_byte = 1
                current_chunk = byte_block & 0x1F
            elif byte_block < 0xF0:
                current_byte = 2
                current_chunk = byte_block & 0x0F
            elif byte_block < 0xF8:
                current_byte = 3
                current_chunk = byte_block & 0x07
        else:
            current_chunk = (current_chunk << 6) | (byte_block & 0x3F)
            current_byte -= 1
            if current_byte == 0:
                result.append(current_chunk.to_bytes(1 + current_byte, 'big'))
    return result