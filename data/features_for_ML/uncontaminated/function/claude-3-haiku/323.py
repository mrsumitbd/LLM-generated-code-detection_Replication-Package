def fnv1_32_hash(identifier: bytes) -> int:
    """32-bit hash of a node according to Fowler-Noll-Vo

    @param identifier: a bytes representation of a node
    @return: hashed value for the node as int
    """
    hash_value = 2166136261
    for byte in identifier:
        hash_value ^= byte
        hash_value *= 16777619
    return hash_value