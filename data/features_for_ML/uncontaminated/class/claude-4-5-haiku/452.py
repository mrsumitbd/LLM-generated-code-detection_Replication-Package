class Output:
    """Output file."""
    
    def __init__(self, filename):
        """Initialize Output with a filename."""
        self.filename = filename
        self.file = None
    
    def __enter__(self):
        """Enter context manager."""
        self.file = open(self.filename, 'w')
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        if self.file:
            self.file.close()
        return False
    
    def write(self, content):
        """Write content to the output file."""
        if self.file is None:
            self.file = open(self.filename, 'w')
        self.file.write(content)
    
    def close(self):
        """Close the output file."""
        if self.file:
            self.file.close()
            self.file = None
    
    def __del__(self):
        """Destructor to ensure file is closed."""
        self.close()