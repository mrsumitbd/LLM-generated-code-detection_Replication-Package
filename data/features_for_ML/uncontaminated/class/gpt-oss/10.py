class Ansi:
    """
    A small helper for working with ANSI escape codes.

    Parameters
    ----------
    ansi_codes : str or iterable of str
        One or more ANSI code strings (e.g. '31' for red, '1' for bold).
    """

    ESC = "\x1b["

    def __init__(self, ansi_codes):
        if isinstance(ansi_codes, str):
            self.codes = [ansi_codes]
        else:
            self.codes = list(ansi_codes)

    def __repr__(self):
        return f"Ansi({self.codes!r})"

    def __str__(self):
        return f"{self.ESC}{';'.join(self.codes)}m"

    def apply(self, text):
        """Wrap *text* with the ANSI codes and reset at the end."""
        return f"{self}{text}\x1b[0m"

    def __call__(self, text):
        """Allow the instance to be called like a function."""
        return self.apply(text)

    def __add__(self, other):
        """Combine two Ansi objects into a new one."""
        if isinstance(other, Ansi):
            return Ansi(self.codes + other.codes)
        return NotImplemented

    def __radd__(self, other):
        """Support right‑hand addition."""
        if isinstance(other, Ansi):
            return Ansi(other.codes + self.codes)
        return NotImplemented