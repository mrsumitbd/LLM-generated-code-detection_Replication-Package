class Output:
    """Output file."""
    
    def __init__(self, filename):
        self.filename = filename
        
    def write(self, text):
        with open(self.filename, 'w') as file:
            file.write(text)