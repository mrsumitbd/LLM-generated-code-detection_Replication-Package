def make_2d_mask(mask):
    if isinstance(mask, (list, tuple)):
        return mask
    else:
        return [[mask]]