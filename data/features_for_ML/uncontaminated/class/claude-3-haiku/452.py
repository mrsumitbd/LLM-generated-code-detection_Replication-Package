class Output:
    """Output file."""

    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def open(self):
        self.file = open(self.filename, 'w')

    def write(self, text):
        self.file.write(text)

    def close(self):
        self.file.close()