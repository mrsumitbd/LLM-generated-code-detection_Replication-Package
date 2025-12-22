def _quantize(x, bins):
    return [sum(1 for b in bins if b <= val) for val in x]