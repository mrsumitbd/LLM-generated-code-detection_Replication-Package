def read_stream(stream, q):
    result = []
    for i in range(q):
        try:
            result.append(next(stream))
        except StopIteration:
            break
    return result