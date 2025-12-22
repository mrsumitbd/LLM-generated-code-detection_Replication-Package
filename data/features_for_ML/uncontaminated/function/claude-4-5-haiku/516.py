def read_stream(stream, q):
    """
    Read items from a stream and put them into a queue.
    
    Args:
        stream: An iterable stream of items
        q: A queue.Queue object to put items into
    """
    for item in stream:
        q.put(item)
    q.put(None)  # Signal end of stream