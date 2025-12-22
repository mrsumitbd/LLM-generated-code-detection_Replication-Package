def fnv1_32_hash(identifier: bytes) -> int:
    """32-bit hash of a node according to Fowler-Noll-Vo

    @param identifier: a bytes representation of a node
    @return: hashed value for the node as int
    """
    id_hash = 2166136261
    for byte in identifier:
        id_hash = (id_hash * 16777619) & 0xFFFFFFFF
        id_hash ^= byte

    return id_hash