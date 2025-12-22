class _String:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        return _String(self.value + other.value)

    def __mul__(self, n):
        return _String(self.value * n)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __len__(self):
        return len(self.value)