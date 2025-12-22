class _String:
    def __init__(self, value):
        self.value = str(value)

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"_String({self.value!r})"

    def __len__(self):
        return len(self.value)

    def __eq__(self, other):
        if isinstance(other, _String):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)

    def __add__(self, other):
        if isinstance(other, _String):
            return _String(self.value + other.value)
        return _String(self.value + str(other))

    def __radd__(self, other):
        return _String(str(other) + self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __contains__(self, item):
        return item in self.value

    def __iter__(self):
        return iter(self.value)

    def upper(self):
        return _String(self.value.upper())

    def lower(self):
        return _String(self.value.lower())

    def strip(self, chars=None):
        return _String(self.value.strip(chars))

    def split(self, sep=None, maxsplit=-1):
        return [_String(s) for s in self.value.split(sep, maxsplit)]

    def join(self, iterable):
        return _String(self.value.join(str(x) for x in iterable))

    def replace(self, old, new, count=-1):
        return _String(self.value.replace(old, new, count))

    def find(self, sub, start=0, end=None):
        return self.value.find(sub, start, len(self.value) if end is None else end)

    def rfind(self, sub, start=0, end=None):
        return self.value.rfind(sub, start, len(self.value) if end is None else end)

    def startswith(self, prefix, start=0, end=None):
        return self.value.startswith(prefix, start, len(self.value) if end is None else end)

    def endswith(self, suffix, start=0, end=None):
        return self.value.endswith(suffix, start, len(self.value) if end is None else end)