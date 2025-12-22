class Ansi:

    def __init__(self, ansi_codes):
        self.ansi_codes = ansi_codes

    def apply(self, text):
        return f"\033[{self.ansi_codes}m{text}\033[0m"