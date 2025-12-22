class StreamToQueue:
    """A helper class to redirect stream output (like stdout) to a queue."""

    def __init__(self, queue):
        self.queue = queue

    def write(self, buf):
        if buf and buf != '\n':
            self.queue.put(buf)

    def flush(self):
        pass