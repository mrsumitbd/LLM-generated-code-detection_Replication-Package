def guess_block_id(name):
    import hashlib

    # Convert the input name to bytes
    name_bytes = name.encode('utf-8')

    # Calculate the SHA-256 hash of the name
    hash_object = hashlib.sha256(name_bytes)
    hash_value = hash_object.hexdigest()

    # Extract the first 8 characters of the hash as the block ID
    block_id = hash_value[:8]

    return block_id