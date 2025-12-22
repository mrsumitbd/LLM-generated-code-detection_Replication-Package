def guess_block_id(name):
    block_id = 0
    for char in name:
        block_id += ord(char)
    return block_id % 1000