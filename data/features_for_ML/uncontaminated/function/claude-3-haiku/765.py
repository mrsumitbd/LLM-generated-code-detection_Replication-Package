def bitwise_xor(self):
    result = None
    for item in self:
        if result is None:
            result = item
        else:
            result = result | item
    return result