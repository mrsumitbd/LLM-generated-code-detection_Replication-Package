class _String:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"_String({self.value!r})"

    def __eq__(self, other):
        if isinstance(other, _String):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, index):
        return self.value[index]

    def __contains__(self, item):
        return item in self.value

    def __add__(self, other):
        if isinstance(other, _String):
            return _String(self.value + other.value)
        return _String(self.value + str(other))

    def __radd__(self, other):
        return _String(str(other) + self.value)

    def __mul__(self, other):
        return _String(self.value * other)

    def __rmul__(self, other):
        return _String(other * self.value)

    def __lt__(self, other):
        if isinstance(other, _String):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, _String):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, _String):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, _String):
            return self.value >= other.value
        return self.value >= other

    def __ne__(self, other):
        return not self.__eq__(other)

    def upper(self):
        return _String(self.value.upper())

    def lower(self):
        return _String(self.value.lower())

    def strip(self):
        return _String(self.value.strip())

    def split(self, sep=None):
        return self.value.split(sep)

    def replace(self, old, new):
        return _String(self.value.replace(old, new))

    def startswith(self, prefix):
        return self.value.startswith(prefix)

    def endswith(self, suffix):
        return self.value.endswith(suffix)

    def find(self, sub):
        return self.value.find(sub)

    def count(self, sub):
        return self.value.count(sub)

    def join(self, iterable):
        return _String(self.value.join(iterable))

    def format(self, *args, **kwargs):
        return _String(self.value.format(*args, **kwargs))