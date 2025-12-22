
class StreamToQueue:
    """A helper class to redirect stream output (like stdout) to a queue."""
    def __init__(self, queue):
        self.queue = queue
        self.buffer = ''

    def write(self, buf):
        # We buffer the output and send it line-by-line to get clean logs.
        self.buffer += buf
        if '\n' in self.buffer:
            lines = self.buffer.split('\n')
            for line in lines[:-1]:
                self.queue.put(line + '\n')
            self.buffer = lines[-1]
    
    def flush(self):
        # When flush is called (e.g., at script end), send any remaining text.
        if self.buffer:
            self.queue.put(self.buffer + '\n')
            self.buffer = ''