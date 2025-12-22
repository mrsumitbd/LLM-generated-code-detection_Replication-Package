class Ansi:
    def __init__(self, ansi_codes):
        self.ansi_codes = ansi_codes

    def __enter__(self):
        print(self.ansi_codes, end="")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("\033[0m", end="")

    def __getattr__(self, name):
        if name in self.ansi_codes:
            return lambda: print(self.ansi_codes[name], end="")
        else:
            raise AttributeError(f"Ansi class has no attribute '{name}'")