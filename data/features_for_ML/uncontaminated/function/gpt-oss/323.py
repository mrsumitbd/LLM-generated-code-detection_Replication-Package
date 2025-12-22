def fnv1_32_hash(identifier: bytes) -> int:
    """32-bit hash of a node according to Fowler‑Noll‑Vo

    @param identifier: a bytes representation of a node
    @return: hashed value for the node as int
    """
    # FNV-1 32‑bit parameters
    fnv_prime = 16777619
    fnv_offset_basis = 2166136261

    hash_val = fnv_offset_basis
    for byte in identifier:
        hash_val = (hash_val * fnv_prime) & 0xffffffff
        hash_val ^= byte
    return hash_val & 0xffffffff  # ensure 32‑bit unsigned int