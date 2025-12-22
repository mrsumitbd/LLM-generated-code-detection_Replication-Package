def fnv1_32_hash(identifier: bytes) -> int:
    FNV_offset_basis = 2166136261
    FNV_prime = 16777619
    hash_value = FNV_offset_basis
    for byte in identifier:
        hash_value ^= byte
        hash_value *= FNV_prime
        hash_value &= 0xFFFFFFFF
    return hash_value