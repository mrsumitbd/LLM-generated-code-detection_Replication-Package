def fnv1_32_hash(identifier: bytes) -> int:
    """32-bit hash of a node according to Fowler-Noll-Vo

    @param identifier: a bytes representation of a node
    @return: hashed value for the node as int
    """
    FNV_32_PRIME = 16777619
    FNV1_32A_INIT = 2166136261
    
    hash_value = FNV1_32A_INIT
    
    for byte in identifier:
        hash_value ^= byte
        hash_value = (hash_value * FNV_32_PRIME) & 0xffffffff
    
    return hash_value