def sequence_mask(length, max_length=None):
    if max_length is None:
        max_length = length
    mask = [[1] * length for _ in range(max_length)]
    for i in range(max_length):
        if i >= length:
            mask[i] = [0] * length
    return mask