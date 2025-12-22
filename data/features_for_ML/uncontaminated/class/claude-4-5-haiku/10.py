class Ansi:

    def __init__(self, ansi_codes):
        self.ansi_codes = ansi_codes
    
    def __getattr__(self, name):
        if name in self.ansi_codes:
            return self.ansi_codes[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __call__(self, text):
        return f"{self.ansi_codes.get('code', '')}{text}{self.ansi_codes.get('reset', '')}"