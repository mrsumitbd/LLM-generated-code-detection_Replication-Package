
class Ansi:
    def __init__(self, ansi_codes):
        self.ansi_codes = ansi_codes
        for key, value in ansi_codes.items():
            setattr(self, key, value)