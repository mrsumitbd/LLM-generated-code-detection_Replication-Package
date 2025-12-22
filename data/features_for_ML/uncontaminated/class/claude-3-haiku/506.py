class _String:
    def __init__(self, value):
        self._value = str(value)

    def __len__(self):
        return len(self._value)

    def __getitem__(self, index):
        return self._value[index]

    def __iter__(self):
        return iter(self._value)

    def __contains__(self, item):
        return item in self._value

    def __add__(self, other):
        if isinstance(other, _String):
            return _String(self._value + other._value)
        elif isinstance(other, str):
            return _String(self._value + other)
        else:
            raise TypeError("Can only concatenate _String or str (not 'int')")

    def __radd__(self, other):
        if isinstance(other, _String):
            return _String(other._value + self._value)
        elif isinstance(other, str):
            return _String(other + self._value)
        else:
            raise TypeError("Can only concatenate _String or str (not 'int')")

    def __str__(self):
        return self._value

    def __repr__(self):
        return f"_String('{self._value}')"