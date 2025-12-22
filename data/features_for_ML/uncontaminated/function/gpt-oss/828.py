def merge(a, b):
    """Merge two sorted lists `a` and `b` into a single sorted list."""
    i, j = 0, 0
    merged = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    # Append any remaining elements
    if i < len(a):
        merged.extend(a[i:])
    if j < len(b):
        merged.extend(b[j:])
    return merged