import queue

def read_stream(stream, q):
    """
    Read all lines from a file-like `stream` and put them into the queue `q`.
    When the stream is exhausted, a sentinel value `None` is put into the queue
    to signal completion.

    Parameters
    ----------
    stream : file-like object
        An object supporting the `readline()` method (e.g., a file, socket, or
        any stream that yields text lines).
    q : queue.Queue
        The queue into which lines will be enqueued. The queue must be thread-
        safe if used across multiple threads.

    Returns
    -------
    None
    """
    try:
        while True:
            line = stream.readline()
            if not line:
                break
            q.put(line)
    finally:
        # Signal that reading is complete
        q.put(None)